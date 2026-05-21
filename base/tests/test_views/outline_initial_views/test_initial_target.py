# Copyright 2021 Rafał Safin (rafsaf). All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from django.urls import reverse

from base.models import TargetVertex, WeightMaximum
from base.tests.test_utils.mini_setup import MiniSetup


class InitialForm(MiniSetup):
    def test_planer_initial_detail___302_not_auth_redirect_login(self):
        outline = self.get_outline(test_world=True, written="active")
        self.create_target_on_test_world(outline)
        target = TargetVertex.objects.get(target="200|200")
        PATH = reverse("base:planer_initial_detail", args=[outline.pk, target.pk])

        response = self.client.get(PATH)
        assert response.status_code == 302
        assert getattr(response, "url") == self.login_page_path(next=PATH)

    def test_planer_initial_detail___404_foreign_user_no_access(self):
        outline = self.get_outline(test_world=True, written="active")
        self.create_target_on_test_world(outline)
        target = TargetVertex.objects.get(target="200|200")
        PATH = reverse("base:planer_initial_detail", args=[outline.pk, target.pk])

        self.login_foreign_user()
        response = self.client.get(PATH)
        assert response.status_code == 404

        response = self.client.post(PATH)
        assert response.status_code == 404

    def test_planer_initial_detail___404_target_must_belong_to_outline(self):
        own_outline = self.get_outline(test_world=True, written="active")
        foreign_outline = self.create_foreign_outline(test_world=True, written="active")
        self.create_target_on_test_world(foreign_outline)
        foreign_target = TargetVertex.objects.get(
            target="200|200", outline=foreign_outline
        )

        PATH = reverse(
            "base:planer_initial_detail", args=[own_outline.pk, foreign_target.pk]
        )

        self.login_me()
        response = self.client.get(PATH)
        assert response.status_code == 404

    def test_planer_initial_detail___200_proper_response(self):
        outline = self.get_outline(test_world=True, written="active")
        self.create_target_on_test_world(outline)
        target = TargetVertex.objects.get(target="200|200")
        PATH = reverse("base:planer_initial_detail", args=[outline.pk, target.pk])
        self.login_me()
        response = self.client.get(PATH)
        assert response.status_code == 200

    def test_planer_initial_detail___200_malformed_filtr_values(self):
        outline = self.get_outline(test_world=True, written="active")
        self.create_target_on_test_world(outline)
        target = TargetVertex.objects.get(target="200|200")
        path = reverse("base:planer_initial_detail", args=[outline.pk, target.pk])
        self.login_me()

        for filtr in ["command", "command>", "command>abc", "||||", "<>"]:
            response = self.client.get(path + f"?filtr={filtr}")
            assert response.status_code == 200

    def test_planer_initial_detail___302_main_form_handling(self):
        outline = self.get_outline(test_world=True, written="active")
        self.create_target_on_test_world(outline)
        target = TargetVertex.objects.get(target="200|200")
        weight_max = self.create_weight_maximum(outline=outline)
        weight_max.catapult_left = 100
        weight_max.catapult_state = 100
        weight_max.catapult_max = 200
        weight_max.nobleman_left = 1
        weight_max.nobleman_state = 1
        weight_max.nobleman_max = 2
        weight_max.off_left = 2000
        weight_max.off_state = 1000
        weight_max.off_max = 3000
        weight_max.save()
        weight1 = self.create_weight(target=target, weight_max=weight_max)
        weight1.off = 100
        weight1.catapult = 10
        weight1.nobleman = 1
        weight1.save()
        PATH = reverse("base:planer_initial_detail", args=[outline.pk, target.pk])
        self.login_me()
        response = self.client.post(
            PATH,
            data={
                "form": "",
                "weight_id": weight1.pk,
                "off_no_catapult": "200",
                "deff": "0",
                "catapult": "20",
                "nobleman": "2",
            },
        )
        assert response.status_code == 302
        weight1.refresh_from_db()
        weight_max.refresh_from_db()
        assert weight1.off == 360
        assert weight1.nobleman == 2
        assert weight1.catapult == 20

        assert weight_max.off_left == 1740
        assert weight_max.off_state == 1260

        assert weight_max.catapult_left == 90
        assert weight_max.catapult_state == 110

        assert weight_max.nobleman_left == 0
        assert weight_max.nobleman_state == 2

    def test_planer_initial_detail___302_main_form_handling_for_deff_wave(self):
        outline = self.get_outline(test_world=True, written="active")
        self.create_target_on_test_world(outline)
        target = TargetVertex.objects.get(target="200|200")
        weight_max = self.create_weight_maximum(outline=outline)
        weight_max.deff_left = 600
        weight_max.deff_state = 400
        weight_max.deff_max = 1000
        weight_max.nobleman_left = 1
        weight_max.nobleman_state = 1
        weight_max.nobleman_max = 2
        weight_max.off_left = 0
        weight_max.off_state = 0
        weight_max.off_max = 0
        weight_max.catapult_left = 0
        weight_max.catapult_state = 0
        weight_max.catapult_max = 0
        weight_max.save()
        weight1 = self.create_weight(target=target, weight_max=weight_max)
        weight1.off = 0
        weight1.deff = 400
        weight1.catapult = 0
        weight1.nobleman = 1
        weight1.save()
        path = reverse("base:planer_initial_detail", args=[outline.pk, target.pk])
        self.login_me()
        response = self.client.post(
            path,
            data={
                "form": "",
                "weight_id": weight1.pk,
                "off_no_catapult": "0",
                "deff": "550",
                "catapult": "0",
                "nobleman": "2",
            },
        )
        assert response.status_code == 302
        weight1.refresh_from_db()
        weight_max.refresh_from_db()
        assert weight1.off == 0
        assert weight1.deff == 550
        assert weight1.nobleman == 2
        assert weight1.catapult == 0

        assert weight_max.deff_left == 450
        assert weight_max.deff_state == 550
        assert weight_max.nobleman_left == 0
        assert weight_max.nobleman_state == 2

    def test_planer_initial_detail___200_deff_wave_hides_divide_and_keeps_edit(self):
        outline = self.get_outline(test_world=True, written="active")
        self.create_target_on_test_world(outline)
        target = TargetVertex.objects.get(target="200|200", outline=outline)
        state = self.create_weight_maximum(outline=outline, start="148|148")
        deff_wave = self.create_weight(target=target, weight_max=state, start="148|148")
        deff_wave.off = 0
        deff_wave.deff = 15001
        deff_wave.nobleman = 1
        deff_wave.order = 1
        deff_wave.save(update_fields=["off", "deff", "nobleman", "order"])

        path = reverse("base:planer_initial_detail", args=[outline.pk, target.pk])
        self.login_me()
        response = self.client.get(path + "?filtr=148")

        assert response.status_code == 200
        content = response.content.decode()
        assert 'data-deff="15001"' in content
        assert 'data-leftdeff="0"' in content
        assert (
            reverse(
                "base:planer_divide",
                args=[outline.pk, target.pk, deff_wave.pk, 2],
            )
            not in content
        )

    def test_planer_initial_detail___404_weight_to_edit_must_match_target(self):
        outline = self.get_outline(test_world=True, written="active")
        self.create_target_on_test_world(outline)
        target = TargetVertex.objects.get(target="200|200", outline=outline)

        own_weight_max = self.create_weight_maximum(outline=outline)
        self.create_weight(target=target, weight_max=own_weight_max)

        foreign_outline = self.create_foreign_outline(test_world=True, written="active")
        self.create_target_on_test_world(foreign_outline)
        foreign_target = TargetVertex.objects.get(
            target="200|200", outline=foreign_outline
        )
        foreign_weight_max = self.create_weight_maximum(foreign_outline)
        foreign_weight = self.create_weight(
            target=foreign_target,
            weight_max=foreign_weight_max,
        )

        PATH = reverse("base:planer_initial_detail", args=[outline.pk, target.pk])
        self.login_me()
        response = self.client.post(
            PATH,
            data={
                "form": "",
                "weight_id": foreign_weight.pk,
                "off_no_catapult": "200",
                "deff": "0",
                "catapult": "20",
                "nobleman": "1",
            },
        )
        assert response.status_code == 404

    def test_planer_initial_detail___200_deff_target_uses_role_based_candidates(self):
        outline = self.get_outline(test_world=True, written="active")
        outline.filter_weights_min = 1000
        outline.filter_weights_max = 30000
        outline.filter_weights_deff_min = 10000
        outline.filter_weights_deff_max = 30000
        outline.filter_weights_nobles_min = 1
        outline.save(
            update_fields=[
                "filter_weights_min",
                "filter_weights_max",
                "filter_weights_deff_min",
                "filter_weights_deff_max",
                "filter_weights_nobles_min",
            ]
        )
        self.create_target_on_test_world(outline)
        target = TargetVertex.objects.get(target="200|200", outline=outline)
        target.has_deff_noble = True
        target.deff_noble_order = 4
        target.save(update_fields=["has_deff_noble", "deff_noble_order"])

        pure_deff = WeightMaximum.objects.create(
            outline=outline,
            start="148|148",
            player="deff-player",
            off_max=0,
            off_left=0,
            nobleman_max=4,
            nobleman_left=4,
            nobleman_state=0,
            deff_max=15000,
            deff_left=15000,
            deff_state=0,
            catapult_max=0,
            catapult_left=0,
            catapult_state=0,
            ram_max=0,
            ram_left=0,
            ram_state=0,
            x_coord=148,
            y_coord=148,
            village_id=148148,
            player_id=1,
            first_line=False,
            too_far_away=False,
            hidden=False,
            points=0,
        )
        off_with_small_deff = WeightMaximum.objects.create(
            outline=outline,
            start="120|120",
            player="off-player",
            off_max=18000,
            off_left=18000,
            nobleman_max=4,
            nobleman_left=4,
            nobleman_state=0,
            deff_max=200,
            deff_left=200,
            deff_state=0,
            catapult_max=100,
            catapult_left=100,
            catapult_state=0,
            ram_max=0,
            ram_left=0,
            ram_state=0,
            x_coord=120,
            y_coord=120,
            village_id=120120,
            player_id=2,
            first_line=False,
            too_far_away=False,
            hidden=False,
            points=0,
        )

        path = reverse("base:planer_initial_detail", args=[outline.pk, target.pk])
        self.login_me()
        response = self.client.get(path)

        assert response.status_code == 200
        page_items = list(response.context["page_obj"].object_list)
        roles = {item.start: item.candidate_role for item in page_items}
        assert roles[pure_deff.start] == "deff"
        assert roles[off_with_small_deff.start] == "off"
        content = response.content.decode()
        assert pure_deff.start in content
        assert off_with_small_deff.start in content
        assert (
            reverse(
                "base:planer_add_first_deff_noble",
                args=[outline.pk, target.pk, pure_deff.pk],
            )
            in content
        )
        assert (
            reverse(
                "base:planer_add_first_off",
                args=[outline.pk, target.pk, pure_deff.pk],
            )
            not in content
        )

    def test_planer_initial_detail___200_displays_existing_deff_noble_wave_as_deff(
        self,
    ):
        outline = self.get_outline(test_world=True, written="active")
        self.create_target_on_test_world(outline)
        target = TargetVertex.objects.get(target="200|200", outline=outline)
        target.has_deff_noble = True
        target.deff_noble_order = 1
        target.save(update_fields=["has_deff_noble", "deff_noble_order"])

        state = self.create_weight_maximum(outline=outline, start="148|148")
        deff_wave = self.create_weight(target=target, weight_max=state, start="148|148")
        deff_wave.off = 0
        deff_wave.deff = 15001
        deff_wave.nobleman = 0
        deff_wave.order = 1
        deff_wave.player = "deff-player"
        deff_wave.save(update_fields=["off", "deff", "nobleman", "order", "player"])

        path = reverse("base:planer_initial_detail", args=[outline.pk, target.pk])
        self.login_me()
        response = self.client.get(path + "?filtr=148")

        assert response.status_code == 200
        result_items = list(response.context["result_lst"])
        stored_wave = next(item for item in result_items if item.pk == deff_wave.pk)
        assert stored_wave.is_deff_wave is True
        content = response.content.decode()
        assert deff_wave.start in content
        assert "15001" in content

    def test_planer_initial_detail___200_keeps_deff_role_candidates_after_deff_noble_exists(
        self,
    ):
        outline = self.get_outline(test_world=True, written="active")
        outline.filter_weights_min = 1000
        outline.filter_weights_max = 30000
        outline.filter_weights_deff_min = 10000
        outline.filter_weights_deff_max = 30000
        outline.filter_weights_nobles_min = 1
        outline.save(
            update_fields=[
                "filter_weights_min",
                "filter_weights_max",
                "filter_weights_deff_min",
                "filter_weights_deff_max",
                "filter_weights_nobles_min",
            ]
        )
        self.create_target_on_test_world(outline)
        target = TargetVertex.objects.get(target="200|200", outline=outline)
        target.has_deff_noble = True
        target.deff_noble_order = 1
        target.save(update_fields=["has_deff_noble", "deff_noble_order"])

        existing_deff_state = self.create_weight_maximum(
            outline=outline, start="147|147"
        )
        existing_deff_wave = self.create_weight(
            target=target,
            weight_max=existing_deff_state,
            start="147|147",
        )
        existing_deff_wave.off = 0
        existing_deff_wave.deff = 14000
        existing_deff_wave.nobleman = 1
        existing_deff_wave.order = 1
        existing_deff_wave.save(update_fields=["off", "deff", "nobleman", "order"])

        pure_deff = WeightMaximum.objects.create(
            outline=outline,
            start="148|148",
            player="deff-player",
            off_max=0,
            off_left=0,
            nobleman_max=4,
            nobleman_left=4,
            nobleman_state=0,
            deff_max=15000,
            deff_left=15000,
            deff_state=0,
            catapult_max=0,
            catapult_left=0,
            catapult_state=0,
            ram_max=0,
            ram_left=0,
            ram_state=0,
            x_coord=148,
            y_coord=148,
            village_id=148148,
            player_id=1,
            first_line=False,
            too_far_away=False,
            hidden=False,
            points=0,
        )

        path = reverse("base:planer_initial_detail", args=[outline.pk, target.pk])
        self.login_me()
        response = self.client.get(path + "?filtr=148")

        assert response.status_code == 200
        page_items = list(response.context["page_obj"].object_list)
        starts = {item.start for item in page_items}
        assert pure_deff.start not in starts
        content = response.content.decode()
        assert "15000" not in content
        assert (
            reverse(
                "base:planer_add_first_off",
                args=[outline.pk, target.pk, pure_deff.pk],
            )
            not in content
        )
        assert (
            reverse(
                "base:planer_add_first",
                args=[outline.pk, target.pk, pure_deff.pk],
            )
            not in content
        )

    def test_planer_initial_detail___200_hides_off_role_village_when_only_deff_filter_matches(
        self,
    ):
        outline = self.get_outline(test_world=True, written="active")
        outline.filter_weights_min = 19000
        outline.filter_weights_max = 30000
        outline.filter_weights_deff_min = 100
        outline.filter_weights_deff_max = 30000
        outline.filter_weights_nobles_min = 1
        outline.save(
            update_fields=[
                "filter_weights_min",
                "filter_weights_max",
                "filter_weights_deff_min",
                "filter_weights_deff_max",
                "filter_weights_nobles_min",
            ]
        )
        self.create_target_on_test_world(outline)
        target = TargetVertex.objects.get(target="200|200", outline=outline)
        target.has_deff_noble = True
        target.deff_noble_order = 4
        target.save(update_fields=["has_deff_noble", "deff_noble_order"])

        off_with_small_deff = WeightMaximum.objects.create(
            outline=outline,
            start="120|120",
            player="off-player",
            off_max=18000,
            off_left=18000,
            nobleman_max=4,
            nobleman_left=4,
            nobleman_state=0,
            deff_max=200,
            deff_left=200,
            deff_state=0,
            catapult_max=100,
            catapult_left=100,
            catapult_state=0,
            ram_max=0,
            ram_left=0,
            ram_state=0,
            x_coord=120,
            y_coord=120,
            village_id=120120,
            player_id=2,
            first_line=False,
            too_far_away=False,
            hidden=False,
            points=0,
        )

        pure_deff = WeightMaximum.objects.create(
            outline=outline,
            start="148|148",
            player="deff-player",
            off_max=0,
            off_left=0,
            nobleman_max=4,
            nobleman_left=4,
            nobleman_state=0,
            deff_max=15600,
            deff_left=15600,
            deff_state=0,
            catapult_max=0,
            catapult_left=0,
            catapult_state=0,
            ram_max=0,
            ram_left=0,
            ram_state=0,
            x_coord=148,
            y_coord=148,
            village_id=148148,
            player_id=1,
            first_line=False,
            too_far_away=False,
            hidden=False,
            points=0,
        )

        path = reverse("base:planer_initial_detail", args=[outline.pk, target.pk])
        self.login_me()
        response = self.client.get(path)

        assert response.status_code == 200
        page_items = list(response.context["page_obj"].object_list)
        starts = {item.start for item in page_items}
        assert pure_deff.start in starts
        assert off_with_small_deff.start not in starts

    def test_planer_initial_detail___200_hides_off_based_village_when_only_deff_left_remains(
        self,
    ):
        outline = self.get_outline(test_world=True, written="active")
        outline.filter_weights_min = 1000
        outline.filter_weights_max = 30000
        outline.filter_weights_deff_min = 100
        outline.filter_weights_deff_max = 30000
        outline.filter_weights_nobles_min = 1
        outline.save(
            update_fields=[
                "filter_weights_min",
                "filter_weights_max",
                "filter_weights_deff_min",
                "filter_weights_deff_max",
                "filter_weights_nobles_min",
            ]
        )
        self.create_target_on_test_world(outline)
        target = TargetVertex.objects.get(target="200|200", outline=outline)
        target.has_deff_noble = True
        target.deff_noble_order = 4
        target.save(update_fields=["has_deff_noble", "deff_noble_order"])

        off_based_with_only_deff_left = WeightMaximum.objects.create(
            outline=outline,
            start="145|145",
            player="AllyPlayer4",
            off_max=7045,
            off_left=0,
            nobleman_max=4,
            nobleman_left=4,
            nobleman_state=0,
            deff_max=2845,
            deff_left=200,
            deff_state=2645,
            catapult_max=0,
            catapult_left=0,
            catapult_state=0,
            ram_max=0,
            ram_left=0,
            ram_state=0,
            x_coord=145,
            y_coord=145,
            village_id=145145,
            player_id=4,
            first_line=False,
            too_far_away=False,
            hidden=False,
            points=0,
        )

        path = reverse("base:planer_initial_detail", args=[outline.pk, target.pk])
        self.login_me()
        response = self.client.get(path + "?filtr=145")

        assert response.status_code == 200
        page_items = list(response.context["page_obj"].object_list)
        starts = {item.start for item in page_items}
        assert off_based_with_only_deff_left.start not in starts
