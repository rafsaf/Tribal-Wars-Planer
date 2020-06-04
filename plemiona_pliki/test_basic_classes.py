
""" Tests for basic_classes file """

from math import sqrt
from django.test import TestCase
from base import models
from . import basic_classes as basic


class Wioska_test(TestCase):
    """ test for Wioska class """
    def setUp(self) -> None:
        self.wioska1 = basic.Wioska("345|555")
        self.wioska2 = basic.Wioska("345|455 ")
        self.wioska3 = basic.Wioska(" 342|455 ")

        self.world1 = models.World(1, "Świat 150", 150, 1.2, 0.8)
        self.world1.save()

        self.village1 = models.Village(1, 2, 345, 555, 1, 150, 150)
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
        village = basic.Wioska("523|426")
        village2 = basic.Wioska("522|425")
        self.assertEqual(3094, village.time_distance(village2, "szlachcic",
                                                     150))
        self.assertEqual(2652, village.time_distance(village2, "taran", 150))

    def test_get_village(self):
        self.assertEqual(self.village1, self.wioska1.get_village(150))

    def test_get_player(self):
        self.assertEqual("player", self.wioska1.get_player(150).name)

    def test_get_id_wioski(self):
        self.assertEqual(2, self.wioska1.get_id_wioski(150))

    def test_get_village_points(self):
        self.assertEqual(150, self.wioska1.get_village_points(150))

    def test_get_player_points(self):
        self.assertEqual(1, self.wioska1.get_player_points(150))
    
    def test_eq(self):
        self.assertTrue(self.wioska1, basic.Wioska('345|555'))

class Map_Test(TestCase):
    """ test for Map class """
    def setUp(self) -> None:
        self.map1 = basic.Map()

    def test_set_as_square(self):
        
        self.map1.set_as_square(1, (3, 0))
        self.assertEqual(set([(2, 1), (3, 1), (4, 1), (2, 0), (3, 0), 
        (4, 0), (2, -1), (3, -1), (4, -1),]), set(self.map1.map))
    
    def test_set_as_circle1(self):
        self.map1.set_as_circle(1, (0, 0))

        self.assertEqual(set([(-1, 0), (0, 0), (1, 0), (0, 1), (0, -1)]), set(self.map1.map))

    def test_set_as_circle2(self):
        self.map1.set_as_circle(2, (2, 1))

        self.assertEqual(set([
            (0, 1), (1, 0), (1, 1), (1, 2), (2, -1), (2, 0), (2, 1), (2, 2),
            (2, 3), (3, 0), (3, 1), (3, 2), (4, 1),
            # becouse of ceil()
            (1, 3), (1, -1), (3, 3), (3, -1),

        ]), set(self.map1.map))
