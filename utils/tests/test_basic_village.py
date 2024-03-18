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

"""Tests for utils folder"""

from math import sqrt

from django.test import TestCase

from base import models
from utils import basic


class VillageTest(TestCase):
    """test for Village class"""

    def setUp(self) -> None:
        self.wioska1 = basic.Village("345|555")
        self.wioska2 = basic.Village("345|455 ")
        self.wioska3 = basic.Village(" 342|455 ")
        self.server = models.Server.objects.create(
            dns="testserver",
            prefix="te",
        )
        self.world1 = models.World.objects.create(
            server=self.server,
            postfix="1",
            speed_world=1.2,
            speed_units=0.8,
        )
        self.world1.save()
        self.tribe1 = models.Tribe.objects.create(
            tribe_id=1,
            tag="name",
            world=self.world1,
        )
        self.player1 = models.Player(
            player_id=1, name="player1", tribe=self.tribe1, world=self.world1
        )
        self.player1.save()
        self.village1 = models.VillageModel(
            coord="345|555",
            village_id=2,
            x_coord=345,
            y_coord=555,
            player=self.player1,
            world=self.world1,
        )
        self.village1.save()

    def test_are_x_and_y_coordinates_correct(self):
        self.assertEqual(self.wioska1.coord, "345|555")
        self.assertEqual(345, self.wioska1.x_coord)
        self.assertEqual(555, self.wioska1.y_coord)

    def test_distance(self):
        self.assertEqual(100, self.wioska1.distance(self.wioska2))
        self.assertEqual(sqrt(10009), self.wioska1.distance(self.wioska3))

    def test_time_distance(self):
        village = basic.Village("523|426")
        village2 = basic.Village("522|425")
        self.assertEqual(3094, village.time_distance(village2, "nobleman", self.world1))
        self.assertEqual(2652, village.time_distance(village2, "ram", self.world1))

    def test_eq(self):
        self.assertTrue(self.wioska1, basic.Village("345|555"))
