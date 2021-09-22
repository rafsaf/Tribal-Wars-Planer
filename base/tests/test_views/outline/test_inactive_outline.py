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


class InactiveOutline(MiniSetup):
    def test_planer_status___302_not_auth_redirect_login(self):
        outline = self.get_outline()
        PATH = reverse("base:planer_status", args=[outline.pk])

        response = self.client.get(PATH)
        assert response.status_code == 302
        assert response.url == self.login_page_path(next=PATH)

        response = self.client.post(PATH)
        assert response.status_code == 302
        assert response.url == self.login_page_path(next=PATH)

    def test_planer_status___404_foreign_user_no_access(self):
        outline = self.get_outline()
        PATH = reverse("base:planer_status", args=[outline.pk])

        self.login_foreign_user()
        response = self.client.get(PATH)
        assert response.status_code == 405

        response = self.client.post(PATH)
        assert response.status_code == 404

    def test_planer_status___302_auth_works_ok_status_active(self):
        outline = self.get_outline()
        outline.status = "active"
        outline.save()

        PATH = reverse("base:planer_status", args=[outline.pk])
        REDIRECT = reverse("base:planer")

        self.login_me()
        response = self.client.get(PATH)
        assert response.status_code == 405

        response = self.client.post(PATH)
        assert response.status_code == 302
        assert response.url == REDIRECT

        outline.refresh_from_db()
        assert outline.status == "inactive"

    def test_planer_status___302_auth_works_ok_status_inactive(self):
        outline = self.get_outline()
        outline.status = "inactive"
        outline.save()

        PATH = reverse("base:planer_status", args=[outline.pk])
        REDIRECT = reverse("base:planer_all")

        self.login_me()
        response = self.client.get(PATH)
        assert response.status_code == 405

        response = self.client.post(PATH)
        assert response.status_code == 302
        assert response.url == REDIRECT

        outline.refresh_from_db()
        assert outline.status == "active"
