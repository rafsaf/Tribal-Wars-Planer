# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

import json

from django.urls import reverse

from base.tests.test_utils.mini_setup import MiniSetup


class StripeCheckoutSession(MiniSetup):
    def test_stripe_session___403_not_auth(self):
        PATH = reverse("rest_api:stripe_session")

        response = self.client.post(
            PATH,
            data=json.dumps({"amount": 999, "currency": "EUR"}),
            content_type="application/json",
        )
        assert response.status_code == 403

    def test_stripe_session___400_invalid_amount(self):
        self.login_me()

        PATH = reverse("rest_api:stripe_session")

        response = self.client.post(
            PATH,
            data=json.dumps({"amount": 999, "currency": "EUR"}),
            content_type="application/json",
        )
        assert response.status_code == 400
        assert response.json() == {
            "error": "Could not found price for given user and amount."
        }
