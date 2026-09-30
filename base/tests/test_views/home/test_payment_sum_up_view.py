# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

from django.urls import reverse

from base.tests.test_utils.create_user import create_user
from base.tests.test_utils.mini_setup import MiniSetup


class PaymentSumUpView(MiniSetup):
    def test_payment_summary___302_not_auth_redirect_login(self):
        PATH = reverse("base:payment_summary")

        response = self.client.get(PATH)

        assert response.status_code == 302
        assert getattr(response, "url") == self.login_page_path(next=PATH)

    def test_payment_summary___404_foreign_user(self):
        self.login_foreign_user()
        PATH = reverse("base:payment_summary")

        response = self.client.get(PATH)
        assert response.status_code == 404

    def test_payment_summary___404_me(self):
        self.login_me()
        PATH = reverse("base:payment_summary")

        response = self.client.get(PATH)
        assert response.status_code == 404

    def test_payment_summary___404_superuser(self):
        username = "some_superuser"
        password = "password123"
        create_user(username, password, is_superuser=True)
        self.client.login(username=username, password=password)

        PATH = reverse("base:payment_summary")

        response = self.client.get(PATH)
        assert response.status_code == 404

    def test_payment_summary___200_superuser_and_admin(self):
        username = "admin"
        password = "password123"
        create_user(username, password, is_superuser=True)
        self.client.login(username=username, password=password)

        PATH = reverse("base:payment_summary")

        response = self.client.get(PATH)
        assert response.status_code == 200

    def test_payment_summary___302_post_superuser_and_admin(self):
        username = "admin"
        password = "password123"
        create_user(username, password, is_superuser=True)
        self.client.login(username=username, password=password)
        for _ in range(100):
            self.create_random_payment()

        PATH = reverse("base:payment_summary")

        response = self.client.post(PATH, {"form": ""})
        assert response.status_code == 302
