import unittest
import plemiona_pliki.wioska as wioska
from math import sqrt


class Wioska_test(unittest.TestCase):
    def setUp(self) -> None:
        self.wioska1 = wioska.Wioska("345|555")
        self.wioska2 = wioska.Wioska("345|455 ")
        self.wioska3 = wioska.Wioska(" 342|455 ")
    def test_are_x_and_y_coordinates_correct(self):
        self.assertEqual(self.wioska1.kordy, "345|555")
        self.assertEqual(345, self.wioska1.x)
        self.assertEqual(555, self.wioska1.y)
    def test_distance(self):
        self.assertEqual(100, self.wioska1.distance(self.wioska2))
        self.assertEqual(sqrt(10009), self.wioska1.distance(self.wioska3))
    def test_time_distance(self):
        w = wioska.Wioska("523|426")
        w2 = wioska.Wioska("522|425")
        self.assertEqual(3094, w.time_distance(w2, "szlachcic", 150))
        self.assertEqual(2652, w.time_distance(w2, "taran", 150))
    def test_get_player(self):
        w = wioska.Wioska("523|426")
        self.assertEqual("Rafsaf", w.get_player(150))