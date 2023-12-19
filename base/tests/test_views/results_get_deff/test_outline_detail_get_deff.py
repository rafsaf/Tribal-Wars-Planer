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

from base.tests.test_utils.mini_setup import MiniSetup


class OutlineDetailGetDeff(MiniSetup):
    def test_planer_detail_get_deff___302_not_auth_redirect_login(self):
        outline = self.get_outline()
        outline_time = self.create_outline_time(outline)
        PATH = reverse("base:planer_detail_get_deff", args=[outline_time.pk])

        response = self.client.get(PATH)
        assert response.status_code == 302
        response = self.client.post(PATH)
        assert response.status_code == 302
        assert getattr(response, "url") == self.login_page_path(next=PATH)

    def test_planer_detail_get_deff___404_foreign_user_no_access(self):
        outline = self.get_outline(add_result=True)
        PATH = reverse("base:planer_detail_get_deff", args=[outline.pk])

        self.login_foreign_user()
        response = self.client.get(PATH)
        assert response.status_code == 404

        response = self.client.post(PATH)
        assert response.status_code == 404

    def test_planer_detail_get_deff___404_when_result_not_exists(self):
        outline = self.get_outline()
        PATH = reverse("base:planer_detail_get_deff", args=[outline.pk])
        self.login_me()

        response = self.client.get(PATH)
        assert response.status_code == 404

    def test_planer_detail_get_deff___302_redirect_when_no_deff_or_off_troops(self):
        outline = self.get_outline(add_result=True)
        PATH = reverse("base:planer_detail_get_deff", args=[outline.pk])
        REDIRECT = reverse("base:planer_detail", args=[outline.pk])
        self.login_me()

        outline.deff_troops = ""
        outline.off_troops = self.random_lower_string()
        outline.save()

        response = self.client.get(PATH)
        assert response.status_code == 302
        assert getattr(response, "url") == REDIRECT

        outline.refresh_from_db()
        outline.deff_troops = self.random_lower_string()
        outline.off_troops = ""
        outline.save()

        response = self.client.get(PATH)
        assert response.status_code == 302
        assert getattr(response, "url") == REDIRECT

        outline.refresh_from_db()
        outline.deff_troops = self.random_lower_string()
        outline.off_troops = self.random_lower_string()
        outline.save()

        response = self.client.get(PATH)
        assert response.status_code == 200

    def test_planer_detail_get_deff___302_form_work_ok_data(self):
        outline = self.get_outline(test_world=True, add_result=True)
        PATH = reverse("base:planer_detail_get_deff", args=[outline.pk])
        REDIRECT_BAD = reverse("base:planer_detail", args=[outline.pk])
        REDIRECT_OK = (
            reverse("base:planer_detail_results", args=[outline.pk]) + "?tab=deff"
        )
        self.login_me()

        outline.off_troops = "102|102,100,100,7002,0,100,2802,0,0,350,100,0,0,0,0,0,"
        outline.deff_troops = (
            "100|100,w wiosce,100,100,7000,0,100,2800,0,0,350,100,0,0,0,0,"
        )
        outline.save()

        response = self.client.post(
            PATH, data={"form": "", "radius": 10, "excluded": "500|500"}
        )
        assert response.status_code == 302
        assert getattr(response, "url") == REDIRECT_OK

        response = self.client.post(
            PATH,
            data={"form": "", "radius": 10, "excluded": self.random_lower_string()},
        )
        assert response.status_code == 200

        outline.refresh_from_db()
        outline.off_troops = self.random_lower_string()
        outline.save()

        response = self.client.post(
            PATH,
            data={"form": "", "radius": 10, "excluded": ""},
        )
        assert response.status_code == 302
        assert getattr(response, "url") == REDIRECT_BAD
