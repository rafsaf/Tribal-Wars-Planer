# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

from django.urls import reverse

from base.tests.test_utils.mini_setup import MiniSetup


class StripeWebhook(MiniSetup):
    def test_stripe_webhook___live_for_not_auth_but_return_400(self):
        PATH = reverse("rest_api:stripe_webhook")

        response = self.client.post(PATH)
        assert response.status_code == 400
