import datetime

from django.test import TestCase
from django.contrib.auth.models import User

from base import models
from tribal_wars import outline_initial as initial


class TestCreateOutlineFunction(TestCase):
    def setUp(self):
        TEXT = (
            "500|500,0,0,10000,0,0,0,0,0,2,0,0,\r\n"
            "500|501,0,0,190,0,0,0,0,0,0,0,0,\r\n"
            "500|502,0,0,19500,0,0,0,0,0,0,0,0,\r\n"
            "500|503,0,0,20100,0,0,0,0,0,0,0,0,\r\n"
            "500|504,0,0,20000,0,0,0,0,0,2,0,0,\r\n"
            "500|505,0,0,20000,0,0,0,0,0,2,0,0,"
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
            ally_tribe_tag=["pl1"],
            enemy_tribe_tag=["pl2"],
            initial_outline_targets="500|499:1:4\r\n500|498:1:2---",
            initial_outline_min_off=15000,
            initial_outline_front_dist=3,
            off_troops=TEXT,
        )
        # front
        self.ally_village1 = models.VillageModel(
            id="500500150",
            village_id=0,
            x_coord=500,
            y_coord=500,
            player_id=0,
            world=150,
        )
        # front
        self.ally_village2 = models.VillageModel(
            id="500501150",
            village_id=1,
            x_coord=500,
            y_coord=501,
            player_id=0,
            world=150,
        )
        # front
        self.ally_village3 = models.VillageModel(
            id="500502150",
            village_id=2,
            x_coord=500,
            y_coord=502,
            player_id=0,
            world=150,
        )
        self.ally_village4 = models.VillageModel(
            id="500503150",
            village_id=3,
            x_coord=500,
            y_coord=503,
            player_id=0,
            world=150,
        )
        self.ally_village5 = models.VillageModel(
            id="500504150",
            village_id=4,
            x_coord=500,
            y_coord=504,
            player_id=0,
            world=150,
        )
        self.ally_village6 = models.VillageModel(
            id="500505150",
            village_id=5,
            x_coord=500,
            y_coord=505,
            player_id=0,
            world=150,
        )

        self.enemy_village1 = models.VillageModel(
            id="500499150",
            village_id=6,
            x_coord=500,
            y_coord=499,
            player_id=1,
            world=150,
        )
        self.enemy_village2 = models.VillageModel(
            id="500498150",
            village_id=7,
            x_coord=500,
            y_coord=498,
            player_id=1,
            world=150,
        )

        self.ally_tribe = models.Tribe(
            id="pl1::150", tribe_id=0, tag="pl1", world=150
        )
        self.enemy_tribe = models.Tribe(
            id="pl2::150", tribe_id=1, tag="pl2", world=150
        )

        self.ally_player = models.Player(
            id="player0:150",
            player_id=0,
            name="player0",
            tribe_id=0,
            world=150,
        )
        self.enemy_player = models.Player(
            "player1:150", player_id=1, name="player1", tribe_id=1, world=150
        )

        self.ally_village1.save()
        self.ally_village2.save()
        self.ally_village3.save()
        self.ally_village4.save()
        self.ally_village5.save()
        self.ally_village6.save()
        self.enemy_village1.save()
        self.enemy_village2.save()
        self.ally_tribe.save()
        self.enemy_tribe.save()
        self.ally_player.save()
        self.enemy_player.save()

    def test_make_outline_2_targets_create(self):
        initial.make_outline(outline=self.outline)
        self.assertEqual(models.TargetVertex.objects.all().count(), 2)

    def test_make_outline_6_weights_max_create_2_is_front(self):
        initial.make_outline(outline=self.outline)
        self.assertEqual(models.WeightMaximum.objects.all().count(), 6)
        self.assertEqual(
            models.WeightMaximum.objects.filter(first_line=True).count(), 3
        )

    def test_make_outline_number_of_queries_is_16(self):
        with self.assertNumQueries(16):
            initial.make_outline(outline=self.outline)

    def test_repeat_make_outline_number_of_queries_is_23(self):
        # second one do not create weight max models
        with self.assertNumQueries(23):
            initial.make_outline(outline=self.outline)
            initial.make_outline(outline=self.outline)


#    def test_correct_updated_weight_max_weight_village_1(self):
#        initial.make_outline(outline=self.outline)
#        weight = models.WeightMaximum.objects.get(
#            outline=self.outline, start="500|500"
#        )
#        self.assertEqual(weight.nobleman_left, 0)
#        self.assertEqual(weight.nobleman_state, 2)
#        self.assertEqual(weight.off_left, 0)
#        self.assertEqual(weight.off_state, 10000)
#
#    def test_correct_updated_weight_max_weight_village_3(self):
#        initial.make_outline(outline=self.outline)
#        weight = models.WeightMaximum.objects.get(
#            outline=self.outline, start="500|502"
#        )
#        self.assertEqual(weight.nobleman_left, 0)
#        self.assertEqual(weight.nobleman_state, 0)
#        self.assertEqual(weight.off_left, 19500)
#        self.assertEqual(weight.off_state, 0)
#
#    def test_correct_updated_weight_max_weight_village_4(self):
#        initial.make_outline(outline=self.outline)
#        weight = models.WeightMaximum.objects.get(
#            outline=self.outline, start="500|502"
#        )
#        self.assertEqual(weight.nobleman_left, 0)
#        self.assertEqual(weight.nobleman_state, 0)
#        self.assertEqual(weight.off_left, 0)
#        self.assertEqual(weight.off_state, 20100)
#
#    def test_correct_updated_weight_max_weight_village_5(self):
#        initial.make_outline(outline=self.outline)
#        weight = models.WeightMaximum.objects.get(
#            outline=self.outline, start="500|504"
#        )
#        self.assertEqual(weight.nobleman_left, 0)
#        self.assertEqual(weight.nobleman_state, 2)
#        self.assertEqual(weight.off_left, 0)
#        self.assertEqual(weight.off_state, 20000)
#
#    def test_correct_updated_weight_max_weight_village_6(self):
#        initial.make_outline(outline=self.outline)
#        weight = models.WeightMaximum.objects.get(
#            outline=self.outline, start="500|505"
#        )
#        self.assertEqual(weight.nobleman_left, 0)
#        self.assertEqual(weight.nobleman_state, 2)
#        self.assertEqual(weight.off_left, 0)
#        self.assertEqual(weight.off_state, 20000)
#