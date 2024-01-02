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

from base.models import Outline, WeightMaximum, WeightModel
from base.models import TargetVertex as Target
from base.models.target_vertex import TargetVertex
from base.tests.test_utils.initial_setup import create_initial_data_write_outline
from base.tests.test_utils.mini_setup import MiniSetup
from utils.outline_initial import MakeOutline
from utils.write_noble_target import WriteNobleTarget


class TestWriteNobleTarget(TestCase):
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
        self.random = SystemRandom("test_write_noble")

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

    def get_write_noble(self, target: TargetVertex) -> WriteNobleTarget:
        write_noble = WriteNobleTarget(
            target=target,
            outline=self.outline,
            weight_max_list=self.get_weight_max_lst(target),
            random=self.random,
        )
        return write_noble

    def test__only_closer_than_target_dist_small_initial_outline_target_dist(self):
        target = self.target()
        write_noble = self.get_write_noble(target)

        write_noble.filters.append(write_noble._only_closer_than_target_dist())
        result = [
            self.weight0.start,
            self.weight1.start,
            self.weight2.start,
            self.weight3.start,
            self.weight4.start,
            self.weight5.start,
        ]
        assert [
            weight.start for weight in write_noble._get_filtered_weight_max_list()
        ] == result

    def test__only_closer_than_target_dist_big_initial_outline_target_dist(self):
        target = self.target("600|500")
        self.outline.initial_outline_target_dist = 99
        write_noble = self.get_write_noble(target)

        write_noble.filters.append(write_noble._only_closer_than_target_dist())
        assert [
            weight.start for weight in write_noble._get_filtered_weight_max_list()
        ] == []

    def test_random_sorted_weights_nobles(self):
        target = self.target()
        self.outline.initial_outline_target_dist = 10
        self.outline.initial_outline_front_dist = 0
        self.outline.initial_outline_min_off = 15000
        self.outline.morale_on = False
        target.required_noble = 10
        target.mode_noble = "random"
        write_noble = self.get_write_noble(target)

        result = [self.weight0.start, self.weight4.start, self.weight5.start]
        assert [
            weight.start for weight in write_noble.sorted_weights_nobles()
        ] == result

    def test_weight(self):
        target = self.target()
        write_noble = self.get_write_noble(target)
        write_noble.index = 999
        self.weight4.distance = 10  # type: ignore
        weight = write_noble._weight_model(
            weight_max=self.weight4, off=1, catapult=2, noble=3, order=4
        )
        self.assertTrue(isinstance(weight, WeightModel))
        self.assertEqual(weight.off, 1)
        self.assertEqual(weight.catapult, 2)
        self.assertEqual(weight.nobleman, 3)
        self.assertEqual(weight.order, 999 + 4)
        self.assertEqual(weight.distance, 10)

    def test_update_weight_max(self):
        target = self.target()
        write_noble = self.get_write_noble(target)

        updated_weight = write_noble._update_weight_max(
            weight_max=self.weight4,
            off_to_left=1000,
            catapult_to_left=10,
            noble_number=1,
        )
        self.assertEqual(updated_weight.off_left, 1000)
        self.assertEqual(updated_weight.off_state, 19800)
        self.assertEqual(updated_weight.catapult_left, 10)
        self.assertEqual(updated_weight.catapult_state, 90)
        self.assertEqual(updated_weight.nobleman_left, 3)
        self.assertEqual(updated_weight.nobleman_state, 1)

    def test_order_distance_default_list(self):
        target = self.target()
        write_noble = self.get_write_noble(target)
        self.weight1.distance = 10
        self.weight2.distance = 5
        self.weight3.distance = 15

        write_noble.default_create_list.append((self.weight1, 1))
        write_noble.default_create_list.append((self.weight2, 1))
        write_noble.default_create_list.append((self.weight3, 1))
        write_noble._order_distance_default_list()
        expected = [(self.weight3, 1), (self.weight1, 1), (self.weight2, 1)]
        self.assertEqual(expected, write_noble.default_create_list)

    def test_fill_default_list_not_single(self):
        target: Target = self.target()
        target.required_noble = 8
        write_noble = self.get_write_noble(target)
        fill_list = [self.weight4, self.weight0]
        write_noble._fill_default_list(fill_list)
        expected1 = [(self.weight4, 4), (self.weight0, 2)]
        self.assertEqual(write_noble.default_create_list, expected1)
        self.assertEqual(write_noble.target.required_noble, 2)

    def test_fill_default_list_single(self):
        target: Target = self.target()
        target.required_noble = 8
        target.mode_guide = "single"
        write_noble = self.get_write_noble(target)
        fill_list = [self.weight4, self.weight0]
        write_noble._fill_default_list(fill_list)
        expected1 = [
            (self.weight4, 1),
            (self.weight0, 1),
        ]
        self.assertEqual(write_noble.default_create_list, expected1)
        self.assertEqual(write_noble.target.required_noble, 6)

    def test_mode_guide_is_one1(self):
        target: Target = self.target()
        target.required_noble = 2
        self.weight4.distance = 10
        self.weight0.distance = 10
        self.weight5.distance = 10
        self.weight3.distance = 10
        write_noble = self.get_write_noble(target)
        fill_list = [self.weight4, self.weight0, self.weight5, self.weight3]
        write_noble._mode_guide_is_one(fill_list)
        expected1 = [
            (self.weight5, 2),
        ]
        self.assertEqual(write_noble.default_create_list, expected1)
        self.assertEqual(write_noble.target.required_noble, 0)

    def test_mode_guide_is_one2(self):
        target: Target = self.target()
        target.required_noble = 4
        self.weight4.distance = 10
        self.weight0.distance = 10
        self.weight5.distance = 10
        self.weight3.distance = 10
        write_noble = self.get_write_noble(target)
        fill_list = [self.weight4, self.weight0, self.weight5, self.weight3]
        write_noble._mode_guide_is_one(fill_list)
        expected1 = [
            (self.weight4, 4),
        ]
        self.assertEqual(write_noble.default_create_list, expected1)
        self.assertEqual(write_noble.target.required_noble, 0)

    def test_mode_guide_is_many(self):
        target: Target = self.target()
        target.required_noble = 4
        write_noble = self.get_write_noble(target)
        self.weight0.distance = 10
        self.weight4.distance = 10
        self.weight5.distance = 10
        fill_list = [self.weight4, self.weight0, self.weight5]

        write_noble._mode_guide_is_many(fill_list)
        expected1 = [
            (self.weight4, 4),
        ]
        self.assertEqual(write_noble.default_create_list, expected1)
        self.assertEqual(write_noble.target.required_noble, 0)

    def test_mode_guide_is_single(self):
        target: Target = self.target()
        target.required_noble = 4
        target.mode_guide = "single"
        write_noble = self.get_write_noble(target)
        self.weight0.distance = 10
        self.weight4.distance = 10
        self.weight5.distance = 10
        fill_list = [self.weight4, self.weight0, self.weight5]

        write_noble._mode_guide_is_single(fill_list)
        expected1 = [
            (self.weight4, 1),
            (self.weight5, 1),
            (self.weight0, 1),
        ]
        self.assertEqual(write_noble.default_create_list, expected1)
        self.assertEqual(write_noble.target.required_noble, 1)

    def test_off_and_first_off_divide(self):
        target: Target = self.target()
        write_noble = self.get_write_noble(target)
        weight: WeightMaximum = self.weight0
        weight.nobleman_left = 3
        weight.off_left = 1000
        write_noble.target.mode_division = "divide"
        off1 = write_noble._off(weight)
        self.assertEqual(off1, 333)
        off2 = write_noble._first_off(weight, off1)
        self.assertEqual(off2, 334)

    def test_off_and_first_off_not_divide(self):
        target: Target = self.target()
        write_noble = self.get_write_noble(target)
        weight: WeightMaximum = self.weight0
        weight.nobleman_left = 3
        weight.off_left = 1000

        write_noble.target.mode_division = "not_divide"
        off3 = write_noble._off(weight)
        self.assertEqual(off3, 200)
        off4 = write_noble._first_off(weight, off3)
        self.assertEqual(off4, 600)

    def test_off_and_first_off_separatly(self):
        target: Target = self.target()
        write_noble = self.get_write_noble(target)
        weight: WeightMaximum = self.weight0
        weight.nobleman_left = 3
        weight.off_left = 1000

        write_noble.target.mode_division = "separatly"
        off3 = write_noble._off(weight)
        self.assertEqual(off3, 200)
        off4 = write_noble._first_off(weight, off3)
        self.assertEqual(off4, 200)

    def test_off_and_first_off_low_off_is_divide_for_every_mode_division(self):
        target: Target = self.target()
        write_noble = self.get_write_noble(target)
        weight: WeightMaximum = self.weight0
        weight.nobleman_left = 3
        weight.off_left = 500

        write_noble.target.mode_division = "not_divide"
        off5 = write_noble._off(weight)
        self.assertEqual(off5, 166)
        off6 = write_noble._first_off(weight, off5)
        self.assertEqual(off6, 168)
        write_noble.target.mode_division = "divide"
        off5 = write_noble._off(weight)
        self.assertEqual(off5, 166)
        off6 = write_noble._first_off(weight, off5)
        self.assertEqual(off6, 168)
        write_noble.target.mode_division = "separatly"
        off5 = write_noble._off(weight)
        self.assertEqual(off5, 166)
        off6 = write_noble._first_off(weight, off5)
        self.assertEqual(off6, 168)

    def test_off_and_first_off_fake_target(self):
        target: Target = self.target()
        target.fake = True
        write_noble = self.get_write_noble(target)
        weight: WeightMaximum = self.weight0
        weight.nobleman_left = 3
        weight.off_left = 500

        write_noble.target.mode_division = "not_divide"
        off5 = write_noble._off(weight)
        self.assertEqual(off5, 0)
        off6 = write_noble._first_off(weight, off5)
        self.assertEqual(off6, 0)
        write_noble.target.mode_division = "divide"
        off5 = write_noble._off(weight)
        self.assertEqual(off5, 0)
        off6 = write_noble._first_off(weight, off5)
        self.assertEqual(off6, 0)
        write_noble.target.mode_division = "separatly"
        off5 = write_noble._off(weight)
        self.assertEqual(off5, 0)
        off6 = write_noble._first_off(weight, off5)
        self.assertEqual(off6, 0)


class TestWriteNobleTargetNew(MiniSetup):
    def test_noble_filter_casual_attack_block_ratio(self) -> None:
        random = SystemRandom("test_write_ram")
        outline = self.get_outline(test_world=True)
        outline.world.casual_attack_block_ratio = 20
        outline.world.save()
        self.create_target_on_test_world(outline=outline)
        target = Target.objects.get(target="200|200")
        weight_max = self.create_weight_maximum(outline=outline)

        write_noble = WriteNobleTarget(
            target=target,
            outline=outline,
            weight_max_list=[weight_max],
            random=random,
        )

        filter_casual_attack_block_ratio = write_noble._casual_attack_block_ratio()

        target.points = 100
        weight_max.points = 130
        assert not filter_casual_attack_block_ratio(weight_max)

        weight_max.points = 119
        assert filter_casual_attack_block_ratio(weight_max)

        weight_max.points = 80
        assert not filter_casual_attack_block_ratio(weight_max)

        weight_max.points = 90
        assert filter_casual_attack_block_ratio(weight_max)
