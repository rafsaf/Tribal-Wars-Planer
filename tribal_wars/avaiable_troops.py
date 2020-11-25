from django.db.models import Sum

from base import models
from . import basic

def legal_coords_near_targets(outline: models.Outline):
    """ Create set with ally_vill without enemy_vill closer than radius """

    radius = int(outline.initial_outline_target_dist)

    ally_villages = [
        weight.coord_tuple()
        for weight in models.WeightMaximum.objects.filter(outline=outline)
    ]
    enemy_villages = [
        target.coord_tuple()
        for target in models.TargetVertex.objects.filter(outline=outline)
    ]

    banned_coords = set()
    ally_set = set()

    for village in ally_villages:
        ally_set.add((village[0], village[1]))
    for village in enemy_villages:
        for coord in basic.yield_circle(radius, (village[0], village[1])):
            if coord not in banned_coords:
                banned_coords.add(coord)

    legal_coords = banned_coords

    starts = [f"{tup[0]}|{tup[1]}" for tup in legal_coords]

    all_weights = models.WeightMaximum.objects.filter(
        outline=outline, off_max__gte=outline.initial_outline_min_off
    )

    front_off = all_weights.filter(start__in=starts).count()


    snob_weights = models.WeightMaximum.objects.filter(
        outline=outline, nobleman_max__gte=1
    )

    front_noble = snob_weights.filter(start__in=starts).aggregate(
        Sum("nobleman_max")
    )["nobleman_max__sum"]

    if front_noble is None:
        front_noble = 0

    outline.avaiable_nobles_near = [front_noble]
    outline.avaiable_offs_near = [front_off]
    outline.save()

def get_legal_coords_outline(outline: models.Outline):
    """ Create set with ally_vill without enemy_vill closer than radius """

    radius = int(outline.initial_outline_front_dist)
    enemy_tribe = outline.enemy_tribe_tag
    enemy_villages = models.VillageModel.objects.all().filter(
        world=outline.world,
        player_id__in=[
            player.player_id
            for player in models.Player.objects.all().filter(
                tribe_id__in=[
                    tribe.tribe_id
                    for tribe in models.Tribe.objects.all().filter(
                        world=outline.world, tag__in=enemy_tribe
                    )
                ],
                world=outline.world,
            )
        ],
    )
    ally_villages = [
        weight.coord_tuple()
        for weight in models.WeightMaximum.objects.filter(outline=outline)
    ]

    banned_coords = set()
    ally_set = set()

    for village in ally_villages:
        ally_set.add((village[0], village[1]))
    for village in enemy_villages:
        pass_bool = False
        if (village.x_coord, village.y_coord) in banned_coords:
            for coord in basic.yield_four_circle_ends(
                radius, (village.x_coord, village.y_coord)
            ):
                if coord in banned_coords:
                    break
                pass_bool = True

        if not pass_bool:
            for coord in basic.yield_circle(
                radius, (village.x_coord, village.y_coord)
            ):
                if coord not in banned_coords:
                    banned_coords.add(coord)

    legal_coords = ally_set - banned_coords
    starts = [f"{tup[0]}|{tup[1]}" for tup in legal_coords]
    all_weights = models.WeightMaximum.objects.filter(
        outline=outline, off_max__gte=outline.initial_outline_min_off
    )

    all_off = all_weights.count()
    back_off = all_weights.filter(start__in=starts).count()
    front_off = all_weights.exclude(start__in=starts).count()

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