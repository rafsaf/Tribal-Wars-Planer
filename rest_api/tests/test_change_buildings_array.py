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


class ChangeBuildingsArray(MiniSetup):
    def test_change_buildings_array___403_not_auth(self):
        outline = self.get_outline()

        PATH = reverse("rest_api:change_buildings_array")
        response = self.client.put(
            PATH,
            data=json.dumps(
                {
                    "buildings": ["stable", "workshop", "academy", "smithy"],
                    "outline_id": outline.pk,
                }
            ),
            content_type="application/json",
        )
        assert response.status_code == 403

    def test_change_buildings_array___404_foreign_user_has_no_access(self):
        outline = self.get_outline()

        PATH = reverse("rest_api:change_buildings_array")

        self.login_foreign_user()
        response = self.client.put(
            PATH,
            data=json.dumps(
                {
                    "buildings": ["stable", "workshop", "academy", "smithy"],
                    "outline_id": outline.pk,
                }
            ),
            content_type="application/json",
        )
        assert response.status_code == 404

    def test_change_buildings_array___200_target_is_deleted_properly(self):
        outline = self.get_outline()

        PATH = reverse("rest_api:change_buildings_array")

        self.login_me()
        response = self.client.put(
            PATH,
            data=json.dumps(
                {
                    "buildings": ["stable", "workshop", "academy", "smithy"],
                    "outline_id": outline.pk,
                }
            ),
            content_type="application/json",
        )

        assert response.status_code == 200
        outline.refresh_from_db()
        assert outline.initial_outline_buildings == [
            "stable",
            "workshop",
            "academy",
            "smithy",
        ]

    def test_change_buildings_array___400_invalid_building_name(self):
        outline = self.get_outline()
        fake_building_name = self.random_lower_string()

        PATH = reverse("rest_api:change_buildings_array")

        self.login_me()

        response = self.client.put(
            PATH,
            data=json.dumps(
                {
                    "buildings": [fake_building_name],
                    "outline_id": outline.pk,
                }
            ),
            content_type="application/json",
        )

        assert response.status_code == 400
        assert response.json() == {
            "buildings": [f"Invalid building: {fake_building_name}"]
        }

    def test_change_buildings_array___400_double_building_name(self):
        outline = self.get_outline()

        PATH = reverse("rest_api:change_buildings_array")

        self.login_me()

        response = self.client.put(
            PATH,
            data=json.dumps(
                {
                    "buildings": ["stable", "stable"],
                    "outline_id": outline.pk,
                }
            ),
            content_type="application/json",
        )

        assert response.status_code == 400
        assert response.json() == {
            "buildings": ["Building occured more than once: stable"]
        }
