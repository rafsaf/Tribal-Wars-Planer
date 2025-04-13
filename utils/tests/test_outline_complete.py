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


import itertools

from django.test import TestCase
from django.utils.translation import activate
from parameterized import parameterized

from base.models import Outline, WeightMaximum, WeightModel
from base.models import TargetVertex as Target
from base.models.player import Player
from base.models.result import Result
from base.tests.test_utils.initial_setup import create_initial_data_write_outline
from utils.avaiable_troops import get_legal_coords_outline
from utils.buildings import BUILDING, BUILDINGS_TRANSLATION
from utils.outline_complete import complete_outline_write
from utils.outline_initial import MakeOutline

# Please note that only extended syntax for the targets should be used.
# The tests should cover many diffrent outline ideas and available modes.
# Every method below is a next outline.
# Outline front dist equals to 3.
# The tests should not! include the "meat" inside.
# The only important are created (or not) weights models and state updates!

# TEXT = (
#    "500|500,0,0,10000,0,0,0,0,100,2,0,0,\r\n" - front
#    "500|501,0,0,190,0,0,0,0,100,0,0,0,\r\n" - front
#    "500|502,0,0,19500,0,0,0,0,100,0,0,0,\r\n" - front
#    "500|503,0,0,20100,0,0,0,0,100,0,0,0,\r\n" - back
#    "500|504,0,0,20000,0,0,0,0,100,4,0,0,\r\n" - back
#    "500|505,0,0,20000,0,0,0,0,100,2,0,0," - back
# )


class TestOutlineCreateTargets(TestCase):
    def setUp(self):
        activate("pl")
        create_initial_data_write_outline()

        self.outline: Outline = Outline.objects.get(id=1)
        # weights max create
        make_outline = MakeOutline(self.outline)
        make_outline()
        get_legal_coords_outline(self.outline)
        self.salt = "test_outline_complete"

    def target(self) -> Target:
        target = Target.objects.create(
            outline=self.outline, target="500|499", player="player1"
        )
        return target

    def weights(self) -> list[WeightModel]:
        return list(WeightModel.objects.all().select_related("state").order_by("order"))

    def test_indexes_are_correct_in_every_distance_real_target(self):
        self.outline.initial_outline_min_off = 100
        self.outline.save()
        target = self.target()
        target.mode_division = "separatly"
        target.exact_off = [1, 1, 1, 1]
        target.exact_noble = [1, 1, 1, 1]
        target.save()
        complete_outline_write(self.outline, salt=self.salt)
        created = self.weights()

        # there should be correct indexes
        self.assertEqual(created[0].order, 0)
        self.assertEqual(created[1].order, 10000)
        self.assertEqual(created[2].order, 20000)
        self.assertEqual(created[3].order, 30000)
        self.assertEqual(created[4].order, 80000)
        self.assertEqual(created[5].order, 90000)
        self.assertEqual(created[6].order, 100000)
        self.assertEqual(created[7].order, 110000)

    def test_indexes_are_correct_in_every_distance_fake_target(self):
        target = self.target()
        target.fake = True
        target.exact_off = [1, 1, 1, 1]
        target.exact_noble = [1, 1, 1, 1]
        target.save()
        # we don't care about modes here
        complete_outline_write(self.outline, salt=self.salt)
        created = self.weights()

        self.assertEqual(len(created), 8)
        # there should be correct indexes
        self.assertEqual(created[0].order, 0)
        self.assertEqual(created[1].order, 10000)
        self.assertEqual(created[2].order, 20000)
        self.assertEqual(created[3].order, 30000)
        self.assertEqual(created[4].order, 80000)
        self.assertEqual(created[5].order, 90000)
        self.assertEqual(created[6].order, 100000)
        self.assertEqual(created[7].order, 110000)

    def test_indexes_are_correct_in_every_distance_ruin_target(self):
        self.outline.initial_outline_min_off = 500
        self.outline.initial_outline_catapult_max_value = 50
        self.outline.save()
        target = self.target()
        target.ruin = True
        target.exact_off = [1, 1, 1, 1]
        target.exact_noble = [1, 1, 1, 1]
        target.save()
        # we don't care about modes here
        complete_outline_write(self.outline, salt=self.salt)
        created = self.weights()

        self.assertEqual(len(created), 8)
        # there should be correct indexes
        self.assertEqual(created[0].order, 0)
        self.assertEqual(created[1].order, 10000)
        self.assertEqual(created[2].order, 20000)
        self.assertEqual(created[3].order, 30000)
        self.assertEqual(created[4].order, 40000)
        self.assertEqual(created[5].order, 50000)
        self.assertEqual(created[6].order, 60000)
        self.assertEqual(created[7].order, 70000)

    def test_real_type_outline_guide_is_many_and_division_is_divide_split(self):
        self.outline.initial_outline_min_off = 500
        self.outline.mode_split = "split"
        self.outline.save()
        target = self.target()
        target.mode_division = "divide"
        target.mode_guide = "many"
        target.exact_off = [0, 0, 3, 0]
        target.exact_noble = [2, 0, 0, 0]
        target.save()
        complete_outline_write(self.outline, salt=self.salt)
        created = self.weights()
        self.assertEqual(len(created), 5)
        self.assertEqual(created[0].order, 10000)
        self.assertEqual(created[0].start, "500|505")
        self.assertEqual(created[0].off, 20800)
        self.assertEqual(created[0].catapult, 100)
        self.assertEqual(created[0].nobleman, 0)
        self.assertEqual(created[0].distance, 6)
        self.assertEqual(created[0].state.off_left, 0)
        self.assertEqual(created[0].state.off_state, 20800)
        self.assertEqual(created[0].state.catapult_left, 0)
        self.assertEqual(created[0].state.catapult_state, 100)
        self.assertEqual(created[0].state.nobleman_left, 2)
        self.assertEqual(created[0].state.nobleman_state, 0)

        self.assertEqual(created[1].order, 10001)
        self.assertEqual(created[1].start, "500|504")
        self.assertEqual(created[1].off, 20800)
        self.assertEqual(created[1].catapult, 100)
        self.assertEqual(created[1].nobleman, 0)
        self.assertEqual(created[1].distance, 5)
        self.assertEqual(created[1].state.off_left, 0)
        self.assertEqual(created[1].state.off_state, 20800)
        self.assertEqual(created[1].state.catapult_left, 0)
        self.assertEqual(created[1].state.catapult_state, 100)
        self.assertEqual(created[1].state.nobleman_left, 4)
        self.assertEqual(created[1].state.nobleman_state, 0)

        self.assertEqual(created[2].order, 10002)
        self.assertEqual(created[2].start, "500|503")
        self.assertEqual(created[2].off, 20900)
        self.assertEqual(created[2].catapult, 100)
        self.assertEqual(created[2].nobleman, 0)
        self.assertEqual(created[2].distance, 4)
        self.assertEqual(created[2].state.off_left, 0)
        self.assertEqual(created[2].state.off_state, 20900)
        self.assertEqual(created[2].state.catapult_left, 0)
        self.assertEqual(created[2].state.catapult_state, 100)
        self.assertEqual(created[2].state.nobleman_left, 0)
        self.assertEqual(created[2].state.nobleman_state, 0)

        self.assertEqual(created[3].order, 110000)
        self.assertEqual(created[3].off, 5400)
        self.assertEqual(created[3].start, "500|500")
        self.assertEqual(created[3].catapult, 100)
        self.assertEqual(created[3].nobleman, 1)
        self.assertEqual(created[3].distance, 1)
        self.assertEqual(created[3].state.off_left, 0)
        self.assertEqual(created[3].state.off_state, 10800)
        self.assertEqual(created[3].state.catapult_left, 0)
        self.assertEqual(created[3].state.catapult_state, 100)
        self.assertEqual(created[3].state.nobleman_left, 0)
        self.assertEqual(created[3].state.nobleman_state, 2)

        self.assertEqual(created[4].order, 110001)
        self.assertEqual(created[4].start, "500|500")
        self.assertEqual(created[4].off, 5400)
        self.assertEqual(created[4].catapult, 0)
        self.assertEqual(created[4].nobleman, 1)
        self.assertEqual(created[4].distance, 1)
        self.assertEqual(created[4].state.off_left, 0)
        self.assertEqual(created[4].state.off_state, 10800)
        self.assertEqual(created[4].state.catapult_left, 0)
        self.assertEqual(created[4].state.catapult_state, 100)
        self.assertEqual(created[4].state.nobleman_left, 0)
        self.assertEqual(created[4].state.nobleman_state, 2)

    def test_real_type_outline_guide_is_many_and_division_is_divide_together(self):
        self.outline.initial_outline_min_off = 500
        self.outline.mode_split = "together"
        self.outline.save()
        target = self.target()
        target.mode_division = "divide"
        target.mode_guide = "many"
        target.exact_off = [0, 0, 3, 0]
        target.exact_noble = [2, 0, 0, 0]
        target.save()
        complete_outline_write(self.outline, salt=self.salt)
        created = self.weights()
        self.assertEqual(len(created), 4)
        self.assertEqual(created[0].order, 10000)
        self.assertEqual(created[0].start, "500|505")
        self.assertEqual(created[0].off, 20800)
        self.assertEqual(created[0].catapult, 100)
        self.assertEqual(created[0].nobleman, 0)
        self.assertEqual(created[0].distance, 6)
        self.assertEqual(created[0].state.off_left, 0)
        self.assertEqual(created[0].state.off_state, 20800)
        self.assertEqual(created[0].state.catapult_left, 0)
        self.assertEqual(created[0].state.catapult_state, 100)
        self.assertEqual(created[0].state.nobleman_left, 2)
        self.assertEqual(created[0].state.nobleman_state, 0)

        self.assertEqual(created[1].order, 10001)
        self.assertEqual(created[1].start, "500|504")
        self.assertEqual(created[1].off, 20800)
        self.assertEqual(created[1].catapult, 100)
        self.assertEqual(created[1].nobleman, 0)
        self.assertEqual(created[1].distance, 5)
        self.assertEqual(created[1].state.off_left, 0)
        self.assertEqual(created[1].state.off_state, 20800)
        self.assertEqual(created[1].state.catapult_left, 0)
        self.assertEqual(created[1].state.catapult_state, 100)
        self.assertEqual(created[1].state.nobleman_left, 4)
        self.assertEqual(created[1].state.nobleman_state, 0)

        self.assertEqual(created[2].order, 10002)
        self.assertEqual(created[2].start, "500|503")
        self.assertEqual(created[2].off, 20900)
        self.assertEqual(created[2].catapult, 100)
        self.assertEqual(created[2].nobleman, 0)
        self.assertEqual(created[2].distance, 4)
        self.assertEqual(created[2].state.off_left, 0)
        self.assertEqual(created[2].state.off_state, 20900)
        self.assertEqual(created[2].state.catapult_left, 0)
        self.assertEqual(created[2].state.catapult_state, 100)
        self.assertEqual(created[2].state.nobleman_left, 0)
        self.assertEqual(created[2].state.nobleman_state, 0)

        self.assertEqual(created[3].order, 110000)
        self.assertEqual(created[3].off, 10800)
        self.assertEqual(created[3].start, "500|500")
        self.assertEqual(created[3].catapult, 100)
        self.assertEqual(created[3].nobleman, 2)
        self.assertEqual(created[3].distance, 1)
        self.assertEqual(created[3].state.off_left, 0)
        self.assertEqual(created[3].state.off_state, 10800)
        self.assertEqual(created[3].state.catapult_left, 0)
        self.assertEqual(created[3].state.catapult_state, 100)
        self.assertEqual(created[3].state.nobleman_left, 0)
        self.assertEqual(created[3].state.nobleman_state, 2)

    def test_real_type_outline_guide_is_one_and_division_is_not_divide_split(self):
        self.outline.initial_outline_min_off = 500
        self.outline.mode_split = "split"
        self.outline.save()
        target = self.target()
        target.mode_division = "not_divide"
        target.mode_guide = "one"
        target.exact_off = [0, 1, 0, 0]
        target.exact_noble = [0, 0, 6, 0]
        target.save()
        complete_outline_write(self.outline, salt=self.salt)
        created = self.weights()
        self.assertEqual(len(created), 7)
        self.assertEqual(created[0].order, 20000)
        self.assertEqual(created[0].start, "500|503")
        self.assertEqual(created[0].off, 20900)
        self.assertEqual(created[0].catapult, 100)
        self.assertEqual(created[0].nobleman, 0)
        self.assertEqual(created[0].distance, 4)
        self.assertEqual(created[0].state.off_left, 0)
        self.assertEqual(created[0].state.off_state, 20900)
        self.assertEqual(created[0].state.catapult_left, 0)
        self.assertEqual(created[0].state.catapult_state, 100)
        self.assertEqual(created[0].state.nobleman_left, 0)
        self.assertEqual(created[0].state.nobleman_state, 0)

        self.assertEqual(created[1].order, 90000)
        self.assertEqual(created[1].start, "500|505")
        self.assertEqual(created[1].off, 20700)
        self.assertEqual(created[1].catapult, 100)
        self.assertEqual(created[1].nobleman, 1)
        self.assertEqual(created[1].distance, 6)
        self.assertEqual(created[1].state.off_left, 0)
        self.assertEqual(created[1].state.off_state, 20800)
        self.assertEqual(created[1].state.catapult_left, 0)
        self.assertEqual(created[1].state.catapult_state, 100)
        self.assertEqual(created[1].state.nobleman_left, 0)
        self.assertEqual(created[1].state.nobleman_state, 2)

        self.assertEqual(created[2].order, 90001)
        self.assertEqual(created[2].start, "500|505")
        self.assertEqual(created[2].off, 100)
        self.assertEqual(created[2].catapult, 0)
        self.assertEqual(created[2].nobleman, 1)
        self.assertEqual(created[2].distance, 6)
        self.assertEqual(created[2].state.off_left, 0)
        self.assertEqual(created[2].state.off_state, 20800)
        self.assertEqual(created[2].state.catapult_left, 0)
        self.assertEqual(created[2].state.catapult_state, 100)
        self.assertEqual(created[2].state.nobleman_left, 0)
        self.assertEqual(created[2].state.nobleman_state, 2)

        self.assertEqual(created[3].order, 90015)
        self.assertEqual(created[3].start, "500|504")
        self.assertEqual(created[3].off, 20500)
        self.assertEqual(created[3].catapult, 100)
        self.assertEqual(created[3].nobleman, 1)
        self.assertEqual(created[3].distance, 5)
        self.assertEqual(created[3].state.off_left, 0)
        self.assertEqual(created[3].state.off_state, 20800)
        self.assertEqual(created[3].state.catapult_left, 0)
        self.assertEqual(created[3].state.catapult_state, 100)
        self.assertEqual(created[3].state.nobleman_left, 0)
        self.assertEqual(created[3].state.nobleman_state, 4)

        self.assertEqual(created[4].order, 90016)
        self.assertEqual(created[4].start, "500|504")
        self.assertEqual(created[4].off, 100)
        self.assertEqual(created[4].catapult, 0)
        self.assertEqual(created[4].nobleman, 1)
        self.assertEqual(created[4].distance, 5)
        self.assertEqual(created[4].state.off_left, 0)
        self.assertEqual(created[4].state.off_state, 20800)
        self.assertEqual(created[4].state.catapult_left, 0)
        self.assertEqual(created[4].state.catapult_state, 100)
        self.assertEqual(created[4].state.nobleman_left, 0)
        self.assertEqual(created[4].state.nobleman_state, 4)

        self.assertEqual(created[5].order, 90017)
        self.assertEqual(created[5].start, "500|504")
        self.assertEqual(created[5].off, 100)
        self.assertEqual(created[5].catapult, 0)
        self.assertEqual(created[5].nobleman, 1)
        self.assertEqual(created[5].distance, 5)
        self.assertEqual(created[5].state.off_left, 0)
        self.assertEqual(created[5].state.off_state, 20800)
        self.assertEqual(created[5].state.catapult_left, 0)
        self.assertEqual(created[5].state.catapult_state, 100)
        self.assertEqual(created[5].state.nobleman_left, 0)
        self.assertEqual(created[5].state.nobleman_state, 4)

        self.assertEqual(created[6].order, 90018)
        self.assertEqual(created[6].start, "500|504")
        self.assertEqual(created[6].off, 100)
        self.assertEqual(created[6].catapult, 0)
        self.assertEqual(created[6].nobleman, 1)
        self.assertEqual(created[6].distance, 5)
        self.assertEqual(created[6].state.off_left, 0)
        self.assertEqual(created[6].state.off_state, 20800)
        self.assertEqual(created[6].state.catapult_left, 0)
        self.assertEqual(created[6].state.catapult_state, 100)
        self.assertEqual(created[6].state.nobleman_left, 0)
        self.assertEqual(created[6].state.nobleman_state, 4)

    def test_real_type_outline_initial_outline_minimum_noble_troops_is_respected_v1(
        self,
    ):
        self.outline.initial_outline_min_off = 500
        self.outline.initial_outline_minimum_noble_troops = 10000
        self.outline.mode_split = "together"
        self.outline.save()
        target = self.target()
        target.mode_division = "divide"
        target.mode_guide = "many"
        target.exact_off = [0, 1, 0, 0]
        target.exact_noble = [0, 0, 6, 0]
        target.save()
        complete_outline_write(self.outline, salt=self.salt)
        created = self.weights()
        self.assertEqual(len(created), 3)
        self.assertEqual(created[0].order, 20000)
        self.assertEqual(created[0].start, "500|503")
        self.assertEqual(created[0].off, 20900)
        self.assertEqual(created[0].catapult, 100)
        self.assertEqual(created[0].nobleman, 0)
        self.assertEqual(created[0].distance, 4)
        self.assertEqual(created[0].state.off_left, 0)
        self.assertEqual(created[0].state.off_state, 20900)
        self.assertEqual(created[0].state.catapult_left, 0)
        self.assertEqual(created[0].state.catapult_state, 100)
        self.assertEqual(created[0].state.nobleman_left, 0)
        self.assertEqual(created[0].state.nobleman_state, 0)

        self.assertEqual(created[1].order, 90000)
        self.assertEqual(created[1].start, "500|505")
        self.assertEqual(created[1].off, 20800)
        self.assertEqual(created[1].catapult, 100)
        self.assertEqual(created[1].nobleman, 2)
        self.assertEqual(created[1].distance, 6)
        self.assertEqual(created[1].state.off_left, 0)
        self.assertEqual(created[1].state.off_state, 20800)
        self.assertEqual(created[1].state.catapult_left, 0)
        self.assertEqual(created[1].state.catapult_state, 100)
        self.assertEqual(created[1].state.nobleman_left, 0)
        self.assertEqual(created[1].state.nobleman_state, 2)

        self.assertEqual(created[2].order, 90001)
        self.assertEqual(created[2].start, "500|504")
        self.assertEqual(created[2].off, 20800)
        self.assertEqual(created[2].catapult, 100)
        self.assertEqual(created[2].nobleman, 2)
        self.assertEqual(created[2].distance, 5)
        self.assertEqual(created[2].state.off_left, 0)
        self.assertEqual(created[2].state.off_state, 20800)
        self.assertEqual(created[2].state.catapult_left, 0)
        self.assertEqual(created[2].state.catapult_state, 100)
        self.assertEqual(created[2].state.nobleman_left, 2)
        self.assertEqual(created[2].state.nobleman_state, 2)

    def test_real_type_outline_initial_outline_minimum_noble_troops_is_respected_v2(
        self,
    ):
        self.outline.initial_outline_min_off = 500
        self.outline.initial_outline_minimum_noble_troops = 15000
        self.outline.mode_split = "together"
        self.outline.save()
        target = self.target()
        target.mode_division = "divide"
        target.mode_guide = "many"
        target.exact_off = [0, 1, 0, 0]
        target.exact_noble = [0, 0, 6, 0]
        target.save()
        complete_outline_write(self.outline, salt=self.salt)
        created = self.weights()
        self.assertEqual(len(created), 3)
        self.assertEqual(created[0].order, 20000)
        self.assertEqual(created[0].start, "500|503")
        self.assertEqual(created[0].off, 20900)
        self.assertEqual(created[0].catapult, 100)
        self.assertEqual(created[0].nobleman, 0)
        self.assertEqual(created[0].distance, 4)
        self.assertEqual(created[0].state.off_left, 0)
        self.assertEqual(created[0].state.off_state, 20900)
        self.assertEqual(created[0].state.catapult_left, 0)
        self.assertEqual(created[0].state.catapult_state, 100)
        self.assertEqual(created[0].state.nobleman_left, 0)
        self.assertEqual(created[0].state.nobleman_state, 0)

        self.assertEqual(created[1].order, 90000)
        self.assertEqual(created[1].start, "500|505")
        self.assertEqual(created[1].off, 20800)
        self.assertEqual(created[1].catapult, 100)
        self.assertEqual(created[1].nobleman, 1)
        self.assertEqual(created[1].distance, 6)
        self.assertEqual(created[1].state.off_left, 0)
        self.assertEqual(created[1].state.off_state, 20800)
        self.assertEqual(created[1].state.catapult_left, 0)
        self.assertEqual(created[1].state.catapult_state, 100)
        self.assertEqual(created[1].state.nobleman_left, 1)
        self.assertEqual(created[1].state.nobleman_state, 1)

        self.assertEqual(created[2].order, 90001)
        self.assertEqual(created[2].start, "500|504")
        self.assertEqual(created[2].off, 20800)
        self.assertEqual(created[2].catapult, 100)
        self.assertEqual(created[2].nobleman, 1)
        self.assertEqual(created[2].distance, 5)
        self.assertEqual(created[2].state.off_left, 0)
        self.assertEqual(created[2].state.off_state, 20800)
        self.assertEqual(created[2].state.catapult_left, 0)
        self.assertEqual(created[2].state.catapult_state, 100)
        self.assertEqual(created[2].state.nobleman_left, 3)
        self.assertEqual(created[2].state.nobleman_state, 1)

    def test_real_type_outline_initial_outline_nobles_limit_is_respected_v1(
        self,
    ):
        self.outline.initial_outline_min_off = 500
        self.outline.initial_outline_minimum_noble_troops = 150
        self.outline.mode_split = "together"
        self.outline.initial_outline_nobles_limit = 1
        self.outline.save()
        target = self.target()
        target.mode_division = "divide"
        target.mode_guide = "many"
        target.exact_off = [0, 1, 0, 0]
        target.exact_noble = [0, 0, 6, 0]
        target.save()

        complete_outline_write(self.outline, salt=self.salt)
        created = self.weights()
        self.assertEqual(len(created), 3)
        self.assertEqual(created[0].order, 20000)
        self.assertEqual(created[0].start, "500|503")
        self.assertEqual(created[0].off, 20900)
        self.assertEqual(created[0].catapult, 100)
        self.assertEqual(created[0].nobleman, 0)
        self.assertEqual(created[0].distance, 4)
        self.assertEqual(created[0].state.off_left, 0)
        self.assertEqual(created[0].state.off_state, 20900)
        self.assertEqual(created[0].state.catapult_left, 0)
        self.assertEqual(created[0].state.catapult_state, 100)
        self.assertEqual(created[0].state.nobleman_left, 0)
        self.assertEqual(created[0].state.nobleman_state, 0)

        self.assertEqual(created[1].order, 90000)
        self.assertEqual(created[1].start, "500|505")
        self.assertEqual(created[1].off, 20800)
        self.assertEqual(created[1].catapult, 100)
        self.assertEqual(created[1].nobleman, 1)
        self.assertEqual(created[1].distance, 6)
        self.assertEqual(created[1].state.off_left, 0)
        self.assertEqual(created[1].state.off_state, 20800)
        self.assertEqual(created[1].state.catapult_left, 0)
        self.assertEqual(created[1].state.catapult_state, 100)
        self.assertEqual(created[1].state.nobleman_left, 1)
        self.assertEqual(created[1].state.nobleman_state, 1)

        self.assertEqual(created[2].order, 90001)
        self.assertEqual(created[2].start, "500|504")
        self.assertEqual(created[2].off, 20800)
        self.assertEqual(created[2].catapult, 100)
        self.assertEqual(created[2].nobleman, 1)
        self.assertEqual(created[2].distance, 5)
        self.assertEqual(created[2].state.off_left, 0)
        self.assertEqual(created[2].state.off_state, 20800)
        self.assertEqual(created[2].state.catapult_left, 0)
        self.assertEqual(created[2].state.catapult_state, 100)
        self.assertEqual(created[2].state.nobleman_left, 3)
        self.assertEqual(created[2].state.nobleman_state, 1)

    def test_real_type_outline_guide_is_single_and_division_is_separatly_split(self):
        self.outline.initial_outline_min_off = 1000
        self.outline.mode_split = "split"
        self.outline.save()
        target = self.target()
        target.mode_division = "separatly"
        target.mode_guide = "single"
        target.exact_off = [2, 0, 0, 0]
        target.exact_noble = [3, 0, 0, 0]
        target.save()
        complete_outline_write(self.outline, salt=self.salt)
        created = self.weights()
        self.assertEqual(len(created), 5)

        self.assertEqual(created[0].order, 30000)
        self.assertEqual(created[0].start, "500|502")
        self.assertEqual(created[0].off, 20300)
        self.assertEqual(created[0].catapult, 100)
        self.assertEqual(created[0].nobleman, 0)
        self.assertEqual(created[0].distance, 3)
        self.assertEqual(created[0].state.off_left, 0)
        self.assertEqual(created[0].state.off_state, 20300)
        self.assertEqual(created[0].state.catapult_left, 0)
        self.assertEqual(created[0].state.catapult_state, 100)
        self.assertEqual(created[0].state.nobleman_left, 0)
        self.assertEqual(created[0].state.nobleman_state, 0)

        self.assertEqual(created[1].order, 30001)
        self.assertEqual(created[1].start, "500|500")
        self.assertEqual(created[1].off, 10700)
        self.assertEqual(created[1].catapult, 100)
        self.assertEqual(created[1].nobleman, 0)
        self.assertEqual(created[1].distance, 1)
        self.assertEqual(created[1].state.off_left, 0)
        self.assertEqual(created[1].state.off_state, 10800)
        self.assertEqual(created[1].state.catapult_left, 0)
        self.assertEqual(created[1].state.catapult_state, 100)
        self.assertEqual(created[1].state.nobleman_left, 1)
        self.assertEqual(created[1].state.nobleman_state, 1)

        self.assertEqual(created[2].order, 110000)
        self.assertEqual(created[2].start, "500|505")
        self.assertEqual(created[2].off, 100)
        self.assertEqual(created[2].catapult, 0)
        self.assertEqual(created[2].nobleman, 1)
        self.assertEqual(created[2].distance, 6)
        self.assertEqual(created[2].state.off_left, 20700)
        self.assertEqual(created[2].state.off_state, 100)
        self.assertEqual(created[2].state.catapult_left, 100)
        self.assertEqual(created[2].state.catapult_state, 0)
        self.assertEqual(created[2].state.nobleman_left, 1)
        self.assertEqual(created[2].state.nobleman_state, 1)

        self.assertEqual(created[3].order, 110015)
        self.assertEqual(created[3].start, "500|504")
        self.assertEqual(created[3].off, 100)
        self.assertEqual(created[3].catapult, 0)
        self.assertEqual(created[3].nobleman, 1)
        self.assertEqual(created[3].distance, 5)
        self.assertEqual(created[3].state.off_left, 20700)
        self.assertEqual(created[3].state.off_state, 100)
        self.assertEqual(created[3].state.catapult_left, 100)
        self.assertEqual(created[3].state.catapult_state, 0)
        self.assertEqual(created[3].state.nobleman_left, 3)
        self.assertEqual(created[3].state.nobleman_state, 1)

        self.assertEqual(created[4].order, 110030)
        self.assertEqual(created[4].start, "500|500")
        self.assertEqual(created[4].off, 100)
        self.assertEqual(created[4].catapult, 0)
        self.assertEqual(created[4].nobleman, 1)
        self.assertEqual(created[4].distance, 1)
        self.assertEqual(created[4].state.off_left, 0)
        self.assertEqual(created[4].state.off_state, 10800)
        self.assertEqual(created[4].state.catapult_left, 0)
        self.assertEqual(created[4].state.catapult_state, 100)
        self.assertEqual(created[4].state.nobleman_left, 1)
        self.assertEqual(created[4].state.nobleman_state, 1)

    def test_real_type_outline_guide_is_single_and_division_is_separatly_together(self):
        self.outline.initial_outline_min_off = 1000
        self.outline.mode_split = "together"
        self.outline.save()
        target = self.target()
        target.mode_division = "separatly"
        target.mode_guide = "single"
        target.exact_off = [2, 0, 0, 0]
        target.exact_noble = [3, 0, 0, 0]
        target.save()
        complete_outline_write(self.outline, salt=self.salt)
        created = self.weights()
        self.assertEqual(len(created), 5)

        self.assertEqual(created[0].order, 30000)
        self.assertEqual(created[0].start, "500|502")
        self.assertEqual(created[0].off, 20300)
        self.assertEqual(created[0].catapult, 100)
        self.assertEqual(created[0].nobleman, 0)
        self.assertEqual(created[0].distance, 3)
        self.assertEqual(created[0].state.off_left, 0)
        self.assertEqual(created[0].state.off_state, 20300)
        self.assertEqual(created[0].state.catapult_left, 0)
        self.assertEqual(created[0].state.catapult_state, 100)
        self.assertEqual(created[0].state.nobleman_left, 0)
        self.assertEqual(created[0].state.nobleman_state, 0)

        self.assertEqual(created[1].order, 30001)
        self.assertEqual(created[1].start, "500|500")
        self.assertEqual(created[1].off, 10700)
        self.assertEqual(created[1].catapult, 100)
        self.assertEqual(created[1].nobleman, 0)
        self.assertEqual(created[1].distance, 1)
        self.assertEqual(created[1].state.off_left, 0)
        self.assertEqual(created[1].state.off_state, 10800)
        self.assertEqual(created[1].state.catapult_left, 0)
        self.assertEqual(created[1].state.catapult_state, 100)
        self.assertEqual(created[1].state.nobleman_left, 1)
        self.assertEqual(created[1].state.nobleman_state, 1)

        self.assertEqual(created[2].order, 110000)
        self.assertEqual(created[2].start, "500|505")
        self.assertEqual(created[2].off, 100)
        self.assertEqual(created[2].catapult, 0)
        self.assertEqual(created[2].nobleman, 1)
        self.assertEqual(created[2].distance, 6)
        self.assertEqual(created[2].state.off_left, 20700)
        self.assertEqual(created[2].state.off_state, 100)
        self.assertEqual(created[2].state.catapult_left, 100)
        self.assertEqual(created[2].state.catapult_state, 0)
        self.assertEqual(created[2].state.nobleman_left, 1)
        self.assertEqual(created[2].state.nobleman_state, 1)

        self.assertEqual(created[3].order, 110001)
        self.assertEqual(created[3].start, "500|504")
        self.assertEqual(created[3].off, 100)
        self.assertEqual(created[3].catapult, 0)
        self.assertEqual(created[3].nobleman, 1)
        self.assertEqual(created[3].distance, 5)
        self.assertEqual(created[3].state.off_left, 20700)
        self.assertEqual(created[3].state.off_state, 100)
        self.assertEqual(created[3].state.catapult_left, 100)
        self.assertEqual(created[3].state.catapult_state, 0)
        self.assertEqual(created[3].state.nobleman_left, 3)
        self.assertEqual(created[3].state.nobleman_state, 1)

        self.assertEqual(created[4].order, 110002)
        self.assertEqual(created[4].start, "500|500")
        self.assertEqual(created[4].off, 100)
        self.assertEqual(created[4].catapult, 0)
        self.assertEqual(created[4].nobleman, 1)
        self.assertEqual(created[4].distance, 1)
        self.assertEqual(created[4].state.off_left, 0)
        self.assertEqual(created[4].state.off_state, 10800)
        self.assertEqual(created[4].state.catapult_left, 0)
        self.assertEqual(created[4].state.catapult_state, 100)
        self.assertEqual(created[4].state.nobleman_left, 1)
        self.assertEqual(created[4].state.nobleman_state, 1)

    def test_real_type_outline_guide_is_single_and_division_is_divide_and_noble_max_1(
        self,
    ):
        self.outline.initial_outline_min_off = 1000
        self.outline.mode_split = "together"
        self.outline.initial_outline_nobles_limit = 1
        self.outline.initial_outline_minimum_fake_noble_troops = 150
        self.outline.save()
        target = self.target()
        target.mode_division = "divide"
        target.mode_guide = "single"
        target.exact_off = [2, 0, 0, 0]
        target.exact_noble = [3, 0, 0, 0]
        target.save()
        complete_outline_write(self.outline, salt=self.salt)
        created = self.weights()
        import pprint

        pprint.pprint([w.__dict__ for w in created])
        self.assertEqual(len(created), 5)

        self.assertEqual(created[0].order, 30000)
        self.assertEqual(created[0].start, "500|503")
        self.assertEqual(created[0].off, 20900)
        self.assertEqual(created[0].catapult, 100)
        self.assertEqual(created[0].nobleman, 0)
        self.assertEqual(created[0].distance, 4.0)
        self.assertEqual(created[0].state.off_left, 0)
        self.assertEqual(created[0].state.off_state, 20900)
        self.assertEqual(created[0].state.catapult_left, 0)
        self.assertEqual(created[0].state.catapult_state, 100)
        self.assertEqual(created[0].state.nobleman_left, 0)
        self.assertEqual(created[0].state.nobleman_state, 0)

        self.assertEqual(created[1].order, 30001)
        self.assertEqual(created[1].start, "500|502")
        self.assertEqual(created[1].off, 20300)
        self.assertEqual(created[1].catapult, 100)
        self.assertEqual(created[1].nobleman, 0)
        self.assertEqual(created[1].distance, 3.0)
        self.assertEqual(created[1].state.off_left, 0)
        self.assertEqual(created[1].state.off_state, 20300)
        self.assertEqual(created[1].state.catapult_left, 0)
        self.assertEqual(created[1].state.catapult_state, 100)
        self.assertEqual(created[1].state.nobleman_left, 0)
        self.assertEqual(created[1].state.nobleman_state, 0)

        self.assertEqual(created[2].order, 110000)
        self.assertEqual(created[2].start, "500|505")
        self.assertEqual(created[2].off, 20650)
        self.assertEqual(created[2].catapult, 100)
        self.assertEqual(created[2].nobleman, 1)
        self.assertEqual(created[2].distance, 6)
        self.assertEqual(created[2].state.off_left, 150)
        self.assertEqual(created[2].state.off_state, 20650)
        self.assertEqual(created[2].state.catapult_left, 0)
        self.assertEqual(created[2].state.catapult_state, 100)
        self.assertEqual(created[2].state.nobleman_left, 1)
        self.assertEqual(created[2].state.nobleman_state, 1)

        self.assertEqual(created[3].order, 110001)
        self.assertEqual(created[3].start, "500|504")
        self.assertEqual(created[3].off, 20650)
        self.assertEqual(created[3].catapult, 100)
        self.assertEqual(created[3].nobleman, 1)
        self.assertEqual(created[3].distance, 5)
        self.assertEqual(created[3].state.off_left, 150)
        self.assertEqual(created[3].state.off_state, 20650)
        self.assertEqual(created[3].state.catapult_left, 0)
        self.assertEqual(created[3].state.catapult_state, 100)
        self.assertEqual(created[3].state.nobleman_left, 3)
        self.assertEqual(created[3].state.nobleman_state, 1)

        self.assertEqual(created[4].order, 110002)
        self.assertEqual(created[4].start, "500|500")
        self.assertEqual(created[4].off, 10650)
        self.assertEqual(created[4].catapult, 100)
        self.assertEqual(created[4].nobleman, 1)
        self.assertEqual(created[4].distance, 1)
        self.assertEqual(created[4].state.off_left, 150)
        self.assertEqual(created[4].state.off_state, 10650)
        self.assertEqual(created[4].state.catapult_left, 0)
        self.assertEqual(created[4].state.catapult_state, 100)
        self.assertEqual(created[4].state.nobleman_left, 1)
        self.assertEqual(created[4].state.nobleman_state, 1)

    def test_fake_type_outline_guide_is_many_and_division_is_divide_split(self):
        self.outline.initial_outline_min_off = 500
        self.outline.mode_split = "split"
        self.outline.save()
        target = self.target()
        target.fake = True
        target.mode_division = "divide"
        target.mode_guide = "many"
        target.exact_off = [0, 0, 3, 0]
        target.exact_noble = [2, 0, 0, 0]
        target.save()
        complete_outline_write(self.outline, salt=self.salt)
        created = self.weights()
        self.assertEqual(len(created), 5)
        self.assertEqual(created[0].order, 10000)
        self.assertEqual(created[0].start, "500|505")
        self.assertEqual(created[0].off, 100)
        self.assertEqual(created[0].catapult, 0)
        self.assertEqual(created[0].nobleman, 0)
        self.assertEqual(created[0].distance, 6)
        self.assertEqual(created[0].state.off_left, 20700)
        self.assertEqual(created[0].state.off_state, 100)
        self.assertEqual(created[0].state.catapult_left, 100)
        self.assertEqual(created[0].state.catapult_state, 0)
        self.assertEqual(created[0].state.nobleman_left, 2)
        self.assertEqual(created[0].state.nobleman_state, 0)

        self.assertEqual(created[1].order, 10001)
        self.assertEqual(created[1].start, "500|504")
        self.assertEqual(created[1].off, 100)
        self.assertEqual(created[1].catapult, 0)
        self.assertEqual(created[1].nobleman, 0)
        self.assertEqual(created[1].distance, 5)
        self.assertEqual(created[1].state.off_left, 20700)
        self.assertEqual(created[1].state.off_state, 100)
        self.assertEqual(created[1].state.catapult_left, 100)
        self.assertEqual(created[1].state.catapult_state, 0)
        self.assertEqual(created[1].state.nobleman_left, 4)
        self.assertEqual(created[1].state.nobleman_state, 0)

        self.assertEqual(created[2].order, 10002)
        self.assertEqual(created[2].start, "500|503")
        self.assertEqual(created[2].off, 100)
        self.assertEqual(created[2].catapult, 0)
        self.assertEqual(created[2].nobleman, 0)
        self.assertEqual(created[2].distance, 4)
        self.assertEqual(created[2].state.off_left, 20800)
        self.assertEqual(created[2].state.off_state, 100)
        self.assertEqual(created[2].state.catapult_left, 100)
        self.assertEqual(created[2].state.catapult_state, 0)
        self.assertEqual(created[2].state.nobleman_left, 0)
        self.assertEqual(created[2].state.nobleman_state, 0)

        self.assertEqual(created[3].order, 110000)
        self.assertEqual(created[3].off, 0)
        self.assertEqual(created[3].start, "500|500")
        self.assertEqual(created[3].catapult, 0)
        self.assertEqual(created[3].nobleman, 1)
        self.assertEqual(created[3].distance, 1)
        self.assertEqual(created[3].state.off_left, 10800)
        self.assertEqual(created[3].state.off_state, 0)
        self.assertEqual(created[3].state.catapult_left, 100)
        self.assertEqual(created[3].state.catapult_state, 0)
        self.assertEqual(created[3].state.nobleman_left, 0)
        self.assertEqual(created[3].state.nobleman_state, 2)

        self.assertEqual(created[4].order, 110001)
        self.assertEqual(created[4].start, "500|500")
        self.assertEqual(created[4].off, 0)
        self.assertEqual(created[4].catapult, 0)
        self.assertEqual(created[4].nobleman, 1)
        self.assertEqual(created[4].distance, 1)
        self.assertEqual(created[4].state.off_left, 10800)
        self.assertEqual(created[4].state.off_state, 0)
        self.assertEqual(created[4].state.catapult_left, 100)
        self.assertEqual(created[4].state.catapult_state, 0)
        self.assertEqual(created[4].state.nobleman_left, 0)
        self.assertEqual(created[4].state.nobleman_state, 2)

    def test_fake_type_outline_guide_is_many_and_division_is_divide_together(self):
        self.outline.initial_outline_min_off = 500
        self.outline.mode_split = "together"
        self.outline.save()
        target = self.target()
        target.fake = True
        target.mode_division = "divide"
        target.mode_guide = "many"
        target.exact_off = [0, 0, 3, 0]
        target.exact_noble = [2, 0, 0, 0]
        target.save()
        complete_outline_write(self.outline, salt=self.salt)
        created = self.weights()
        self.assertEqual(len(created), 4)
        self.assertEqual(created[0].order, 10000)
        self.assertEqual(created[0].start, "500|505")
        self.assertEqual(created[0].off, 100)
        self.assertEqual(created[0].catapult, 0)
        self.assertEqual(created[0].nobleman, 0)
        self.assertEqual(created[0].distance, 6)
        self.assertEqual(created[0].state.off_left, 20700)
        self.assertEqual(created[0].state.off_state, 100)
        self.assertEqual(created[0].state.catapult_left, 100)
        self.assertEqual(created[0].state.catapult_state, 0)
        self.assertEqual(created[0].state.nobleman_left, 2)
        self.assertEqual(created[0].state.nobleman_state, 0)

        self.assertEqual(created[1].order, 10001)
        self.assertEqual(created[1].start, "500|504")
        self.assertEqual(created[1].off, 100)
        self.assertEqual(created[1].catapult, 00)
        self.assertEqual(created[1].nobleman, 0)
        self.assertEqual(created[1].distance, 5)
        self.assertEqual(created[1].state.off_left, 20700)
        self.assertEqual(created[1].state.off_state, 100)
        self.assertEqual(created[1].state.catapult_left, 100)
        self.assertEqual(created[1].state.catapult_state, 0)
        self.assertEqual(created[1].state.nobleman_left, 4)
        self.assertEqual(created[1].state.nobleman_state, 0)

        self.assertEqual(created[2].order, 10002)
        self.assertEqual(created[2].start, "500|503")
        self.assertEqual(created[2].off, 100)
        self.assertEqual(created[2].catapult, 0)
        self.assertEqual(created[2].nobleman, 0)
        self.assertEqual(created[2].distance, 4)
        self.assertEqual(created[2].state.off_left, 20800)
        self.assertEqual(created[2].state.off_state, 100)
        self.assertEqual(created[2].state.catapult_left, 100)
        self.assertEqual(created[2].state.catapult_state, 0)
        self.assertEqual(created[2].state.nobleman_left, 0)
        self.assertEqual(created[2].state.nobleman_state, 0)

        self.assertEqual(created[3].order, 110000)
        self.assertEqual(created[3].off, 0)
        self.assertEqual(created[3].start, "500|500")
        self.assertEqual(created[3].catapult, 0)
        self.assertEqual(created[3].nobleman, 2)
        self.assertEqual(created[3].distance, 1)
        self.assertEqual(created[3].state.off_left, 10800)
        self.assertEqual(created[3].state.off_state, 0)
        self.assertEqual(created[3].state.catapult_left, 100)
        self.assertEqual(created[3].state.catapult_state, 0)
        self.assertEqual(created[3].state.nobleman_left, 0)
        self.assertEqual(created[3].state.nobleman_state, 2)

    def test_ruin_type_outline_headquarters(self):
        self.outline.initial_outline_min_off = 500
        self.outline.mode_split = "split"
        self.outline.initial_outline_buildings = [BUILDING.HEADQUARTERS.value]
        self.outline.initial_outline_catapult_max_value = 100
        self.outline.initial_outline_off_left_catapult = 0
        self.outline.save()
        target = self.target()
        target.ruin = True
        target.exact_off = [0, 0, 0, 0]
        target.exact_noble = [0, 0, 3, 0]
        target.save()
        complete_outline_write(self.outline, salt=self.salt)
        created = self.weights()
        self.assertEqual(len(created), 3)
        self.assertEqual(created[0].order, 50000)
        self.assertEqual(created[0].start, "500|505")
        self.assertEqual(created[0].off, 800)
        self.assertEqual(created[0].catapult, 100)
        self.assertEqual(created[0].building, BUILDING.HEADQUARTERS.value)
        self.assertEqual(created[0].nobleman, 0)
        self.assertEqual(created[0].distance, 6)
        self.assertEqual(created[0].state.off_left, 20000)
        self.assertEqual(created[0].state.off_state, 800)
        self.assertEqual(created[0].state.catapult_left, 0)
        self.assertEqual(created[0].state.catapult_state, 100)
        self.assertEqual(created[0].state.nobleman_left, 2)
        self.assertEqual(created[0].state.nobleman_state, 0)

        self.assertEqual(created[1].order, 50001)
        self.assertEqual(created[1].start, "500|504")
        self.assertEqual(created[1].off, 800)
        self.assertEqual(created[1].catapult, 100)
        self.assertEqual(created[1].building, BUILDING.HEADQUARTERS.value)
        self.assertEqual(created[1].nobleman, 0)
        self.assertEqual(created[1].distance, 5)
        self.assertEqual(created[1].state.off_left, 20000)
        self.assertEqual(created[1].state.off_state, 800)
        self.assertEqual(created[1].state.catapult_left, 0)
        self.assertEqual(created[1].state.catapult_state, 100)
        self.assertEqual(created[1].state.nobleman_left, 4)
        self.assertEqual(created[1].state.nobleman_state, 0)

        self.assertEqual(created[2].order, 50002)
        self.assertEqual(created[2].start, "500|503")
        self.assertEqual(created[2].catapult, 25)
        self.assertEqual(created[2].off, 200)
        self.assertEqual(created[2].building, BUILDING.HEADQUARTERS.value)
        self.assertEqual(created[2].nobleman, 0)
        self.assertEqual(created[2].distance, 4)
        self.assertEqual(created[2].state.off_left, 20700)
        self.assertEqual(created[2].state.off_state, 200)
        self.assertEqual(created[2].state.catapult_left, 75)
        self.assertEqual(created[2].state.catapult_state, 25)
        self.assertEqual(created[2].state.nobleman_left, 0)
        self.assertEqual(created[2].state.nobleman_state, 0)

    @parameterized.expand(sorted([str(name) for name in BUILDINGS_TRANSLATION.keys()]))
    def test_ruin_type_outline_all_buidlings_are_supported(self, building: str):
        self.outline.initial_outline_min_off = 500
        self.outline.mode_split = "split"
        self.outline.initial_outline_buildings = [building]
        self.outline.initial_outline_catapult_max_value = 100
        self.outline.initial_outline_off_left_catapult = 0
        self.outline.save()
        target = self.target()
        target.ruin = True
        target.exact_off = [0, 0, 0, 0]
        target.exact_noble = [0, 0, 3, 0]
        target.save()
        complete_outline_write(self.outline, salt=self.salt)
        created = self.weights()
        self.assertGreaterEqual(len(created), 1)

    def test_ruin_type_outline_smithy(self):
        self.outline.initial_outline_min_off = 500
        self.outline.mode_split = "split"
        self.outline.initial_outline_buildings = [
            BUILDING.SMITHY.value,
            BUILDING.CLAY_PIT.value,
        ]
        self.outline.initial_outline_catapult_max_value = 200
        self.outline.initial_outline_off_left_catapult = 0
        self.outline.save()
        target = self.target()
        target.ruin = True
        target.exact_off = [0, 0, 0, 0]
        target.exact_noble = [0, 0, 3, 0]
        target.save()
        weight: WeightMaximum = WeightMaximum.objects.get(start="500|505")
        weight.catapult_left = 200
        weight.catapult_max = 200
        weight.off_left += 800
        weight.off_max += 800
        weight.save()
        complete_outline_write(self.outline, salt=self.salt)
        created = self.weights()
        self.assertEqual(len(created), 3)
        self.assertEqual(created[0].order, 50000)
        self.assertEqual(created[0].start, "500|505")
        self.assertEqual(created[0].off, 1600)
        self.assertEqual(created[0].catapult, 200)
        self.assertEqual(created[0].building, BUILDING.SMITHY.value)
        self.assertEqual(created[0].nobleman, 0)
        self.assertEqual(created[0].distance, 6)
        self.assertEqual(created[0].state.off_left, 20000)
        self.assertEqual(created[0].state.off_state, 1600)
        self.assertEqual(created[0].state.catapult_left, 0)
        self.assertEqual(created[0].state.catapult_state, 200)
        self.assertEqual(created[0].state.nobleman_left, 2)
        self.assertEqual(created[0].state.nobleman_state, 0)

        self.assertEqual(created[1].order, 50001)
        self.assertEqual(created[1].start, "500|504")
        self.assertEqual(created[1].off, 400)
        self.assertEqual(created[1].catapult, 50)
        self.assertEqual(created[1].building, BUILDING.SMITHY.value)
        self.assertEqual(created[1].nobleman, 0)
        self.assertEqual(created[1].distance, 5)
        self.assertEqual(created[1].state.off_left, 20400)
        self.assertEqual(created[1].state.off_state, 400)
        self.assertEqual(created[1].state.catapult_left, 50)
        self.assertEqual(created[1].state.catapult_state, 50)
        self.assertEqual(created[1].state.nobleman_left, 4)
        self.assertEqual(created[1].state.nobleman_state, 0)

        self.assertEqual(created[2].order, 50002)
        self.assertEqual(created[2].start, "500|503")
        self.assertEqual(created[2].off, 800)
        self.assertEqual(created[2].catapult, 100)
        self.assertEqual(created[2].building, BUILDING.CLAY_PIT.value)
        self.assertEqual(created[2].nobleman, 0)
        self.assertEqual(created[2].distance, 4)
        self.assertEqual(created[2].state.off_left, 20100)
        self.assertEqual(created[2].state.off_state, 800)
        self.assertEqual(created[2].state.catapult_left, 0)
        self.assertEqual(created[2].state.catapult_state, 100)
        self.assertEqual(created[2].state.nobleman_left, 0)
        self.assertEqual(created[2].state.nobleman_state, 0)

    def test_real_type_outline_defuault_settings_initial_outline_max_off_used_no_targets_created(
        self,
    ):
        self.outline.initial_outline_min_off = 10000
        self.outline.initial_outline_max_off = 20300
        self.outline.mode_split = "together"
        self.outline.save()
        target = self.target()
        target.mode_division = "divide"
        target.mode_guide = "many"
        target.exact_off = [0, 0, 5, 0]
        target.save()
        complete_outline_write(self.outline, salt=self.salt)
        created = self.weights()
        assert len(created) == 0

    def test_real_type_outline_defuault_settings_initial_outline_max_off_used_good_offs_taken(
        self,
    ):
        self.outline.initial_outline_min_off = 10000
        self.outline.initial_outline_max_off = 20800
        self.outline.mode_split = "together"
        self.outline.save()
        target = self.target()
        target.mode_division = "divide"
        target.mode_guide = "many"
        target.exact_off = [10, 0, 0, 0]
        target.save()
        complete_outline_write(self.outline, salt=self.salt)
        created = self.weights()
        assert len(created) == 4

        assert created[0].order == 30000
        assert created[0].start == "500|505"
        assert created[0].off == 20800

        assert created[1].order == 30001
        assert created[1].start == "500|504"
        assert created[1].off == 20800

        assert created[2].order == 30002
        assert created[2].start == "500|502"
        assert created[2].off == 20300

        assert created[3].order == 30003
        assert created[3].start == "500|500"
        assert created[3].off == 10800

    def test_no_targets_outline_complete(self):
        Target.objects.all().delete()
        complete_outline_write(self.outline, salt=self.salt)

    def test_all_possible_2304_combionations_of_outline_complete(self):
        MODE_OFF = [mode[0] for mode in Target.MODE_OFF]
        MODE_NOBLE = [mode[0] for mode in Target.MODE_NOBLE]
        MODE_DIVISION = [mode[0] for mode in Target.MODE_DIVISION]
        NOBLE_GUIDELINES = [mode[0] for mode in Target.NOBLE_GUIDELINES]
        MODE_SPLIT = [mode[0] for mode in Outline.MODE_SPLIT]
        RUINED_VILLAGES_POINTS = [mode[0] for mode in Outline.RUINED_VILLAGES_POINTS]
        FAKE_MIN_OFF_CHOICES = [mode[0] for mode in Outline.FAKE_MIN_OFF_CHOICES]
        NIGHT_BONUS = [True, False]

        cases: list[tuple[str, str, str, str, str, str, str, bool]] = itertools.product(
            *[
                MODE_OFF,
                MODE_NOBLE,
                MODE_DIVISION,
                NOBLE_GUIDELINES,
                MODE_SPLIT,
                RUINED_VILLAGES_POINTS,
                FAKE_MIN_OFF_CHOICES,
                NIGHT_BONUS,
            ]
        )  # type: ignore

        Result.objects.create(outline=self.outline)
        self.outline.initial_outline_min_off = 10000
        self.outline.initial_outline_max_off = 28000
        self.outline.save()
        target = self.target()

        for test_input in cases:
            target.mode_off = test_input[0]
            target.mode_noble = test_input[1]
            target.mode_division = test_input[2]
            target.mode_guide = test_input[3]
            target.required_off = 1
            target.required_noble = 1
            target.night_bonus = test_input[7]
            target.save()
            self.outline.mode_split = test_input[4]
            self.outline.initial_outline_average_ruining_points = test_input[5]
            self.outline.initial_outline_fake_mode = test_input[6]
            self.outline.night_bonus = test_input[7]
            self.outline.save()
            complete_outline_write(self.outline, salt="test_outline_complete")
            assert len(self.weights()) == 2
            self.outline.remove_user_outline()

    def test_morale_on_leads_to_skip_all_villages_for_low_morale_value(
        self,
    ):
        self.outline.initial_outline_min_off = 0
        self.outline.initial_outline_max_off = 28000
        self.outline.morale_on = True
        self.outline.morale_on_targets_greater_than = 95
        self.outline.save()

        ally_player: Player = Player.objects.get(name="player0")
        enemy_player: Player = Player.objects.get(name="player1")
        ally_player.points = 1200
        enemy_player.points = 250  # morale 93%
        ally_player.save()
        enemy_player.save()

        # recreate weight maxs so points will not be default 0
        make_outline = MakeOutline(self.outline)
        make_outline()

        target = self.target()
        target.exact_off = [10, 0, 0, 0]
        target.exact_noble = [10, 0, 0, 0]
        target.save()
        complete_outline_write(self.outline, salt=self.salt)
        created = self.weights()
        assert len(created) == 0
