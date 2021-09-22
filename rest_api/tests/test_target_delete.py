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

from base.models import TargetVertex
from base.tests.test_utils.mini_setup import MiniSetup


class TargetTimeUpdate(MiniSetup):
    def test_target_delete___403_not_auth(self):
        outline = self.get_outline()
        self.create_target_on_test_world(outline)
        target: TargetVertex = TargetVertex.objects.get(target="200|200")

        PATH = reverse("rest_api:target_delete", args=[target.pk])

        response = self.client.get(PATH)
        assert response.status_code == 403
        response = self.client.post(PATH)
        assert response.status_code == 403
        response = self.client.delete(PATH)
        assert response.status_code == 403
        response = self.client.put(PATH)
        assert response.status_code == 403

    def test_target_delete___404_foreign_user_has_no_access(self):
        outline = self.get_outline()
        self.create_target_on_test_world(outline)
        target: TargetVertex = TargetVertex.objects.get(target="200|200")

        PATH = reverse("rest_api:target_delete", args=[target.pk])

        self.login_foreign_user()
        response = self.client.get(PATH)
        assert response.status_code == 405

        response = self.client.post(PATH)
        assert response.status_code == 405

        response = self.client.delete(PATH)
        assert response.status_code == 404

        response = self.client.put(PATH)
        assert response.status_code == 405

    def test_target_delete___200_target_is_deleted_properly(self):
        outline = self.get_outline()
        self.create_target_on_test_world(outline)
        target: TargetVertex = TargetVertex.objects.get(target="200|200")

        PATH = reverse("rest_api:target_delete", args=[target.pk])

        self.login_me()
        response = self.client.get(PATH)
        assert response.status_code == 405

        response = self.client.post(PATH)
        assert response.status_code == 405

        response = self.client.put(PATH)
        assert response.status_code == 405

        response = self.client.delete(PATH)
        assert response.status_code == 204

        assert not TargetVertex.objects.filter(target="200|200").exists()
