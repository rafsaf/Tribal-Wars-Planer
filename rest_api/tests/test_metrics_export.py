# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

from django.conf import settings
from django.urls import reverse

from base.tests.test_utils.mini_setup import MiniSetup


class StripeConfig(MiniSetup):
    def test_metrics_export___403_not_auth(self):
        PATH = reverse("rest_api:metrics_export")

        response = self.client.get(PATH)
        assert response.status_code == 403

    def test_metrics_export___403_invalid_token(self):
        PATH = reverse("rest_api:metrics_export")
        response = self.client.get(f"{PATH}?token=wrong")
        assert response.status_code == 403

    def test_metrics_export___200_works_properly(self):
        PATH = reverse("rest_api:metrics_export")
        response = self.client.get(
            f"{PATH}?token={settings.METRICS_EXPORT_ENDPOINT_SECRET}"
        )
        assert response.status_code == 200
        assert (
            response.headers["content-type"]  # type: ignore
            == "text/plain; version=1.0.0; charset=utf-8"
        )
