from math import ceil
from time import time
from typing import List

import numpy as np
from django.db.models import F, Sum
from django.db.models.query import QuerySet
from tw_complex.brute import CDistBrute

from base import models
from utils import get_deff

from . import basic


def get_legal_coords_outline(outline: models.Outline):
    """Create set with ally_vill without enemy_vill closer than radius"""
    excluded_coords_text: str = outline.initial_outline_excluded_coords
    excluded_coords: List[str] = excluded_coords_text.split()

    min_radius: float = float(outline.initial_outline_front_dist)
    max_radius: float = float(outline.initial_outline_maximum_front_dist)

    ally_villages: List[str] = [
        start
        for start in models.WeightMaximum.objects.filter(outline=outline).values_list(
            "start", flat=True
        )
    ]
    target_villages: List[str] = [
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
        front_array, back_array = CDistBrute(
            ally_villages=all_ally,
            enemy_villages=all_enemy,
            min_radius=min_radius,
            max_radius=max_radius,
            _precision=1,
        ).result()
    else:
        front_array = np.array([])
        back_array = all_ally

    front_starts: List[str] = [f"{coord[0]}|{coord[1]}" for coord in front_array]
    back_starts: List[str] = [f"{coord[0]}|{coord[1]}" for coord in back_array]

    models.WeightMaximum.objects.filter(outline=outline).update(
        first_line=False, too_far_away=False
    )
    models.WeightMaximum.objects.filter(outline=outline, start__in=front_starts).update(
        first_line=True
    )

    models.WeightMaximum.objects.filter(outline=outline).exclude(
        first_line=True
    ).exclude(start__in=back_starts).update(too_far_away=True)
    all_weights: "QuerySet[models.WeightMaximum]" = models.WeightMaximum.objects.filter(
        outline=outline,
        off_max__gte=outline.initial_outline_min_off,
    )

    all_off: int = all_weights.count()
    front_off: int = all_weights.filter(first_line=True).count()
    too_far_off: int = all_weights.filter(too_far_away=True).count()
    back_off: int = all_off - front_off - too_far_off

    n_query: "QuerySet[models.WeightMaximum]" = models.WeightMaximum.objects.filter(
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

    close_starts: List[str] = [f"{coord[0]}|{coord[1]}" for coord in close_array]

    all_weights: "QuerySet[models.WeightMaximum]" = models.WeightMaximum.objects.filter(
        outline=outline,
        off_max__gte=outline.initial_outline_min_off,
        too_far_away=False,
    ).filter(start__in=close_starts)

    all_off: int = all_weights.count()
    front_off: int = all_weights.filter(first_line=True).count()
    back_off: int = all_off - front_off

    snob_weights = models.WeightMaximum.objects.filter(
        outline=outline, nobleman_max__gte=1, too_far_away=False
    ).filter(start__in=close_starts)

    all_noble: int = snob_weights.aggregate(n=Sum("nobleman_max"))["n"] or 0
    front_noble: int = (
        snob_weights.filter(first_line=True).aggregate(n=Sum("nobleman_max"))["n"] or 0
    )
    back_noble: int = all_noble - front_noble

    outline.avaiable_nobles_near = [all_noble, front_noble, back_noble]
    outline.avaiable_offs_near = [all_off, front_off, back_off]
    outline.save()


def update_available_ruins(outline: models.Outline) -> None:
    ruins_from_other: int = (
        models.WeightMaximum.objects.filter(
            first_line=False,
            outline=outline,
            off_left__lt=outline.initial_outline_min_off,
        ).aggregate(ruin_sum=Sum("catapult_left"))["ruin_sum"]
        or 0
    )

    ruins_from_offs: int = (
        models.WeightMaximum.objects.filter(
            outline=outline,
            first_line=False,
            catapult_left__gte=outline.initial_outline_off_left_catapult,
            off_left__gte=outline.initial_outline_min_off,
        )
        .annotate(
            ruin_number=(F("catapult_left") - outline.initial_outline_off_left_catapult)
        )
        .aggregate(ruin_sum=Sum("ruin_number"))["ruin_sum"]
        or 0
    )

    outline.avaiable_ruins = ruins_from_offs + ruins_from_other
    outline.save()
