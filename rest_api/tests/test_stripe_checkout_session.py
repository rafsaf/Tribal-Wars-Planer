# Copyright 2021 Rafał Safin (rafsaf). All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

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
