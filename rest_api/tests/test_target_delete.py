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
from base.models.weight_model import WeightModel
from base.tests.test_utils.mini_setup import MiniSetup


class TargetTimeUpdate(MiniSetup):
    def test_target_delete___403_not_auth(self):
        outline = self.get_outline()
        self.create_target_on_test_world(outline)
        target: TargetVertex = TargetVertex.objects.get(target="200|200")

        PATH = reverse("rest_api:target_delete")

        response = self.client.delete(
            PATH,
            data=json.dumps(
                {
                    "target_id": target.pk,
                }
            ),
            content_type="application/json",
        )
        assert response.status_code == 403

    def test_target_delete___404_foreign_user_has_no_access(self):
        outline = self.get_outline()
        self.create_target_on_test_world(outline)
        target: TargetVertex = TargetVertex.objects.get(target="200|200")
        self.login_foreign_user()
        PATH = reverse("rest_api:target_delete")

        response = self.client.delete(
            PATH,
            data=json.dumps(
                {
                    "target_id": target.pk,
                }
            ),
            content_type="application/json",
        )
        assert response.status_code == 404

    def test_target_delete___400_invalid_payload_type(self):
        outline = self.get_outline()
        self.create_target_on_test_world(outline)
        self.login_me()
        PATH = reverse("rest_api:target_delete")

        response = self.client.delete(
            PATH,
            data=json.dumps(
                {
                    "target_id": "text",
                }
            ),
            content_type="application/json",
        )
        assert response.status_code == 400
        assert response.json() == {"target_id": ["A valid integer is required."]}

    def test_target_delete___200_target_empty_is_deleted_properly(self):
        outline = self.get_outline()
        self.create_target_on_test_world(outline)
        target: TargetVertex = TargetVertex.objects.get(target="200|200")

        self.login_me()
        PATH = reverse("rest_api:target_delete")

        response = self.client.delete(
            PATH,
            data=json.dumps(
                {
                    "target_id": target.pk,
                }
            ),
            content_type="application/json",
        )
        assert response.status_code == 204
        assert not TargetVertex.objects.filter(target="200|200").exists()

    def test_target_delete___200_target__with_weights_is_deleted_properly(self):
        outline = self.get_outline()
        self.create_target_on_test_world(outline)
        target: TargetVertex = TargetVertex.objects.get(target="200|200")

        weight_max = self.create_weight_maximum(outline=outline)

        off_state = 1000
        off_left = 1000
        noble_state = 2000
        noble_left = 2000
        catapult_state = 3000
        catapult_left = 3000

        weight_max.off_left = off_left
        weight_max.off_state = off_state
        weight_max.nobleman_left = noble_left
        weight_max.nobleman_state = noble_state
        weight_max.catapult_left = catapult_left
        weight_max.catapult_state = catapult_state
        weight_max.save()

        weight = self.create_weight(target=target, weight_max=weight_max)

        weight.off = 1000
        weight.nobleman = 2000
        weight.catapult = 3000
        weight.save()

        self.login_me()
        PATH = reverse("rest_api:target_delete")

        response = self.client.delete(
            PATH,
            data=json.dumps(
                {
                    "target_id": target.pk,
                }
            ),
            content_type="application/json",
        )
        assert response.status_code == 204
        assert not TargetVertex.objects.filter(target="200|200").exists()
        assert not WeightModel.objects.filter(start="500|500").exists()

        weight_max.refresh_from_db()
        assert weight_max.off_left == 2000
        assert weight_max.off_state == 0
        assert weight_max.nobleman_left == 4000
        assert weight_max.nobleman_state == 0
        assert weight_max.catapult_left == 6000
        assert weight_max.catapult_state == 0
