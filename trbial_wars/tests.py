""" Tests for tribal_wars folder """
import datetime
from math import sqrt
from django.test import TestCase
from django.contrib.auth.models import User
from base import models
from . import basic, get_deff as deff


class VillageTest(TestCase):
    """ test for Village class """

    def setUp(self) -> None:
        self.wioska1 = basic.Village("345|555")
        self.wioska2 = basic.Village("345|455 ")
        self.wioska3 = basic.Village(" 342|455 ")

        self.world1 = models.World(id=1, title="Świat 150", world=150, speed_world=1.2, speed_units=0.8)
        self.world1.save()

        self.village1 = models.VillageModel(id='345555150',village_id=2,x_coord=345,y_coord=555,player_id=1,world=150)
        self.village1.save()

        self.player1 = models.Player(id='player:150', player_id=1, name="player1", tribe_id=1, world=150)
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
        self.assertEqual(3094, village.time_distance(village2, "nobleman", self.world1))
        self.assertEqual(2652, village.time_distance(village2, "ram", self.world1))

    def test_eq(self):
        self.assertTrue(self.wioska1, basic.Village("345|555"))

class TestWorldEvidence(TestCase):
    """ Test for world_evidence function """

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

        self.world1_evidence = basic.world_evidence(1)
        self.world2_evidence = basic.world_evidence(2)
        self.world3_evidence = basic.world_evidence(3)

    def test_world1_result_atribut_is_0_1_0(self):
        self.assertEqual(self.world1_evidence, (0, 0, 1))

    def test_world2_result_atribut_is_0_0_0(self):
        self.assertEqual(self.world2_evidence, (0, 0, 0))

    def test_world3_result_atribut_is_1_1_1(self):
        self.assertEqual(self.world3_evidence, (1, 1, 1))


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


class TestDefence(TestCase):
    """ Test for Defence """

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

        self.text_world1 = "500|500,w wiosce,1,2,3,5,6,8,9,10,12,13,15,"
        self.text_world2 = "500|500,w wiosce,1,2,3,5,6,8,9,10,12,15,"
        self.text_world3 = "500|500,w wiosce,1,2,3,4,5,6,7,8,9,10,11,12,13,15,"
        self.text_world4 = "500|500,w wiosce,1,2,3,4,5,6,7,8,9,10,11,12,15,"

        self.army1 = basic.Defence(self.text_world1, self.world1_evidence)
        self.army2 = basic.Defence(self.text_world2, self.world2_evidence)
        self.army3 = basic.Defence(self.text_world3, self.world3_evidence)
        self.army4 = basic.Defence(self.text_world4, self.world4_evidence)

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


class TestArmyDefenceCleanMethodsAndDictionaryFunction(TestCase):
    def setUp(self):
        self.text_off1 = "500|500,1000,1000,0,0,0,1000,0,0,0,0,0,"
        self.text_off2 = "500|500,1000,1000,0,0,0,1000,0,0,0,0,"
        self.text_deff1 = "500|500,w wiosce,1000,1000,0,0,0,1000,0,0,0,0,"
        self.text_deff2 = "500|500,w drodze,1000,1000,0,0,0,1000,0,0,0,0,"

        self.text_off_bad1 = "500|50,1000,1000,0,0,0,1000,0,0,0,0,0,"
        self.text_off_bad2 = "500|500,1000,1000,0,0,0,1000,0,0,0,0,0"
        self.text_off_bad3 = "500|500,1000,1000,0,0,0,1000,0,0,0,,0,"
        self.text_off_bad4 = "500|500,1000,1000,0,0,0,'xd',0,0,0,0,0,"
        self.text_off_bad5 = "500|500,1000,1000,0,0,0,1000,0,0,0,0,0,0"
        self.text_off_bad6 = "500|500,1000,1000,0,0,0,1000,0,0,0,"
        self.text_off_bad7 = "500|500,1000,1000,0,0,0,1000,0,0,0,0,0,0"
        self.text_off_bad8 = "500|200,1000,1000,0,0,0,1000,0,0,0,0,0,"
        self.text_off_bad9 = "500|0,1000,1000,0,0,0,1000,0,0,0,0,0,"
        self.text_off_bad10 = (
            "500|500,1000,1000,0,0,0,1000,0,0,0,0,500|0,1000,1000,0,0,0,1000,0,0,0,0,0,"
        )

        self.text_deff_bad1 = "500|50,w wiosce,1000,1000,0,0,0,1000,0,0,0,0,"
        self.text_deff_bad2 = "500|500,w drodze,1000,1000,0,0,0,1000,0,0,0,0"
        self.text_deff_bad3 = "500|500,1000,1000,0,0,0,1000,0,0,0,,"
        self.text_deff_bad4 = "500|500,w wiosce,1000,1000,0,0,0,'xd',0,0,0,0,"
        self.text_deff_bad5 = "500|500,w drodze,1000,1000,0,0,0,1000,0,0,0,0,0,0"
        self.text_deff_bad6 = "500|500,w wiosce,1000,1000,0,0,0,1000,0,0,"
        self.text_deff_bad7 = "500|500,w wiosce,1000,1000,0,0,0,1000,0,0,0,0,0"
        self.text_deff_bad8 = "500|200,w wiosce,1000,1000,0,0,0,1000,0,0,0,0,"
        self.text_deff_bad9 = "500|0,w wiosce,1000,1000,0,0,0,1000,0,0,0,0,"
        self.text_deff_bad10 = "500|500,w wiosce,1000,1000,0,0,0,1000,0,0,0,0,500|0,1000,1000,0,0,0,1000,0,0,0,0,0,"
        self.world = models.World.objects.create(
            title="Świat 150",
            world=150,
            paladin="inactive",
            militia="inactive",
            archer="inactive",
        )
        self.admin = User.objects.create_user("admin", None, None)
        self.outline = models.Outline.objects.create(
            owner=self.admin,
            date=datetime.date.today(),
            name="name",
            world="150",
            ally_tribe_tag="pl1, pl2",
            enemy_tribe_tag="pl3, pl4",
        )
        self.ally_village1 = models.VillageModel(id='500500150',village_id=1,x_coord=500,y_coord=500,player_id=2,world=150)
        self.ally_village2 = models.VillageModel(id='499500150',village_id=2,x_coord=499,y_coord=500,player_id=1,world=150)
        #legal below
        self.ally_village3 = models.VillageModel(id='498503150',village_id=3,x_coord=498,y_coord=503,player_id=2,world=150)
        self.ally_village4 = models.VillageModel(id='500502150',village_id=4,x_coord=500,y_coord=502,player_id=2,world=150)
        self.ally_village5 = models.VillageModel(id='498502150',village_id=5,x_coord=498,y_coord=502,player_id=2,world=150)
        self.ally_village6 = models.VillageModel(id='500499150',village_id=6,x_coord=500,y_coord=499,player_id=2,world=150)

        self.enemy_village1 = models.VillageModel(id='503500150',village_id=1,x_coord=503,y_coord=500,player_id=3,world=150)
        self.enemy_village2 = models.VillageModel(id='500506150',village_id=1,x_coord=500,y_coord=506,player_id=4,world=150)

        self.ally_tribe1 = models.Tribe(id='pl1::150', tribe_id=1, tag="pl1", world=150)
        self.ally_tribe2 = models.Tribe(id='pl2::150', tribe_id=2, tag="pl2", world=150)
        self.enemy_tribe1 = models.Tribe(id='pl3::150', tribe_id=3, tag="pl3", world=150)
        self.enemy_tribe2 = models.Tribe(id='pl4::150', tribe_id=4, tag="pl4", world=150)

        self.ally_player1 = models.Player(id='player1:150', player_id=1, name="player1", tribe_id=1, world=150)
        self.ally_player2 = models.Player('player2:150', player_id=2, name="player2",tribe_id=2, world=150)

        self.enemy_player1 = models.Player('player3:150', player_id=3, name="player3", tribe_id=3, world=150)
        self.enemy_player2 = models.Player('player4:150', player_id=4, name="player4", tribe_id=4, world=150)
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
        self.player_dict = basic.coord_to_player(self.outline)
        self.evidence = basic.world_evidence(self.world.world)

    def test_coord_to_player(self):
        players = {
            "500|500": "player2",
            "498|503": "player2",
            "499|500": "player1",
            "500|499": "player2",
            "500|502": "player2",
            "498|502": "player2",
        }

        self.assertEqual(basic.coord_to_player(self.outline), players)

    def test_clean_army_text_off1_pass(self):
        with self.assertRaises(Exception):
            try:
                army = basic.Army(self.text_off1, evidence=self.evidence)
                army.clean_init(self.player_dict)
            except:
                pass
            else:
                raise Exception

    def test_clean_army_text_off2_pass(self):
        with self.assertRaises(Exception):
            try:
                army = basic.Army(self.text_off2, evidence=self.evidence)
                army.clean_init(self.player_dict)
            except:
                pass
            else:
                raise Exception

    def test_clean_army_text_deff1_pass(self):
        with self.assertRaises(Exception):
            try:
                army = basic.Defence(self.text_deff1, evidence=self.evidence)
                army.clean_init(self.player_dict)
            except:
                pass
            else:
                raise Exception

    def test_clean_army_text_deff2_pass(self):
        with self.assertRaises(Exception):
            try:
                army = basic.Defence(self.text_deff2, evidence=self.evidence)
                army.clean_init(self.player_dict)
            except:
                pass
            else:
                raise Exception

    def test_clean_init_army_text_off_bad1_raise_exception(self):
        with self.assertRaises(Exception):
            army = basic.Army(self.text_off_bad1, evidence=self.evidence)
            army.clean_init(self.player_dict)

    def test_clean_init_army_text_off_bad2_raise_exception(self):
        with self.assertRaises(Exception):
            army = basic.Army(self.text_off_bad2, evidence=self.evidence)
            army.clean_init(self.player_dict)

    def test_clean_init_army_text_off_bad3_raise_exception(self):
        with self.assertRaises(Exception):
            army = basic.Army(self.text_off_bad3, evidence=self.evidence)
            army.clean_init(self.player_dict)

    def test_clean_init_army_text_off_bad4_raise_exception(self):
        with self.assertRaises(Exception):
            army = basic.Army(self.text_off_bad4, evidence=self.evidence)
            army.clean_init(self.player_dict)

    def test_clean_init_army_text_off_bad5_raise_exception(self):
        with self.assertRaises(Exception):
            army = basic.Army(self.text_off_bad5, evidence=self.evidence)
            army.clean_init(self.player_dict)

    def test_clean_init_army_text_off_bad6_raise_exception(self):
        with self.assertRaises(Exception):
            army = basic.Army(self.text_off_bad6, evidence=self.evidence)
            army.clean_init(self.player_dict)

    def test_clean_init_army_text_off_bad7_raise_exception(self):
        with self.assertRaises(Exception):
            army = basic.Army(self.text_off_bad7, evidence=self.evidence)
            army.clean_init(self.player_dict)

    def test_clean_init_army_text_off_bad8_raise_exception(self):
        with self.assertRaises(Exception):
            army = basic.Army(self.text_off_bad8, evidence=self.evidence)
            army.clean_init(self.player_dict)

    def test_clean_init_army_text_off_bad9_raise_exception(self):
        with self.assertRaises(Exception):
            army = basic.Army(self.text_off_bad9, evidence=self.evidence)
            army.clean_init(self.player_dict)

    def test_clean_init_army_text_off_bad10_raise_exception(self):
        with self.assertRaises(Exception):
            army = basic.Army(self.text_off_bad10, evidence=self.evidence)
            army.clean_init(self.player_dict)

    def test_clean_init_army_text_deff_bad1_raise_exception(self):
        with self.assertRaises(Exception):
            army = basic.Defence(self.text_deff_bad1, evidence=self.evidence)
            army.clean_init(self.player_dict)

    def test_clean_init_army_text_deff_bad2_raise_exception(self):
        with self.assertRaises(Exception):
            army = basic.Defence(self.text_deff_bad2, evidence=self.evidence)
            army.clean_init(self.player_dict)

    def test_clean_init_army_text_deff_bad3_raise_exception(self):
        with self.assertRaises(Exception):
            army = basic.Defence(self.text_deff_bad3, evidence=self.evidence)
            army.clean_init(self.player_dict)

    def test_clean_init_army_text_deff_bad4_raise_exception(self):
        with self.assertRaises(Exception):
            army = basic.Defence(self.text_deff_bad4, evidence=self.evidence)
            army.clean_init(self.player_dict)

    def test_clean_init_army_text_deff_bad5_raise_exception(self):
        with self.assertRaises(Exception):
            army = basic.Defence(self.text_deff_bad5, evidence=self.evidence)
            army.clean_init(self.player_dict)

    def test_clean_init_army_text_deff_bad6_raise_exception(self):
        with self.assertRaises(Exception):
            army = basic.Defence(self.text_deff_bad6, evidence=self.evidence)
            army.clean_init(self.player_dict)

    def test_clean_init_army_text_deff_bad7_raise_exception(self):
        with self.assertRaises(Exception):
            army = basic.Defence(self.text_deff_bad7, evidence=self.evidence)
            army.clean_init(self.player_dict)

    def test_clean_init_army_text_deff_bad8_raise_exception(self):
        with self.assertRaises(Exception):
            army = basic.Defence(self.text_deff_bad8, evidence=self.evidence)
            army.clean_init(self.player_dict)

    def test_clean_init_army_text_deff_bad9_raise_exception(self):
        with self.assertRaises(Exception):
            army = basic.Defence(self.text_deff_bad9, evidence=self.evidence)
            army.clean_init(self.player_dict)

    def test_clean_init_army_text_deff_bad10_raise_exception(self):
        with self.assertRaises(Exception):
            army = basic.Defence(self.text_deff_bad10, evidence=self.evidence)
            army.clean_init(self.player_dict)


class GetDeffFunctionTest(TestCase):
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
        self.outline = models.Outline.objects.create(
            owner=self.admin,
            date=datetime.date.today(),
            name="name",
            world="150",
            ally_tribe_tag="pl1, pl2",
            enemy_tribe_tag="pl3, pl4",
            deff_troops=TEXT,
        )

        self.ally_village1 = models.VillageModel(id='500500150',village_id=1,x_coord=500,y_coord=500,player_id=2,world=150)
        self.ally_village2 = models.VillageModel(id='499500150',village_id=2,x_coord=499,y_coord=500,player_id=1,world=150)
        #legal below
        self.ally_village3 = models.VillageModel(id='498503150',village_id=3,x_coord=498,y_coord=503,player_id=2,world=150)
        self.ally_village4 = models.VillageModel(id='500502150',village_id=4,x_coord=500,y_coord=502,player_id=2,world=150)
        self.ally_village5 = models.VillageModel(id='498502150',village_id=5,x_coord=498,y_coord=502,player_id=2,world=150)
        self.ally_village6 = models.VillageModel(id='500499150',village_id=6,x_coord=500,y_coord=499,player_id=2,world=150)

        self.enemy_village1 = models.VillageModel(id='503500150',village_id=1,x_coord=503,y_coord=500,player_id=3,world=150)
        self.enemy_village2 = models.VillageModel(id='500506150',village_id=1,x_coord=500,y_coord=506,player_id=4,world=150)

        self.ally_tribe1 = models.Tribe(id='pl1::150', tribe_id=1, tag="pl1", world=150)
        self.ally_tribe2 = models.Tribe(id='pl2::150', tribe_id=2, tag="pl2", world=150)
        self.enemy_tribe1 = models.Tribe(id='pl3::150', tribe_id=3, tag="pl3", world=150)
        self.enemy_tribe2 = models.Tribe(id='pl4::150', tribe_id=4, tag="pl4", world=150)

        self.ally_player1 = models.Player(id='player1:150', player_id=1, name="player1", tribe_id=1, world=150)
        self.ally_player2 = models.Player('player2:150', player_id=2, name="player2",tribe_id=2, world=150)

        self.enemy_player1 = models.Player('player3:150', player_id=3, name="player3", tribe_id=3, world=150)
        self.enemy_player2 = models.Player('player4:150', player_id=4, name="player4", tribe_id=4, world=150)

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
        result = deff.get_deff(outline=self.outline, radius=3)
        self.assertEqual(
            result,
            """\r\nplayer1\r\n499|500 - 6000\r\nŁącznie - 6000 - miejsc w zagrodzie, CK liczone jako x4\r\n\r\nplayer2\r\n500|502 - 6000\r\n498|502 - 6000\r\n500|499 - 6000\r\nŁącznie - 18000 - miejsc w zagrodzie, CK liczone jako x4\r\n""",
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



