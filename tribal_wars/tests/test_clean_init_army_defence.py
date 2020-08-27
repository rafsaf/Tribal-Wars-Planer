import datetime

from django.test import TestCase
from django.contrib.auth.models import User

from base import models
from tribal_wars import basic


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
            "500|500,1000,1000,0,0,0,1000,0,0,"
            "0,0,500|0,1000,1000,0,0,0,1000,0,0,0,0,0,"
        )
        self.text_deff_bad1 = "500|50,w wiosce,1000,1000,0,0,0,1000,0,0,0,0,"
        self.text_deff_bad2 = "500|500,w drodze,1000,1000,0,0,0,1000,0,0,0,0"
        self.text_deff_bad3 = "500|500,1000,1000,0,0,0,1000,0,0,0,,"
        self.text_deff_bad4 = "500|500,w wiosce,1000,1000,0,0,0,'xd',0,0,0,0,"
        self.text_deff_bad5 = (
            "500|500,w drodze,1000,1000,0,0,0,1000,0,0,0,0,0,0"
        )
        self.text_deff_bad6 = "500|500,w wiosce,1000,1000,0,0,0,1000,0,0,"
        self.text_deff_bad7 = "500|500,w wiosce,1000,1000,0,0,0,1000,0,0,0,0,0"
        self.text_deff_bad8 = "500|200,w wiosce,1000,1000,0,0,0,1000,0,0,0,0,"
        self.text_deff_bad9 = "500|0,w wiosce,1000,1000,0,0,0,1000,0,0,0,0,"
        self.text_deff_bad10 = (
            "500|500,w wiosce,1000,1000,0,0,0,1000,0,0,0,0,"
            "500|0,1000,1000,0,0,0,1000,0,0,0,0,0,"
        )
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
            ally_tribe_tag=["pl1", "pl2"],
            enemy_tribe_tag=["pl3", " pl4"],
        )
        self.ally_village1 = models.VillageModel(
            id="500500150",
            village_id=1,
            x_coord=500,
            y_coord=500,
            player_id=2,
            world=150,
        )
        self.ally_village2 = models.VillageModel(
            id="499500150",
            village_id=2,
            x_coord=499,
            y_coord=500,
            player_id=1,
            world=150,
        )
        # legal below
        self.ally_village3 = models.VillageModel(
            id="498503150",
            village_id=3,
            x_coord=498,
            y_coord=503,
            player_id=2,
            world=150,
        )
        self.ally_village4 = models.VillageModel(
            id="500502150",
            village_id=4,
            x_coord=500,
            y_coord=502,
            player_id=2,
            world=150,
        )
        self.ally_village5 = models.VillageModel(
            id="498502150",
            village_id=5,
            x_coord=498,
            y_coord=502,
            player_id=2,
            world=150,
        )
        self.ally_village6 = models.VillageModel(
            id="500499150",
            village_id=6,
            x_coord=500,
            y_coord=499,
            player_id=2,
            world=150,
        )

        self.enemy_village1 = models.VillageModel(
            id="503500150",
            village_id=1,
            x_coord=503,
            y_coord=500,
            player_id=3,
            world=150,
        )
        self.enemy_village2 = models.VillageModel(
            id="500506150",
            village_id=1,
            x_coord=500,
            y_coord=506,
            player_id=4,
            world=150,
        )

        self.ally_tribe1 = models.Tribe(
            id="pl1::150", tribe_id=1, tag="pl1", world=150
        )
        self.ally_tribe2 = models.Tribe(
            id="pl2::150", tribe_id=2, tag="pl2", world=150
        )
        self.enemy_tribe1 = models.Tribe(
            id="pl3::150", tribe_id=3, tag="pl3", world=150
        )
        self.enemy_tribe2 = models.Tribe(
            id="pl4::150", tribe_id=4, tag="pl4", world=150
        )

        self.ally_player1 = models.Player(
            id="player1:150",
            player_id=1,
            name="player1",
            tribe_id=1,
            world=150,
        )
        self.ally_player2 = models.Player(
            "player2:150", player_id=2, name="player2", tribe_id=2, world=150
        )

        self.enemy_player1 = models.Player(
            "player3:150", player_id=3, name="player3", tribe_id=3, world=150
        )
        self.enemy_player2 = models.Player(
            "player4:150", player_id=4, name="player4", tribe_id=4, world=150
        )
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
            except Exception as error:
                print(error)
                pass
            else:
                raise Exception

    def test_clean_army_text_off2_pass(self):
        with self.assertRaises(Exception):
            try:
                army = basic.Army(self.text_off2, evidence=self.evidence)
                army.clean_init(self.player_dict)
            except Exception as error:
                print(error)
                pass
            else:
                raise Exception

    def test_clean_army_text_deff1_pass(self):
        with self.assertRaises(Exception):
            try:
                army = basic.Defence(self.text_deff1, evidence=self.evidence)
                army.clean_init(self.player_dict)
            except Exception as error:
                print(error)
                pass
            else:
                raise Exception

    def test_clean_army_text_deff2_pass(self):
        with self.assertRaises(Exception):
            try:
                army = basic.Defence(self.text_deff2, evidence=self.evidence)
                army.clean_init(self.player_dict)
            except Exception as error:
                print(error)
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
