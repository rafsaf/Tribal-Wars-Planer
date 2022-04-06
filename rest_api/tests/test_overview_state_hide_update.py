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


class OverviewStateHideUpdate(MiniSetup):
    def test_hide_state_update___403_not_auth(self):
        outline = self.get_outline()
        overview = self.create_overview(outline)

        PATH = reverse("rest_api:hide_state_update")

        response = self.client.put(
            PATH,
            data=json.dumps(
                {
                    "outline_id": outline.pk,
                    "token": overview.token,
                }
            ),
            content_type="application/json",
        )
        assert response.status_code == 403

    def test_hide_state_update___404_foreign_user_has_no_access(self):
        outline = self.get_outline()
        overview = self.create_overview(outline)

        PATH = reverse("rest_api:hide_state_update")

        self.login_foreign_user()

        response = self.client.put(
            PATH,
            data=json.dumps(
                {
                    "outline_id": outline.pk,
                    "token": overview.token,
                }
            ),
            content_type="application/json",
        )
        assert response.status_code == 404

    def test_hide_state_update___400_invalid_payload_types(self):
        outline = self.get_outline()
        overview = self.create_overview(outline)

        PATH = reverse("rest_api:hide_state_update")

        self.login_me()

        response = self.client.put(
            PATH,
            data=json.dumps(
                {
                    "outline_id": "text",
                    "token": overview.token,
                }
            ),
            content_type="application/json",
        )
        assert response.status_code == 400
        assert response.json() == {"outline_id": ["A valid integer is required."]}

    def test_hide_state_update___200_overview_properly_state_changed(self):
        outline = self.get_outline()
        overview = self.create_overview(outline)

        PATH = reverse("rest_api:hide_state_update")

        self.login_me()

        response = self.client.put(
            PATH,
            data=json.dumps(
                {
                    "outline_id": outline.pk,
                    "token": overview.token,
                }
            ),
            content_type="application/json",
        )
        assert response.status_code == 200

        overview.refresh_from_db()
        assert overview.show_hidden is True
        result = response.json()
        assert result["name"] == "True"
        assert result["class"] == "btn btn-light btn-light-no-border md-blue"

        response = self.client.put(
            PATH,
            data=json.dumps(
                {
                    "outline_id": outline.pk,
                    "token": overview.token,
                }
            ),
            content_type="application/json",
        )
        assert response.status_code == 200

        overview.refresh_from_db()
        assert overview.show_hidden is False
        result = response.json()
        assert result["name"] == "False"
        assert result["class"] == "btn btn-light btn-light-no-border md-error"
