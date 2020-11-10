import datetime

from django.test import TestCase
from django.contrib.auth.models import User

from base import models
from tribal_wars import get_deff as deff


class GetDeffFunctionTest(TestCase):
    ''' Test for get_deff_text file SHOULD be very exact '''

    def setUp(self):
        ARMY_TEXT = (
            '500|500,3000,1000,0,0,0,1000,0,0,0,0,0,0,\r\n'
            '499|500,2000,1000,0,0,0,1000,0,0,0,0,0,0,\r\n'
            '498|503,2000,1000,0,0,0,1000,0,0,0,0,0,0,\r\n'
            '500|502,0,0,0,0,0,1000,0,0,0,0,0,0,\r\n'
            '498|502,2000,1000,0,0,0,1000,0,0,0,0,0,0,\r\n'
            '500|499,2000,1000,0,0,0,1000,0,0,0,0,0,0,\r\n'
        )
        DEFF_TEXT = (
            '500|500,w wiosce,13000,13000,0,0,0,1000,0,0,0,0,0,\r\n'
            '500|500,w drodze,0,0,0,0,0,0,0,0,0,0,0,\r\n'
            '499|500,w wiosce,1000,1000,0,0,0,1000,0,0,0,0,0,\r\n'
            '499|500,w drodze,0,0,0,0,0,0,0,0,0,0,0,\r\n'
            '498|503,w wiosce,1000,1000,0,0,0,1000,0,0,0,0,0,\r\n'
            '498|503,w drodze,0,0,0,0,0,0,0,0,0,0,0,\r\n'
            '500|502,w wiosce,1000,1000,0,0,0,1000,0,0,0,0,0,\r\n'
            '500|502,w drodze,0,0,0,0,0,0,0,0,0,0,0,\r\n'
            '498|502,w wiosce,1000,1000,0,0,0,1000,0,0,0,0,0,\r\n'
            '498|502,w drodze,0,0,0,0,0,0,0,0,0,0,0,\r\n'
            '500|499,w wiosce,1000,1000,0,0,0,1000,0,0,0,0,0,\r\n'
            '500|499,w drodze,0,0,0,0,0,0,0,0,0,0,0,'
        )
        self.world = models.World.objects.create(
            title='Świat 150',
            world=150,
            paladin='inactive',
            militia='inactive',
            archer='inactive',
        )
        
        self.admin = User.objects.create_user('admin', None, None)
        self.outline = models.Outline.objects.create(
            owner=self.admin,
            date=datetime.date.today(),
            name='name',
            world='150',
            ally_tribe_tag=['pl1', 'pl2'],
            enemy_tribe_tag=['pl3', 'pl4'],
            deff_troops=DEFF_TEXT,
            off_troops=ARMY_TEXT,
        )
        # not legal below
        self.ally_village1 = models.VillageModel(
            id='500500150',
            village_id=1,
            x_coord=500,
            y_coord=500,
            player_id=2,
            world=150,
        )
        self.ally_village2 = models.VillageModel(
            id='499500150',
            village_id=2,
            x_coord=499,
            y_coord=500,
            player_id=1,
            world=150,
        )
        # legal below
        self.ally_village3 = models.VillageModel(
            id='498503150',
            village_id=3,
            x_coord=498,
            y_coord=503,
            player_id=2,
            world=150,
        )
        self.ally_village4 = models.VillageModel(
            id='500502150',
            village_id=4,
            x_coord=500,
            y_coord=502,
            player_id=2,
            world=150,
        )
        self.ally_village5 = models.VillageModel(
            id='498502150',
            village_id=5,
            x_coord=498,
            y_coord=502,
            player_id=2,
            world=150,
        )
        self.ally_village6 = models.VillageModel(
            id='500499150',
            village_id=6,
            x_coord=500,
            y_coord=499,
            player_id=2,
            world=150,
        )
        # enemy villages
        self.enemy_village1 = models.VillageModel(
            id='503500150',
            village_id=7,
            x_coord=503,
            y_coord=500,
            player_id=3,
            world=150,
        )
        self.enemy_village2 = models.VillageModel(
            id='500506150',
            village_id=8,
            x_coord=500,
            y_coord=506,
            player_id=4,
            world=150,
        )

        self.ally_tribe1 = models.Tribe(
            id='pl1::150', tribe_id=1, tag='pl1', world=150
        )
        self.ally_tribe2 = models.Tribe(
            id='pl2::150', tribe_id=2, tag='pl2', world=150
        )
        self.enemy_tribe1 = models.Tribe(
            id='pl3::150', tribe_id=3, tag='pl3', world=150
        )
        self.enemy_tribe2 = models.Tribe(
            id='pl4::150', tribe_id=4, tag='pl4', world=150
        )

        self.ally_player1 = models.Player(
            id='player1:150',
            player_id=1,
            name='player1',
            tribe_id=1,
            world=150,
        )
        self.ally_player2 = models.Player(
            'player2:150', player_id=2, name='player2', tribe_id=2, world=150
        )

        self.enemy_player1 = models.Player(
            'player3:150', player_id=3, name='player3', tribe_id=3, world=150
        )
        self.enemy_player2 = models.Player(
            'player4:150', player_id=4, name='player4', tribe_id=4, world=150
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
        self.maxDiff = None
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
            '\r\nplayer1\r\n'
            'Na froncie 0 wsi, 0 deffa W WIOSKACH, zaś 0 CAŁEGO SWOJEGO.\r\n'
            'Na zapleczu 1 wsi, 6000 deffa W WIOSKACH, zaś 7000 CAŁEGO SWOJEGO.\r\n'
            '\r\n'
            'player2\r\n'
            'Na froncie 2 wsi, 36000 deffa W WIOSKACH, zaś 15000 CAŁEGO SWOJEGO.\r\n'
            'Na zapleczu 3 wsi, 18000 deffa W WIOSKACH, zaś 18000 CAŁEGO SWOJEGO.\r\n'
            '\r\n\r\n'
            'player1\r\n'
            '---------FRONT---------\r\n'
            '---------ZAPLECZE---------\r\n'
            '499|500- W wiosce- 6000  (CAŁY własny deff [ 7000 ])\r\n'
            '\r\n\r\n'
            'player2\r\n'
            '---------FRONT---------\r\n'
            '500|500- W wiosce- 30000  (CAŁY własny deff [ 8000 ])\r\n'
            '498|503- W wiosce- 6000  (CAŁY własny deff [ 7000 ])\r\n'
            '---------ZAPLECZE---------\r\n'
            '500|502- W wiosce- 6000  (CAŁY własny deff [ 4000 ])\r\n'
            '498|502- W wiosce- 6000  (CAŁY własny deff [ 7000 ])\r\n'
            '500|499- W wiosce- 6000  (CAŁY własny deff [ 7000 ])\r\n'
        )

        self.assertEqual(result, expected)

    def test_get_legal_coords_is_map_correct1(self):
        list_enemy = [self.ally_village1]
        list_ally = [
            self.ally_village2,
            self.ally_village3,
            self.ally_village4,
            self.ally_village5,
            self.ally_village6,
        ]
        self.assertEqual(
            deff.get_legal_coords(list_ally, list_enemy, 4), set()
        )

    def test_get_legal_coords_is_map_correct2(self):
        list_ally = [self.enemy_village2]
        list_enemy = [self.ally_village2, self.ally_village6]
        self.assertEqual(
            deff.get_legal_coords(list_ally, list_enemy, 4), {(500, 506)}
        )
