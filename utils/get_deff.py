"""
Model contains functions to convert text

From script Obrona to nice good looking version

Also prining only villages in center

"""

from base import models
from . import basic


def get_deff(
    outline: models.Outline,
    radius: int,
    excluded_villages="",
):
    """
    Args is instance of Outline, WARNING! be sure to use CORRECT
    data in instance, returns text with deff results.
    """
    excluded_coords = excluded_villages.split()

    my_tribe_villages = (
        models.VillageModel.objects.select_related()
        .filter(player__tribe__tag__in=outline.ally_tribe_tag, world=outline.world)
        .values("x_coord", "y_coord", "coord")
    )

    enemy_tribe_villages = (
        models.VillageModel.objects.select_related()
        .filter(player__tribe__tag__in=outline.enemy_tribe_tag, world=outline.world)
        .exclude(coord__in=excluded_coords)
        .values("x_coord", "y_coord")
    )

    return deff_text(
        my_tribe_villages,
        enemy_tribe_villages,
        radius,
        outline,
    )


def get_legal_coords(ally_villages, enemy_villages, radius):
    """Create set with ally_vill without enemy_vill closer than radius"""
    ally_set = set()
    for village in ally_villages.iterator(chunk_size=1000):
        ally_set.add((int(village["x_coord"]), int(village["y_coord"])))
    for village in enemy_villages.iterator(chunk_size=1000):
        for coord in basic.yield_circle(
            radius, (village["x_coord"], village["y_coord"])
        ):
            ally_set.discard(coord)

    return ally_set


def get_set_of_villages(ally_villages, enemy_villages, radius):
    """get list of legal villages from ally villages"""
    result_villages = set()
    legal_cords = get_legal_coords(ally_villages, enemy_villages, radius)
    for i in ally_villages:
        if (i["x_coord"], i["y_coord"]) in legal_cords:
            result_villages.add(i["coord"])

    return result_villages


def deff_text(
    ally_villages,
    enemy_villages,
    radius: int,
    outline: models.Outline,
):
    """
    uses get_list_of_villages to get legal villages in legal area,
    from text_obrona get numbers of units finaly returns text with results
    """

    not_in_front = get_set_of_villages(ally_villages, enemy_villages, radius)
    village_dictionary = basic.dictionary.coord_to_player(outline=outline)
    deff_in_village_back: dict = {}
    deff_in_village_front: dict = {}
    deff_own_from_village_back: dict = {}
    deff_own_from_village_front: dict = {}

    world_evidence = basic.world_evidence(world=outline.world)

    for i, line in enumerate(outline.deff_troops.strip().split("\r\n")):
        if i % 2 == 1:
            continue

        deff_instance = basic.Defence(text_army=line, evidence=world_evidence)
        try:
            owner = village_dictionary[deff_instance.coord]  # type: ignore
        except KeyError:
            raise basic.DeffException()

        if deff_instance.coord in not_in_front:
            deff_in_village_back[deff_instance.coord] = deff_instance
        else:
            deff_in_village_front[deff_instance.coord] = deff_instance

    for line in outline.off_troops.strip().split("\r\n"):
        army_instance = basic.Army(text_army=line, evidence=world_evidence)
        try:
            owner = village_dictionary[army_instance.coord]
        except KeyError:
            raise basic.DeffException()

        if army_instance.coord in not_in_front:
            deff_own_from_village_back[army_instance.coord] = army_instance
        else:
            deff_own_from_village_front[army_instance.coord] = army_instance

    all_deff_text = basic.NewDeffText()

    for coord, deff_instance in deff_in_village_back.items():
        try:
            army_instance = deff_own_from_village_back[coord]
        except KeyError:
            army_instance = None
        owner = village_dictionary[coord]
        all_deff_text.add_back_village(owner, deff_instance, army_instance)

    for coord, deff_instance in deff_in_village_front.items():
        try:
            army_instance = deff_own_from_village_front[coord]
        except KeyError:
            army_instance = None
        owner = village_dictionary[coord]
        all_deff_text.add_front_village(owner, deff_instance, army_instance)

    return str(all_deff_text)