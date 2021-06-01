""" Tests for basic.army.py, later tests for init and fiew test for off form """
import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from base import forms, models
from utils import basic


class TestArmy(TestCase):
    """Test for Army"""

    def setUp(self):
        self.server = models.Server.objects.create(
            dns="testserver",
            prefix="te",
        )
        self.world1 = models.World.objects.create(
            server=self.server,
            postfix="1",
            paladin="inactive",
            archer="inactive",
            militia="active",
        )
        self.world2 = models.World.objects.create(
            server=self.server,
            postfix="2",
            paladin="inactive",
            archer="inactive",
            militia="inactive",
        )
        self.world3 = models.World.objects.create(
            server=self.server,
            postfix="3",
            paladin="active",
            archer="active",
            militia="active",
        )
        self.world4 = models.World.objects.create(
            server=self.server,
            postfix="4",
            paladin="active",
            archer="active",
            militia="inactive",
        )

        self.world1_evidence = basic.world_evidence(self.world1)
        self.world2_evidence = basic.world_evidence(self.world2)
        self.world3_evidence = basic.world_evidence(self.world3)
        self.world4_evidence = basic.world_evidence(self.world4)

        self.text_world1 = "500|500,1,2,3,5,6,8,9,10,12,13,14,15,"
        self.text_world2 = "500|500,1,2,3,5,6,8,9,10,12,14,15,"
        self.text_world3 = "500|500,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,"
        self.text_world4 = "500|500,1,2,3,4,5,6,7,8,9,10,11,12,14,15,"

        self.text_world5 = "537|535,0,0,6135,50,2743,100,276,243,2,3,0,"
        self.text_world6 = "537|534,1,0,6205,8,2778,100,309,231,0,3,0,"
        self.text_world7 = "402|277,2794,1898,5000,50,0,580,200,100,0,4,0,"
        self.text_world8 = "407|277,2825,1892,3000,91,0,608,0,51,0,0,0,"
        self.text_world9 = "407|277,0,0,4613,20,2313,0,250,75,0,0,0,"
        self.text_world10 = "537|535,0,0,6135,500,2743,100,276,243,2,3,0,"
        self.text_world11 = "537|535,0,0,6135,200,2743,100,276,243,2,3,0,"
        self.text_world12 = "537|535,0,0,6135,100,2743,100,276,243,2,3,0,"
        self.text_world13 = "500|500,1,2,3,4,100,6,7,8,9,10,11,12,13,14,15,"
        self.text_world14 = "500|500,1,2,3,4,200,6,7,8,9,10,11,12,13,14,15,"
        self.text_world15 = "500|500,1,2,3,4,300,6,7,8,9,10,11,12,13,14,15,"
        self.text_world16 = "500|500,1,2,3003,4,300,6,7,8,9,10,11,12,13,14,15,"

        self.army1 = basic.Army(self.text_world1, self.world1_evidence)
        self.army2 = basic.Army(self.text_world2, self.world2_evidence)
        self.army3 = basic.Army(self.text_world3, self.world3_evidence)
        self.army4 = basic.Army(self.text_world4, self.world4_evidence)
        self.army5 = basic.Army(self.text_world5, self.world2_evidence)
        self.army6 = basic.Army(self.text_world6, self.world2_evidence)
        self.army7 = basic.Army(self.text_world7, self.world2_evidence)
        self.army8 = basic.Army(self.text_world8, self.world2_evidence)
        self.army9 = basic.Army(self.text_world9, self.world2_evidence)
        self.army10 = basic.Army(self.text_world10, self.world2_evidence)
        self.army11 = basic.Army(self.text_world11, self.world2_evidence)
        self.army12 = basic.Army(self.text_world12, self.world2_evidence)
        self.army13 = basic.Army(self.text_world13, self.world3_evidence)
        self.army14 = basic.Army(self.text_world14, self.world3_evidence)
        self.army15 = basic.Army(self.text_world15, self.world3_evidence)
        self.army16 = basic.Army(self.text_world16, self.world3_evidence)

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
        self.assertEqual(self.army1.off, 210)

    def test_off_army2_correct_int_return(self):
        self.assertEqual(self.army2.off, 210)

    def test_off_army3_correct_int_return(self):
        self.assertEqual(self.army3.off, 245)

    def test_off_army4_correct_int_return(self):
        self.assertEqual(self.army4.off, 245)

    def test_off_army5_correct_int_return(self):
        self.assertEqual(self.army5.off, 21131)

    def test_off_army6_correct_int_return(self):
        self.assertEqual(self.army6.off, 21326)

    def test_off_army7_correct_int_return(self):
        self.assertEqual(self.army7.off, 10380)

    def test_off_army8_correct_int_return(self):
        self.assertEqual(self.army8.off, 3408)

    def test_off_army9_correct_int_return(self):
        self.assertEqual(self.army9.off, 15755)

    def test_off_army10_correct_int_return(self):
        self.assertEqual(self.army10.off, 21431)

    def test_off_army11_correct_int_return(self):
        self.assertEqual(self.army11.off, 21431)

    def test_off_army12_correct_int_return(self):
        self.assertEqual(self.army12.off, 21231)

    def test_off_army13_correct_int_return(self):
        self.assertEqual(self.army13.off, 435)

    def test_off_army14_correct_int_return(self):
        self.assertEqual(self.army14.off, 635)

    def test_off_army15_correct_int_return(self):
        self.assertEqual(self.army15.off, 187)

    def test_off_army16_correct_int_return(self):
        self.assertEqual(self.army16.off, 3635)

    def test_catapult_army1_correct_int_return(self):
        self.assertEqual(self.army1.catapult, 10)

    def test_catapult_army2_correct_int_return(self):
        self.assertEqual(self.army2.catapult, 10)

    def test_catapult_army3_correct_int_return(self):
        self.assertEqual(self.army3.catapult, 10)

    def test_catapult_army4_correct_int_return(self):
        self.assertEqual(self.army4.catapult, 10)

    def test_catapult_army9_correct_int_return(self):
        self.assertEqual(self.army9.catapult, 75)


class TestDefence(TestCase):
    """Test for Defence"""

    def setUp(self):
        self.server = models.Server.objects.create(
            dns="testserver",
            prefix="te",
        )
        self.world1 = models.World.objects.create(
            server=self.server,
            postfix="1",
            paladin="inactive",
            archer="inactive",
            militia="active",
        )
        self.world2 = models.World.objects.create(
            server=self.server,
            postfix="2",
            paladin="inactive",
            archer="inactive",
            militia="inactive",
        )
        self.world3 = models.World.objects.create(
            server=self.server,
            postfix="3",
            paladin="active",
            archer="active",
            militia="active",
        )
        self.world4 = models.World.objects.create(
            server=self.server,
            postfix="4",
            paladin="active",
            archer="active",
            militia="inactive",
        )

        self.world1_evidence = basic.world_evidence(self.world1)
        self.world2_evidence = basic.world_evidence(self.world2)
        self.world3_evidence = basic.world_evidence(self.world3)
        self.world4_evidence = basic.world_evidence(self.world4)

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


class TestWorldEvidence(TestCase):
    """Test for world_evidence function"""

    def setUp(self):

        self.server = models.Server.objects.create(
            dns="testserver",
            prefix="te",
        )
        self.world1 = models.World.objects.create(
            server=self.server,
            postfix="1",
            paladin="inactive",
            archer="inactive",
            militia="active",
        )
        self.world2 = models.World.objects.create(
            server=self.server,
            postfix="2",
            paladin="inactive",
            archer="inactive",
            militia="inactive",
        )
        self.world3 = models.World.objects.create(
            server=self.server,
            postfix="3",
            paladin="active",
            archer="active",
            militia="active",
        )
        self.world4 = models.World.objects.create(
            server=self.server,
            postfix="4",
            paladin="active",
            archer="active",
            militia="inactive",
        )

        self.world1_evidence = basic.world_evidence(self.world1)
        self.world2_evidence = basic.world_evidence(self.world2)
        self.world3_evidence = basic.world_evidence(self.world3)
        self.world4_evidence = basic.world_evidence(self.world4)

    def test_world1_result_atribut_is_0_1_0(self):
        self.assertEqual(self.world1_evidence, (0, 0, 1))

    def test_world2_result_atribut_is_0_0_0(self):
        self.assertEqual(self.world2_evidence, (0, 0, 0))

    def test_world3_result_atribut_is_1_1_1(self):
        self.assertEqual(self.world3_evidence, (1, 1, 1))


class TestArmyDefenceCleanMethodsAndDictionaryFunction(TestCase):
    def setUp(self):
        self.text_off1 = "500|500,1000,1000,0,0,0,1000,0,0,0,0,0,"
        self.text_off2 = "500|500,1000,1000,0,0,0,1000,0,0,0,0,"
        self.text_deff1 = "500|500,w wiosce,1000,1000,0,0,0,1000,0,0,0,0,"
        self.text_deff2 = "500|500,w drodze,1000,1000,0,0,0,1000,0,0,0,0,"
        self.text_deff3 = "500|500,w wiosce,1000,1000,0,0,0,1000,0,0,0,"

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
            "500|500,1000,1000,0,0,0,1000,0,0,"
            "0,0,500|0,1000,1000,0,0,0,1000,0,0,0,0,0,"
        )
        self.text_off_bad11 = " 500|500,1000,1000,0,0,0,1000,0,0,0,0,"
        self.text_off_bad12 = "500|500,1000,1000,0,0,0,1000,0,0,0,0, "
        self.text_off_bad13 = "500|500 ,1000,1000,0,0,0,1000,0,0,0,0, "
        self.text_off_bad14 = " 500|500,1000,1000,0,0,0,1000,0,0,0,0, "
        self.text_deff_bad1 = "500|50,w wiosce,1000,1000,0,0,0,1000,0,0,0,0,"
        self.text_deff_bad2 = "500|500,w drodze,1000,1000,0,0,0,1000,0,0,0,0"
        self.text_deff_bad3 = "500|500,1000,1000,0,0,0,1000,0,0,0,,"
        self.text_deff_bad4 = "500|500,w wiosce,1000,1000,0,0,0,'xd',0,0,0,0,"
        self.text_deff_bad5 = "500|500,w drodze,1000,1000,0,0,0,1000,0,0,0,0,0,0"
        self.text_deff_bad6 = "500|500,w wiosce,1000,1000,0,0,0,1000,0,0,"
        self.text_deff_bad7 = "500|500,w wiosce,1000,1000,0,0,0,1000,0,0,0,0,0"
        self.text_deff_bad8 = "500|200,w wiosce,1000,1000,0,0,0,1000,0,0,0,0,"
        self.text_deff_bad9 = "500|0,w wiosce,1000,1000,0,0,0,1000,0,0,0,0,"
        self.text_deff_bad10 = (
            "500|500,w wiosce,1000,1000,0,0,0,1000,0,0,0,0,"
            "500|0,1000,1000,0,0,0,1000,0,0,0,0,0,"
        )
        self.text_deff_bad11 = " 500|500,w wiosce,1000,1000,0,0,0,1000,0,0,0,0,"
        self.text_deff_bad12 = " 500|500,w wiosce,1000,1000,0,0,0,1000,0,0,0,0, "
        self.text_deff_bad13 = "500|500,w wiosce,1000,1000,0,0,0,1000,0,0,0,0, "
        self.text_deff_bad14 = " 500|500 ,w wiosce,1000,1000,0,0,0,1000,0,0,0,0,"
        self.server = models.Server.objects.create(
            dns="testserver",
            prefix="te",
        )
        self.world1 = models.World.objects.create(
            server=self.server,
            postfix="1",
            paladin="inactive",
            archer="inactive",
            militia="inactive",
        )
        self.admin = User.objects.create_user("admin", None, None)  # type: ignore
        self.outline = models.Outline.objects.create(
            owner=self.admin,
            date=datetime.date.today(),
            name="name",
            world=self.world1,
            ally_tribe_tag=["pl1", "pl2"],
            enemy_tribe_tag=["pl3", " pl4"],
        )
        self.ally_tribe1 = models.Tribe(tribe_id=1, tag="pl1", world=self.world1)
        self.ally_tribe2 = models.Tribe(tribe_id=2, tag="pl2", world=self.world1)
        self.enemy_tribe1 = models.Tribe(tribe_id=3, tag="pl3", world=self.world1)
        self.enemy_tribe2 = models.Tribe(tribe_id=4, tag="pl4", world=self.world1)

        self.ally_player1 = models.Player(
            player_id=1,
            name="player1",
            tribe=self.ally_tribe1,
            world=self.world1,
        )
        self.ally_player2 = models.Player(
            player_id=2, name="player2", tribe=self.ally_tribe2, world=self.world1
        )

        self.enemy_player1 = models.Player(
            player_id=3, name="player3", tribe=self.enemy_tribe1, world=self.world1
        )
        self.enemy_player2 = models.Player(
            player_id=4, name="player4", tribe=self.enemy_tribe2, world=self.world1
        )
        self.ally_village1 = models.VillageModel(
            coord="500|500",
            village_id=1,
            x_coord=500,
            y_coord=500,
            player=self.ally_player2,
            world=self.world1,
        )
        self.ally_village2 = models.VillageModel(
            coord="499|500",
            village_id=2,
            x_coord=499,
            y_coord=500,
            player=self.ally_player1,
            world=self.world1,
        )
        # legal below
        self.ally_village3 = models.VillageModel(
            coord="498|503",
            village_id=3,
            x_coord=498,
            y_coord=503,
            player=self.ally_player2,
            world=self.world1,
        )
        self.ally_village4 = models.VillageModel(
            coord="500|502",
            village_id=4,
            x_coord=500,
            y_coord=502,
            player=self.ally_player2,
            world=self.world1,
        )
        self.ally_village5 = models.VillageModel(
            coord="498|502",
            village_id=5,
            x_coord=498,
            y_coord=502,
            player=self.ally_player2,
            world=self.world1,
        )
        self.ally_village6 = models.VillageModel(
            coord="500|499",
            village_id=6,
            x_coord=500,
            y_coord=499,
            player=self.ally_player2,
            world=self.world1,
        )

        self.enemy_village1 = models.VillageModel(
            coord="503|500",
            village_id=1,
            x_coord=503,
            y_coord=500,
            player=self.enemy_player1,
            world=self.world1,
        )
        self.enemy_village2 = models.VillageModel(
            coord="500|506",
            village_id=1,
            x_coord=500,
            y_coord=506,
            player=self.enemy_player2,
            world=self.world1,
        )

        self.ally_tribe1.save()
        self.ally_tribe2.save()
        self.enemy_tribe1.save()
        self.enemy_tribe2.save()
        self.ally_player1.save()
        self.ally_player2.save()
        self.enemy_player1.save()
        self.enemy_player2.save()
        self.ally_village1.save()
        self.ally_village2.save()
        self.ally_village3.save()
        self.ally_village4.save()
        self.ally_village5.save()
        self.ally_village6.save()
        self.enemy_village1.save()
        self.enemy_village2.save()
        self.player_dict = basic.coord_to_player(self.outline)
        self.evidence = basic.world_evidence(self.world1)

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
            except basic.ArmyError as error:
                print(error)
            else:
                raise Exception

    def test_clean_army_text_off2_pass(self):
        with self.assertRaises(Exception):
            try:
                army = basic.Army(self.text_off2, evidence=self.evidence)
                army.clean_init(self.player_dict)
            except basic.ArmyError as error:
                print(error)
            else:
                raise Exception

    def test_clean_army_text_deff1_pass(self):
        with self.assertRaises(Exception):
            try:
                army = basic.Defence(self.text_deff1, evidence=self.evidence)
                army.clean_init(self.player_dict)
            except basic.DefenceError as error:
                print(error)
            else:
                raise Exception

    def test_clean_army_text_deff2_pass(self):
        with self.assertRaises(Exception):
            try:
                army = basic.Defence(self.text_deff2, evidence=self.evidence)
                army.clean_init(self.player_dict)
            except basic.DefenceError as error:
                print(error)
            else:
                raise Exception

    def test_clean_army_text_deff3_pass(self):
        with self.assertRaises(Exception):
            try:
                army = basic.Defence(self.text_deff3, evidence=self.evidence)
                army.clean_init(self.player_dict)
            except basic.DefenceError as error:
                print(error)
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

    def test_clean_init_army_text_off_bad11_raise_exception(self):
        with self.assertRaises(Exception):
            army = basic.Army(self.text_off_bad11, evidence=self.evidence)
            army.clean_init(self.player_dict)

    def test_clean_init_army_text_off_bad12_raise_exception(self):
        with self.assertRaises(Exception):
            army = basic.Army(self.text_off_bad12, evidence=self.evidence)
            army.clean_init(self.player_dict)

    def test_clean_init_army_text_off_bad13_raise_exception(self):
        with self.assertRaises(Exception):
            army = basic.Army(self.text_off_bad13, evidence=self.evidence)
            army.clean_init(self.player_dict)

    def test_clean_init_army_text_off_bad14_raise_exception(self):
        with self.assertRaises(Exception):
            army = basic.Army(self.text_off_bad14, evidence=self.evidence)
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

    def test_clean_init_army_text_deff_bad11_raise_exception(self):
        with self.assertRaises(Exception):
            army = basic.Defence(self.text_deff_bad11, evidence=self.evidence)
            army.clean_init(self.player_dict)

    def test_clean_init_army_text_deff_bad12_raise_exception(self):
        with self.assertRaises(Exception):
            army = basic.Defence(self.text_deff_bad12, evidence=self.evidence)
            army.clean_init(self.player_dict)

    def test_clean_init_army_text_deff_bad13_raise_exception(self):
        with self.assertRaises(Exception):
            army = basic.Defence(self.text_deff_bad13, evidence=self.evidence)
            army.clean_init(self.player_dict)

    def test_clean_init_army_text_deff_bad14_raise_exception(self):
        with self.assertRaises(Exception):
            army = basic.Defence(self.text_deff_bad14, evidence=self.evidence)
            army.clean_init(self.player_dict)

    def test_off_form_correct_one_line_correct(self):
        off_form = forms.OffTroopsForm(
            {"off_troops": self.text_off1}, outline=self.outline
        )
        self.assertTrue(off_form.is_valid())

    def test_off_form_not_correct_when_village_is_barbarian(self):
        barbarian_village = models.VillageModel.objects.get(coord="500|500")
        barbarian_village.player = None
        barbarian_village.save()
        off_form = forms.OffTroopsForm(
            {"off_troops": self.text_off1}, outline=self.outline
        )
        self.assertFalse(off_form.is_valid())

    def test_off_form_is_not_correct_one_line_with_empty_line_first(self):
        off_form = forms.OffTroopsForm(
            {"off_troops": "\r\n" + self.text_off1}, outline=self.outline
        )
        self.assertFalse(off_form.is_valid())

    def test_off_form_is_not_correct_one_line_with_empty_line_last(self):
        off_form = forms.OffTroopsForm(
            {"off_troops": self.text_off1 + "\r\n"}, outline=self.outline
        )
        self.assertFalse(off_form.is_valid())

    def test_off_form_is_not_correct_one_line_bad1(self):
        off_form = forms.OffTroopsForm(
            {"off_troops": self.text_off_bad1}, outline=self.outline
        )
        self.assertFalse(off_form.is_valid())

    def test_off_form_is_not_correct_one_line_bad11(self):
        off_form = forms.OffTroopsForm(
            {"off_troops": self.text_off_bad11}, outline=self.outline
        )
        self.assertFalse(off_form.is_valid())

    def test_off_form_is_not_correct_one_line_bad12(self):
        off_form = forms.OffTroopsForm(
            {"off_troops": self.text_off_bad12}, outline=self.outline
        )
        self.assertFalse(off_form.is_valid())

    def test_off_form_is_not_correct_one_line_bad13(self):
        off_form = forms.OffTroopsForm(
            {"off_troops": self.text_off_bad13}, outline=self.outline
        )
        self.assertFalse(off_form.is_valid())

    def test_off_form_is_not_correct_one_line_bad14(self):
        off_form = forms.OffTroopsForm(
            {"off_troops": self.text_off_bad14}, outline=self.outline
        )
        self.assertFalse(off_form.is_valid())

    def test_off_form_is_not_correct_with_only_second_line_bad11(self):
        off_form = forms.OffTroopsForm(
            {"off_troops": self.text_off1 + "\r\n" + self.text_off_bad11},
            outline=self.outline,
        )
        self.assertFalse(off_form.is_valid())

    def test_off_form_correct_is_not_correct_with_doubled_correct_lines(self):
        off_form = forms.OffTroopsForm(
            {"off_troops": self.text_off1 + "\r\n" + self.text_off1},
            outline=self.outline,
        )
        self.assertFalse(off_form.is_valid())

    def test_deff_form_correct_one_line_correct(self):
        deff_form = forms.DeffTroopsForm(
            {"deff_troops": self.text_deff1}, outline=self.outline
        )
        self.assertTrue(deff_form.is_valid())

    def test_deff_form_not_correct_when_village_is_barbarian(self):
        barbarian_village = models.VillageModel.objects.get(coord="500|500")
        barbarian_village.player = None
        barbarian_village.save()
        deff_form = forms.DeffTroopsForm(
            {"deff_troops": self.text_deff1}, outline=self.outline
        )
        self.assertFalse(deff_form.is_valid())

    def test_deff_form_is_not_correct_one_line_bad1(self):
        deff_form = forms.DeffTroopsForm(
            {"deff_troops": self.text_deff_bad1}, outline=self.outline
        )
        self.assertFalse(deff_form.is_valid())

    def test_deff_form_is_not_correct_one_line_with_empty_line_first(self):
        deff_form = forms.DeffTroopsForm(
            {"deff_troops": "\r\n" + self.text_deff1}, outline=self.outline
        )
        self.assertFalse(deff_form.is_valid())

    def test_deff_form_is_not_correct_one_line_with_empty_line_last(self):
        deff_form = forms.DeffTroopsForm(
            {"deff_troops": self.text_deff1 + "\r\n"}, outline=self.outline
        )
        self.assertFalse(deff_form.is_valid())

    def test_deff_form_is_not_correct_one_line_bad11(self):
        deff_form = forms.DeffTroopsForm(
            {"deff_troops": self.text_deff_bad11}, outline=self.outline
        )
        self.assertFalse(deff_form.is_valid())

    def test_deff_form_is_not_correct_one_line_bad12(self):
        deff_form = forms.DeffTroopsForm(
            {"deff_troops": self.text_deff_bad12}, outline=self.outline
        )
        self.assertFalse(deff_form.is_valid())

    def test_deff_form_is_not_correct_one_line_bad13(self):
        deff_form = forms.DeffTroopsForm(
            {"deff_troops": self.text_deff_bad13}, outline=self.outline
        )
        self.assertFalse(deff_form.is_valid())

    def test_deff_form_is_not_correct_one_line_bad14(self):
        deff_form = forms.DeffTroopsForm(
            {"deff_troops": self.text_deff_bad14}, outline=self.outline
        )
        self.assertFalse(deff_form.is_valid())

    def test_deff_form_correct_is_not_correct_with_doubled_correct_lines(self):
        off_form = forms.OffTroopsForm(
            {
                "off_troops": self.text_deff1
                + "\r\n"
                + self.text_deff2
                + "\r\n"
                + self.text_deff1
            },
            outline=self.outline,
        )
        self.assertFalse(off_form.is_valid())
