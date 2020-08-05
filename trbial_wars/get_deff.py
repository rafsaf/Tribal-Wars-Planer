"""
 Model contains functions to convert text
 from script Obrona to nice good looking version, also prining only villages in center
"""

from base import models
from . import basic


def get_deff(
    outline: models.Outline,
    radius: int,
    ally_name_list=None,
    enemy_name_list=None,
    excluded_villages="",
):
    """
    Args is instance of Outline, WARNING! be sure to use CORRECT
    data in instance, returns text with deff results.
    """
    if ally_name_list is None:
        ally_name_list = []
    if enemy_name_list is None:
        enemy_name_list = []

    if outline.deff_troops == "":
        return ""

    my_tribe = outline.ally_tribe_tag
    ally_tribe_pk = [f"{tag}::{outline.world}" for tag in my_tribe]
    enemy_tribe = outline.enemy_tribe_tag

    my_tribe_id = [
        tribe.tribe_id
        for tribe in models.Tribe.objects.all().filter(id__in=ally_tribe_pk)
    ]
    ally_players = models.Player.objects.all().filter(tribe_id__in=my_tribe_id, world=outline.world)

    my_tribe_villages = models.VillageModel.objects.all().filter(
        world=outline.world,
        player_id__in=[
            player.player_id
            for player in ally_players
        ]
        + [
            player.player_id
            for player in models.Player.objects.all().filter(
                name__in=ally_name_list, world=outline.world
            )
        ],
    )

    if excluded_villages != "":
        excluded_villages = basic.many_villages(excluded_villages)

        my_tribe_villages = my_tribe_villages.exclude(
            id__in=[
                f'{village.coord}-{outline.world}' for village in excluded_villages
            ]
        )

    enemy_tribe_villages = models.VillageModel.objects.all().filter(
        world=outline.world,
        player_id__in=[
            player.player_id
            for player in models.Player.objects.all().filter(
                tribe_id__in=[
                    tribe.tribe_id
                    for tribe in models.Tribe.objects.all().filter(
                        world=outline.world, tag__in=enemy_tribe
                    )
                ]
                + [
                    player.player_id
                    for player in models.Player.objects.all().filter(
                        name__in=enemy_name_list
                    )
                ],
                world=outline.world,
            )
        ],
    )

    village_dictionary = {}
    player_dictionary = {}

    for player in ally_players:
        player_dictionary[player.player_id] = player.name
    for village_model in my_tribe_villages:
        village_dictionary[
            f"{village_model.x_coord}|{village_model.y_coord}"
        ] = player_dictionary[village_model.player_id]

    return deff_text(
        my_tribe_villages,
        enemy_tribe_villages,
        radius,
        outline.deff_troops,
        int(outline.world),
        village_dictionary,
    )

def get_legal_coords(ally_villages, enemy_villages, radius):
    """ create map with ally_vill without enemy_vill """
    banned_coords = set()
    ally_set = set()
    for village in ally_villages:
        ally_set.add((village.x_coord, village.y_coord))
    for village in enemy_villages:
        pass_bool = False
        if (village.x_coord, village.y_coord) in banned_coords:
            for coord in basic.yield_four_circle_ends(radius, (village.x_coord, village.y_coord)):
                if coord in banned_coords:
                    break
                pass_bool = True

        if not pass_bool:
            for coord in basic.yield_circle(radius, (village.x_coord, village.y_coord)):
                if coord not in banned_coords:
                    banned_coords.add(coord)

    return ally_set - banned_coords


def get_set_of_villages(ally_villages, enemy_villages, radius):
    """ get list of legal villages from ally villages"""
    result_villages = set()
    legal_cords = get_legal_coords(ally_villages, enemy_villages, radius)
    for i in ally_villages:
        if (i.x_coord, i.y_coord) in legal_cords:
            result_villages.add(f'{i.x_coord}|{i.y_coord}')

    return result_villages



def deff_text(
    ally_villages, enemy_villages, radius, text_obrona, world, village_dictionary
):
    """
    uses get_list_of_villages to get legal villages in legal area,
    from text_obrona get numbers of units finaly returns text with results
    """

    lista_wiosek = get_set_of_villages(ally_villages, enemy_villages, radius)

    context_all: dict = {}
    context_details: dict = {}
    if text_obrona == "":
        return ""

    world_evidence = basic.world_evidence(world_number=world)

    for i, line in enumerate(text_obrona.strip().split("\r\n")):
        
        if i % 2 == 1:
            continue
        
        deff_instance = basic.Defence(text_army=line, evidence=world_evidence)
        try:
            owner = village_dictionary[deff_instance.coord]
        except KeyError:
            raise KeyError()
        if deff_instance.coord not in lista_wiosek:
            continue
        deff = deff_instance.deff
        if deff <= 0:
            continue

        if owner not in context_all:
            context_all[owner] = deff
            context_details[owner] = f"\r\n{owner}\r\n{deff_instance.coord} - {deff}"
        else:
            context_all[owner] += deff
            context_details[owner] += f"\r\n{deff_instance.coord} - {deff}"
        
    output = ""
    for i in context_details:

        context_details[
            i
        ] += f"\r\nŁącznie - {context_all[i]} - miejsc w zagrodzie, CK liczone jako x4\r\n"

        output += context_details[i]
    
    return output
