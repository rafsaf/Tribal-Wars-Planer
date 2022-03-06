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


class TargetTimeUpdate(MiniSetup):
    def test_target_time_update___403_not_auth(self):
        outline = self.get_outline()
        self.create_target_on_test_world(outline)
        target: TargetVertex = TargetVertex.objects.get(target="200|200")
        outline_time = self.create_outline_time(outline)

        PATH = reverse("rest_api:target_time_update")

        response = self.client.put(
            PATH,
            data=json.dumps({"target_id": target.pk, "time_id": outline_time.pk}),
            content_type="application/json",
        )
        assert response.status_code == 403

    def test_target_time_update___404_foreign_user_has_no_access(self):
        outline = self.get_outline()
        self.create_target_on_test_world(outline)
        target: TargetVertex = TargetVertex.objects.get(target="200|200")
        outline_time = self.create_outline_time(outline)
        self.login_foreign_user()
        PATH = reverse("rest_api:target_time_update")

        response = self.client.put(
            PATH,
            data=json.dumps({"target_id": target.pk, "time_id": outline_time.pk}),
            content_type="application/json",
        )
        assert response.status_code == 404

    def test_target_time_update___400_invalid_payload_types(self):
        outline = self.get_outline()
        self.create_target_on_test_world(outline)
        target: TargetVertex = TargetVertex.objects.get(target="200|200")
        self.create_outline_time(outline)
        self.login_me()
        PATH = reverse("rest_api:target_time_update")

        response = self.client.put(
            PATH,
            data=json.dumps({"target_id": target.pk, "time_id": "text"}),
            content_type="application/json",
        )
        assert response.status_code == 400
        assert response.json() == {"time_id": ["Wymagana poprawna liczba całkowita."]}

    def test_target_time_update___200_target_updated_correct_target_no_time(self):
        outline = self.get_outline()
        self.create_target_on_test_world(outline)
        target: TargetVertex = TargetVertex.objects.get(target="200|200")
        outline_time = self.create_outline_time(outline)
        self.login_me()
        PATH = reverse("rest_api:target_time_update")

        response = self.client.put(
            PATH,
            data=json.dumps({"target_id": target.pk, "time_id": outline_time.pk}),
            content_type="application/json",
        )
        assert response.status_code == 200

        result = response.json()
        assert result["new"] == f"{target.pk}-time-{outline_time.pk}"
        assert result["old"] == "none"
        target.refresh_from_db()
        assert target.outline_time == outline_time

    def test_target_time_update___200_target_updated_correct_target_with_time(self):
        outline = self.get_outline()
        self.create_target_on_test_world(outline)
        target: TargetVertex = TargetVertex.objects.get(target="200|200")
        outline_time_old = self.create_outline_time(outline)
        target.outline_time = outline_time_old
        target.save()
        outline_time_new = self.create_outline_time(outline)
        self.login_me()
        PATH = reverse("rest_api:target_time_update")

        response = self.client.put(
            PATH,
            data=json.dumps({"target_id": target.pk, "time_id": outline_time_new.pk}),
            content_type="application/json",
        )
        assert response.status_code == 200

        result = response.json()
        assert result["new"] == f"{target.pk}-time-{outline_time_new.pk}"
        assert result["old"] == f"{target.pk}-time-{outline_time_old.pk}"
        target.refresh_from_db()
        assert target.outline_time == outline_time_new
