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
from django.utils import timezone

from base import forms
from base.models import TargetVertex, WeightMaximum
from base.tests.test_utils.mini_setup import MiniSetup


class InitialForm(MiniSetup):
    def test_planer_initial_form___302_not_auth_redirect_login(self):
        outline = self.get_outline()
        PATH = reverse("base:planer_initial_form", args=[outline.pk])

        response = self.client.get(PATH)
        assert response.status_code == 302
        assert response.url == self.login_page_path(next=PATH)

    def test_planer_initial_form___404_foreign_user_no_access(self):
        outline = self.get_outline()
        PATH = reverse("base:planer_initial_form", args=[outline.pk])

        self.login_foreign_user()
        response = self.client.get(PATH)
        assert response.status_code == 404

        response = self.client.post(PATH)
        assert response.status_code == 404

    def test_planer_initial_form___302_redirect_when_off_troops_empty(self):
        outline = self.get_outline()
        PATH = reverse("base:planer_initial_form", args=[outline.pk])
        REDIRECT = reverse("base:planer_detail", args=[outline.pk])
        self.login_me()
        response = self.client.get(PATH)
        assert response.status_code == 302
        assert response.url == REDIRECT

    def test_planer_initial_form___302_redirect_when_invalid_off_troops(self):
        outline = self.get_outline()
        outline.off_troops = self.random_lower_string()
        outline.save()
        PATH = reverse("base:planer_initial_form", args=[outline.pk])
        REDIRECT = reverse("base:planer_detail", args=[outline.pk])

        self.login_me()
        response = self.client.get(PATH)
        assert response.status_code == 302
        assert response.url == REDIRECT

    def test_planer_initial_form___302_redirect_when_written(self):
        outline = self.get_outline(written="active")
        outline.off_troops = self.random_lower_string()
        outline.save()
        PATH = reverse("base:planer_initial_form", args=[outline.pk])
        REDIRECT = reverse("base:planer_initial", args=[outline.pk])

        self.login_me()
        response = self.client.get(PATH)
        assert response.status_code == 302
        assert response.url == REDIRECT

    def test_planer_initial_form___200_off_troops_correct_and_creating_weights_and_mode_always_correct(
        self,
    ):
        outline = self.get_outline(test_world=True)
        outline.off_troops = "102|102,100,100,7002,0,100,2802,0,0,350,100,0,0,0,0,0,"
        outline.save()
        PATH = reverse("base:planer_initial_form", args=[outline.pk])

        self.login_me()
        response = self.client.get(PATH)
        assert response.status_code == 200
        assert (
            WeightMaximum.objects.filter(outline=outline, start="102|102").count() == 1
        )
        assert response.context.get("premium_error") is False
        assert response.context.get("real_dups") == []
        assert response.context.get("fake_dups") == []
        assert response.context.get("ruin_dups") == []
        assert response.context.get("len_real") == 0
        assert response.context.get("len_fake") == 0
        assert response.context.get("len_ruin") == 0
        assert response.context.get("estimated_time") == 0
        assert response.context.get("mode") == "real"
        response = self.client.get(PATH + "?t=fake")
        assert response.status_code == 200
        assert response.context.get("mode") == "fake"
        response = self.client.get(PATH + "?t=ruin")
        assert response.status_code == 200
        assert response.context.get("mode") == "ruin"

        session = self.client.session
        session["premium_error"] = True
        session.save()
        response = self.client.get(PATH)
        assert response.context.get("premium_error") is True

    def test_planer_initial_form___200_show_lens_and_duplicates_correct(self):
        outline = self.get_outline(test_world=True)
        outline.off_troops = "102|102,100,100,7002,0,100,2802,0,0,350,100,0,0,0,0,0,"
        outline.save()
        PATH = reverse("base:planer_initial_form", args=[outline.pk])
        self.create_target_on_test_world(outline=outline)
        self.create_target_on_test_world(outline=outline, fake=True)
        self.create_target_on_test_world(outline=outline, fake=True)
        self.create_target_on_test_world(outline=outline, ruin=True)
        self.create_target_on_test_world(outline=outline, ruin=True)
        self.create_target_on_test_world(outline=outline, ruin=True)
        self.create_target_on_test_world(outline=outline, ruin=True)

        self.login_me()
        response = self.client.get(PATH)
        assert response.status_code == 200
        assert response.context.get("premium_error") is False
        assert response.context.get("real_dups") == []
        assert response.context.get("fake_dups") == [
            {"target": "200|200", "duplicate": 2, "lines": "1,2"}
        ]
        assert response.context.get("ruin_dups") == [
            {"target": "200|200", "duplicate": 4, "lines": "1,2,3,..."}
        ]
        assert response.context.get("len_real") == 1
        assert response.context.get("len_fake") == 2
        assert response.context.get("len_ruin") == 4
        assert response.context.get("estimated_time") == 236
        assert response.context.get("mode") == "real"

    def test_planer_initial_form___200_initial_values_for_forms_works_well_1(self):
        # form1
        initial_outline_targets = self.random_lower_string()
        initial_outline_fakes = self.random_lower_string()
        initial_outline_ruins = self.random_lower_string()
        # form2
        initial_outline_front_dist = self.random_integer()
        initial_outline_maximum_front_dist = self.random_integer()
        initial_outline_target_dist = self.random_integer()
        initial_outline_min_off = self.random_integer()
        initial_outline_excluded_coords = self.random_lower_string()
        # form3
        date = ""
        # form4
        mode_off = "far"
        mode_noble = "far"
        mode_division = "separatly"
        mode_guide = "single"
        mode_split = "together"
        initial_outline_fake_limit = self.random_integer(maximum=15)
        initial_outline_fake_mode = "all"
        # form 5
        night_bonus = True
        enter_t1 = self.random_integer(0, 10)
        enter_t2 = self.random_integer(10, 20)
        # form6
        initial_outline_off_left_catapult = 200
        initial_outline_catapult_default = 300
        initial_outline_average_ruining_points = "medium"

        # outline
        outline = self.get_outline(test_world=True)
        outline.off_troops = "102|102,100,100,7002,0,100,2802,0,0,350,100,0,0,0,0,0,"
        outline.initial_outline_targets = initial_outline_targets
        outline.initial_outline_fakes = initial_outline_fakes
        outline.initial_outline_ruins = initial_outline_ruins
        outline.initial_outline_front_dist = initial_outline_front_dist
        outline.initial_outline_maximum_front_dist = initial_outline_maximum_front_dist
        outline.initial_outline_target_dist = initial_outline_target_dist
        outline.initial_outline_min_off = initial_outline_min_off
        outline.initial_outline_excluded_coords = initial_outline_excluded_coords
        outline.mode_off = mode_off
        outline.mode_noble = mode_noble
        outline.mode_division = mode_division
        outline.mode_guide = mode_guide
        outline.mode_split = mode_split
        outline.initial_outline_fake_limit = initial_outline_fake_limit
        outline.initial_outline_fake_mode = initial_outline_fake_mode
        outline.night_bonus = night_bonus
        outline.enter_t1 = enter_t1
        outline.enter_t2 = enter_t2
        outline.initial_outline_off_left_catapult = initial_outline_off_left_catapult
        outline.initial_outline_catapult_default = initial_outline_catapult_default
        outline.initial_outline_average_ruining_points = (
            initial_outline_average_ruining_points
        )
        outline.save()
        PATH = reverse("base:planer_initial_form", args=[outline.pk])

        self.login_me()
        response = self.client.get(PATH)
        assert response.status_code == 200
        form1: forms.InitialOutlineForm = response.context["form1"]
        form2: forms.AvailableTroopsForm = response.context["form2"]
        form3: forms.SettingDateForm = response.context["form3"]
        form4: forms.ModeOutlineForm = response.context["form4"]
        form5: forms.NightBonusSetForm = response.context["form5"]
        form6: forms.RuiningOutlineForm = response.context["form6"]
        assert form1["target"].initial == initial_outline_targets

        assert form2["initial_outline_front_dist"].initial == initial_outline_front_dist
        assert (
            form2["initial_outline_maximum_front_dist"].initial
            == initial_outline_maximum_front_dist
        )
        assert (
            form2["initial_outline_target_dist"].initial == initial_outline_target_dist
        )
        assert form2["initial_outline_min_off"].initial == initial_outline_min_off
        assert (
            form2["initial_outline_excluded_coords"].initial
            == initial_outline_excluded_coords
        )

        assert form3["date"].initial == date

        assert form4["mode_off"].initial == mode_off
        assert form4["mode_noble"].initial == mode_noble
        assert form4["mode_division"].initial == mode_division
        assert form4["mode_guide"].initial == mode_guide
        assert form4["mode_split"].initial == mode_split
        assert form4["initial_outline_fake_limit"].initial == initial_outline_fake_limit
        assert form4["initial_outline_fake_mode"].initial == initial_outline_fake_mode

        assert form5["night_bonus"].initial == night_bonus
        assert form5["enter_t1"].initial == enter_t1
        assert form5["enter_t2"].initial == enter_t2

        assert (
            form6["initial_outline_off_left_catapult"].initial
            == initial_outline_off_left_catapult
        )
        assert (
            form6["initial_outline_catapult_default"].initial
            == initial_outline_catapult_default
        )
        assert (
            form6["initial_outline_average_ruining_points"].initial
            == initial_outline_average_ruining_points
        )

        response = self.client.get(PATH + "?t=fake")
        assert response.status_code == 200
        form1: forms.InitialOutlineForm = response.context["form1"]
        assert form1["target"].initial == initial_outline_fakes

        response = self.client.get(PATH + "?t=ruin")
        assert response.status_code == 200
        form1: forms.InitialOutlineForm = response.context["form1"]
        assert form1["target"].initial == initial_outline_ruins

    def test_planer_initial_form___200_initial_values_for_forms_works_well_2(self):
        # form1
        initial_outline_targets = self.random_lower_string()
        initial_outline_fakes = self.random_lower_string()
        initial_outline_ruins = self.random_lower_string()
        # form2
        initial_outline_front_dist = self.random_integer()
        initial_outline_maximum_front_dist = self.random_integer()
        initial_outline_target_dist = self.random_integer()
        initial_outline_min_off = self.random_integer()
        initial_outline_excluded_coords = self.random_lower_string()
        # form3
        date = ""
        # form4
        mode_off = "closest"
        mode_noble = "random"
        mode_division = "not_divide"
        mode_guide = "many"
        mode_split = "split"
        initial_outline_fake_limit = self.random_integer(maximum=15)
        initial_outline_fake_mode = "off"
        # form 5
        night_bonus = False
        enter_t1 = self.random_integer(0, 10)
        enter_t2 = self.random_integer(10, 20)
        # form6
        initial_outline_off_left_catapult = 75
        initial_outline_catapult_default = 99
        initial_outline_average_ruining_points = "big"

        # outline
        outline = self.get_outline(test_world=True)
        outline.off_troops = "102|102,100,100,7002,0,100,2802,0,0,350,100,0,0,0,0,0,"
        outline.initial_outline_targets = initial_outline_targets
        outline.initial_outline_fakes = initial_outline_fakes
        outline.initial_outline_ruins = initial_outline_ruins
        outline.initial_outline_front_dist = initial_outline_front_dist
        outline.initial_outline_maximum_front_dist = initial_outline_maximum_front_dist
        outline.initial_outline_target_dist = initial_outline_target_dist
        outline.initial_outline_min_off = initial_outline_min_off
        outline.initial_outline_excluded_coords = initial_outline_excluded_coords
        outline.mode_off = mode_off
        outline.mode_noble = mode_noble
        outline.mode_division = mode_division
        outline.mode_guide = mode_guide
        outline.mode_split = mode_split
        outline.initial_outline_fake_limit = initial_outline_fake_limit
        outline.initial_outline_fake_mode = initial_outline_fake_mode
        outline.night_bonus = night_bonus
        outline.enter_t1 = enter_t1
        outline.enter_t2 = enter_t2
        outline.initial_outline_off_left_catapult = initial_outline_off_left_catapult
        outline.initial_outline_catapult_default = initial_outline_catapult_default
        outline.initial_outline_average_ruining_points = (
            initial_outline_average_ruining_points
        )
        outline.save()
        PATH = reverse("base:planer_initial_form", args=[outline.pk])

        self.login_me()
        response = self.client.get(PATH)
        assert response.status_code == 200
        form1: forms.InitialOutlineForm = response.context["form1"]
        form2: forms.AvailableTroopsForm = response.context["form2"]
        form3: forms.SettingDateForm = response.context["form3"]
        form4: forms.ModeOutlineForm = response.context["form4"]
        form5: forms.NightBonusSetForm = response.context["form5"]
        form6: forms.RuiningOutlineForm = response.context["form6"]
        assert form1["target"].initial == initial_outline_targets

        assert form2["initial_outline_front_dist"].initial == initial_outline_front_dist
        assert (
            form2["initial_outline_maximum_front_dist"].initial
            == initial_outline_maximum_front_dist
        )
        assert (
            form2["initial_outline_target_dist"].initial == initial_outline_target_dist
        )
        assert form2["initial_outline_min_off"].initial == initial_outline_min_off
        assert (
            form2["initial_outline_excluded_coords"].initial
            == initial_outline_excluded_coords
        )

        assert form3["date"].initial == date

        assert form4["mode_off"].initial == mode_off
        assert form4["mode_noble"].initial == mode_noble
        assert form4["mode_division"].initial == mode_division
        assert form4["mode_guide"].initial == mode_guide
        assert form4["mode_split"].initial == mode_split
        assert form4["initial_outline_fake_limit"].initial == initial_outline_fake_limit
        assert form4["initial_outline_fake_mode"].initial == initial_outline_fake_mode

        assert form5["night_bonus"].initial == night_bonus
        assert form5["enter_t1"].initial == enter_t1
        assert form5["enter_t2"].initial == enter_t2

        assert (
            form6["initial_outline_off_left_catapult"].initial
            == initial_outline_off_left_catapult
        )
        assert (
            form6["initial_outline_catapult_default"].initial
            == initial_outline_catapult_default
        )
        assert (
            form6["initial_outline_average_ruining_points"].initial
            == initial_outline_average_ruining_points
        )

        response = self.client.get(PATH + "?t=fake")
        assert response.status_code == 200
        form1: forms.InitialOutlineForm = response.context["form1"]
        assert form1["target"].initial == initial_outline_fakes

        response = self.client.get(PATH + "?t=ruin")
        assert response.status_code == 200
        form1: forms.InitialOutlineForm = response.context["form1"]
        assert form1["target"].initial == initial_outline_ruins

    def test_planer_initial_form___302_test_form1_real(self):
        outline = self.get_outline(test_world=True)
        outline.off_troops = "102|102,100,100,7002,0,100,2802,0,0,350,100,0,0,0,0,0,"
        outline.save()
        PATH = reverse("base:planer_initial_form", args=[outline.pk])
        self.login_me()

        # INVALID TRY 1
        response = self.client.post(
            PATH, data={"form1": "", "target": self.random_lower_string()}
        )
        assert response.status_code == 200
        form1: forms.InitialOutlineForm = response.context["form1"]
        assert len(form1.errors) == 1
        assert TargetVertex.objects.filter(fake=False, ruin=False).count() == 0

        # INVALID TRY 2
        outline.off_troops = self.random_lower_string()
        outline.save()

        response = self.client.post(PATH, data={"form1": "", "target": "200|200:0:0"})
        REDIRECT = reverse("base:planer_detail", args=[outline.pk])
        assert response.status_code == 302
        assert response.url == REDIRECT
        assert TargetVertex.objects.filter(fake=False, ruin=False).count() == 0

        outline.off_troops = "102|102,100,100,7002,0,100,2802,0,0,350,100,0,0,0,0,0,"
        outline.save()

        # VALID TRY 1
        response = self.client.post(
            PATH, data={"form1": "", "target": "200|200:0:0\r\n200|200:0:0"}
        )
        assert response.status_code == 302
        response = self.client.get(PATH)
        assert response.status_code == 200
        assert TargetVertex.objects.filter(fake=False, ruin=False).count() == 2
        TargetVertex.objects.all().delete()

    def test_planer_initial_form___302_test_form1_fake(self):
        outline = self.get_outline(test_world=True)
        outline.off_troops = "102|102,100,100,7002,0,100,2802,0,0,350,100,0,0,0,0,0,"
        outline.save()
        PATH = reverse("base:planer_initial_form", args=[outline.pk]) + "?t=fake"
        self.login_me()

        # INVALID TRY 1
        response = self.client.post(
            PATH, data={"form1": "", "target": self.random_lower_string()}
        )
        assert response.status_code == 200
        form1: forms.InitialOutlineForm = response.context["form1"]
        assert len(form1.errors) == 1
        assert TargetVertex.objects.filter(fake=True, ruin=False).count() == 0

        # INVALID TRY 2
        outline.off_troops = self.random_lower_string()
        outline.save()

        response = self.client.post(PATH, data={"form1": "", "target": "200|200:0:0"})
        REDIRECT = reverse("base:planer_detail", args=[outline.pk])
        assert response.status_code == 302
        assert response.url == REDIRECT
        assert TargetVertex.objects.filter(fake=True, ruin=False).count() == 0

        outline.off_troops = "102|102,100,100,7002,0,100,2802,0,0,350,100,0,0,0,0,0,"
        outline.save()

        # VALID TRY 1
        response = self.client.post(
            PATH, data={"form1": "", "target": "200|200:0:0\r\n200|200:0:0"}
        )
        assert response.status_code == 302
        response = self.client.get(PATH)
        assert response.status_code == 200
        assert TargetVertex.objects.filter(fake=True, ruin=False).count() == 2
        TargetVertex.objects.all().delete()

    def test_planer_initial_form___302_test_form1_ruin(self):
        outline = self.get_outline(test_world=True)
        outline.off_troops = "102|102,100,100,7002,0,100,2802,0,0,350,100,0,0,0,0,0,"
        outline.save()
        PATH = reverse("base:planer_initial_form", args=[outline.pk]) + "?t=ruin"
        self.login_me()

        # INVALID TRY 1
        response = self.client.post(
            PATH, data={"form1": "", "target": self.random_lower_string()}
        )
        assert response.status_code == 200
        form1: forms.InitialOutlineForm = response.context["form1"]
        assert len(form1.errors) == 1
        assert TargetVertex.objects.filter(fake=False, ruin=True).count() == 0

        # INVALID TRY 2
        outline.off_troops = self.random_lower_string()
        outline.save()

        response = self.client.post(PATH, data={"form1": "", "target": "200|200:0:0"})
        REDIRECT = reverse("base:planer_detail", args=[outline.pk])
        assert response.status_code == 302
        assert response.url == REDIRECT
        assert TargetVertex.objects.filter(fake=False, ruin=True).count() == 0

        outline.off_troops = "102|102,100,100,7002,0,100,2802,0,0,350,100,0,0,0,0,0,"
        outline.save()

        # VALID TRY 1
        response = self.client.post(
            PATH, data={"form1": "", "target": "200|200:0:0\r\n200|200:0:0"}
        )
        assert response.status_code == 302
        response = self.client.get(PATH)
        assert response.status_code == 200
        assert TargetVertex.objects.filter(fake=False, ruin=True).count() == 2
        TargetVertex.objects.all().delete()

    def test_planer_initial_form___302_test_form2(self):
        outline = self.get_outline(test_world=True)
        outline.off_troops = self.TEST_WORLD_DATA
        outline.save()
        self.create_target_on_test_world(outline)
        PATH = reverse("base:planer_initial_form", args=[outline.pk])
        self.login_me()

        response = self.client.post(
            PATH,
            data={
                "form2": "",
                "initial_outline_min_off": 15000,
                "initial_outline_front_dist": 90,
                "initial_outline_maximum_front_dist": 115,
                "initial_outline_target_dist": 100,
                "initial_outline_excluded_coords": "250|250 251|251",
            },
        )
        assert response.status_code == 302
        assert response.url == PATH + "?t=real"
        outline.refresh_from_db()
        assert outline.initial_outline_min_off == 15000
        assert outline.initial_outline_front_dist == 90
        assert outline.initial_outline_maximum_front_dist == 115
        assert outline.initial_outline_target_dist == 100
        assert outline.initial_outline_excluded_coords == "250|250 251|251"
        # also table is filled correctly
        assert outline.avaiable_offs == [50, 13, 18, 19]
        assert outline.avaiable_nobles == [60, 46, 14, 0]
        assert outline.avaiable_offs_near == [20, 13, 7, 0]
        assert outline.avaiable_nobles_near == [60, 46, 14, 0]
        assert outline.avaiable_ruins == 1850

        assert WeightMaximum.objects.filter(too_far_away=True).count() == 19
        assert WeightMaximum.objects.filter(first_line=True).count() == 13

    def test_planer_initial_form___302_test_form3(self):
        outline = self.get_outline(test_world=True)
        outline.off_troops = "102|102,100,100,7002,0,100,2802,0,0,350,100,0,0,0,0,0,"
        outline.save()

        PATH = reverse("base:planer_initial_form", args=[outline.pk])
        self.login_me()

        date = timezone.localdate()
        response = self.client.post(
            PATH,
            data={
                "form3": "",
                "date": date,
            },
        )
        assert response.status_code == 302
        assert response.url == PATH + "?t=real"
        outline.refresh_from_db()
        assert outline.date == date

    def test_planer_initial_form___302_test_form4(self):
        outline = self.get_outline(test_world=True)
        outline.off_troops = "102|102,100,100,7002,0,100,2802,0,0,350,100,0,0,0,0,0,"
        outline.save()
        self.create_target_on_test_world(outline)

        PATH = reverse("base:planer_initial_form", args=[outline.pk])
        self.login_me()

        mode_off = "far"
        mode_noble = "far"
        mode_division = "separatly"
        mode_guide = "single"
        mode_split = "together"
        initial_outline_fake_limit = self.random_integer(maximum=15)
        initial_outline_fake_mode = "all"

        response = self.client.post(
            PATH,
            data={
                "form4": "",
                "mode_off": mode_off,
                "mode_noble": mode_noble,
                "mode_division": mode_division,
                "mode_guide": mode_guide,
                "mode_split": mode_split,
                "initial_outline_fake_limit": initial_outline_fake_limit,
                "initial_outline_fake_mode": initial_outline_fake_mode,
            },
        )
        assert response.status_code == 302
        assert response.url == PATH + "?t=real"
        outline.refresh_from_db()
        assert outline.mode_off == mode_off
        assert outline.mode_noble == mode_noble
        assert outline.mode_division == mode_division
        assert outline.mode_guide == mode_guide
        assert outline.mode_split == mode_split
        assert outline.initial_outline_fake_limit == initial_outline_fake_limit
        assert outline.initial_outline_fake_mode == initial_outline_fake_mode

        target: TargetVertex = TargetVertex.objects.get(target="200|200")
        assert target.mode_off == mode_off
        assert target.mode_noble == mode_noble
        assert target.mode_division == mode_division
        assert target.mode_guide == mode_guide

        weight_max: WeightMaximum = WeightMaximum.objects.get(start="102|102")
        assert weight_max.fake_limit == initial_outline_fake_limit

    def test_planer_initial_form___200_test_form5(self):
        outline = self.get_outline(test_world=True)
        outline.off_troops = "102|102,100,100,7002,0,100,2802,0,0,350,100,0,0,0,0,0,"
        outline.save()
        self.create_target_on_test_world(outline)

        PATH = reverse("base:planer_initial_form", args=[outline.pk])
        self.login_me()

        night_bonus = "on"
        enter_t1 = self.random_integer(0, 10)
        enter_t2 = self.random_integer(10, 20)

        response = self.client.post(
            PATH,
            data={
                "form5": "",
                "night_bonus": night_bonus,
                "enter_t1": enter_t1,
                "enter_t2": enter_t2,
            },
        )
        assert response.status_code == 302
        assert response.url == PATH + "?t=real"
        outline.refresh_from_db()
        assert outline.night_bonus is True
        assert outline.enter_t1 == enter_t1
        assert outline.enter_t2 == enter_t2

    def test_planer_initial_form___200_test_form6(self):
        outline = self.get_outline(test_world=True)
        outline.off_troops = "102|102,100,100,7002,0,100,2802,0,0,350,100,0,0,0,0,0,"
        outline.save()
        self.create_target_on_test_world(outline)

        PATH = reverse("base:planer_initial_form", args=[outline.pk])
        self.login_me()

        initial_outline_off_left_catapult = 200
        initial_outline_catapult_default = 75
        initial_outline_average_ruining_points = "medium"

        response = self.client.post(
            PATH,
            data={
                "form6": "",
                "initial_outline_off_left_catapult": initial_outline_off_left_catapult,
                "initial_outline_catapult_default": initial_outline_catapult_default,
                "initial_outline_average_ruining_points": initial_outline_average_ruining_points,
            },
        )
        assert response.status_code == 302
        assert response.url == PATH + "?t=real"
        outline.refresh_from_db()
        assert (
            outline.initial_outline_off_left_catapult
            == initial_outline_off_left_catapult
        )
        assert (
            outline.initial_outline_catapult_default == initial_outline_catapult_default
        )
        assert (
            outline.initial_outline_average_ruining_points
            == initial_outline_average_ruining_points
        )
