# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

from django.urls import reverse

from base.tests.test_utils.mini_setup import MiniSetup


class BaseView(MiniSetup):
    def test_base(self):
        response = self.client.get(reverse("base:base"))
        self.assertEqual(response.status_code, 200)
