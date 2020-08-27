""" Tests for tribal_wars folder """
from math import sqrt

from django.test import TestCase

from base import models
from tribal_wars import basic


class VillageTest(TestCase):
    """ test for Village class """

    def setUp(self) -> None:
        self.wioska1 = basic.Village("345|555")
        self.wioska2 = basic.Village("345|455 ")
        self.wioska3 = basic.Village(" 342|455 ")

        self.world1 = models.World(
            id=1,
            title="Świat 150",
            world=150,
            speed_world=1.2,
            speed_units=0.8,
        )
        self.world1.save()

        self.village1 = models.VillageModel(
            id="345555150",
            village_id=2,
            x_coord=345,
            y_coord=555,
            player_id=1,
            world=150,
        )
        self.village1.save()

        self.player1 = models.Player(
            id="player:150", player_id=1, name="player1", tribe_id=1, world=150
        )
        self.player1.save()

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
        self.assertEqual(
            3094, village.time_distance(village2, "nobleman", self.world1)
        )
        self.assertEqual(
            2652, village.time_distance(village2, "ram", self.world1)
        )

    def test_eq(self):
        self.assertTrue(self.wioska1, basic.Village("345|555"))
