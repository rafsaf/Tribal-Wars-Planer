
""" Tests for plemiona_pliki folder """
import datetime
from math import sqrt
from django.test import TestCase
from django.contrib.auth.models import User
from base import models
from . import basic_classes as basic, get_deff as deff



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

class Get_deff_function_Test(TestCase):
    """ Test for get_deff_text file SHOULD be very exact """
    def setUp(self):
        TEXT = '500|500,w wiosce,1000,1000,0,0,0,1000,0,0,0,0,0,\r\n500|500,w drodze,0,0,0,0,0,0,0,0,0,0,0,\r\n499|500,w wiosce,1000,1000,0,0,0,1000,0,0,0,0,0,\r\n499|500,w drodze,0,0,0,0,0,0,0,0,0,0,0,\r\n498|503,w wiosce,1000,1000,0,0,0,1000,0,0,0,0,0,\r\n498|503,w drodze,0,0,0,0,0,0,0,0,0,0,0,\r\n500|502,w wiosce,1000,1000,0,0,0,1000,0,0,0,0,0,\r\n500|502,w drodze,0,0,0,0,0,0,0,0,0,0,0,\r\n498|502,w wiosce,1000,1000,0,0,0,1000,0,0,0,0,0,\r\n498|502,w drodze,0,0,0,0,0,0,0,0,0,0,0,\r\n500|499,w wiosce,1000,1000,0,0,0,1000,0,0,0,0,0,\r\n500|499,w drodze,0,0,0,0,0,0,0,0,0,0,0,'
        
        self.admin = User.objects.create_user("admin", None, None)
        self.outline = models.New_Outline.objects.create(owner=self.admin, 
        data_akcji=datetime.date.today(), nazwa="nazwa",swiat="150",
        moje_plemie_skrot="pl1, pl2", przeciwne_plemie_skrot="pl3, pl4",
        zbiorka_obrona=TEXT)

        self.ally_village1 = models.Village(0,1,500,500,2,150,1)
        self.ally_village3 = models.Village(2,3,498,503,2,150,1)
        #legal below
        self.ally_village2 = models.Village(1,2,499,500,1,150,1)
        self.ally_village4 = models.Village(3,4,500,502,2,150,1)
        self.ally_village5 = models.Village(6,7,498,502,2,150,1)
        self.ally_village6 = models.Village(7,8,500,499,2,150,1)


        self.enemy_village1 = models.Village(4,5,503,500,3,150,1)
        self.enemy_village2 = models.Village(5,6,500,506,4,150,1)

        self.ally_tribe1 = models.Tribe(0,1,"pl1","pl1",3,3,3,3,3,150)
        self.ally_tribe2 = models.Tribe(1,2,"pl2","pl2",3,3,3,3,3,150)
        self.enemy_tribe1 = models.Tribe(2,3,"pl3","pl3",3,3,3,3,3,150)
        self.enemy_tribe2 = models.Tribe(3,4,"pl4","pl4",3,3,3,3,3,150)

        self.ally_player1 = models.Player(0,1,"player1",1,1,1,1,150)
        self.ally_player2 = models.Player(1,2,"player2",2,1,1,1,150)
        self.enemy_player1 = models.Player(2,3,"player3",3,1,1,1,150)
        self.enemy_player2 = models.Player(3,4,"player4",4,1,1,1,150)


        self.ally_village1.save()
        self.ally_village2.save()
        self.ally_village3.save()
        self.ally_village4.save()
        self.ally_village5.save()
        self.ally_village6.save()
        self.enemy_village1.save()
        self.enemy_village2.save()
        self.ally_tribe1.save()
        self.ally_tribe2.save()
        self.enemy_tribe1.save()
        self.enemy_tribe2.save()
        self.ally_player1.save()
        self.ally_player2.save()
        self.enemy_player1.save()
        self.enemy_player2.save()

    def test_get_deff_general_test_is_output_correct(self):
        result = deff.get_deff(new_Outline=self.outline, radius=3)
        self.assertEqual(result, '''\r\nplayer1\r\n499|500 Piki - 1000, Miecze - 1000, CK - 1000\r\nŁącznie - 6000 - miejsc w zagrodzie, CK liczone jako x4\r\n\r\nplayer2\r\n500|502 Piki - 1000, Miecze - 1000, CK - 1000\r\n498|502 Piki - 1000, Miecze - 1000, CK - 1000\r\n500|499 Piki - 1000, Miecze - 1000, CK - 1000\r\nŁącznie - 18000 - miejsc w zagrodzie, CK liczone jako x4\r\n''')

    def test_get_legal_coords_is_map_correct1(self):
        list_enemy = [self.ally_village1]
        list_ally = [self.ally_village2, self.ally_village3, self.ally_village4,
        self.ally_village5, self.ally_village6,
        ]
        self.assertEqual(deff.get_legal_coords(list_ally,list_enemy,4), set())

    def test_get_legal_coords_is_map_correct2(self):
        list_ally = [self.enemy_village2]
        list_enemy = [self.ally_village2, self.ally_village6]
        self.assertEqual(deff.get_legal_coords(list_ally,list_enemy,4), {(500,506)})
    #napisać dla innych funckji kiedyś
