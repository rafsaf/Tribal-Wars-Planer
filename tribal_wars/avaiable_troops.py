from math import ceil

from django.db.models import Sum

from base import models
from . import basic
from tribal_wars import get_deff

def legal_coords_near_targets(outline: models.Outline):
    """ Create set with ally_vill without enemy_vill closer than radius """
    excluded_coords = outline.initial_outline_excluded_coords.split()

    radius = int(outline.initial_outline_target_dist)
    ally_villages = [weight["start"] for weight in models.WeightMaximum.objects.filter(outline=outline).values("start")]
    enemy_villages = [target["target"] for target in models.TargetVertex.objects.filter(outline=outline).values("target")]

    my_villages = models.VillageModel.objects.filter(coord__in=ally_villages, world=outline.world).values("x_coord", "y_coord", "coord")
    enemy_villages = models.VillageModel.objects.exclude(coord__in=excluded_coords).filter(coord__in=enemy_villages, world=outline.world).values("x_coord", "y_coord")

    starts = get_deff.get_set_of_villages(
        ally_villages=my_villages,
        enemy_villages=enemy_villages,
        radius=radius
    )

    all_weights = models.WeightMaximum.objects.filter(
        outline=outline, off_max__gte=outline.initial_outline_min_off
    ).exclude(start__in=starts)

    all_off = all_weights.count()
    front_off = all_weights.filter(first_line=True).count()
    back_off = all_off - front_off

    snob_weights = models.WeightMaximum.objects.filter(
        outline=outline, nobleman_max__gte=1
    ).exclude(start__in=starts)

    all_noble = snob_weights.aggregate(
        Sum("nobleman_max")
    )["nobleman_max__sum"]
    front_noble = snob_weights.filter(
       first_line=True
    ).aggregate(Sum("nobleman_max"))["nobleman_max__sum"]


    if all_noble is None:
        all_noble = 0
    if front_noble is None:
        front_noble = 0

    back_noble = all_noble - front_noble

    outline.avaiable_nobles_near = [all_noble, front_noble, back_noble]
    outline.avaiable_offs_near = [all_off, front_off, back_off]
    outline.save()


def get_legal_coords_outline(outline: models.Outline):
    """ Create set with ally_vill without enemy_vill closer than radius """
    excluded_coords = outline.initial_outline_excluded_coords.split()

    radius = int(outline.initial_outline_front_dist)
    ally_villages = [weight["start"] for weight in models.WeightMaximum.objects.filter(outline=outline).values("start")]

    my_villages = models.VillageModel.objects.filter(coord__in=ally_villages, world=outline.world).values("x_coord", "y_coord", "coord")
    enemy_villages = models.VillageModel.objects.select_related().exclude(coord__in=excluded_coords).filter(player__tribe__tag__in=outline.enemy_tribe_tag, world=outline.world).values("x_coord", "y_coord")

    starts = get_deff.get_set_of_villages(
        ally_villages=my_villages,
        enemy_villages=enemy_villages,
        radius=radius
    )

    models.WeightMaximum.objects.filter(
        outline=outline, start__in=starts
    ).update(first_line=False)
    models.WeightMaximum.objects.filter(outline=outline).exclude(
        start__in=starts
    ).update(first_line=True)

    all_weights = models.WeightMaximum.objects.filter(
        outline=outline, off_max__gte=outline.initial_outline_min_off
    )

    all_off = all_weights.count()
    back_off = all_weights.filter(start__in=starts)
    back_off = back_off.count()

    front_off = all_weights.exclude(start__in=starts)
    front_off = front_off.count()

    snob_weights = models.WeightMaximum.objects.filter(
        outline=outline, nobleman_max__gte=1
    )

    all_noble = snob_weights.aggregate(Sum("nobleman_max"))[
        "nobleman_max__sum"
    ]
    back_noble = snob_weights.filter(start__in=starts).aggregate(
        Sum("nobleman_max")
    )["nobleman_max__sum"]
    front_noble = snob_weights.exclude(start__in=starts).aggregate(
        Sum("nobleman_max")
    )["nobleman_max__sum"]

    if all_noble is None:
        all_noble = 0
    if back_noble is None:
        back_noble = 0
    if front_noble is None:
        front_noble = 0

    outline.avaiable_nobles = [all_noble, front_noble, back_noble]
    outline.avaiable_offs = [all_off, front_off, back_off]
    outline.save()
