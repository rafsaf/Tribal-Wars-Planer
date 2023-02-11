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


class InitialForm(MiniSetup):
    def test_planer_initial_detail___302_not_auth_redirect_login(self):
        outline = self.get_outline(test_world=True, written="active")
        self.create_target_on_test_world(outline)
        target = TargetVertex.objects.get(target="200|200")
        PATH = reverse("base:planer_initial_detail", args=[outline.pk, target.pk])

        response = self.client.get(PATH)
        assert response.status_code == 302
        assert response.url == self.login_page_path(next=PATH)

    def test_planer_initial_detail___404_foreign_user_no_access(self):
        outline = self.get_outline(test_world=True, written="active")
        self.create_target_on_test_world(outline)
        target = TargetVertex.objects.get(target="200|200")
        PATH = reverse("base:planer_initial_detail", args=[outline.pk, target.pk])

        self.login_foreign_user()
        response = self.client.get(PATH)
        assert response.status_code == 404

        response = self.client.post(PATH)
        assert response.status_code == 404

    def test_planer_initial_detail___200_proper_response(self):
        outline = self.get_outline(test_world=True, written="active")
        self.create_target_on_test_world(outline)
        target = TargetVertex.objects.get(target="200|200")
        PATH = reverse("base:planer_initial_detail", args=[outline.pk, target.pk])
        self.login_me()
        response = self.client.get(PATH)
        assert response.status_code == 200

    def test_planer_initial_detail___302_main_form_handling(self):
        outline = self.get_outline(test_world=True, written="active")
        self.create_target_on_test_world(outline)
        target = TargetVertex.objects.get(target="200|200")
        weight_max = self.create_weight_maximum(outline=outline)
        weight_max.catapult_left = 100
        weight_max.catapult_state = 100
        weight_max.catapult_max = 200
        weight_max.nobleman_left = 1
        weight_max.nobleman_state = 1
        weight_max.nobleman_max = 2
        weight_max.off_left = 2000
        weight_max.off_state = 1000
        weight_max.off_max = 3000
        weight_max.save()
        weight1 = self.create_weight(target=target, weight_max=weight_max)
        weight1.off = 100
        weight1.catapult = 10
        weight1.nobleman = 1
        weight1.save()
        PATH = reverse("base:planer_initial_detail", args=[outline.pk, target.pk])
        self.login_me()
        response = self.client.post(
            PATH,
            data={
                "form": "",
                "weight_id": weight1.pk,
                "off_no_catapult": "200",
                "catapult": "20",
                "nobleman": "2",
            },
        )
        assert response.status_code == 302
        weight1.refresh_from_db()
        weight_max.refresh_from_db()
        assert weight1.off == 360
        assert weight1.nobleman == 2
        assert weight1.catapult == 20

        assert weight_max.off_left == 1740
        assert weight_max.off_state == 1260

        assert weight_max.catapult_left == 90
        assert weight_max.catapult_state == 110

        assert weight_max.nobleman_left == 0
        assert weight_max.nobleman_state == 2
