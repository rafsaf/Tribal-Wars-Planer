""" functions to generate coord-to-player dictionaries """

from base import models


def coord_to_player(outline: models.Outline):
    """ Dictionary coord : player name for tribes in outline """
    village_dictionary = {}
    player_dictionary = {}

    ally_tribe = outline.ally_tribe_tag.split(', ')
    ally_tribe_pk = [
        f'{tag}::{outline.world}' for tag in ally_tribe
    ]
    ally_tribe_id = [
        tribe.tribe_id for tribe in models.Tribe.objects.filter(pk__in=ally_tribe_pk)
    ]

    for player in models.Player.objects.filter(tribe_id__in=ally_tribe_id):
        
        player_dictionary[player.player_id] = player.name

    for village_model in models.VillageModel.objects.filter(
        player_id__in=player_dictionary
    ):
        village_dictionary[
            f"{village_model.x_coord}|{village_model.y_coord}"
        ] = player_dictionary[village_model.player_id]
    return village_dictionary
