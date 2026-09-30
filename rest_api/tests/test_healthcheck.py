# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

from django.urls import reverse

from base.tests.test_utils.mini_setup import MiniSetup


class Healthcheck(MiniSetup):
    def test_healthcheck__200(self):
        PATH = reverse("rest_api:healthcheck")

        response = self.client.get(PATH)
        assert response.status_code == 200
