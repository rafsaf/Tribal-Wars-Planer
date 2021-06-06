from base import models

from base.tests.test_utils.mini_setup import MiniSetup


class RemoveUserOutline(MiniSetup):
    def test_reset_outline_to_defaults(self):
        outline = self.get_outline(add_result=True)
        outline_time = self.create_outline_time(outline)
        outline.written = "active"
        outline.avaiable_offs = [1, 23, 5]
        outline.avaiable_offs_near = [123, 123, 5]
        outline.avaiable_nobles = [1]
        outline.avaiable_nobles_near = [55]
        outline.avaiable_ruins = 66
        outline.filter_weights_min = 15000
        outline.filter_weights_max = 15001
        outline.filter_card_number = 25
        outline.filter_targets_number = 5
        outline.filter_hide_front = "front"
        outline.choice_sort = "random_noblemans"
        outline.default_off_time_id = outline_time.pk
        outline.default_fake_time_id = outline_time.pk
        outline.default_ruin_time_id = outline_time.pk
        outline.remove_user_outline()

        assert outline.written == "inactive"
        assert outline.avaiable_offs == []
        assert outline.avaiable_offs_near == []
        assert outline.avaiable_nobles == []
        assert outline.avaiable_nobles_near == []
        assert outline.avaiable_ruins == None
        assert outline.filter_weights_min == 0
        assert outline.filter_weights_max == 30000
        assert outline.filter_card_number == 12
        assert outline.filter_targets_number == 12
        assert outline.filter_hide_front == "all"
        assert outline.choice_sort == "distance"
        assert outline.default_off_time_id == None
        assert outline.default_fake_time_id == None
        assert outline.default_ruin_time_id == None

    def test_reset_results_to_defaults(self):
        outline = self.get_outline(add_result=True)
        result: models.Result = models.Result.objects.get(outline=outline)
        result.results_outline = self.random_lower_string()
        result.results_players = self.random_lower_string()
        result.results_sum_up = self.random_lower_string()
        result.results_export = self.random_lower_string()
        result.save()
        outline.remove_user_outline()

        result.refresh_from_db()
        assert result.results_outline == ""
        assert result.results_players == ""
        assert result.results_sum_up == ""
        assert result.results_export == ""

    def test_delete_all_weights_and_outline_times_and_update_overviews(self):
        outline = self.get_outline(add_result=True, test_world=True)
        self.create_target_on_test_world(outline)
        target = models.TargetVertex.objects.get(target="200|200")
        weight_max = self.create_weight_maximum(outline)

        self.create_outline_time(outline)
        self.create_weight(target, weight_max)
        overview = self.create_overview(outline)

        assert overview.removed == False
        assert models.WeightMaximum.objects.count() == 1
        assert models.TargetVertex.objects.count() == 1
        assert models.WeightModel.objects.count() == 1
        assert models.OutlineTime.objects.count() == 1

        outline.remove_user_outline()
        overview.refresh_from_db()

        assert overview.removed == True
        assert models.WeightModel.objects.count() == 0
        assert models.OutlineTime.objects.count() == 0
        assert models.WeightMaximum.objects.count() == 0
        assert models.TargetVertex.objects.count() == 0

    def test_weight_max_still_exists_but_is_updated_correctly_and_target_deleted(self):
        outline = self.get_outline(add_result=True, test_world=True)
        outline.off_troops = "102|102,100,100,7002,0,100,2802,0,0,350,100,0,0,0,0,0,"
        outline.initial_outline_targets = self.random_lower_string()
        outline.initial_outline_fake_limit = 10
        outline.save()

        self.create_target_on_test_world(outline)

        weight_max = self.create_weight_maximum(outline, start="102|102")
        weight_max.off_max = 15000
        weight_max.off_left = 10000
        weight_max.off_state = 5000
        weight_max.nobleman_max = 15
        weight_max.nobleman_left = 10
        weight_max.nobleman_state = 5
        weight_max.catapult_max = 150
        weight_max.catapult_left = 100
        weight_max.catapult_state = 50
        weight_max.x_coord = 102
        weight_max.y_coord = 102
        weight_max.player = "some-player"
        weight_max.hidden = True
        weight_max.first_line = True
        weight_max.too_far_away = True
        weight_max.fake_limit = 0
        weight_max.save()

        assert models.WeightMaximum.objects.count() == 1
        assert models.TargetVertex.objects.count() == 1

        outline.remove_user_outline()

        assert models.WeightMaximum.objects.count() == 1
        assert models.TargetVertex.objects.count() == 0

        weight_max.refresh_from_db()

        assert weight_max.off_max == 15000
        assert weight_max.off_left == 15000
        assert weight_max.off_state == 0
        assert weight_max.nobleman_max == 15
        assert weight_max.nobleman_left == 15
        assert weight_max.nobleman_state == 0
        assert weight_max.catapult_max == 150
        assert weight_max.catapult_left == 150
        assert weight_max.catapult_state == 0
        assert weight_max.x_coord == 102
        assert weight_max.y_coord == 102
        assert weight_max.player == "some-player"
        assert weight_max.hidden == False
        assert weight_max.first_line == False
        assert weight_max.too_far_away == False
        assert weight_max.fake_limit == 10

    def test_weight_max_ok_real_target_bad(self):
        outline = self.get_outline(add_result=True, test_world=True)
        outline.off_troops = "102|102,100,100,7002,0,100,2802,0,0,350,100,0,0,0,0,0,"
        outline.initial_outline_targets = "200|200:4:4"
        outline.initial_outline_fakes = "201|201:4:4"
        outline.initial_outline_ruins = "202|202:4:4"
        outline.save()

        self.create_target_on_test_world(outline)
        self.create_target_on_test_world(outline, fake=True, coord="201|201")
        self.create_target_on_test_world(outline, ruin=True, coord="202|202")
        self.create_weight_maximum(outline, start="102|102")

        assert models.WeightMaximum.objects.count() == 1
        assert models.TargetVertex.objects.count() == 3

        # WORKS WHEN OK
        outline.remove_user_outline()

        assert models.WeightMaximum.objects.count() == 1
        assert models.TargetVertex.objects.count() == 3

        # TARGET DELETED WHEN VILLAGE BECAME BARBARIAN
        models.VillageModel.objects.filter(coord="200|200").update(player=None)
        outline.remove_user_outline()

        assert models.WeightMaximum.objects.count() == 1
        assert models.TargetVertex.objects.count() == 0

    def test_weight_max_ok_fake_target_bad(self):
        outline = self.get_outline(add_result=True, test_world=True)
        outline.off_troops = "102|102,100,100,7002,0,100,2802,0,0,350,100,0,0,0,0,0,"
        outline.initial_outline_targets = "200|200:4:4"
        outline.initial_outline_fakes = "201|201:4:4"
        outline.initial_outline_ruins = "202|202:4:4"
        outline.save()

        self.create_target_on_test_world(outline)
        self.create_target_on_test_world(outline, fake=True, coord="201|201")
        self.create_target_on_test_world(outline, ruin=True, coord="202|202")
        self.create_weight_maximum(outline, start="102|102")

        assert models.WeightMaximum.objects.count() == 1
        assert models.TargetVertex.objects.count() == 3

        # WORKS WHEN OK
        outline.remove_user_outline()

        assert models.WeightMaximum.objects.count() == 1
        assert models.TargetVertex.objects.count() == 3

        # TARGET DELETED WHEN VILLAGE BECAME BARBARIAN
        models.VillageModel.objects.filter(coord="201|201").update(player=None)
        outline.remove_user_outline()

        assert models.WeightMaximum.objects.count() == 1
        assert models.TargetVertex.objects.count() == 0

    def test_weight_max_ok_ruin_target_bad(self):
        outline = self.get_outline(add_result=True, test_world=True)
        outline.off_troops = "102|102,100,100,7002,0,100,2802,0,0,350,100,0,0,0,0,0,"
        outline.initial_outline_targets = "200|200:4:4"
        outline.initial_outline_fakes = "201|201:4:4"
        outline.initial_outline_ruins = "202|202:4:4"
        outline.save()

        self.create_target_on_test_world(outline)
        self.create_target_on_test_world(outline, fake=True, coord="201|201")
        self.create_target_on_test_world(outline, ruin=True, coord="202|202")
        self.create_weight_maximum(outline, start="102|102")

        assert models.WeightMaximum.objects.count() == 1
        assert models.TargetVertex.objects.count() == 3

        # WORKS WHEN OK
        outline.remove_user_outline()

        assert models.WeightMaximum.objects.count() == 1
        assert models.TargetVertex.objects.count() == 3

        # TARGET DELETED WHEN VILLAGE BECAME BARBARIAN
        models.VillageModel.objects.filter(coord="202|202").update(player=None)
        outline.remove_user_outline()

        assert models.WeightMaximum.objects.count() == 1
        assert models.TargetVertex.objects.count() == 0