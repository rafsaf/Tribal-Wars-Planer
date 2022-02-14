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

from secrets import SystemRandom

from django.db.models import ExpressionWrapper, F, FloatField
from django.test import TestCase
from django.utils.translation import activate

from base.models import Outline
from base.models import TargetVertex as Target
from base.models import WeightMaximum
from base.models.target_vertex import TargetVertex
from base.tests.test_utils.initial_setup import create_initial_data_write_outline
from utils.outline_initial import MakeOutline
from utils.write_ram_target import WriteRamTarget


class TestWriteRamTarget(TestCase):
    def setUp(self):
        activate("pl")
        create_initial_data_write_outline()
        self.outline: Outline = Outline.objects.get(id=1)
        make_outline: MakeOutline = MakeOutline(self.outline)
        make_outline()
        self.weight0: WeightMaximum = WeightMaximum.objects.get(start="500|500")
        self.weight1: WeightMaximum = WeightMaximum.objects.get(start="500|501")
        self.weight2: WeightMaximum = WeightMaximum.objects.get(start="500|502")
        self.weight3: WeightMaximum = WeightMaximum.objects.get(start="500|503")
        self.weight4: WeightMaximum = WeightMaximum.objects.get(start="500|504")
        self.weight5: WeightMaximum = WeightMaximum.objects.get(start="500|505")
        self.random = SystemRandom("test_write_target")

    def target(self, coord: str = "500|499") -> TargetVertex:
        target = Target.objects.create(
            outline=self.outline, target=coord, player="player1"
        )
        return target

    def get_weight_max_lst(self, target: TargetVertex) -> list[WeightMaximum]:
        coord = target.coord_tuple()
        return list(
            WeightMaximum.objects.filter(
                outline=self.outline, too_far_away=False
            ).annotate(
                distance=ExpressionWrapper(
                    ((F("x_coord") - coord[0]) ** 2 + (F("y_coord") - coord[1]) ** 2)
                    ** (1 / 2),
                    output_field=FloatField(max_length=5),
                )
            )
        )

    def get_write_target(self, target: TargetVertex) -> WriteRamTarget:
        write_noble = WriteRamTarget(
            target=target,
            outline=self.outline,
            weight_max_list=self.get_weight_max_lst(target),
            random=self.random,
        )
        return write_noble

    def test__add_night_bonus_annotations_cases(self):
        cases = [
            ("500|510", 1, 1, 7, 7, 1),
            ("500|515", 1, 1, 7, 7, 3),
            ("500|514", 1, 1, 7, 7, 2),
            ("500|513", 1, 1, 7, 7, 1),
            ("500|563", 1, 1, 7, 7, 3),
            ("500|562", 1, 1, 7, 7, 2),
            ("500|600", 0.5, 0.5, 7, 7, 3),
            ("499|600", 0.5, 0.5, 7, 9, 2),
            ("500|600", 0.5, 0.5, 21, 21, 3),
            ("500|600", 0.5, 0.5, 15, 15, 3),
            ("500|600", 0.5, 0.5, 22, 24, 3),
        ]
        for i, case in enumerate(cases):
            with self.subTest(number=i):
                target = self.target(case[0])
                self.outline.world.speed_world = case[1]
                self.outline.world.speed_units = case[2]
                target.enter_t1 = case[3]
                target.enter_t2 = case[4]
                write_target = self.get_write_target(target)
                write_target._add_night_bonus_annotations(write_target.weight_max_list)
                assert (
                    write_target.weight_max_list[0].night_bool == case[5]
                ), f"case {i}"
