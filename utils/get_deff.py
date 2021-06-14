"""
Model contains functions to convert text

From script Obrona to nice good looking version

Also prining only villages in center

"""
from logging import getLogger

import numpy as np
from tw_complex.brute import CDistBrute

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

    my_tribe_villages: np.ndarray = np.array(
        models.VillageModel.objects.select_related()
        .filter(player__tribe__tag__in=outline.ally_tribe_tag, world=outline.world)
        .values_list("x_coord", "y_coord")
    )

    enemy_tribe_villages: np.ndarray = np.array(
        models.VillageModel.objects.select_related()
        .filter(player__tribe__tag__in=outline.enemy_tribe_tag, world=outline.world)
        .exclude(coord__in=excluded_coords)
        .values_list("x_coord", "y_coord")
    )

    return deff_text(
        my_tribe_villages,
        enemy_tribe_villages,
        radius,
        outline,
    )


def get_set_of_villages(
    ally_villages: np.ndarray, enemy_villages: np.ndarray, radius: int
):
    """get list of legal villages from ally villages"""
    if enemy_villages.size > 0:
        _, back_array = CDistBrute(
            ally_villages=ally_villages,
            enemy_villages=enemy_villages,
            min_radius=radius,
            max_radius=1000,
            _precision=1,
        ).result()
    else:
        back_array = ally_villages

    return set(f"{coord[0]}|{coord[1]}" for coord in back_array)


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
