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

    def test_public_outline_overview___400_invalid_data_in_db(self):
        PATH = reverse("rest_api:public_outline_overview")
        overview = self.create_overview(self.get_outline())
        overview.outline_overview.targets_json = "{}"
        overview.outline_overview.weights_json = "{}"
        overview.outline_overview.save()
        response = self.client.get(f"{PATH}?token={overview.token}")
        assert response.status_code == 400
