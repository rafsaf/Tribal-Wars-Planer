from math import sqrt
from django.test import TestCase
from base import models
from . import wioska


class Wioska_test(TestCase):
    def setUp(self) -> None:
        self.wioska1 = wioska.Wioska("345|555")
        self.wioska2 = wioska.Wioska("345|455 ")
        self.wioska3 = wioska.Wioska(" 342|455 ")

        self.world1 = models.World(1, "Świat 150", 150, 1.2, 0.8)
        self.world1.save()

        self.village1 = models.Village(1, 1, 345, 555, 1, 150, 150)
        self.village1.save()

        self.player1 = models.Player(1, 1, "player", 1, 1, 1, 1, 150)
        self.player1.save()

    def test_are_x_and_y_coordinates_correct(self):
        self.assertEqual(self.wioska1.kordy, "345|555")
        self.assertEqual(345, self.wioska1.x)
        self.assertEqual(555, self.wioska1.y)

    def test_distance(self):
        self.assertEqual(100, self.wioska1.distance(self.wioska2))
        self.assertEqual(sqrt(10009), self.wioska1.distance(self.wioska3))

    def test_time_distance(self):
        village = wioska.Wioska("523|426")
        village2 = wioska.Wioska("522|425")
        self.assertEqual(3094, village.time_distance(village2, "szlachcic",
                                                     150))
        self.assertEqual(2652, village.time_distance(village2, "taran", 150))

    def test_village(self):
        self.assertEqual(self.village1, self.wioska1.get_village(150))

    def test_get_player(self):
        self.assertEqual("player", self.wioska1.get_player(150))