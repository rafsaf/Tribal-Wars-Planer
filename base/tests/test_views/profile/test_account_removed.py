# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

from django.urls import reverse

from base.tests.test_utils.mini_setup import MiniSetup


class OutlineProfileAccountRemoved(MiniSetup):
    def test_account_removed___200_no_auth_ok(self):
        PATH = reverse("base:account_removed")

        response = self.client.get(PATH)
        assert response.status_code == 200

    def test_account_removed___200_foreign_user_works_ok(self):
        self.login_foreign_user()
        PATH = reverse("base:account_removed")

        response = self.client.get(PATH)
        assert response.status_code == 200

    def test_account_removed___200_auth_works_ok(self):
        PATH = reverse("base:account_removed")

        self.login_me()
        response = self.client.get(PATH)
        assert response.status_code == 200
