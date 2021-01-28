import datetime

from django.test import TestCase
from django.contrib.auth.models import User
from django.utils.translation import activate

from base import models
from tribal_wars import get_deff as deff


class GetDeffFunctionTest(TestCase):
    """ Test for get_deff_text file SHOULD be very exact """

    def setUp(self):
        activate("en")
        ARMY_TEXT = (
            "500|500,3000,1000,0,0,0,1000,0,0,0,0,0,0,\r\n"
            "499|500,2000,1000,0,0,0,1000,0,0,0,0,0,0,\r\n"
            "498|503,2000,1000,0,0,0,1000,0,0,0,0,0,0,\r\n"
            "500|502,0,0,0,0,0,1000,0,0,0,0,0,0,\r\n"
            "498|502,2000,1000,0,0,0,1000,0,0,0,0,0,0,\r\n"
            "500|499,2000,1000,0,0,0,1000,0,0,0,0,0,0,\r\n"
        )
        DEFF_TEXT = (
            "500|500,w wiosce,13000,13000,0,0,0,1000,0,0,0,0,0,\r\n"
            "500|500,w drodze,0,0,0,0,0,0,0,0,0,0,0,\r\n"
            "499|500,w wiosce,1000,1000,0,0,0,1000,0,0,0,0,0,\r\n"
            "499|500,w drodze,0,0,0,0,0,0,0,0,0,0,0,\r\n"
            "498|503,w wiosce,1000,1000,0,0,0,1000,0,0,0,0,0,\r\n"
            "498|503,w drodze,0,0,0,0,0,0,0,0,0,0,0,\r\n"
            "500|502,w wiosce,1000,1000,0,0,0,1000,0,0,0,0,0,\r\n"
            "500|502,w drodze,0,0,0,0,0,0,0,0,0,0,0,\r\n"
            "498|502,w wiosce,1000,1000,0,0,0,1000,0,0,0,0,0,\r\n"
            "498|502,w drodze,0,0,0,0,0,0,0,0,0,0,0,\r\n"
            "500|499,w wiosce,1000,1000,0,0,0,1000,0,0,0,0,0,\r\n"
            "500|499,w drodze,0,0,0,0,0,0,0,0,0,0,0,"
        )


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
        self.admin = User.objects.create_user("admin", None, None)
        self.outline = models.Outline.objects.create(
            owner=self.admin,
            date=datetime.date.today(),
            name="name",
            world=self.world1,
            ally_tribe_tag=["pl1", "pl2"],
            enemy_tribe_tag=["pl3", " pl4"],
            deff_troops=DEFF_TEXT,
            off_troops=ARMY_TEXT,
        )
        models.Result.objects.create(outline=self.outline)
        self.ally_tribe1 = models.Tribe(
            tribe_id=1, tag="pl1", world=self.world1
        )
        self.ally_tribe2 = models.Tribe(
            tribe_id=2, tag="pl2", world=self.world1
        )
        self.enemy_tribe1 = models.Tribe(
            tribe_id=3, tag="pl3", world=self.world1
        )
        self.enemy_tribe2 = models.Tribe(
            tribe_id=4, tag="pl4", world=self.world1
        )

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



        self.maxDiff = None

    def test_get_deff_all_excluded_is_correct(self):
        result = deff.get_deff(outline=self.outline, radius=3, excluded_villages="503|500 500|506")

        expected = (
            "Tested. LEGEND: \r\n"
            "HEAVY counted as x4 and not x6, scouts are NOT counted.\r\n"
            "IN VILLAGES = troops in the village + everyone else's troops.\r\n"
            "ALL OWN = troops in the village + troops outside the village.\r\n\r\n"
            "\r\nplayer2\r\n"
            "On front 0 villages, 0 deff IN VILLAGE and "
            "0 ALL OWN.\r\n"
            "On back 5 villages, 54000 deff IN VILLAGE and "
            "33000 ALL OWN.\r\n"
            "\r\n"
            "player1\r\n"
            "On front 0 villages, 0 deff IN VILLAGE and 0 ALL OWN.\r\n"
            "On back 1 villages, 6000 deff IN VILLAGE and "
            "7000 ALL OWN.\r\n"
            "\r\n\r\n"
            "player2\r\n"
            "---------FRONT---------\r\n"
            "---------BACK---------\r\n"
            "500|500- In village- 30000  (All deff [ 8000 ])\r\n"
            "498|503- In village- 6000  (All deff [ 7000 ])\r\n"
            "500|502- In village- 6000  (All deff [ 4000 ])\r\n"
            "498|502- In village- 6000  (All deff [ 7000 ])\r\n"
            "500|499- In village- 6000  (All deff [ 7000 ])\r\n"
            "\r\n\r\n"
            "player1\r\n"
            "---------FRONT---------\r\n"
            "---------BACK---------\r\n"
            "499|500- In village- 6000  (All deff [ 7000 ])\r\n"


        )

        self.assertEqual(result, expected)

    def test_get_deff_general_test_is_output_correct(self):
        result = deff.get_deff(outline=self.outline, radius=3)
        
        # expected = (
        #     '\r\n'
        #     'player1\r\n'
        #     '499|500 - 6000\r\n'
        #     'Łącznie - 6000 - miejsc w zagrodzie, CK liczone jako x4\r\n'
        #     '\r\n'
        #     'player2\r\n'
        #     '500|502 - 6000\r\n'
        #     '498|502 - 6000\r\n'
        #     '500|499 - 6000\r\n'
        #     'Łącznie - 18000 - miejsc w zagrodzie, CK liczone jako x4\r\n'
        # )

        expected = (
            "Tested. LEGEND: \r\n"
            "HEAVY counted as x4 and not x6, scouts are NOT counted.\r\n"
            "IN VILLAGES = troops in the village + everyone else's troops.\r\n"
            "ALL OWN = troops in the village + troops outside the village.\r\n\r\n"
            "\r\nplayer1\r\n"
            "On front 0 villages, 0 deff IN VILLAGE and 0 ALL OWN.\r\n"
            "On back 1 villages, 6000 deff IN VILLAGE and "
            "7000 ALL OWN.\r\n"
            "\r\n"
            "player2\r\n"
            "On front 1 villages, 30000 deff IN VILLAGE and "
            "8000 ALL OWN.\r\n"
            "On back 4 villages, 24000 deff IN VILLAGE and "
            "25000 ALL OWN.\r\n"
            "\r\n\r\n"
            "player1\r\n"
            "---------FRONT---------\r\n"
            "---------BACK---------\r\n"
            "499|500- In village- 6000  (All deff [ 7000 ])\r\n"
            "\r\n\r\n"
            "player2\r\n"
            "---------FRONT---------\r\n"
            "500|500- In village- 30000  (All deff [ 8000 ])\r\n"
            "---------BACK---------\r\n"
            "498|503- In village- 6000  (All deff [ 7000 ])\r\n"
            "500|502- In village- 6000  (All deff [ 4000 ])\r\n"
            "498|502- In village- 6000  (All deff [ 7000 ])\r\n"
            "500|499- In village- 6000  (All deff [ 7000 ])\r\n"
        )

        self.assertEqual(result, expected)

    def test_get_legal_coords_is_map_correct1(self):
        list_enemy_pk = [village.pk for village in [self.ally_village1]]
        list_ally_pk = [
            village.pk
            for village in [
                self.ally_village2,
                self.ally_village3,
                self.ally_village4,
                self.ally_village5,
                self.ally_village6,
            ]
        ]
        list_ally = models.VillageModel.objects.filter(pk__in=list_ally_pk).values()
        list_enemy = models.VillageModel.objects.filter(pk__in=list_enemy_pk).values()
        self.assertEqual(
            deff.get_legal_coords(list_ally, list_enemy, 4), set()
        )

    def test_get_legal_coords_is_map_correct2(self):
        list_ally_pk = [village.pk for village in [self.enemy_village2]]
        list_enemy_pk = [
            village.pk for village in [self.ally_village2, self.ally_village6]
        ]
        list_ally = models.VillageModel.objects.filter(pk__in=list_ally_pk).values()
        list_enemy = models.VillageModel.objects.filter(pk__in=list_enemy_pk).values()
        self.assertEqual(
            deff.get_legal_coords(list_ally, list_enemy, 4), {(500, 506)}
        )
