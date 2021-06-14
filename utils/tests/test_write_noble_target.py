from django.test import TestCase
from django.utils.translation import activate

from base.models import Outline
from base.models import TargetVertex as Target
from base.models import WeightMaximum, WeightModel
from base.tests.test_utils.initial_setup import create_initial_data_write_outline
from utils.outline_initial import MakeOutline
from utils.write_noble_target import WriteNobleTarget


class TestWriteNobleTarget(TestCase):
    def setUp(self):
        activate("pl")
        create_initial_data_write_outline()
        self.outline: Outline = Outline.objects.get(id=1)
        make_outline: MakeOutline = MakeOutline(self.outline)
        make_outline()
        self.weight0 = WeightMaximum.objects.get(start="500|500")
        self.weight1 = WeightMaximum.objects.get(start="500|501")
        self.weight2 = WeightMaximum.objects.get(start="500|502")
        self.weight3 = WeightMaximum.objects.get(start="500|503")
        self.weight4 = WeightMaximum.objects.get(start="500|504")
        self.weight5 = WeightMaximum.objects.get(start="500|505")

    def target(self):
        target = Target.objects.create(
            outline=self.outline, target="500|499", player="player1"
        )
        return target

    def test_weight(self):
        target = self.target()
        write_noble = WriteNobleTarget(target=target, outline=self.outline)
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

    def test_updated_weight_max(self):
        target = self.target()
        write_noble = WriteNobleTarget(target=target, outline=self.outline)

        updated_weight = write_noble._updated_weight_max(
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
        write_noble = WriteNobleTarget(target=target, outline=self.outline)
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
        write_noble = WriteNobleTarget(target=target, outline=self.outline)
        fill_list = [self.weight4, self.weight0]
        write_noble._fill_default_list(fill_list, single=False)
        expected1 = [(self.weight4, 4), (self.weight0, 2)]
        self.assertEqual(write_noble.default_create_list, expected1)
        self.assertEqual(write_noble.target.required_noble, 2)

    def test_fill_default_list_single(self):
        target: Target = self.target()
        target.required_noble = 8
        write_noble = WriteNobleTarget(target=target, outline=self.outline)
        fill_list = [self.weight4, self.weight0]
        write_noble._fill_default_list(fill_list, single=True)
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
        write_noble = WriteNobleTarget(target=target, outline=self.outline)
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
        write_noble = WriteNobleTarget(target=target, outline=self.outline)
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
        write_noble = WriteNobleTarget(target=target, outline=self.outline)
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
        write_noble = WriteNobleTarget(target=target, outline=self.outline)
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
        write_noble = WriteNobleTarget(target=target, outline=self.outline)
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
        write_noble = WriteNobleTarget(target=target, outline=self.outline)
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
        write_noble = WriteNobleTarget(target=target, outline=self.outline)
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
        write_noble = WriteNobleTarget(target=target, outline=self.outline)
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
        write_noble = WriteNobleTarget(target=target, outline=self.outline)
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
