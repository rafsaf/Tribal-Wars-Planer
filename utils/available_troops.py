# Copyright 2021 Rafał Safin (rafsaf). All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================


import numpy as np
from django.db.models import F, Q, QuerySet, Sum

from base import models
from utils.basic.cdist_brute import CDistBrute


def get_legal_coords_outline(outline: models.Outline):  # noqa: PLR0912
    """Create set with ally_vill without enemy_vill closer than radius"""
    excluded_coords_text: str = outline.initial_outline_excluded_coords
    excluded_coords: list[str] = excluded_coords_text.split()

    min_radius: float = float(outline.initial_outline_front_dist)
    max_radius: float = float(outline.initial_outline_maximum_off_dist)

    ally_villages: list[str] = [
        start
        for start in models.WeightMaximum.objects.filter(outline=outline).values_list(
            "start", flat=True
        )
    ]
    target_villages: list[str] = [
        target
        for target in models.TargetVertex.objects.filter(
            outline=outline, fake=False, ruin=False
        ).values_list("target", flat=True)
    ]

    all_ally: np.ndarray = np.array(
        models.VillageModel.objects.filter(
            coord__in=ally_villages, world=outline.world
        ).values_list("x_coord", "y_coord")
    )

    all_enemy: np.ndarray = np.array(
        models.VillageModel.objects.select_related()
        .exclude(coord__in=excluded_coords)
        .filter(player__tribe__tag__in=outline.enemy_tribe_tag, world=outline.world)
        .values_list("x_coord", "y_coord")
    )

    real_target_enemy: np.ndarray = np.array(
        models.VillageModel.objects.exclude(coord__in=excluded_coords)
        .filter(coord__in=target_villages, world=outline.world)
        .values_list("x_coord", "y_coord")
    )

    if all_enemy.size > 0:
        front_array, back_array, away_array = CDistBrute(
            ally_villages=all_ally,
            enemy_villages=all_enemy,
            min_radius=min_radius,
            max_radius=max_radius,
        ).triple_result()
    else:
        front_array = np.array([])
        away_array = np.array([])

    front_starts: list[str] = [f"{coord[0]}|{coord[1]}" for coord in front_array]
    away_starts: list[str] = [f"{coord[0]}|{coord[1]}" for coord in away_array]

    models.WeightMaximum.objects.filter(outline=outline).update(
        first_line=False, too_far_away=False
    )

    batch_size = 1000
    for i in range(0, len(front_starts), batch_size):
        batch = front_starts[i : i + batch_size]
        models.WeightMaximum.objects.filter(outline=outline, start__in=batch).update(
            first_line=True
        )
    for i in range(0, len(away_starts), batch_size):
        batch = away_starts[i : i + batch_size]
        models.WeightMaximum.objects.filter(outline=outline, start__in=batch).update(
            too_far_away=True
        )

    all_weights: QuerySet[models.WeightMaximum] = models.WeightMaximum.objects.filter(
        outline=outline,
        off_left__gte=outline.initial_outline_min_off,
        off_left__lte=outline.initial_outline_max_off,
    )

    all_off: int = all_weights.count()
    front_off: int = all_weights.filter(first_line=True).count()
    too_far_off: int = all_weights.filter(too_far_away=True).count()
    back_off: int = all_off - front_off - too_far_off

    all_full_noble_weights: QuerySet[models.WeightMaximum] = (
        models.WeightMaximum.objects.filter(
            outline=outline,
            off_left__gte=outline.initial_outline_min_off,
            off_left__lte=outline.initial_outline_max_off,
            nobleman_left__gte=1,
        )
    )

    all_full_noble_off: int = all_full_noble_weights.count()
    front_full_noble_off: int = all_full_noble_weights.filter(first_line=True).count()
    too_far_full_noble_off: int = all_full_noble_weights.filter(
        too_far_away=True
    ).count()
    back_full_noble_off: int = (
        all_full_noble_off - front_full_noble_off - too_far_full_noble_off
    )

    n_query: QuerySet[models.WeightMaximum] = models.WeightMaximum.objects.filter(
        outline=outline, nobleman_left__gte=1
    )

    all_noble: int = n_query.aggregate(n=Sum("nobleman_left"))["n"] or 0
    front_noble: int = (
        n_query.filter(first_line=True).aggregate(n=Sum("nobleman_left"))["n"] or 0
    )
    too_far_noble: int = (
        n_query.filter(too_far_away=True).aggregate(n=Sum("nobleman_left"))["n"] or 0
    )
    back_noble = all_noble - front_noble - too_far_noble

    outline.available_nobles = [all_noble, front_noble, back_noble, too_far_noble]
    outline.available_offs = [all_off, front_off, back_off, too_far_off]
    outline.available_full_noble_offs = [
        all_full_noble_off,
        front_full_noble_off,
        back_full_noble_off,
        too_far_full_noble_off,
    ]
    outline.save(
        update_fields=[
            "available_nobles",
            "available_offs",
            "available_full_noble_offs",
        ]
    )

    # #
    # #
    # AROUND TARGETS
    target_radius = float(outline.initial_outline_target_dist)
    if real_target_enemy.size > 0:
        close_array, _ = CDistBrute(
            ally_villages=all_ally,
            enemy_villages=real_target_enemy,
            min_radius=target_radius,
            max_radius=target_radius,
        ).result()
    else:
        return

    close_starts: list[str] = [f"{coord[0]}|{coord[1]}" for coord in close_array]

    all_off = 0
    front_off = 0
    too_far_off = 0
    back_off = 0

    for i in range(0, len(close_starts), batch_size):
        batch = close_starts[i : i + batch_size]
        batch_weights = models.WeightMaximum.objects.filter(
            outline=outline,
            start__in=batch,
            off_left__gte=outline.initial_outline_min_off,
            off_left__lte=outline.initial_outline_max_off,
        )
        all_off += batch_weights.count()
        front_off += batch_weights.filter(first_line=True).count()
        too_far_off += batch_weights.filter(too_far_away=True).count()

    back_off = all_off - front_off - too_far_off

    snob_weights = models.WeightMaximum.objects.filter(
        outline=outline, nobleman_left__gte=1, too_far_away=False
    ).filter(start__in=close_starts)

    all_noble = snob_weights.aggregate(n=Sum("nobleman_left"))["n"] or 0
    front_noble = (
        snob_weights.filter(first_line=True).aggregate(n=Sum("nobleman_left"))["n"] or 0
    )
    too_far_noble = (
        snob_weights.filter(too_far_away=True).aggregate(n=Sum("nobleman_left"))["n"]
        or 0
    )
    back_noble = all_noble - front_noble - too_far_noble

    outline.available_nobles_near = [all_noble, front_noble, back_noble, too_far_off]
    outline.available_offs_near = [all_off, front_off, back_off, too_far_noble]
    outline.save(update_fields=["available_nobles_near", "available_offs_near"])


def get_available_catapults_lst(outline: models.Outline) -> list[int]:
    catapults = models.WeightMaximum.objects.filter(outline=outline)
    all_catapults: int = catapults.aggregate(n=Sum("catapult_left"))["n"] or 0
    front_catapults: int = (
        catapults.filter(first_line=True).aggregate(n=Sum("catapult_left"))["n"] or 0
    )
    too_far_catapults: int = (
        catapults.filter(too_far_away=True).aggregate(n=Sum("catapult_left"))["n"] or 0
    )
    back_catapults: int = all_catapults - front_catapults - too_far_catapults
    available_catapults_lst = [
        all_catapults,
        front_catapults,
        back_catapults,
        too_far_catapults,
    ]
    return available_catapults_lst


def get_available_ruins(outline: models.Outline) -> int:
    available_ruins_from_other: int = (
        models.WeightMaximum.objects.filter(
            first_line=False,
            too_far_away=False,
            outline=outline,
            catapult_left__gte=outline.initial_outline_catapult_min_value,
        )
        .filter(
            Q(off_left__lt=outline.initial_outline_min_off)
            | Q(off_left__gt=outline.initial_outline_max_off)
        )
        .aggregate(ruin_sum=Sum("catapult_left"))["ruin_sum"]
        or 0
    )

    available_ruins_from_offs: int = (
        models.WeightMaximum.objects.filter(
            outline=outline,
            first_line=False,
            too_far_away=False,
            catapult_left__gte=outline.initial_outline_off_left_catapult
            + outline.initial_outline_catapult_min_value,
            off_left__gte=outline.initial_outline_min_off,
            off_left__lte=outline.initial_outline_max_off,
        )
        .annotate(
            ruin_number=(F("catapult_left") - outline.initial_outline_off_left_catapult)
        )
        .aggregate(ruin_sum=Sum("ruin_number"))["ruin_sum"]
        or 0
    )
    return available_ruins_from_other + available_ruins_from_offs


def add_extra_available_troops_data(outline: models.Outline) -> None:
    outline.available_ruins = get_available_ruins(outline=outline)
    outline.available_catapults = get_available_catapults_lst(outline=outline)
    outline.save(update_fields=["available_ruins", "available_catapults"])
