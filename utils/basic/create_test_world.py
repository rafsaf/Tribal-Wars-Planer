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

from base.models import Player, Server, Tribe, VillageModel, World


def create_test_world(server: Server):
    test_world = World.objects.create(server=server, postfix="Test")
    tribe1 = Tribe.objects.create(tribe_id=0, tag="ALLY", world=test_world)
    tribe2 = Tribe.objects.create(tribe_id=1, tag="ENEMY", world=test_world)
    ally_villages = []
    ally_players = []
    enemy_players = []
    enemy_villages = []
    for i in range(5):
        ally_players.append(
            Player(tribe=tribe1, world=test_world, player_id=i, name=f"AllyPlayer{i}")
        )
        enemy_players.append(
            Player(
                tribe=tribe2, world=test_world, player_id=i + 5, name=f"EnemyPlayer{i}"
            )
        )
    Player.objects.bulk_create(enemy_players)
    Player.objects.bulk_create(ally_players)
    ally_players = list(Player.objects.filter(world=test_world, player_id__lte=4))
    enemy_players = list(Player.objects.filter(world=test_world, player_id__gte=5))
    for i in range(50):
        ids = i // 10
        ally_villages.append(
            VillageModel(
                world=test_world,
                x_coord=100 + i,
                y_coord=100 + i,
                coord=f"{100+i}|{100+i}",
                village_id=i,
                player=ally_players[ids],
            )
        )
        enemy_villages.append(
            VillageModel(
                world=test_world,
                x_coord=200 + i,
                y_coord=200 + i,
                coord=f"{200+i}|{200+i}",
                village_id=i + 50,
                player=enemy_players[ids],
            )
        )

    VillageModel.objects.bulk_create(enemy_villages)
    VillageModel.objects.bulk_create(ally_villages)
