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
from django.db.models import F, Sum
from django.db.models.query import Q, QuerySet
from tw_complex.cdist_brute import CDistBrute

from base import models


def get_legal_coords_outline(outline: models.Outline):
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
            _precision=1,
        ).triple_result()
    else:
        front_array = np.array([])
        away_array = np.array([])

    front_starts: list[str] = [f"{coord[0]}|{coord[1]}" for coord in front_array]
    away_starts: list[str] = [f"{coord[0]}|{coord[1]}" for coord in away_array]

    models.WeightMaximum.objects.filter(outline=outline).update(
        first_line=False, too_far_away=False
    )
    if len(front_starts) > 1000:
        front_iterations = len(front_starts) // 1000 + 1
        for i in range(front_iterations):
            starts_batch = front_starts[i * 1000 : (i + 1) * 1000]
            models.WeightMaximum.objects.filter(
                outline=outline, start__in=starts_batch
            ).update(first_line=True)
    else:
        models.WeightMaximum.objects.filter(
            outline=outline, start__in=front_starts
        ).update(first_line=True)

    if len(away_starts) > 1000:
        away_iterations = len(away_starts) // 1000 + 1
        for i in range(away_iterations):
            away_batch = away_starts[i * 1000 : (i + 1) * 1000]
            models.WeightMaximum.objects.filter(
                outline=outline, start__in=away_batch
            ).update(too_far_away=True)
    else:
        models.WeightMaximum.objects.filter(
            outline=outline, start__in=away_starts
        ).update(too_far_away=True)

    all_weights: QuerySet[models.WeightMaximum] = models.WeightMaximum.objects.filter(
        outline=outline,
        off_max__gte=outline.initial_outline_min_off,
        off_max__lte=outline.initial_outline_max_off,
    )

    all_off: int = all_weights.count()
    front_off: int = all_weights.filter(first_line=True).count()
    too_far_off: int = all_weights.filter(too_far_away=True).count()
    back_off: int = all_off - front_off - too_far_off

    n_query: QuerySet[models.WeightMaximum] = models.WeightMaximum.objects.filter(
        outline=outline, nobleman_max__gte=1
    )

    all_noble: int = n_query.aggregate(n=Sum("nobleman_max"))["n"] or 0
    front_noble: int = (
        n_query.filter(first_line=True).aggregate(n=Sum("nobleman_max"))["n"] or 0
    )
    too_far_noble: int = (
        n_query.filter(too_far_away=True).aggregate(n=Sum("nobleman_max"))["n"] or 0
    )
    back_noble = all_noble - front_noble - too_far_noble

    outline.avaiable_nobles = [all_noble, front_noble, back_noble, too_far_noble]
    outline.avaiable_offs = [all_off, front_off, back_off, too_far_off]
    outline.save()

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
            _precision=1,
        ).result()
    else:
        outline.save()
        return

    close_starts: list[str] = [f"{coord[0]}|{coord[1]}" for coord in close_array]

    all_off: int = 0
    front_off: int = 0
    too_far_off: int = 0
    back_off: int = 0

    if len(close_starts) > 1000:
        close_iterations = len(close_starts) // 1000 + 1
        for i in range(close_iterations):
            close_batch = close_starts[i * 1000 : (i + 1) * 1000]
            batch_weights: QuerySet[
                models.WeightMaximum
            ] = models.WeightMaximum.objects.filter(
                outline=outline,
                off_max__gte=outline.initial_outline_min_off,
                off_max__lte=outline.initial_outline_max_off,
            ).filter(
                start__in=close_batch
            )
            all_off += batch_weights.count()
            front_off += batch_weights.filter(first_line=True).count()
            too_far_off += batch_weights.filter(too_far_away=True).count()

    else:
        all_weights: QuerySet[
            models.WeightMaximum
        ] = models.WeightMaximum.objects.filter(
            outline=outline,
            off_max__gte=outline.initial_outline_min_off,
            off_max__lte=outline.initial_outline_max_off,
        ).filter(
            start__in=close_starts
        )
        all_off += all_weights.count()
        front_off += all_weights.filter(first_line=True).count()
        too_far_off += all_weights.filter(too_far_away=True).count()

    back_off: int = all_off - front_off - too_far_off

    snob_weights = models.WeightMaximum.objects.filter(
        outline=outline, nobleman_max__gte=1, too_far_away=False
    ).filter(start__in=close_starts)

    all_noble: int = snob_weights.aggregate(n=Sum("nobleman_max"))["n"] or 0
    front_noble: int = (
        snob_weights.filter(first_line=True).aggregate(n=Sum("nobleman_max"))["n"] or 0
    )
    too_far_noble: int = (
        snob_weights.filter(too_far_away=True).aggregate(n=Sum("nobleman_max"))["n"]
        or 0
    )
    back_noble: int = all_noble - front_noble - too_far_noble

    outline.avaiable_nobles_near = [all_noble, front_noble, back_noble, too_far_off]
    outline.avaiable_offs_near = [all_off, front_off, back_off, too_far_noble]
    outline.save()


def update_available_ruins(outline: models.Outline) -> None:
    catapults = models.WeightMaximum.objects.filter(outline=outline)
    all_catapults: int = catapults.aggregate(n=Sum("catapult_max"))["n"] or 0
    front_catapults: int = (
        catapults.filter(first_line=True).aggregate(n=Sum("catapult_max"))["n"] or 0
    )
    too_far_catapults: int = (
        catapults.filter(too_far_away=True).aggregate(n=Sum("catapult_max"))["n"] or 0
    )
    back_catapults: int = all_catapults - front_catapults - too_far_catapults

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
        .aggregate(ruin_sum=Sum("catapult_max"))["ruin_sum"]
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
            ruin_number=(F("catapult_max") - outline.initial_outline_off_left_catapult)
        )
        .aggregate(ruin_sum=Sum("ruin_number"))["ruin_sum"]
        or 0
    )

    outline.avaiable_ruins = available_ruins_from_other + available_ruins_from_offs
    outline.available_catapults = [
        all_catapults,
        front_catapults,
        back_catapults,
        too_far_catapults,
    ]
    outline.save()
