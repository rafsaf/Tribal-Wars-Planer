from typing import List
from django.test import TestCase
from django.utils.translation import activate
from base.tests.initial_setup import create_initial_data_write_outline
from base.models import (
    Outline,
    TargetVertex as Target,
    WeightModel,
)
from tribal_wars.outline_complete import complete_outline_write
from tribal_wars.outline_initial import MakeOutline

# Please note that only extended syntax for the targets should be used.
# The tests should cover many diffrent outline ideas and available modes.
# Every method below is a next outline.
# Outline front dist equals to 3.
# The tests should not! include the "meat" inside.
# The only important are created (or not) weights models and state updates!

# TEXT = (
#    "500|500,0,0,10000,0,0,0,0,100,2,0,0,\r\n"
#    "500|501,0,0,190,0,0,0,0,100,0,0,0,\r\n"
#    "500|502,0,0,19500,0,0,0,0,100,0,0,0,\r\n"
#    "500|503,0,0,20100,0,0,0,0,100,0,0,0,\r\n"
#    "500|504,0,0,20000,0,0,0,0,100,4,0,0,\r\n"
#    "500|505,0,0,20000,0,0,0,0,100,2,0,0,"
# )


class TestOutlineCreateTargets(TestCase):
    def setUp(self):
        activate("pl")
        create_initial_data_write_outline()
        self.outline: Outline = Outline.objects.get(id=1)
        # weights max create
        make_outline = MakeOutline(self.outline)
        make_outline()

    def target(self) -> Target:
        target = Target.objects.create(
            outline=self.outline, target="500|499", player="player1"
        )
        return target

    def weights(self) -> List[WeightModel]:
        return list(WeightModel.objects.all().order_by("order"))

    def test_indexes_are_correct_in_every_distance_real_target(self):
        self.outline.initial_outline_min_off = 100
        self.outline.mode_division = "separatly"
        self.outline.save()
        target = self.target()
        target.exact_off = [1, 1, 1, 1]
        target.exact_noble = [1, 1, 1, 1]
        target.save()
        # we don't care about modes here
        complete_outline_write(self.outline)
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

    def test_indexes_are_correct_in_every_distance_fake_target(self):
        target = self.target()
        target.fake = True
        target.exact_off = [1, 1, 1, 1]
        target.exact_noble = [1, 1, 1, 1]
        target.save()
        # we don't care about modes here
        complete_outline_write(self.outline)
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
        self.outline.initial_outline_catapult_default = 50
        self.outline.save()
        target = self.target()
        target.ruin = True
        target.exact_off = [1, 1, 1, 1]
        target.exact_noble = [1, 1, 1, 1]
        target.save()
        # we don't care about modes here
        complete_outline_write(self.outline)
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