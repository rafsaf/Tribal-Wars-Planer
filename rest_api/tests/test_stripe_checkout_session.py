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

from django.urls import reverse

from base.tests.test_utils.mini_setup import MiniSetup


class StripeCheckoutSession(MiniSetup):
    def test_stripe_session___403_not_auth(self):

        PATH = reverse("rest_api:stripe_session", args=[30])

        response = self.client.get(PATH)
        assert response.status_code == 403
        response = self.client.post(PATH)
        assert response.status_code == 403
        response = self.client.delete(PATH)
        assert response.status_code == 403
        response = self.client.put(PATH)
        assert response.status_code == 403

    def test_stripe_session___200_works_properly(self):
        self.login_me()
        PATH = reverse("rest_api:stripe_session", args=[33])

        response = self.client.get(PATH)
        assert response.status_code == 400

        PATH = reverse("rest_api:stripe_session", args=[80])

        response = self.client.get(PATH)
        assert response.status_code == 400

        response = self.client.post(PATH)
        assert response.status_code == 405

        response = self.client.delete(PATH)
        assert response.status_code == 405

        response = self.client.put(PATH)
        assert response.status_code == 405
