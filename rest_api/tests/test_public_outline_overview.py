# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

from django.urls import reverse

from base.tests.test_utils.mini_setup import MiniSetup

# one success test moved to test_outline_finish.py


class TestPublicOutlineOverview(MiniSetup):
    def test_public_outline_overview___404_not_auth(self):
        PATH = reverse("rest_api:public_outline_overview")

        response = self.client.get(PATH)
        assert response.status_code == 404

    def test_public_outline_overview___404_invalid_token(self):
        PATH = reverse("rest_api:public_outline_overview")
        response = self.client.get(f"{PATH}?token=wrong")
        assert response.status_code == 404

    def test_public_outline_overview___500_invalid_data_in_db(self):
        PATH = reverse("rest_api:public_outline_overview")
        overview = self.create_overview(self.get_outline())
        overview.outline_overview.targets_json = "{}"
        overview.outline_overview.weights_json = "{}"
        overview.outline_overview.save()
        response = self.client.get(f"{PATH}?token={overview.token}")
        assert response.status_code == 500
