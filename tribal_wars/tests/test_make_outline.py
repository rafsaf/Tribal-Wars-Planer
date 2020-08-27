import datetime

from django.test import TestCase
from django.contrib.auth.models import User

from base import models
from tribal_wars import outline_initial as initial


class TestCreateOutlineFunction(TestCase):
    def setUp(self):
        TEXT = (
            "500|500,0,0,10000,0,0,0,0,0,4,0,0,\r\n"
            "499|500,0,0,190,0,0,0,0,0,0,0,0,\r\n"
            "498|503,0,0,19500,0,0,0,0,0,0,0,0,\r\n"
            "500|502,0,0,20100,0,0,0,0,0,0,0,0,\r\n"
            "498|502,0,0,20000,0,0,0,0,0,2,0,0,\r\n"
            "500|499,0,0,20000,0,0,0,0,0,2,0,0,"
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
            enemy_tribe_tag=["pl3", "pl4"],
            initial_outline_targets="500|506:2:3\r\n503|500:1:1",
            initial_outline_min_off=15000,
            initial_outline_front_dist=3,
            off_troops=TEXT,
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
            village_id=7,
            x_coord=503,
            y_coord=500,
            player_id=3,
            world=150,
        )
        self.enemy_village2 = models.VillageModel(
            id="500506150",
            village_id=8,
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

    def test_make_outline_2_targets_create(self):
        initial.make_outline(outline=self.outline)
        self.assertEqual(models.TargetVertex.objects.all().count(), 2)

    def test_make_outline_5_weights_max_create_2_is_front(self):
        initial.make_outline(outline=self.outline)
        self.assertEqual(models.WeightMaximum.objects.all().count(), 5)
        self.assertEqual(
            models.WeightMaximum.objects.filter(first_line=True).count(), 2
        )
