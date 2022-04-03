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

from base.models import TargetVertex
from base.tests.test_utils.mini_setup import MiniSetup


class ChangeWeightModelBuilding(MiniSetup):
    def test_change_weight_building___403_not_auth(self):
        outline = self.get_outline()
        self.create_target_on_test_world(outline)
        target = TargetVertex.objects.get(target="200|200")
        weight_max = self.create_weight_maximum(outline)
        weight = self.create_weight(target=target, weight_max=weight_max)

        PATH = reverse("rest_api:change_weight_building")

        response = self.client.put(
            PATH,
            data=json.dumps(
                {
                    "building": "headquarters",
                    "outline_id": outline.pk,
                    "weight_id": weight.pk,
                }
            ),
            content_type="application/json",
        )
        assert response.status_code == 403

    def test_change_weight_building___404_foreign_user_has_no_access(self):
        outline = self.get_outline()
        self.create_target_on_test_world(outline)
        target = TargetVertex.objects.get(target="200|200")
        weight_max = self.create_weight_maximum(outline)
        weight = self.create_weight(target=target, weight_max=weight_max)

        PATH = reverse("rest_api:change_weight_building")

        self.login_foreign_user()

        response = self.client.put(
            PATH,
            data=json.dumps(
                {
                    "building": "headquarters",
                    "outline_id": outline.pk,
                    "weight_id": weight.pk,
                }
            ),
            content_type="application/json",
        )
        assert response.status_code == 404

    def test_change_weight_building___200_building_is_changed_properly(self):
        outline = self.get_outline()
        self.create_target_on_test_world(outline)
        target = TargetVertex.objects.get(target="200|200")
        weight_max = self.create_weight_maximum(outline)
        weight = self.create_weight(target=target, weight_max=weight_max)

        PATH = reverse("rest_api:change_weight_building")

        self.login_me()
        response = self.client.put(
            PATH,
            data=json.dumps(
                {
                    "building": "headquarters",
                    "outline_id": outline.pk,
                    "weight_id": weight.pk,
                }
            ),
            content_type="application/json",
        )
        assert response.json() == {"name": "Headquarters"}

        assert response.status_code == 200
        weight.refresh_from_db()
        assert weight.building == "headquarters"

    def test_change_weight_building___400_building_name_invalid(self):
        outline = self.get_outline()
        self.create_target_on_test_world(outline)
        target = TargetVertex.objects.get(target="200|200")
        weight_max = self.create_weight_maximum(outline)
        weight = self.create_weight(target=target, weight_max=weight_max)

        PATH = reverse("rest_api:change_weight_building")

        self.login_me()
        fake_building_name = self.random_lower_string()
        response = self.client.put(
            PATH,
            data=json.dumps(
                {
                    "building": fake_building_name,
                    "outline_id": outline.pk,
                    "weight_id": weight.pk,
                }
            ),
            content_type="application/json",
        )

        assert response.status_code == 400
        assert response.json() == {
            "building": [f"Invalid building: {fake_building_name}"]
        }
