from django.contrib.auth.models import User
from django.urls import reverse
from django_otp.oath import totp
from django_otp.plugins.otp_totp.models import TOTPDevice

from base.tests.test_utils.create_user import create_user
from base.tests.test_utils.mini_setup import MiniSetup


class TestLoginSecurity(MiniSetup):
    def _auth_payload(self, username: str, password: str) -> dict[str, str]:
        return {
            "login_view-current_step": "auth",
            "auth-username": username,
            "auth-password": password,
        }

    def _token_payload(self, token: str) -> dict[str, str]:
        return {
            "login_view-current_step": "token",
            "token-otp_token": token,
        }

    def test_login___password_and_other_email___not_authenticated(self):
        user = create_user("secure-user", "secure-pass")
        user.email = "owner@example.com"
        user.save(update_fields=["email"])

        path = reverse("two_factor:login")
        response = self.client.post(
            path,
            data=self._auth_payload(
                username="other@example.com", password="secure-pass"
            ),
        )

        assert response.status_code == 200
        assert "_auth_user_id" not in self.client.session

    def test_login___user_with_totp___password_only_not_enough(self):
        user = create_user("totp-user", "secure-pass")
        TOTPDevice.objects.create(user=user, name="default")

        path = reverse("two_factor:login")
        response = self.client.post(
            path,
            data=self._auth_payload(username="totp-user", password="secure-pass"),
        )

        assert response.status_code == 200
        assert "_auth_user_id" not in self.client.session
        assert b"token-otp_token" in response.content

    def test_login___user_with_totp___valid_token_authenticates(self):
        user: User = create_user("totp-user-ok", "secure-pass")
        device = TOTPDevice.objects.create(user=user, name="default")

        path = reverse("two_factor:login")
        response = self.client.post(
            path,
            data=self._auth_payload(username="totp-user-ok", password="secure-pass"),
        )

        assert response.status_code == 200
        assert "_auth_user_id" not in self.client.session

        otp_token = str(
            totp(
                device.bin_key,
                step=device.step,
                t0=device.t0,
                digits=device.digits,
                drift=device.drift,
            )
        ).zfill(device.digits)

        response2 = self.client.post(path, data=self._token_payload(otp_token))

        assert response2.status_code == 302
        assert self.client.session.get("_auth_user_id") == str(user.pk)

    def test_login___token_step_without_auth_step___not_authenticated(self):
        path = reverse("two_factor:login")

        response = self.client.post(path, data=self._token_payload("123456"))

        assert response.status_code == 200
        assert "_auth_user_id" not in self.client.session

    def test_login___token_step_with_forged_auth_fields___not_authenticated(self):
        user = create_user("forged-user", "secure-pass")
        TOTPDevice.objects.create(user=user, name="default")
        path = reverse("two_factor:login")

        payload = {
            "login_view-current_step": "token",
            "token-otp_token": "123456",
            "auth-username": "forged-user",
            "auth-password": "secure-pass",
        }
        response = self.client.post(path, data=payload)

        assert response.status_code == 200
        assert "_auth_user_id" not in self.client.session

    def test_login___unsafe_next_redirect___ignored(self):
        user = create_user("redirect-user", "secure-pass")
        path = reverse("two_factor:login") + "?next=https://evil.example/steal"

        response = self.client.post(
            path,
            data=self._auth_payload(username="redirect-user", password="secure-pass"),
        )

        assert response.status_code == 302
        assert getattr(response, "url") == reverse("base:base")
        assert self.client.session.get("_auth_user_id") == str(user.pk)
