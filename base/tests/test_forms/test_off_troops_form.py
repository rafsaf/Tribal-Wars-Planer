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

from base import forms, models
from utils import basic


class TestArmy(TestCase):
    """Test for Army"""

    def setUp(self):
        self.text_off1 = "500|500,1000,1000,0,0,0,1000,0,0,0,0,0,"
        self.text_off2 = "500|500,1000,1000,0,0,0,1000,0,0,0,0,"
        self.text_deff1 = "500|500,w wiosce,1000,1000,0,0,0,1000,0,0,0,0,"
        self.text_deff2 = "500|500,w drodze,1000,1000,0,0,0,1000,0,0,0,0,"
        self.text_deff3 = "500|500,w wiosce,1000,1000,0,0,0,1000,0,0,0,"

        self.text_off_bad1 = "500|50,1000,1000,0,0,0,1000,0,0,0,0,0,"
        self.text_off_bad2 = "500|500,1000,1000,0,0,0,1000,0,0,0,0,0"
        self.text_off_bad3 = "500|500,1000,1000,0,0,0,1000,0,0,0,,0,"
        self.text_off_bad4 = "500|500,1000,1000,0,0,0,'xd',0,0,0,0,0,"
        self.text_off_bad5 = "500|500,1000,1000,0,0,0,1000,0,0,0,0,0,0"
        self.text_off_bad6 = "500|500,1000,1000,0,0,0,1000,0,0,0,"
        self.text_off_bad7 = "500|500,1000,1000,0,0,0,1000,0,0,0,0,0,0"
        self.text_off_bad8 = "500|200,1000,1000,0,0,0,1000,0,0,0,0,0,"
        self.text_off_bad9 = "500|0,1000,1000,0,0,0,1000,0,0,0,0,0,"
        self.text_off_bad10 = (
            "500|500,1000,1000,0,0,0,1000,0,0,"
            "0,0,500|0,1000,1000,0,0,0,1000,0,0,0,0,0,"
        )
        self.text_off_bad11 = " 500|500,1000,1000,0,0,0,1000,0,0,0,0,"
        self.text_off_bad12 = "500|500,1000,1000,0,0,0,1000,0,0,0,0, "
        self.text_off_bad13 = "500|500 ,1000,1000,0,0,0,1000,0,0,0,0, "
        self.text_off_bad14 = " 500|500,1000,1000,0,0,0,1000,0,0,0,0, "
        self.text_deff_bad1 = "500|50,w wiosce,1000,1000,0,0,0,1000,0,0,0,0,"
        self.text_deff_bad2 = "500|500,w drodze,1000,1000,0,0,0,1000,0,0,0,0"
        self.text_deff_bad3 = "500|500,1000,1000,0,0,0,1000,0,0,0,,"
        self.text_deff_bad4 = "500|500,w wiosce,1000,1000,0,0,0,'xd',0,0,0,0,"
        self.text_deff_bad5 = "500|500,w drodze,1000,1000,0,0,0,1000,0,0,0,0,0,0"
        self.text_deff_bad6 = "500|500,w wiosce,1000,1000,0,0,0,1000,0,0,"
        self.text_deff_bad7 = "500|500,w wiosce,1000,1000,0,0,0,1000,0,0,0,0,0"
        self.text_deff_bad8 = "500|200,w wiosce,1000,1000,0,0,0,1000,0,0,0,0,"
        self.text_deff_bad9 = "500|0,w wiosce,1000,1000,0,0,0,1000,0,0,0,0,"
        self.text_deff_bad10 = (
            "500|500,w wiosce,1000,1000,0,0,0,1000,0,0,0,0,"
            "500|0,1000,1000,0,0,0,1000,0,0,0,0,0,"
        )
        self.text_deff_bad11 = " 500|500,w wiosce,1000,1000,0,0,0,1000,0,0,0,0,"
        self.text_deff_bad12 = " 500|500,w wiosce,1000,1000,0,0,0,1000,0,0,0,0, "
        self.text_deff_bad13 = "500|500,w wiosce,1000,1000,0,0,0,1000,0,0,0,0, "
        self.text_deff_bad14 = " 500|500 ,w wiosce,1000,1000,0,0,0,1000,0,0,0,0,"
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
        self.outline = models.Outline.objects.create(
            owner=self.admin,
            date=datetime.date.today(),
            name="name",
            world=self.world1,
            ally_tribe_tag=["pl1", "pl2"],
            enemy_tribe_tag=["pl3", " pl4"],
        )
        self.ally_tribe1 = models.Tribe(tribe_id=1, tag="pl1", world=self.world1)
        self.ally_tribe2 = models.Tribe(tribe_id=2, tag="pl2", world=self.world1)
        self.enemy_tribe1 = models.Tribe(tribe_id=3, tag="pl3", world=self.world1)
        self.enemy_tribe2 = models.Tribe(tribe_id=4, tag="pl4", world=self.world1)

        self.ally_player1 = models.Player(
            player_id=1,
            name="player1",
            tribe=self.ally_tribe1,
            world=self.world1,
        )
        self.ally_player2 = models.Player(
            player_id=2, name="player2", tribe=self.ally_tribe2, world=self.world1
        )

        self.enemy_player1 = models.Player(
            player_id=3, name="player3", tribe=self.enemy_tribe1, world=self.world1
        )
        self.enemy_player2 = models.Player(
            player_id=4, name="player4", tribe=self.enemy_tribe2, world=self.world1
        )
        self.ally_village1 = models.VillageModel(
            coord="500|500",
            village_id=1,
            x_coord=500,
            y_coord=500,
            player=self.ally_player2,
            world=self.world1,
        )
        self.ally_village2 = models.VillageModel(
            coord="499|500",
            village_id=2,
            x_coord=499,
            y_coord=500,
            player=self.ally_player1,
            world=self.world1,
        )
        # legal below
        self.ally_village3 = models.VillageModel(
            coord="498|503",
            village_id=3,
            x_coord=498,
            y_coord=503,
            player=self.ally_player2,
            world=self.world1,
        )
        self.ally_village4 = models.VillageModel(
            coord="500|502",
            village_id=4,
            x_coord=500,
            y_coord=502,
            player=self.ally_player2,
            world=self.world1,
        )
        self.ally_village5 = models.VillageModel(
            coord="498|502",
            village_id=5,
            x_coord=498,
            y_coord=502,
            player=self.ally_player2,
            world=self.world1,
        )
        self.ally_village6 = models.VillageModel(
            coord="500|499",
            village_id=6,
            x_coord=500,
            y_coord=499,
            player=self.ally_player2,
            world=self.world1,
        )

        self.enemy_village1 = models.VillageModel(
            coord="503|500",
            village_id=1,
            x_coord=503,
            y_coord=500,
            player=self.enemy_player1,
            world=self.world1,
        )
        self.enemy_village2 = models.VillageModel(
            coord="500|506",
            village_id=1,
            x_coord=500,
            y_coord=506,
            player=self.enemy_player2,
            world=self.world1,
        )

        self.ally_tribe1.save()
        self.ally_tribe2.save()
        self.enemy_tribe1.save()
        self.enemy_tribe2.save()
        self.ally_player1.save()
        self.ally_player2.save()
        self.enemy_player1.save()
        self.enemy_player2.save()
        self.ally_village1.save()
        self.ally_village2.save()
        self.ally_village3.save()
        self.ally_village4.save()
        self.ally_village5.save()
        self.ally_village6.save()
        self.enemy_village1.save()
        self.enemy_village2.save()
        self.player_dict = basic.coord_to_player(self.outline)
        self.evidence = basic.world_evidence(self.world1)

    def test_off_form_correct_one_line_correct(self):
        off_form = forms.OffTroopsForm(
            {"off_troops": self.text_off1}, outline=self.outline
        )
        self.assertTrue(off_form.is_valid())

    def test_off_form_not_correct_when_village_is_barbarian(self):
        barbarian_village = models.VillageModel.objects.get(coord="500|500")
        barbarian_village.player = None
        barbarian_village.save()
        off_form = forms.OffTroopsForm(
            {"off_troops": self.text_off1}, outline=self.outline
        )
        self.assertFalse(off_form.is_valid())

    def test_off_form_is_not_correct_one_line_with_empty_line_first(self):
        off_form = forms.OffTroopsForm(
            {"off_troops": "\r\n" + self.text_off1}, outline=self.outline
        )
        self.assertFalse(off_form.is_valid())

    def test_off_form_is_not_correct_one_line_with_empty_line_last(self):
        off_form = forms.OffTroopsForm(
            {"off_troops": self.text_off1 + "\r\n"}, outline=self.outline
        )
        self.assertFalse(off_form.is_valid())

    def test_off_form_is_not_correct_one_line_bad1(self):
        off_form = forms.OffTroopsForm(
            {"off_troops": self.text_off_bad1}, outline=self.outline
        )
        self.assertFalse(off_form.is_valid())

    def test_off_form_is_not_correct_one_line_bad11(self):
        off_form = forms.OffTroopsForm(
            {"off_troops": self.text_off_bad11}, outline=self.outline
        )
        self.assertFalse(off_form.is_valid())

    def test_off_form_is_not_correct_one_line_bad12(self):
        off_form = forms.OffTroopsForm(
            {"off_troops": self.text_off_bad12}, outline=self.outline
        )
        self.assertFalse(off_form.is_valid())

    def test_off_form_is_not_correct_one_line_bad13(self):
        off_form = forms.OffTroopsForm(
            {"off_troops": self.text_off_bad13}, outline=self.outline
        )
        self.assertFalse(off_form.is_valid())

    def test_off_form_is_not_correct_one_line_bad14(self):
        off_form = forms.OffTroopsForm(
            {"off_troops": self.text_off_bad14}, outline=self.outline
        )
        self.assertFalse(off_form.is_valid())

    def test_off_form_is_not_correct_with_only_second_line_bad11(self):
        off_form = forms.OffTroopsForm(
            {"off_troops": self.text_off1 + "\r\n" + self.text_off_bad11},
            outline=self.outline,
        )
        self.assertFalse(off_form.is_valid())

    def test_off_form_correct_is_not_correct_with_doubled_correct_lines(self):
        off_form = forms.OffTroopsForm(
            {"off_troops": self.text_off1 + "\r\n" + self.text_off1},
            outline=self.outline,
        )
        self.assertFalse(off_form.is_valid())
