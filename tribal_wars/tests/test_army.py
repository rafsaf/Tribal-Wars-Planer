from django.test import TestCase

from base import models
from tribal_wars import basic


class TestArmy(TestCase):
    """ Test for Army"""

    def setUp(self):
        self.world1 = models.World.objects.create(
            title="Świat 1",
            world=1,
            paladin="inactive",
            archer="inactive",
            militia="active",
        )
        self.world2 = models.World.objects.create(
            title="Świat 2",
            world=2,
            paladin="inactive",
            archer="inactive",
            militia="inactive",
        )
        self.world3 = models.World.objects.create(
            title="Świat 3",
            world=3,
            paladin="active",
            archer="active",
            militia="active",
        )
        self.world4 = models.World.objects.create(
            title="Świat 4",
            world=4,
            paladin="active",
            archer="active",
            militia="inactive",
        )

        self.world1_evidence = basic.world_evidence(1)
        self.world2_evidence = basic.world_evidence(2)
        self.world3_evidence = basic.world_evidence(3)
        self.world4_evidence = basic.world_evidence(4)

        self.text_world1 = "500|500,1,2,3,5,6,8,9,10,12,13,14,15,"
        self.text_world2 = "500|500,1,2,3,5,6,8,9,10,12,14,15,"
        self.text_world3 = "500|500,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,"
        self.text_world4 = "500|500,1,2,3,4,5,6,7,8,9,10,11,12,14,15,"

        self.army1 = basic.Army(self.text_world1, self.world1_evidence)
        self.army2 = basic.Army(self.text_world2, self.world2_evidence)
        self.army3 = basic.Army(self.text_world3, self.world3_evidence)
        self.army4 = basic.Army(self.text_world4, self.world4_evidence)

    def test_army1_coord_is_correct(self):
        self.assertEqual(self.army1.coord, "500|500")

    def test_army1_village_is_correct(self):
        self.assertEqual(self.army1.village, basic.Village("500|500"))

    def test_nobleman_army1_correct_int_return(self):
        self.assertEqual(self.army1.nobleman, 12)

    def test_nobleman_army2_correct_int_return(self):
        self.assertEqual(self.army2.nobleman, 12)

    def test_nobleman_army3_correct_int_return(self):
        self.assertEqual(self.army3.nobleman, 12)

    def test_nobleman_army4_correct_int_return(self):
        self.assertEqual(self.army4.nobleman, 12)

    def test_deff_army1_correct_int_return(self):
        self.assertEqual(self.army1.deff, 35)

    def test_deff_army2_correct_int_return(self):
        self.assertEqual(self.army2.deff, 35)

    def test_deff_army3_correct_int_return(self):
        self.assertEqual(self.army3.deff, 39)

    def test_deff_army4_correct_int_return(self):
        self.assertEqual(self.army4.deff, 39)

    def test_off_army1_correct_int_return(self):
        self.assertEqual(self.army1.off, 152)

    def test_off_army2_correct_int_return(self):
        self.assertEqual(self.army2.off, 152)

    def test_off_army3_correct_int_return(self):
        self.assertEqual(self.army3.off, 187)

    def test_off_army4_correct_int_return(self):
        self.assertEqual(self.army4.off, 187)
