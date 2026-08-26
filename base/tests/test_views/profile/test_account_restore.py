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

from datetime import timedelta

from django.conf import settings
from django.core import signing
from django.test import override_settings
from django.urls import reverse
from django.utils import timezone

from base.models import Profile
from base.tests.test_utils.mini_setup import MiniSetup
from base.views import profile as profile_view


class OutlineProfileAccountRestore(MiniSetup):
    def test_account_restore___404_no_auth(self):
        PATH = reverse("base:account_restore")

        response = self.client.get(PATH)
        assert response.status_code == 404

    def test_account_restore___404_foreign_user(self):
        self.login_foreign_user()
        PATH = reverse("base:account_restore")

        response = self.client.get(PATH)
        assert response.status_code == 404

    def test_account_restore___404_auth(self):
        self.login_me()
        PATH = reverse("base:account_restore")

        response = self.client.get(PATH)
        assert response.status_code == 404

    def test_account_restore___404_invalid_token(self):
        self.me()
        PATH = reverse("base:account_restore") + "?token=abcdef"

        response = self.client.get(PATH)
        assert response.status_code == 404

    @override_settings(ACCOUNT_PERMANENT_REMOVAL_DAYS=7)
    def test_account_restore___404_different_signer(self):
        now = timezone.now()
        exp = now + timedelta(days=settings.ACCOUNT_PERMANENT_REMOVAL_DAYS)

        self.me()
        profile: Profile = self.me().profile  # type: ignore
        profile.deleted_at = now
        profile.deleted_at_exp = exp
        profile.save()

        token = signing.dumps(
            {
                "pk": self.me().pk,
                "iat": int(now.timestamp()),
                "exp": exp.timestamp(),
            },
            key="INVALID",
            salt=profile_view.PROFILE_SALT,
        )

        PATH = reverse("base:account_restore") + f"?token={token}"
        response = self.client.get(PATH)

        assert response.status_code == 404
        profile.refresh_from_db()
        assert profile.deleted_at == now
        assert profile.deleted_at_exp == exp

    def test_account_restore___200_valid_key_expired_exp(self):
        exp = timezone.now()
        now = exp - timedelta(days=settings.ACCOUNT_PERMANENT_REMOVAL_DAYS)

        self.me()
        profile: Profile = self.me().profile  # type: ignore
        profile.deleted_at = now
        profile.deleted_at_exp = exp
        profile.save()

        token = signing.dumps(
            {
                "pk": self.me().pk,
                "iat": int(now.timestamp()),
                "exp": exp.timestamp(),
            },
            salt=profile_view.PROFILE_SALT,
            compress=True,
        )
        PATH = reverse("base:account_restore") + f"?token={token}"
        response = self.client.get(PATH)

        assert response.status_code == 200
        profile.refresh_from_db()
        assert profile.deleted_at == now
        assert profile.deleted_at_exp == exp
        assert response.context["expired"]

    def test_account_restore___200_valid_key_expired_iat(self):
        now = timezone.now()
        exp = now + timedelta(days=settings.ACCOUNT_PERMANENT_REMOVAL_DAYS)

        self.me()
        profile: Profile = self.me().profile  # type: ignore
        profile.deleted_at = now - timedelta(minutes=5)
        profile.deleted_at_exp = exp - timedelta(minutes=5)
        profile.save()

        token = signing.dumps(
            {
                "pk": self.me().pk,
                "iat": int(now.timestamp()),
                "exp": exp.timestamp(),
            },
            salt=profile_view.PROFILE_SALT,
            compress=True,
        )
        PATH = reverse("base:account_restore") + f"?token={token}"
        response = self.client.get(PATH)

        assert response.status_code == 200
        profile.refresh_from_db()
        assert profile.deleted_at == now - timedelta(minutes=5)
        assert profile.deleted_at_exp == exp - timedelta(minutes=5)
        assert response.context["expired"]

    def test_account_restore___200_valid_key(self):
        now = timezone.now()
        exp = now + timedelta(days=settings.ACCOUNT_PERMANENT_REMOVAL_DAYS)

        self.me()
        profile: Profile = self.me().profile  # type: ignore
        profile.deleted_at = now
        profile.deleted_at_exp = exp
        profile.save()

        token = signing.dumps(
            {
                "pk": self.me().pk,
                "iat": int(now.timestamp()),
                "exp": exp.timestamp(),
            },
            salt=profile_view.PROFILE_SALT,
            compress=True,
        )
        PATH = reverse("base:account_restore") + f"?token={token}"
        response = self.client.get(PATH)

        assert response.status_code == 200
        profile.refresh_from_db()
        assert profile.deleted_at == now
        assert profile.deleted_at_exp == exp
        assert not response.context["expired"]
        assert response.context["recovery_user"].pk == self.me().pk

    def test_account_restore___200_valid_key_post_account_recovery(self):
        now = timezone.now()
        exp = now + timedelta(days=settings.ACCOUNT_PERMANENT_REMOVAL_DAYS)

        self.me()
        profile: Profile = self.me().profile  # type: ignore
        profile.deleted_at = now
        profile.deleted_at_exp = exp
        profile.save()

        token = signing.dumps(
            {
                "pk": self.me().pk,
                "iat": int(now.timestamp()),
                "exp": exp.timestamp(),
            },
            salt=profile_view.PROFILE_SALT,
            compress=True,
        )
        PATH = reverse("base:account_restore") + f"?token={token}"
        response = self.client.post(PATH, data={"form1": ""})

        assert response.status_code == 302
        assert getattr(response, "url") == reverse("base:base")
        profile.refresh_from_db()
        assert profile.deleted_at is None
        assert profile.deleted_at_exp is None
