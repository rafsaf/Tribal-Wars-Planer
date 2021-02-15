import datetime

from django.test import TestCase
from django.contrib.auth.models import User

from base import models
from tribal_wars import basic, outline_initial as initial


class TestMakeOutlineFunction(TestCase):
    def setUp(self):
        TEXT = (
            "500|500,0,0,10000,0,0,0,0,0,2,0,0,\r\n"
            "500|501,0,0,190,0,0,0,0,0,0,0,0,\r\n"
            "500|502,0,0,19500,0,0,0,0,0,0,0,0,\r\n"
            "500|503,0,0,20100,0,0,0,0,0,0,0,0,\r\n"
            "500|504,0,0,20000,0,0,0,0,0,2,0,0,\r\n"
            "500|505,0,0,20000,0,0,0,0,0,2,0,0,"
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
            militia="active",
        )
        self.real_target_mode = basic.TargetMode("real")
        self.fake_target_mode = basic.TargetMode("fake")

        self.admin = User.objects.create_user("admin", None, None)

        self.outline: models.Outline = models.Outline.objects.create(
            owner=self.admin,
            date=datetime.date.today(),
            name="name",
            world=self.world1,
            ally_tribe_tag=["pl1"],
            enemy_tribe_tag=["pl2"],
            initial_outline_targets="500|499:1:4\r\n500|498:1:2",
            initial_outline_min_off=15000,
            initial_outline_front_dist=3,
            off_troops=TEXT,
        )
        # front

        self.ally_tribe = models.Tribe(tribe_id=0, tag="pl1", world=self.world1)
        self.enemy_tribe = models.Tribe(tribe_id=1, tag="pl2", world=self.world1)

        self.ally_player = models.Player(
            player_id=0,
            name="player0",
            tribe=self.ally_tribe,
            world=self.world1,
        )
        self.enemy_player = models.Player(
            player_id=1, name="player1", tribe=self.enemy_tribe, world=self.world1
        )
        self.ally_village1 = models.VillageModel(
            coord="500|500",
            village_id=0,
            x_coord=500,
            y_coord=500,
            player=self.ally_player,
            world=self.world1,
        )
        # front
        self.ally_village2 = models.VillageModel(
            coord="500|501",
            village_id=1,
            x_coord=500,
            y_coord=501,
            player=self.ally_player,
            world=self.world1,
        )
        # front
        self.ally_village3 = models.VillageModel(
            coord="500|502",
            village_id=2,
            x_coord=500,
            y_coord=502,
            player=self.ally_player,
            world=self.world1,
        )
        self.ally_village4 = models.VillageModel(
            coord="500|503",
            village_id=3,
            x_coord=500,
            y_coord=503,
            player=self.ally_player,
            world=self.world1,
        )
        self.ally_village5 = models.VillageModel(
            coord="500|504",
            village_id=4,
            x_coord=500,
            y_coord=504,
            player=self.ally_player,
            world=self.world1,
        )
        self.ally_village6 = models.VillageModel(
            coord="500|505",
            village_id=5,
            x_coord=500,
            y_coord=505,
            player=self.ally_player,
            world=self.world1,
        )

        self.enemy_village1 = models.VillageModel(
            coord="500|499",
            village_id=6,
            x_coord=500,
            y_coord=499,
            player=self.enemy_player,
            world=self.world1,
        )
        self.enemy_village2 = models.VillageModel(
            coord="500|498",
            village_id=7,
            x_coord=500,
            y_coord=498,
            player=self.enemy_player,
            world=self.world1,
        )
        self.enemy_village3 = models.VillageModel(
            coord="500|497",
            village_id=8,
            x_coord=500,
            y_coord=497,
            player=self.enemy_player,
            world=self.world1,
        )
        self.ally_tribe.save()
        self.enemy_tribe.save()
        self.ally_player.save()
        self.enemy_player.save()
        self.ally_village1.save()
        self.ally_village2.save()
        self.ally_village3.save()
        self.ally_village4.save()
        self.ally_village5.save()
        self.ally_village6.save()
        self.enemy_village1.save()
        self.enemy_village2.save()
        self.enemy_village3.save()

    def test_make_outline_2_targets_real_create(self):
        initial.make_outline(outline=self.outline, target_mode=self.real_target_mode)
        self.assertEqual(models.TargetVertex.objects.all().count(), 2)

    def test_make_outline_2_targets_real_1_fake_create(self):
        self.outline.initial_outline_targets = "500|499:1:4\r\n500|498:1:2"
        self.outline.initial_outline_fakes = "500|497:0:0"
        self.outline.save()
        initial.make_outline(outline=self.outline, target_mode=self.real_target_mode)
        initial.make_outline(outline=self.outline, target_mode=self.fake_target_mode)
        self.assertEqual(models.TargetVertex.objects.all().count(), 3)

    def test_make_outline_target1_exists(self):
        initial.make_outline(outline=self.outline, target_mode=self.real_target_mode)
        self.assertEqual(
            models.TargetVertex.objects.filter(
                outline=self.outline, target="500|499", fake=False, ruin=False
            ).count(),
            1,
        )

    def test_make_outline_target1_required_off_1_required_noble_4(self):
        initial.make_outline(outline=self.outline, target_mode=self.real_target_mode)
        target1 = models.TargetVertex.objects.get(
            target="500|499", outline=self.outline, fake=False, ruin=False
        )
        self.assertEqual(target1.required_off, 1)
        self.assertEqual(target1.required_noble, 4)
        self.assertEqual(target1.exact_off, [])
        self.assertEqual(target1.exact_noble, [])

    def test_make_outline_target2_required_off_1_required_noble_2(self):
        initial.make_outline(outline=self.outline, target_mode=self.real_target_mode)
        target2 = models.TargetVertex.objects.get(
            target="500|498", outline=self.outline, fake=False, ruin=False
        )
        self.assertEqual(target2.required_off, 1)
        self.assertEqual(target2.required_noble, 2)
        self.assertEqual(target2.exact_off, [])
        self.assertEqual(target2.exact_noble, [])

    def test_make_outline_target1_off_0_noble_5_exact_correct_off(self):
        self.outline.initial_outline_targets = "500|499:1|2|3|4:5\r\n500|498:6:7|8|9|10"
        self.outline.save()
        initial.make_outline(outline=self.outline, target_mode=self.real_target_mode)
        target1 = models.TargetVertex.objects.get(
            target="500|499",
            outline=self.outline,
            fake=False,
            ruin=False,
        )
        self.assertEqual(target1.required_off, 0)
        self.assertEqual(target1.required_noble, 5)
        self.assertEqual(target1.exact_off, [1, 2, 3, 4])
        self.assertEqual(target1.exact_noble, [])

    def test_make_outline_target2_off_1_noble_0_exact_correct_noble(self):
        self.outline.initial_outline_targets = "500|499:1|2|3|4:5\r\n500|498:6:7|8|9|10"
        self.outline.save()
        initial.make_outline(outline=self.outline, target_mode=self.real_target_mode)
        target2 = models.TargetVertex.objects.get(
            target="500|498",
            outline=self.outline,
            ruin=False,
            fake=False,
        )
        self.assertEqual(target2.required_off, 6)
        self.assertEqual(target2.required_noble, 0)
        self.assertEqual(target2.exact_off, [])
        self.assertEqual(target2.exact_noble, [7, 8, 9, 10])

    def test_make_outline_target1_has_same_default_modes_as_outline(self):
        initial.make_outline(outline=self.outline, target_mode=self.real_target_mode)
        target1 = models.TargetVertex.objects.get(
            target="500|498", outline=self.outline, fake=False, ruin=False
        )
        self.assertEqual(target1.mode_off, self.outline.mode_off)
        self.assertEqual(target1.mode_noble, self.outline.mode_noble)
        self.assertEqual(target1.mode_division, self.outline.mode_division)
        self.assertEqual(target1.mode_guide, self.outline.mode_guide)

    def test_make_outline_target1_has_same_other_modes_as_outline(self):
        self.outline.mode_noble = "far"
        self.outline.mode_off = "closest"
        self.outline.mode_guide = "single"
        self.outline.mode_division = "separatly"
        self.outline.save()
        initial.make_outline(outline=self.outline, target_mode=self.real_target_mode)
        target1 = models.TargetVertex.objects.get(
            target="500|498", outline=self.outline, fake=False, ruin=False
        )
        self.assertEqual(target1.mode_off, self.outline.mode_off)
        self.assertEqual(target1.mode_noble, self.outline.mode_noble)
        self.assertEqual(target1.mode_division, self.outline.mode_division)
        self.assertEqual(target1.mode_guide, self.outline.mode_guide)

    def test_make_outline_6_weights_max_create_0_is_front(self):
        initial.make_outline(outline=self.outline, target_mode=self.real_target_mode)
        self.assertEqual(models.WeightMaximum.objects.all().count(), 6)
        self.assertEqual(
            models.WeightMaximum.objects.filter(first_line=True).count(), 0
        )

    def test_make_outline_number_of_queries_is_6(self):
        with self.assertNumQueries(6):
            initial.make_outline(
                outline=self.outline, target_mode=self.real_target_mode
            )

    def test_repeat_make_outline_number_of_queries_is_13(self):
        # second one do not create weight max models
        with self.assertNumQueries(13):
            initial.make_outline(
                outline=self.outline, target_mode=self.real_target_mode
            )
            initial.make_outline(
                outline=self.outline, target_mode=self.real_target_mode
            )

    def test_repeat_make_outline_number_of_queries_is_20(self):
        # second one do not create weight max models
        with self.assertNumQueries(20):
            initial.make_outline(
                outline=self.outline, target_mode=self.real_target_mode
            )
            initial.make_outline(
                outline=self.outline, target_mode=self.real_target_mode
            )
            initial.make_outline(
                outline=self.outline, target_mode=self.real_target_mode
            )


class TestCompleteOutlineFunction(TestCase):
    def setUp(self):
        TEXT = (
            "500|500,0,0,16000,0,0,0,0,0,2,0,0,\r\n"
            "500|501,0,0,190,0,0,0,0,0,0,0,0,\r\n"
            "500|502,0,0,19500,0,0,0,0,0,0,0,0,\r\n"
            "500|503,0,0,20100,0,0,0,0,0,0,0,0,\r\n"
            "500|504,0,0,20000,0,0,0,0,0,2,0,0,\r\n"
            "500|505,0,0,20000,0,0,0,0,0,8,0,0,\r\n"
            "500|506,0,0,20000,0,0,0,0,0,0,0,0,\r\n"
            "500|507,0,0,20000,0,0,0,0,0,0,0,0,\r\n"
            "500|508,0,0,20000,0,0,0,0,0,0,0,0,\r\n"
            "500|509,0,0,20000,0,0,0,0,0,0,0,0,\r\n"
            "500|510,0,0,10000,0,0,0,0,0,0,0,0,"
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
            militia="active",
        )

        self.admin = User.objects.create_user("admin", None, None)

        self.real_target_mode: basic.TargetMode = basic.TargetMode("real")

        self.outline: models.Outline = models.Outline.objects.create(
            owner=self.admin,
            date=datetime.date.today(),
            name="name",
            world=self.world1,
            ally_tribe_tag=["pl1"],
            enemy_tribe_tag=["pl2"],
            initial_outline_targets="500|499:1:4\r\n500|498:1:2---",
            initial_outline_min_off=15000,
            initial_outline_front_dist=3,
            off_troops=TEXT,
        )
        # front

        self.ally_tribe = models.Tribe(tribe_id=0, tag="pl1", world=self.world1)
        self.enemy_tribe = models.Tribe(tribe_id=1, tag="pl2", world=self.world1)

        self.ally_player = models.Player(
            player_id=0,
            name="player0",
            tribe=self.ally_tribe,
            world=self.world1,
        )
        self.enemy_player = models.Player(
            player_id=1, name="player1", tribe=self.enemy_tribe, world=self.world1
        )
        self.ally_village1 = models.VillageModel(
            coord="500|500",
            village_id=0,
            x_coord=500,
            y_coord=500,
            player=self.ally_player,
            world=self.world1,
        )
        # front
        self.ally_village2 = models.VillageModel(
            coord="500|501",
            village_id=1,
            x_coord=500,
            y_coord=501,
            player=self.ally_player,
            world=self.world1,
        )
        # front
        self.ally_village3 = models.VillageModel(
            coord="500|502",
            village_id=2,
            x_coord=500,
            y_coord=502,
            player=self.ally_player,
            world=self.world1,
        )
        self.ally_village4 = models.VillageModel(
            coord="500|503",
            village_id=3,
            x_coord=500,
            y_coord=503,
            player=self.ally_player,
            world=self.world1,
        )
        self.ally_village5 = models.VillageModel(
            coord="500|504",
            village_id=4,
            x_coord=500,
            y_coord=504,
            player=self.ally_player,
            world=self.world1,
        )
        self.ally_village6 = models.VillageModel(
            coord="500|505",
            village_id=5,
            x_coord=500,
            y_coord=505,
            player=self.ally_player,
            world=self.world1,
        )
        self.ally_village7 = models.VillageModel(
            coord="500|506",
            village_id=6,
            x_coord=500,
            y_coord=506,
            player=self.ally_player,
            world=self.world1,
        )
        self.ally_village8 = models.VillageModel(
            coord="500|507",
            village_id=7,
            x_coord=500,
            y_coord=507,
            player=self.ally_player,
            world=self.world1,
        )
        self.ally_village9 = models.VillageModel(
            coord="500|508",
            village_id=8,
            x_coord=500,
            y_coord=508,
            player=self.ally_player,
            world=self.world1,
        )
        self.ally_village10 = models.VillageModel(
            coord="500|509",
            village_id=9,
            x_coord=500,
            y_coord=509,
            player=self.ally_player,
            world=self.world1,
        )
        self.ally_village11 = models.VillageModel(
            coord="500|510",
            village_id=10,
            x_coord=500,
            y_coord=510,
            player=self.ally_player,
            world=self.world1,
        )

        self.enemy_village1 = models.VillageModel(
            coord="500|499",
            village_id=6,
            x_coord=500,
            y_coord=499,
            player=self.enemy_player,
            world=self.world1,
        )
        self.enemy_village2 = models.VillageModel(
            coord="500|498",
            village_id=7,
            x_coord=500,
            y_coord=498,
            player=self.enemy_player,
            world=self.world1,
        )
        self.enemy_village3 = models.VillageModel(
            coord="500|497",
            village_id=8,
            x_coord=500,
            y_coord=497,
            player=self.enemy_player,
            world=self.world1,
        )
        self.ally_tribe.save()
        self.enemy_tribe.save()
        self.ally_player.save()
        self.enemy_player.save()
        self.ally_village1.save()
        self.ally_village2.save()
        self.ally_village3.save()
        self.ally_village4.save()
        self.ally_village5.save()
        self.ally_village6.save()
        self.ally_village7.save()
        self.ally_village8.save()
        self.ally_village9.save()
        self.ally_village10.save()
        self.ally_village11.save()
        self.enemy_village1.save()
        self.enemy_village2.save()
        self.enemy_village3.save()

    def test_outline_complete_far_off_correct1(self):
        self.outline.initial_outline_targets = "500|499:1:0"
        self.outline.save()
        initial.make_outline(outline=self.outline, target_mode=self.real_target_mode)
        target1 = models.TargetVertex.objects.get(target="500|499")
        target1.mode_off = "far"
        target1.save()
        initial.complete_outline(outline=self.outline)
        target1 = models.TargetVertex.objects.get(target="500|499")
        weight = models.WeightModel.objects.get(target=target1)
        self.assertTrue(
            weight.start
            in [
                "500|507",
                "500|508",
                "500|509",
            ]
        )

    def test_outline_complete_random_off_correct1(self):
        self.outline.initial_outline_targets = "500|499:1:0"
        self.outline.save()
        initial.make_outline(outline=self.outline, target_mode=self.real_target_mode)
        target1 = models.TargetVertex.objects.get(target="500|499")
        target1.mode_off = "random"
        target1.save()
        initial.complete_outline(outline=self.outline)
        target1 = models.TargetVertex.objects.get(target="500|499")
        weight = models.WeightModel.objects.get(target=target1)
        self.assertTrue(int(weight.start[4:7]) > 502)

    def test_outline_complete_close_off_correct1(self):
        self.outline.initial_outline_targets = "500|499:1:0"
        self.outline.save()
        initial.make_outline(outline=self.outline, target_mode=self.real_target_mode)
        target1 = models.TargetVertex.objects.get(target="500|499")
        target1.mode_off = "close"
        target1.save()
        initial.complete_outline(outline=self.outline)
        target1 = models.TargetVertex.objects.get(target="500|499")
        weight = models.WeightModel.objects.get(target=target1)
        self.assertTrue(
            weight.start
            in [
                "500|503",
                "500|502",
            ]
        )

    def test_outline_complete_closest_off_correct1(self):
        self.outline.initial_outline_targets = "500|499:1:0"
        self.outline.save()
        initial.make_outline(outline=self.outline, target_mode=self.real_target_mode)
        target1 = models.TargetVertex.objects.get(target="500|499")
        target1.mode_off = "closest"
        target1.save()
        initial.complete_outline(outline=self.outline)
        target1 = models.TargetVertex.objects.get(target="500|499")
        weight = models.WeightModel.objects.get(target=target1)
        self.assertTrue(weight.start in ["500|502"])
