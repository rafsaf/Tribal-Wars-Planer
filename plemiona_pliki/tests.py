""" Tests for plemiona_pliki folder """
import datetime
from math import sqrt
from django.test import TestCase
from django.contrib.auth.models import User
from base import models
from . import basic_classes as basic, get_deff as deff, outline_initial as initial


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
        self.assertEqual(3094, village.time_distance(village2, "szlachcic", 150))
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
        self.assertTrue(self.wioska1, basic.Wioska("345|555"))


class Map_Test(TestCase):
    """ test for Map class """

    def setUp(self) -> None:
        self.map1 = basic.Map()

    def test_set_as_square(self):

        self.map1.set_as_square(1, (3, 0))
        self.assertEqual(
            set(
                [
                    (2, 1),
                    (3, 1),
                    (4, 1),
                    (2, 0),
                    (3, 0),
                    (4, 0),
                    (2, -1),
                    (3, -1),
                    (4, -1),
                ]
            ),
            set(self.map1.map),
        )

    def test_set_as_circle1(self):
        self.map1.set_as_circle(1, (0, 0))

        self.assertEqual(
            set([(-1, 0), (0, 0), (1, 0), (0, 1), (0, -1)]), set(self.map1.map)
        )

    def test_set_as_circle2(self):
        self.map1.set_as_circle(2, (2, 1))

        self.assertEqual(
            set(
                [
                    (0, 1),
                    (1, 0),
                    (1, 1),
                    (1, 2),
                    (2, -1),
                    (2, 0),
                    (2, 1),
                    (2, 2),
                    (2, 3),
                    (3, 0),
                    (3, 1),
                    (3, 2),
                    (4, 1),
                    # becouse of ceil()
                    (1, 3),
                    (1, -1),
                    (3, 3),
                    (3, -1),
                ]
            ),
            set(self.map1.map),
        )

class Test_Parent_Army_Defence_World_Evidenve(TestCase):
    """ Test for Parent_Army_Defence_World_Evidenve class """
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

        self.world1_evidence = basic.Parent_Army_Defence_World_Evidence(1)
        self.world2_evidence = basic.Parent_Army_Defence_World_Evidence(2)
        self.world3_evidence = basic.Parent_Army_Defence_World_Evidence(3)

    # set data about world method in fact
    def test_world1_result_atribut_is_0_1_0(self):
        self.assertEqual(self.world1_evidence.result, [0, 0, 1])
    def test_world2_result_atribut_is_0_0_0(self):
        self.assertEqual(self.world2_evidence.result, [0, 0, 0])
    def test_world3_result_atribut_is_1_1_1(self):
        self.assertEqual(self.world3_evidence.result, [1, 1, 1])
    def test_get_world_method_returns_correct_world(self):
        self.assertEqual(self.world1_evidence.get_world(), self.world1)

class Test_Army_Class(TestCase):
    """ Test for Army class from basic classes
    
    DANGER!!!
    
    in tests, in every moment we ASSUME that text_army data given by user
    
    IS CORRECT(it is tested earlier!), method for testing text_army is 
    
    clean_init() """
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

        self.world1_evidence = basic.Parent_Army_Defence_World_Evidence(1)
        self.world2_evidence = basic.Parent_Army_Defence_World_Evidence(2)
        self.world3_evidence = basic.Parent_Army_Defence_World_Evidence(3)
        self.world4_evidence = basic.Parent_Army_Defence_World_Evidence(4)

        self.text_world1 = "500|500,1,2,3,5,6,8,9,10,12,13,14,15,"
        self.text_world2 = "500|500,1,2,3,5,6,8,9,10,12,14,15,"
        self.text_world3 = "500|500,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,"
        self.text_world4 = "500|500,1,2,3,4,5,6,7,8,9,10,11,12,14,15,"
    
        self.army1 = basic.Army(self.text_world1, self.world1_evidence)
        self.army2 = basic.Army(self.text_world2, self.world2_evidence)
        self.army3 = basic.Army(self.text_world3, self.world3_evidence)
        self.army4 = basic.Army(self.text_world4, self.world4_evidence)

    def test_Army_get_pikinier_army1_correct_int_return(self):
        self.assertEqual(self.army1.get_pikinier(), 1)

    def test_Army_get_pikinier_army4_correct_int_return(self):
        self.assertEqual(self.army4.get_pikinier(), 1)

    def test_Army_get_miecznik_army2_correct_int_return(self):
        self.assertEqual(self.army2.get_miecznik(), 2)

    def test_Army_get_lucznik_army1_correct_exception_raise(self):
        with self.assertRaises(ValueError):
            self.army1.get_lucznik()

    def test_Army_get_lucznik_army4_correct_int_return(self):
        self.assertEqual(self.army4.get_lucznik(), 4)

    def test_Army_get_zwiad_army2_correct_int_return(self):
        self.assertEqual(self.army2.get_zwiadowca(), 5)

    def test_Army_get_zwiad_army3_correct_int_return(self):
        self.assertEqual(self.army3.get_zwiadowca(), 5)

    def test_Army_get_lk_army1_correct_int_return(self):
        self.assertEqual(self.army1.get_lk(), 6)

    def test_Army_get_lk_army4_correct_int_return(self):
        self.assertEqual(self.army4.get_lk(), 6)

    def test_Army_get_lucznik_konny_army2_correct_exception_raise(self):
        with self.assertRaises(ValueError):
            self.army2.get_lucznik_konny()

    def test_Army_get_lucznik_konny_army3_correct_int_return(self):
        self.assertEqual(self.army3.get_lucznik_konny(), 7)

    def test_Army_get_ck_army3_correct_int_return(self):
        self.assertEqual(self.army3.get_ck(), 8)

    def test_Army_get_ck_army1_correct_int_return(self):
        self.assertEqual(self.army1.get_ck(), 8)

    def test_Army_get_taran_army1_correct_int_return(self):
        self.assertEqual(self.army2.get_taran(), 9)

    def test_Army_get_taran_army3_correct_int_return(self):
        self.assertEqual(self.army3.get_taran(), 9)

    def test_Army_get_katapulta_army4_correct_int_return(self):
        self.assertEqual(self.army4.get_katapulta(), 10)

    def test_Army_get_katapulta_army2_correct_int_return(self):
        self.assertEqual(self.army2.get_katapulta(), 10)

    def test_Army_get_szlachic_army1_correct_int_return(self):
        self.assertEqual(self.army1.get_szlachcic(), 12)

    def test_Army_get_szlachcic_army4_correct_int_return(self):
        self.assertEqual(self.army4.get_szlachcic(), 12)

    def test_Army_get_deff_units_army1_correct_int_return(self):
        self.assertEqual(self.army1.get_deff_units(), 35)

    def test_Army_get_deff_units_army3_correct_int_return(self):
        self.assertEqual(self.army3.get_deff_units(), 39)

    def test_Army_get_off_units_army1_correct_int_return(self):
        self.assertEqual(self.army1.get_off_units(), 152)

    def test_Army_get_off_units_army3_correct_int_return(self):
        self.assertEqual(self.army3.get_off_units(), 187)

    def test_Army_deff_greater_than_army3_correct_true_return(self):
        self.assertTrue(self.army3.deff_greater_than(38))

    def test_Army_off_grater_than_army1_correct_true_return(self):
        self.assertTrue(self.army1.off_greater_than(151))

    def test_Army_have_szlachci_army3_correct_true_return(self):
        self.assertTrue(self.army3.have_szlachcic())


class Test_Defence_Class(TestCase):
    """ Test for Defence class from basic classes
    
    DANGER!!!
    
    in tests, in every moment we ASSUME that text_army data given by user
    
    IS CORRECT(it is tested earlier!), method for testing text_army is 
    
    clean_init() """
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

        self.world1_evidence = basic.Parent_Army_Defence_World_Evidence(1)
        self.world2_evidence = basic.Parent_Army_Defence_World_Evidence(2)
        self.world3_evidence = basic.Parent_Army_Defence_World_Evidence(3)
        self.world4_evidence = basic.Parent_Army_Defence_World_Evidence(4)

        self.text_world1 = "500|500,w wiosce,1,2,3,5,6,8,9,10,12,13,15,"
        self.text_world2 = "500|500,w wiosce,1,2,3,5,6,8,9,10,12,15,"
        self.text_world3 = "500|500,w wiosce,1,2,3,4,5,6,7,8,9,10,11,12,13,15,"
        self.text_world4 = "500|500,w wiosce,1,2,3,4,5,6,7,8,9,10,11,12,15,"
    
        self.army1 = basic.Defence(self.text_world1, self.world1_evidence)
        self.army2 = basic.Defence(self.text_world2, self.world2_evidence)
        self.army3 = basic.Defence(self.text_world3, self.world3_evidence)
        self.army4 = basic.Defence(self.text_world4, self.world4_evidence)

    def test_Defence_get_pikinier_army1_correct_int_return(self):
        self.assertEqual(self.army1.get_pikinier(), 1)

    def test_Defence_get_pikinier_army4_correct_int_return(self):
        self.assertEqual(self.army4.get_pikinier(), 1)

    def test_Defence_get_miecznik_army2_correct_int_return(self):
        self.assertEqual(self.army2.get_miecznik(), 2)

    def test_Defence_get_lucznik_army1_correct_exception_raise(self):
        with self.assertRaises(ValueError):
            self.army1.get_lucznik()

    def test_Defence_get_lucznik_army4_correct_int_return(self):
        self.assertEqual(self.army4.get_lucznik(), 4)

    def test_Defence_get_zwiad_army2_correct_int_return(self):
        self.assertEqual(self.army2.get_zwiadowca(), 5)

    def test_Defence_get_zwiad_army3_correct_int_return(self):
        self.assertEqual(self.army3.get_zwiadowca(), 5)

    def test_Defence_get_lk_army1_correct_int_return(self):
        self.assertEqual(self.army1.get_lk(), 6)

    def test_Defence_get_lk_army4_correct_int_return(self):
        self.assertEqual(self.army4.get_lk(), 6)

    def test_Defence_get_lucznik_konny_army2_correct_exception_raise(self):
        with self.assertRaises(ValueError):
            self.army2.get_lucznik_konny()

    def test_Defence_get_lucznik_konny_army3_correct_int_return(self):
        self.assertEqual(self.army3.get_lucznik_konny(), 7)

    def test_Defence_get_ck_army3_correct_int_return(self):
        self.assertEqual(self.army3.get_ck(), 8)

    def test_Defence_get_ck_army1_correct_int_return(self):
        self.assertEqual(self.army1.get_ck(), 8)

    def test_Defence_get_taran_army1_correct_int_return(self):
        self.assertEqual(self.army2.get_taran(), 9)

    def test_Defence_get_taran_army3_correct_int_return(self):
        self.assertEqual(self.army3.get_taran(), 9)

    def test_Defence_get_katapulta_army4_correct_int_return(self):
        self.assertEqual(self.army4.get_katapulta(), 10)

    def test_Defence_get_katapulta_army2_correct_int_return(self):
        self.assertEqual(self.army2.get_katapulta(), 10)

    def test_Defence_get_szlachic_army1_correct_int_return(self):
        self.assertEqual(self.army1.get_szlachcic(), 12)

    def test_Defence_get_szlachcic_army4_correct_int_return(self):
        self.assertEqual(self.army4.get_szlachcic(), 12)

    def test_Defence_get_deff_units_army1_correct_int_return(self):
        self.assertEqual(self.army1.get_deff_units(), 35)

    def test_Defence_get_deff_units_army3_correct_int_return(self):
        self.assertEqual(self.army3.get_deff_units(), 39)

    def test_Defence_get_off_units_army1_correct_int_return(self):
        self.assertEqual(self.army1.get_off_units(), 152)

    def test_Defence_get_off_units_army3_correct_int_return(self):
        self.assertEqual(self.army3.get_off_units(), 187)

    def test_Defence_deff_greater_than_army3_correct_true_return(self):
        self.assertTrue(self.army3.deff_greater_than(38))

    def test_Defence_off_grater_than_army1_correct_true_return(self):
        self.assertTrue(self.army1.off_greater_than(151))

    def test_Defence_have_szlachci_army3_correct_true_return(self):
        self.assertTrue(self.army3.have_szlachcic())





class Get_deff_function_Test(TestCase):
    """ Test for get_deff_text file SHOULD be very exact """

    def setUp(self):
        TEXT = "500|500,w wiosce,1000,1000,0,0,0,1000,0,0,0,0,0,\r\n500|500,w drodze,0,0,0,0,0,0,0,0,0,0,0,\r\n499|500,w wiosce,1000,1000,0,0,0,1000,0,0,0,0,0,\r\n499|500,w drodze,0,0,0,0,0,0,0,0,0,0,0,\r\n498|503,w wiosce,1000,1000,0,0,0,1000,0,0,0,0,0,\r\n498|503,w drodze,0,0,0,0,0,0,0,0,0,0,0,\r\n500|502,w wiosce,1000,1000,0,0,0,1000,0,0,0,0,0,\r\n500|502,w drodze,0,0,0,0,0,0,0,0,0,0,0,\r\n498|502,w wiosce,1000,1000,0,0,0,1000,0,0,0,0,0,\r\n498|502,w drodze,0,0,0,0,0,0,0,0,0,0,0,\r\n500|499,w wiosce,1000,1000,0,0,0,1000,0,0,0,0,0,\r\n500|499,w drodze,0,0,0,0,0,0,0,0,0,0,0,"
        self.world = models.World.objects.create(
            title="Świat 150",
            world=150,
            paladin="inactive",
            militia="inactive",
            archer="inactive",
        )

        self.admin = User.objects.create_user("admin", None, None)
        self.outline = models.New_Outline.objects.create(
            owner=self.admin,
            data_akcji=datetime.date.today(),
            nazwa="nazwa",
            swiat="150",
            moje_plemie_skrot="pl1, pl2",
            przeciwne_plemie_skrot="pl3, pl4",
            zbiorka_obrona=TEXT,
        )

        self.ally_village1 = models.Village(0, 1, 500, 500, 2, 150, 1)
        self.ally_village3 = models.Village(2, 3, 498, 503, 2, 150, 1)
        # legal below
        self.ally_village2 = models.Village(1, 2, 499, 500, 1, 150, 1)
        self.ally_village4 = models.Village(3, 4, 500, 502, 2, 150, 1)
        self.ally_village5 = models.Village(6, 7, 498, 502, 2, 150, 1)
        self.ally_village6 = models.Village(7, 8, 500, 499, 2, 150, 1)

        self.enemy_village1 = models.Village(4, 5, 503, 500, 3, 150, 1)
        self.enemy_village2 = models.Village(5, 6, 500, 506, 4, 150, 1)

        self.ally_tribe1 = models.Tribe(0, 1, "pl1", "pl1", 3, 3, 3, 3, 3, 150)
        self.ally_tribe2 = models.Tribe(1, 2, "pl2", "pl2", 3, 3, 3, 3, 3, 150)
        self.enemy_tribe1 = models.Tribe(2, 3, "pl3", "pl3", 3, 3, 3, 3, 3, 150)
        self.enemy_tribe2 = models.Tribe(3, 4, "pl4", "pl4", 3, 3, 3, 3, 3, 150)

        self.ally_player1 = models.Player(0, 1, "player1", 1, 1, 1, 1, 150)
        self.ally_player2 = models.Player(1, 2, "player2", 2, 1, 1, 1, 150)
        self.enemy_player1 = models.Player(2, 3, "player3", 3, 1, 1, 1, 150)
        self.enemy_player2 = models.Player(3, 4, "player4", 4, 1, 1, 1, 150)

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
        self.assertEqual(
            result,
            """\r\nplayer1\r\n499|500 Piki - 1000, Miecze - 1000, CK - 1000\r\nŁącznie - 6000 - miejsc w zagrodzie, CK liczone jako x4\r\n\r\nplayer2\r\n500|502 Piki - 1000, Miecze - 1000, CK - 1000\r\n498|502 Piki - 1000, Miecze - 1000, CK - 1000\r\n500|499 Piki - 1000, Miecze - 1000, CK - 1000\r\nŁącznie - 18000 - miejsc w zagrodzie, CK liczone jako x4\r\n""",
        )

    def test_get_legal_coords_is_map_correct1(self):
        list_enemy = [self.ally_village1]
        list_ally = [
            self.ally_village2,
            self.ally_village3,
            self.ally_village4,
            self.ally_village5,
            self.ally_village6,
        ]
        self.assertEqual(deff.get_legal_coords(list_ally, list_enemy, 4), set())

    def test_get_legal_coords_is_map_correct2(self):
        list_ally = [self.enemy_village2]
        list_enemy = [self.ally_village2, self.ally_village6]
        self.assertEqual(deff.get_legal_coords(list_ally, list_enemy, 4), {(500, 506)})

    # napisać dla innych funckji kiedyś


#graph = initial.Graph_Initial_Outline(models.New_Outline.objects.get(pk=2))
#graph.get_players()
