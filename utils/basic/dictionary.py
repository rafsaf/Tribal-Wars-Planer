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

"""functions to generate coord-to-player dictionaries"""

from django.db.models.query import QuerySet

from base.models import Outline, Player, VillageModel, World


def coord_to_player(outline: Outline) -> dict[str, Player]:
    """Dictionary coord : player name for tribes in outline"""
    ally_villages = VillageModel.objects.select_related("player").filter(
        player__tribe__tag__in=outline.ally_tribe_tag, world=outline.world
    )
    village_dictionary: dict[str, Player] = {}
    for village in ally_villages.iterator(chunk_size=10000):
        assert village.player
        village_dictionary[village.coord] = village.player

    return village_dictionary


def coord_to_player_model_from_string(
    village_coord_list: str, world: World
) -> dict[str, Player]:
    """Dictionary coord : player model for villages in coord_list

    We assume for those coords player cant be none
    """
    village_dictionary = {}
    village_list: list[str] = village_coord_list.split()

    villages: QuerySet[VillageModel] = VillageModel.objects.select_related(
        "player"
    ).filter(world=world, coord__in=village_list)

    for village in villages:
        village_dictionary[village.coord] = village.player

    return village_dictionary
