# Copyright 2024 Rafał Safin (rafsaf). All Rights Reserved.
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


class InitialSetAllTime(MiniSetup):
    def test_planer_set_all_time_page___302_not_auth_redirect_login(self) -> None:
        outline = self.get_outline()
        outline_time = self.create_outline_time(outline)
        PATH = reverse("base:planer_set_all_time_page", args=[outline_time.pk])

        response = self.client.get(PATH)
        assert response.status_code == 302
        response = self.client.post(PATH)
        assert response.status_code == 302
        assert getattr(response, "url") == self.login_page_path(next=PATH)

    def test_planer_set_all_time_page___404_foreign_user_no_access(self) -> None:
        outline = self.get_outline()
        outline_time = self.create_outline_time(outline)
        PATH = reverse("base:planer_set_all_time_page", args=[outline_time.pk])

        self.login_foreign_user()
        response = self.client.get(PATH)
        assert response.status_code == 405

        response = self.client.post(PATH)
        assert response.status_code == 404

    def test_planer_set_all_time_page___302_no_outline_time_on_empty_targets(
        self,
    ) -> None:
        outline = self.get_outline()
        self.create_target_on_test_world(outline)
        self.create_target_on_test_world(outline, fake=True, coord="201|200")
        self.create_target_on_test_world(outline, ruin=True, coord="202|200")
        outline_time = self.create_outline_time(outline)

        PATH = (
            reverse("base:planer_set_all_time_page", args=[outline_time.pk])
            + "?page=1&mode=time&filtr="
        )
        REDIRECT = (
            reverse("base:planer_initial", args=[outline.pk])
            + "?page=1&mode=time&filtr="
        )

        self.login_me()
        response = self.client.post(PATH)
        assert response.status_code == 302
        assert getattr(response, "url") == REDIRECT

        assert TargetVertex.objects.filter(outline_time=outline_time).count() == 0

    def test_planer_set_all_time_page___302_proper_outline_time_on_targets(
        self,
    ) -> None:
        outline = self.get_outline()
        self.create_target_on_test_world(outline, many=5)
        targets = list(TargetVertex.objects.filter(outline=outline))
        for i in range(5):
            weight_max = self.create_weight_maximum(outline=outline)
            self.create_weight(target=targets[i], weight_max=weight_max)

        outline_time = self.create_outline_time(outline)

        PATH = (
            reverse("base:planer_set_all_time_page", args=[outline_time.pk])
            + "?page=1&mode=time&filtr="
        )
        REDIRECT = (
            reverse("base:planer_initial", args=[outline.pk])
            + "?page=1&mode=time&filtr="
        )

        self.login_me()
        response = self.client.post(PATH)
        assert response.status_code == 302
        assert getattr(response, "url") == REDIRECT

        assert TargetVertex.objects.filter(outline_time=outline_time).count() == 5

    def test_planer_set_all_time_page___302_proper_outline_time_on_targets_only_2_page(
        self,
    ) -> None:
        outline = self.get_outline()
        outline.filter_targets_number = 2
        outline.save()
        self.create_target_on_test_world(outline, many=5)
        targets = list(TargetVertex.objects.filter(outline=outline).order_by("pk"))
        for i in range(5):
            weight_max = self.create_weight_maximum(outline=outline)
            self.create_weight(target=targets[i], weight_max=weight_max)

        outline_time = self.create_outline_time(outline)

        PATH = (
            reverse("base:planer_set_all_time_page", args=[outline_time.pk])
            + "?page=2&mode=time"
        )
        REDIRECT = (
            reverse("base:planer_initial", args=[outline.pk])
            + "?page=2&mode=time&filtr="
        )

        self.login_me()
        response = self.client.post(PATH)
        assert response.status_code == 302
        assert getattr(response, "url") == REDIRECT

        targets = list(TargetVertex.objects.filter(outline=outline).order_by("pk"))
        assert TargetVertex.objects.filter(outline_time=outline_time).count() == 2
        assert targets[2].outline_time == outline_time
        assert targets[3].outline_time == outline_time

    def test_planer_set_all_time_page___302_respects_filter_param(
        self,
    ) -> None:
        outline = self.get_outline()
        self.create_target_on_test_world(outline, many=5)
        targets = list(TargetVertex.objects.filter(outline=outline).order_by("pk"))

        test_target_pk = targets[4].pk
        for i in range(5):
            weight_max = self.create_weight_maximum(outline=outline)
            self.create_weight(target=targets[i], weight_max=weight_max)
            if i == 4:
                self.create_weight(target=targets[i], weight_max=weight_max)

        outline_time = self.create_outline_time(outline)

        PATH = (
            reverse("base:planer_set_all_time_page", args=[outline_time.pk])
            + "?page=1&mode=time&filtr=command>1"
        )
        REDIRECT = (
            reverse("base:planer_initial", args=[outline.pk])
            + "?page=1&mode=time&filtr=command%3E1"
        )

        self.login_me()
        response = self.client.post(PATH)
        assert response.status_code == 302
        assert getattr(response, "url") == REDIRECT

        assert TargetVertex.objects.filter(outline_time=outline_time).count() == 1
        assert TargetVertex.objects.get(pk=test_target_pk).outline_time == outline_time
