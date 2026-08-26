# Copyright 2026 Rafał Safin (rafsaf). All Rights Reserved.
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

from django.contrib.auth.models import User
from django.urls import reverse

from base.tests.test_utils.create_user import create_user
from base.tests.test_utils.mini_setup import MiniSetup


class TestAdminSecurity(MiniSetup):
    def test_admin_index___unauthenticated___redirects_to_admin_login(self):
        path = reverse("admin:index")

        response = self.client.get(path)

        assert response.status_code == 302
        assert getattr(response, "url").startswith(reverse("admin:login"))
        assert "next=" in getattr(response, "url")

    def test_admin_index___non_staff_authenticated___redirects_to_admin_login(self):
        user = create_user("normal-user", "secure-pass")
        self.client.force_login(user)
        path = reverse("admin:index")

        response = self.client.get(path)

        assert response.status_code == 302
        assert getattr(response, "url").startswith(reverse("admin:login"))

    def test_admin_index___staff_without_otp_verification___redirects_to_admin_login(
        self,
    ):
        user: User = create_user("admin-user", "secure-pass")
        user.is_staff = True
        user.is_superuser = True
        user.save(update_fields=["is_staff", "is_superuser"])

        self.client.force_login(user)
        path = reverse("admin:index")

        response = self.client.get(path)

        assert response.status_code == 302
        assert getattr(response, "url").startswith(reverse("admin:login"))

    def test_admin_login___redirects_to_two_factor_login(self):
        path = reverse("admin:login") + "?next=/en/admin/"

        response = self.client.get(path)

        assert response.status_code == 302
        redirect_url = getattr(response, "url")
        assert redirect_url.startswith(reverse("two_factor:login"))
        assert "next=" in redirect_url

    def test_admin_login___unsafe_next___not_reflected(self):
        path = reverse("admin:login") + "?next=https://evil.example/admin"

        response = self.client.get(path)

        assert response.status_code == 302
        redirect_url = getattr(response, "url")
        assert redirect_url.startswith(reverse("two_factor:login"))
        assert "evil.example" not in redirect_url
