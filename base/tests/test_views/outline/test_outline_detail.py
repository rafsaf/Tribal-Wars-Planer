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

from base.models import Outline, Stats
from base.tests.test_utils.mini_setup import MiniSetup


class InactiveOutline(MiniSetup):
    def test_planer_detail___302_not_auth_redirect_login(self):
        outline = self.get_outline()
        PATH = reverse("base:planer_detail", args=[outline.pk])

        response = self.client.get(PATH)
        assert response.status_code == 302
        assert response.url == self.login_page_path(next=PATH)

    def test_planer_detail___404_foreign_user_no_access(self):
        outline = self.get_outline(editable="inactive")
        PATH = reverse("base:planer_detail", args=[outline.pk])

        self.login_foreign_user()
        response = self.client.get(PATH)
        assert response.status_code == 404

    def test_planer_detail___404_auth_editable_is_removed_do_not_touch_others(self):
        outline = self.get_outline()
        self.create_foreign_outline()
        PATH = reverse("base:planer_detail", args=[outline.pk])

        self.login_me()
        assert Outline.objects.count() == 2
        response = self.client.get(PATH)
        assert Outline.objects.count() == 1
        assert response.status_code == 404

    def test_planer_detail___200_auth_works_ok(self):
        outline = self.get_outline(editable="inactive")

        PATH = reverse("base:planer_detail", args=[outline.pk])

        self.login_me()
        response = self.client.get(PATH)
        assert response.status_code == 200

    def test_planer_detail___302_auth_works_ok_on_Test_world_army_troops(self):
        outline = self.get_outline(editable="inactive", test_world=True)
        assert outline.ally_tribe_tag == ["ALLY"]
        outline.create_stats()
        stats: Stats = Stats.objects.get(outline=outline)
        assert stats.off_troops == 0

        PATH = reverse("base:planer_detail", args=[outline.pk])
        TROOPS = "100|100,100,100,7000,0,100,2800,0,0,350,100,0,0,0,0,0,"
        self.login_me()
        response = self.client.post(
            PATH,
            data={
                "form-1": "",
                "off_troops": TROOPS,
            },
        )
        assert response.status_code == 302
        assert response.url == PATH

        outline.refresh_from_db()
        stats.refresh_from_db()
        assert stats.off_troops == 1
        assert outline.off_troops == TROOPS
        assert (
            outline.off_troops_hash
            == "6e229ad27b9bdfbf5fa635fd7291d3a61899ec0da9064c08c516ac2e7749d544"
        )

    def test_planer_detail___302_auth_works_ok_on_Test_world_deff_troops(self):
        outline = self.get_outline(editable="inactive", test_world=True)
        outline.create_stats()
        stats: Stats = Stats.objects.get(outline=outline)
        assert stats.deff_troops == 0
        PATH = reverse("base:planer_detail", args=[outline.pk])
        DEFF = "101|101,w wiosce,100,100,7001,0,100,2801,0,0,350,100,0,0,0,0,"
        self.login_me()
        response = self.client.post(
            PATH,
            data={
                "form-2": "",
                "deff_troops": DEFF,
            },
        )
        assert response.status_code == 302
        assert response.url == PATH

        outline.refresh_from_db()
        stats.refresh_from_db()
        assert stats.deff_troops == 1
        assert outline.deff_troops == DEFF
        assert (
            outline.deff_troops_hash
            == "f2f2d2b0a9f51cd2def7c25571b1b07b0ce835359902ac46700b6731e0cb5da4"
        )

    def test_planer_detail___200_auth_form_error_when_nonsense(self):
        outline = self.get_outline(editable="inactive", test_world=True)

        PATH = reverse("base:planer_detail", args=[outline.pk])
        DEFF = "101|101,some_big_nonsene"
        self.login_me()
        response = self.client.post(
            PATH,
            data={
                "form-2": "",
                "deff_troops": DEFF,
            },
        )
        assert response.status_code == 200
        deff_troops = response.context["deff_troops"]
        assert len(deff_troops.errors) == 1

        outline.refresh_from_db()
        assert outline.deff_troops == ""
