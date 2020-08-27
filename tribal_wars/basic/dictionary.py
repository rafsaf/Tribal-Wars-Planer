""" functions to generate coord-to-player dictionaries """

from base import models


def coord_to_player(outline: models.Outline):
    """ Dictionary coord : player name for tribes in outline """
    village_dictionary = {}
    player_dictionary = {}

    ally_tribe_pk = [
        f"{tag}::{outline.world}" for tag in outline.ally_tribe_tag
    ]
    ally_tribe_id = [
        tribe.tribe_id
        for tribe in models.Tribe.objects.filter(
            pk__in=ally_tribe_pk
        ).order_by("id")
    ]

    for player in models.Player.objects.filter(
        tribe_id__in=ally_tribe_id, world=outline.world
    ).order_by("id"):

        player_dictionary[player.player_id] = player.name

    for village_model in models.VillageModel.objects.filter(
        player_id__in=player_dictionary, world=outline.world
    ).order_by("id"):
        village_dictionary[
            f"{village_model.x_coord}|{village_model.y_coord}"
        ] = player_dictionary[village_model.player_id]
    return village_dictionary


def coord_to_player_from_string(village_coord_list: str, world: int):
    """ Dictionary coord : player name for villages in coord_list """
    village_dictionary = {}
    player_dictionary = {}

    village_list = village_coord_list.split()

    village_model_list = models.VillageModel.objects.filter(
        pk__in=[f"{coord[0:3]}{coord[4:7]}{world}" for coord in village_list]
    )

    player_id_list = [
        village_model.player_id for village_model in village_model_list
    ]

    for player_model in models.Player.objects.filter(
        player_id__in=player_id_list, world=world
    ):
        player_dictionary[player_model.player_id] = player_model.name

    for village_model in village_model_list:
        village_dictionary[
            f"{village_model.x_coord}|{village_model.y_coord}"
        ] = player_dictionary[village_model.player_id]

    return village_dictionary

