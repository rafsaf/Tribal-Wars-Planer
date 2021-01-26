""" functions to generate coord-to-player dictionaries """
from django.db.models import F, ExpressionWrapper, CharField
from base import models


def coord_to_player(outline: models.Outline):
    """ Dictionary coord : player name for tribes in outline """
    ally_villages = (
        models.VillageModel.objects.select_related()
        .filter(player__tribe__tag__in=outline.ally_tribe_tag, world=outline.world)
        .values("coord", "player__name")
    )
    village_dictionary = {}
    for village in ally_villages.iterator(chunk_size=10000):
        village_dictionary[village["coord"]] = village["player__name"]

    return village_dictionary


def coord_to_player_from_string(village_coord_list: str, world: models.World):
    """ Dictionary coord : player name for villages in coord_list """
    village_dictionary = {}
    village_list = village_coord_list.split()

    villages = (
        models.VillageModel.objects.select_related()
        .filter(world=world, coord__in=village_list)
        .values("coord", "player__name")
    )

    for village in villages:
        village_dictionary[village["coord"]] = village["player__name"]

    return village_dictionary
