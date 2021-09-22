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

from base.models import WeightMaximum
from base.tests.test_utils.mini_setup import MiniSetup


class UpdateOutlineTroops(MiniSetup):
    def test_planer_update_troops___302_not_auth_redirect_login(self):
        outline = self.get_outline()
        PATH = reverse("base:planer_update_troops", args=[outline.pk])

        response = self.client.get(PATH)
        assert response.status_code == 302
        response = self.client.post(PATH)
        assert response.status_code == 302
        assert response.url == self.login_page_path(next=PATH)

    def test_planer_update_troops___404_foreign_user_no_access(self):
        outline = self.get_outline()
        PATH = reverse("base:planer_update_troops", args=[outline.pk])

        self.login_foreign_user()
        response = self.client.get(PATH)
        assert response.status_code == 405

        response = self.client.post(PATH)
        assert response.status_code == 404

    def test_planer_update_troops___302_redirect_when_off_troops_invalid(self):
        outline = self.get_outline()
        outline.off_troops = self.random_lower_string()
        outline.save()

        PATH = reverse("base:planer_update_troops", args=[outline.pk])
        REDIRECT = reverse("base:planer_detail", args=[outline.pk])
        self.login_me()
        response = self.client.get(PATH)
        assert response.status_code == 405
        response = self.client.post(PATH)
        assert response.status_code == 302
        assert response.url == REDIRECT

    def test_planer_update_troops___302_redirect_when_off_troops_ok_and_is_ok(self):
        outline = self.get_outline(test_world=True)
        outline.off_troops = "102|102,100,100,7002,0,100,2802,0,0,350,100,0,0,0,0,0,"
        outline.avaiable_offs = [1, 2, 3, 4]
        outline.avaiable_offs_near = [1, 2, 3, 4]
        outline.avaiable_nobles = [4, 4, 4]
        outline.avaiable_nobles_near = [4, 4, 4]
        outline.avaiable_ruins = 1555
        outline.save()

        PATH = reverse("base:planer_update_troops", args=[outline.pk]) + "?t=fake"
        REDIRECT = reverse("base:planer_initial_form", args=[outline.pk]) + "?t=fake"

        self.login_me()
        response = self.client.get(REDIRECT)
        # this should create one weight_max from off_troops
        assert response.status_code == 200
        assert WeightMaximum.objects.count() == 1

        outline.refresh_from_db()
        outline.off_troops = self.TEST_WORLD_DATA
        outline.save()
        response = self.client.post(PATH)
        assert response.status_code == 302
        assert response.url == REDIRECT

        assert WeightMaximum.objects.count() == 50
        outline.refresh_from_db()
        assert outline.avaiable_offs == []
        assert outline.avaiable_offs_near == []
        assert outline.avaiable_nobles == []
        assert outline.avaiable_nobles_near == []
        assert outline.avaiable_ruins is None
