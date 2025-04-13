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

from base import forms
from base.models import TargetVertex
from base.tests.test_utils.mini_setup import MiniSetup
from utils import basic


class InitialPlaner(MiniSetup):
    def test_planer_initial___302_not_auth_redirect_login(self):
        outline = self.get_outline(written="active")
        PATH = reverse("base:planer_initial", args=[outline.pk])

        response = self.client.get(PATH)
        assert response.status_code == 302
        assert getattr(response, "url") == self.login_page_path(next=PATH)

        response = self.client.post(PATH)
        assert response.status_code == 302
        assert getattr(response, "url") == self.login_page_path(next=PATH)

    def test_planer_initial___404_foreign_user_no_access(self):
        outline = self.get_outline(written="active")
        PATH = reverse("base:planer_initial", args=[outline.pk])

        self.login_foreign_user()
        response = self.client.get(PATH)
        assert response.status_code == 404

        response = self.client.post(PATH)
        assert response.status_code == 404

    def test_planer_initial___404_when_not_written(self):
        outline = self.get_outline(written="inactive")
        PATH = reverse("base:planer_initial", args=[outline.pk])

        self.login_me()
        response = self.client.get(PATH)
        assert response.status_code == 404

        response = self.client.post(PATH)
        assert response.status_code == 404

    def test_planer_initial___200_filter_form_correct_initials(self):
        outline = self.get_outline(written="active")
        outline.filter_targets_number = 15
        outline.simple_textures = True
        outline.save()

        PATH = (
            reverse("base:planer_initial", args=[outline.pk])
            + "?mode=ruin&page=5&filtr=xxx"
        )

        self.login_me()
        response = self.client.get(PATH)
        assert response.status_code == 200
        filter_form: forms.SetTargetsMenuFilters = response.context["filter_form"]
        assert filter_form.fields["filter_targets_number"].initial == 15
        assert filter_form.fields["simple_textures"].initial is True

    def test_planer_initial___200_correct_GET_params(self):
        outline = self.get_outline(written="active")
        outline.save()
        self.login_me()

        PATH = reverse("base:planer_initial", args=[outline.pk])

        response_1 = self.client.get(PATH + "?mode=ruin&page=5&filtr=xxx")
        assert response_1.status_code == 200
        mode_1: basic.Mode = response_1.context["mode"]
        filtr_1: str = response_1.context["filtr"]
        assert mode_1.is_ruin
        assert filtr_1 == "xxx"

        response_2 = self.client.get(PATH + "?mode=time&page=5&filtr=yyy")
        assert response_2.status_code == 200
        mode_2: basic.Mode = response_2.context["mode"]
        filtr_2: str = response_2.context["filtr"]
        assert mode_2.is_time
        assert filtr_2 == "yyy"

        response_3 = self.client.get(PATH + "?mode=add_and_remove&page=5&filtr=yyy")
        assert response_3.status_code == 200
        mode_3: basic.Mode = response_3.context["mode"]
        filtr_3: str = response_3.context["filtr"]
        assert mode_3.is_add_and_remove
        assert filtr_3 == "yyy"

        response_4 = self.client.get(PATH + "?mode=menu&page=5&filtr=yyy")
        assert response_4.status_code == 200
        mode_4: basic.Mode = response_4.context["mode"]
        filtr_4: str = response_4.context["filtr"]
        assert mode_4.is_menu
        assert filtr_4 == "yyy"

        response_5 = self.client.get(PATH + "?mode=fake&page=5&filtr=yyy")
        assert response_5.status_code == 200
        mode_5: basic.Mode = response_5.context["mode"]
        filtr_5: str = response_5.context["filtr"]
        assert mode_5.is_fake
        assert filtr_5 == "yyy"

    def test_planer_initial___302_go_back_button(self):
        outline = self.get_outline(written="active", add_result=True)
        outline_time = self.create_outline_time(outline)
        outline.written = "active"
        outline.available_offs = [155, 5555, 1111, 100]
        outline.available_offs_near = [123, 123, 5, 0]
        outline.available_nobles = [1, 2, 3, 7]
        outline.available_nobles_near = [55, 33, 3, 5]
        outline.available_full_noble_offs = [55, 33, 3, 5]
        outline.available_catapults = [55, 33, 3, 5]
        outline.available_ruins = 6661
        outline.filter_weights_min = 150005
        outline.filter_weights_max = 150015
        outline.filter_card_number = 15
        outline.filter_targets_number = 8
        outline.filter_hide_front = "back"
        outline.choice_sort = "-distance"
        outline.default_off_time_id = outline_time.pk
        outline.default_fake_time_id = outline_time.pk
        outline.default_ruin_time_id = outline_time.pk
        outline.save()
        self.login_me()

        PATH = reverse("base:planer_initial", args=[outline.pk])
        REDIRECT = reverse("base:planer_initial_form", args=[outline.pk])

        response = self.client.post(PATH, data={"form1": ""})
        assert response.status_code == 302
        assert getattr(response, "url") == REDIRECT

        outline.refresh_from_db()
        assert outline.written == "inactive"
        assert outline.available_offs == []
        assert outline.available_offs_near == []
        assert outline.available_nobles == []
        assert outline.available_nobles_near == []
        assert outline.available_full_noble_offs == []
        assert outline.available_catapults == []
        assert outline.available_ruins is None
        assert outline.filter_weights_min == 0
        assert outline.filter_weights_max == 30000
        assert outline.filter_card_number == 15
        assert outline.filter_targets_number == 8
        assert outline.filter_hide_front == "all"
        assert outline.choice_sort == "distance"
        assert outline.default_off_time_id is None
        assert outline.default_fake_time_id is None
        assert outline.default_ruin_time_id is None

    def test_planer_initial___filter_form_works_ok(self):
        outline = self.get_outline(written="active")
        outline.filter_targets_number = 5
        outline.simple_textures = False
        outline.save()
        self.login_me()

        PATH = reverse("base:planer_initial", args=[outline.pk])

        response = self.client.post(
            PATH,
            data={
                "form-filter-targets": "",
                "filter_targets_number": 15,
                "simple_textures": "on",
            },
        )
        assert response.status_code == 302
        assert getattr(response, "url") == PATH + "?page=None&mode=menu&filtr="
        outline.refresh_from_db()
        assert outline.simple_textures is True
        assert outline.filter_targets_number == 15

    def test_planer_initial___create_form_works_ok(self):
        outline = self.get_outline(written="active", test_world=True)
        self.login_me()

        PATH = reverse("base:planer_initial", args=[outline.pk])

        response = self.client.post(
            PATH,
            data={
                "create": "",
                "target_type": "real",
                "target": "200|200",
            },
        )
        assert response.status_code == 302
        assert getattr(response, "url") == PATH + "?page=None&mode=menu&filtr="

        response = self.client.post(
            PATH,
            data={
                "create": "",
                "target_type": "fake",
                "target": "200|200",
            },
        )
        assert response.status_code == 302
        assert getattr(response, "url") == PATH + "?page=None&mode=menu&filtr="

        response = self.client.post(
            PATH,
            data={
                "create": "",
                "target_type": "ruin",
                "target": "200|200",
            },
        )
        assert response.status_code == 302
        assert getattr(response, "url") == PATH + "?page=None&mode=menu&filtr="

        assert TargetVertex.objects.filter(fake=False, ruin=False).count() == 1
        assert TargetVertex.objects.filter(fake=True, ruin=False).count() == 1
        assert TargetVertex.objects.filter(fake=False, ruin=True).count() == 1
