from typing import List
from django.test import TestCase
from django.utils.translation import activate
from tribal_wars.outline_initial import MakeOutline
from base.tests.initial_setup import create_initial_data_write_outline
from base.models import (
    Outline,
    WeightMaximum,
)

# TEXT = (
#     "500|500,0,0,10000,0,0,0,0,100,2,0,0,\r\n"
#     "500|501,0,0,190  ,0,0,0,0,100,0,0,0,\r\n"
#     "500|502,0,0,19500,0,0,0,0,100,0,0,0,\r\n"
#     "500|503,0,0,20100,0,0,0,0,100,0,0,0,\r\n"
#     "500|504,0,0,20000,0,0,0,0,100,4,0,0,\r\n"
#     "500|505,0,0,20000,0,0,0,0,100,2,0,0,"
# )


class TestOutlineCreateTargets(TestCase):
    def setUp(self):
        activate("pl")
        create_initial_data_write_outline()
        self.outline: Outline = Outline.objects.get(id=1)

    def test_make_outline_creates_weight_max_properly(self):
        make_outline = MakeOutline(self.outline)
        make_outline()

        lst: List[WeightMaximum] = list(
            WeightMaximum.objects.filter(outline=self.outline).order_by("pk")
        )
        self.assertEqual(len(lst), 6)

        self.assertEqual(lst[0].start, "500|500")
        self.assertEqual(lst[0].off_left, 10800)
        self.assertEqual(lst[0].off_max, 10800)
        self.assertEqual(lst[0].off_state, 0)
        self.assertEqual(lst[0].catapult_left, 100)
        self.assertEqual(lst[0].catapult_max, 100)
        self.assertEqual(lst[0].catapult_state, 0)
        self.assertEqual(lst[0].nobleman_left, 2)
        self.assertEqual(lst[0].nobleman_max, 2)
        self.assertEqual(lst[0].nobleman_state, 0)

        self.assertEqual(lst[1].start, "500|501")
        self.assertEqual(lst[1].off_left, 990)
        self.assertEqual(lst[1].off_max, 990)
        self.assertEqual(lst[1].off_state, 0)
        self.assertEqual(lst[1].catapult_left, 100)
        self.assertEqual(lst[1].catapult_max, 100)
        self.assertEqual(lst[1].catapult_state, 0)
        self.assertEqual(lst[1].nobleman_left, 0)
        self.assertEqual(lst[1].nobleman_max, 0)
        self.assertEqual(lst[1].nobleman_state, 0)

        self.assertEqual(lst[2].start, "500|502")
        self.assertEqual(lst[2].off_left, 20300)
        self.assertEqual(lst[2].off_max, 20300)
        self.assertEqual(lst[2].off_state, 0)
        self.assertEqual(lst[2].catapult_left, 100)
        self.assertEqual(lst[2].catapult_max, 100)
        self.assertEqual(lst[2].catapult_state, 0)
        self.assertEqual(lst[2].nobleman_left, 0)
        self.assertEqual(lst[2].nobleman_max, 0)
        self.assertEqual(lst[2].nobleman_state, 0)

        self.assertEqual(lst[3].start, "500|503")
        self.assertEqual(lst[3].off_left, 20900)
        self.assertEqual(lst[3].off_max, 20900)
        self.assertEqual(lst[3].off_state, 0)
        self.assertEqual(lst[3].catapult_left, 100)
        self.assertEqual(lst[3].catapult_max, 100)
        self.assertEqual(lst[3].catapult_state, 0)
        self.assertEqual(lst[3].nobleman_left, 0)
        self.assertEqual(lst[3].nobleman_max, 0)
        self.assertEqual(lst[3].nobleman_state, 0)

        self.assertEqual(lst[4].start, "500|504")
        self.assertEqual(lst[4].off_left, 20800)
        self.assertEqual(lst[4].off_max, 20800)
        self.assertEqual(lst[4].off_state, 0)
        self.assertEqual(lst[4].catapult_left, 100)
        self.assertEqual(lst[4].catapult_max, 100)
        self.assertEqual(lst[4].catapult_state, 0)
        self.assertEqual(lst[4].nobleman_left, 4)
        self.assertEqual(lst[4].nobleman_max, 4)
        self.assertEqual(lst[4].nobleman_state, 0)

        self.assertEqual(lst[5].start, "500|505")
        self.assertEqual(lst[5].off_left, 20800)
        self.assertEqual(lst[5].off_max, 20800)
        self.assertEqual(lst[5].off_state, 0)
        self.assertEqual(lst[5].catapult_left, 100)
        self.assertEqual(lst[5].catapult_max, 100)
        self.assertEqual(lst[5].catapult_state, 0)
        self.assertEqual(lst[5].nobleman_left, 2)
        self.assertEqual(lst[5].nobleman_max, 2)
        self.assertEqual(lst[5].nobleman_state, 0)