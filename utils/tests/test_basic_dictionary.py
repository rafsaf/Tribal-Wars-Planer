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

import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from base import models
from utils import basic


class TestCoordToPlayerAndFromCoordFunctions(TestCase):
    def setUp(self):
        TEXT = (
            "500|500,0,0,10000,0,0,0,0,0,2,0,0,\r\n"
            "500|501,0,0,190,0,0,0,0,0,0,0,0,\r\n"
            "500|502,0,0,19500,0,0,0,0,0,0,0,0,\r\n"
            "500|503,0,0,20100,0,0,0,0,0,0,0,0,\r\n"
            "500|504,0,0,20000,0,0,0,0,0,2,0,0,\r\n"
            "500|505,0,0,20000,0,0,0,0,0,2,0,0,"
        )

        self.server = models.Server.objects.create(
            dns="testserver",
            prefix="te",
        )
        self.world1 = models.World.objects.create(
            server=self.server,
            postfix="1",
            paladin="inactive",
            archer="inactive",
            militia="active",
        )

        self.admin = User.objects.create_user("admin", None, None)  # type: ignore

        self.outline = models.Outline.objects.create(
            owner=self.admin,
            date=datetime.date.today(),
            name="name",
            world=self.world1,
            ally_tribe_tag=["pl1"],
            enemy_tribe_tag=["pl2"],
            initial_outline_targets="500|499:1:4\r\n500|498:1:2---",
            initial_outline_min_off=15000,
            initial_outline_front_dist=3,
            off_troops=TEXT,
        )
        # front

        self.ally_tribe = models.Tribe(tribe_id=0, tag="pl1", world=self.world1)
        self.enemy_tribe = models.Tribe(tribe_id=1, tag="pl2", world=self.world1)

        self.ally_player = models.Player(
            player_id=0,
            name="player0",
            tribe=self.ally_tribe,
            world=self.world1,
            points=999955,
        )
        self.enemy_player = models.Player(
            player_id=1, name="player1", tribe=self.enemy_tribe, world=self.world1
        )
        self.ally_village1 = models.VillageModel(
            coord="500|500",
            village_id=0,
            x_coord=500,
            y_coord=500,
            player=self.ally_player,
            world=self.world1,
        )
        # front
        self.ally_village2 = models.VillageModel(
            coord="500|501",
            village_id=1,
            x_coord=500,
            y_coord=501,
            player=self.ally_player,
            world=self.world1,
        )
        # front
        self.ally_village3 = models.VillageModel(
            coord="500|502",
            village_id=2,
            x_coord=500,
            y_coord=502,
            player=self.ally_player,
            world=self.world1,
        )
        self.ally_village4 = models.VillageModel(
            coord="500|503",
            village_id=3,
            x_coord=500,
            y_coord=503,
            player=self.ally_player,
            world=self.world1,
        )
        self.ally_village5 = models.VillageModel(
            coord="500|504",
            village_id=4,
            x_coord=500,
            y_coord=504,
            player=self.ally_player,
            world=self.world1,
        )
        self.ally_village6 = models.VillageModel(
            coord="500|505",
            village_id=5,
            x_coord=500,
            y_coord=505,
            player=self.ally_player,
            world=self.world1,
        )

        self.enemy_village1 = models.VillageModel(
            coord="500|499",
            village_id=6,
            x_coord=500,
            y_coord=499,
            player=self.enemy_player,
            world=self.world1,
        )
        self.enemy_village2 = models.VillageModel(
            coord="500|498",
            village_id=7,
            x_coord=500,
            y_coord=498,
            player=self.enemy_player,
            world=self.world1,
        )
        self.enemy_village3 = models.VillageModel(
            coord="500|497",
            village_id=8,
            x_coord=500,
            y_coord=497,
            player=self.enemy_player,
            world=self.world1,
        )
        self.ally_tribe.save()
        self.enemy_tribe.save()
        self.ally_player.save()
        self.enemy_player.save()
        self.ally_village1.save()
        self.ally_village2.save()
        self.ally_village3.save()
        self.ally_village4.save()
        self.ally_village5.save()
        self.ally_village6.save()
        self.enemy_village1.save()
        self.enemy_village2.save()
        self.enemy_village3.save()

    def test_coord_to_player_for_tribe1_result_dict_is_correct(self):
        expected_dict = {
            "500|500": "player0",
            "500|501": "player0",
            "500|502": "player0",
            "500|503": "player0",
            "500|504": "player0",
            "500|505": "player0",
        }
        coord_map = basic.coord_to_player(self.outline)
        self.assertEqual(
            {coord: coord_map[coord].name for coord in coord_map}, expected_dict
        )

    def test_coord_to_player_queries_first_are_equal(self):
        with self.assertNumQueries(1):
            basic.coord_to_player(self.outline)

    def test_coord_to_player_points_for_tribe1_result_dict_is_correct(self):
        expected_dict = {
            "500|500": 999955,
            "500|501": 999955,
            "500|502": 999955,
            "500|503": 999955,
            "500|504": 999955,
            "500|505": 999955,
        }
        coord_player_map = basic.coord_to_player(self.outline)

        self.assertEqual(
            {coord: coord_player_map[coord].points for coord in coord_player_map},
            expected_dict,
        )
