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

""" Tests for forms.py """
import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from base import forms, models
from utils import basic


class TestInitialOutlineForm(TestCase):
    def setUp(self):
        self.server = models.Server.objects.create(
            dns="testserver",
            prefix="te",
        )
        self.world1 = models.World.objects.create(
            server=self.server,
            postfix="1",
            paladin="inactive",
            archer="inactive",
            militia="inactive",
        )
        self.admin = User.objects.create_user("admin", None, None)  # type: ignore

        self.real_target_mode: basic.TargetMode = basic.TargetMode("real")

        self.outline = models.Outline.objects.create(
            owner=self.admin,
            date=datetime.date.today(),
            name="name",
            world=self.world1,
            ally_tribe_tag=["pl1", "pl2"],
            enemy_tribe_tag=["pl3", " pl4"],
        )
        self.ally_tribe1 = models.Tribe(tribe_id=1, tag="pl1", world=self.world1)
        self.ally_player1 = models.Player(
            player_id=1,
            name="player1",
            tribe=self.ally_tribe1,
            world=self.world1,
        )
        self.ally_village1 = models.VillageModel(
            coord="500|500",
            village_id=1,
            x_coord=500,
            y_coord=500,
            player=self.ally_player1,
            world=self.world1,
        )
        self.ally_tribe1.save()
        self.ally_player1.save()
        self.ally_village1.save()

    def test_input1_correct_target_should_be_valid(self):
        off_form = forms.InitialOutlineForm(
            {"target": "500|500"},
            outline=self.outline,
            target_mode=self.real_target_mode,
        )
        self.assertTrue(off_form.is_valid())

    def test_input1_correct_target_not_valid_if_target_no_exists(self):
        off_form = forms.InitialOutlineForm(
            {"target": "499|500"},
            outline=self.outline,
            target_mode=self.real_target_mode,
        )
        self.assertFalse(off_form.is_valid())

    def test_input1_correct_target_not_valid_if_target_is_barbarian(self):
        self.ally_village1.player = None
        self.ally_village1.save()
        off_form = forms.InitialOutlineForm(
            {"target": "500|500"},
            outline=self.outline,
            target_mode=self.real_target_mode,
        )
        self.assertFalse(off_form.is_valid())
