# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

from django.urls import reverse

from base.tests.test_utils.mini_setup import MiniSetup


class PaymentDone(MiniSetup):
    def test_payment_done___302_not_auth_redirect_login(self):
        PATH = reverse("base:payment_done")

        response = self.client.get(PATH)
        assert response.status_code == 302
        assert getattr(response, "url") == self.login_page_path(next=PATH)

    def test_payment_done___200_foreign_user_works_ok(self):
        self.login_foreign_user()
        PATH = reverse("base:payment_done")

        response = self.client.get(PATH)
        assert response.status_code == 200

    def test_payment_done___200_auth_works_ok(self):
        PATH = reverse("base:payment_done")

        self.login_me()
        response = self.client.get(PATH)
        assert response.status_code == 200
