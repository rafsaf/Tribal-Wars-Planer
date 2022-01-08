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

import datetime

from django.urls import reverse

from base.forms import OutlineForm
from base.models import Outline, Result, Stats
from base.models.profile import Profile
from base.tests.test_utils.mini_setup import MiniSetup


class NewOutlineCreate(MiniSetup):
    def test_planer_create___302_not_auth_redirect_login(self):
        PATH = reverse("base:planer_create")

        response = self.client.get(PATH)

        assert response.status_code == 302
        assert response.url == self.login_page_path(next=PATH)

    def test_planer_create___200_auth(self):
        PATH = reverse("base:planer_create")

        self.login_me()
        response = self.client.get(PATH)
        form: OutlineForm = response.context["form1"]

        assert response.status_code == 200
        assert len(form.errors) == 0

    def test_planer_create___200_auth_form_not_work_world_invalid(self):
        PATH = reverse("base:planer_create")

        self.login_me()
        response = self.client.post(
            PATH,
            data={
                "form1": "",
                "name": "name",
                "date": datetime.date.today(),
                "world": "xxxx",
            },
        )
        form: OutlineForm = response.context["form1"]

        assert response.status_code == 200
        assert len(form.errors) == 1
        assert "world" in form.errors

    def test_planer_create___200_auth_form_create_outline_and_redirect(self):
        PATH = reverse("base:planer_create")

        world = self.get_world()

        self.login_me()
        response = self.client.post(
            PATH,
            data={
                "form1": "",
                "name": "name",
                "date": datetime.date.today(),
                "world": world.pk,
            },
        )

        assert response.status_code == 302
        assert Outline.objects.filter(name="name").count() == 1
        assert Result.objects.all().count() == 1
        assert Stats.objects.all().count() == 1

        outline: Outline = Outline.objects.get(name="name")
        REDIRECT = reverse("base:planer_create_select", args=[outline.pk])

        assert response.url == REDIRECT
        assert outline.name == "name"
        assert outline.date == datetime.date.today()
        assert outline.world == world
        assert outline.owner == self.me()

        result: Result = Result.objects.get(outline=outline)

        assert result.results_export == ""
        assert result.results_get_deff == ""
        assert result.results_players == ""
        assert result.results_outline == ""
        assert result.results_sum_up == ""

        stats: Stats = Stats.objects.get(outline=outline)

        assert stats.outline_pk == outline.pk
        assert stats.premium_user is True
        assert stats.owner_name == self.me().username
        assert stats.world == str(outline.world)

    def test_planer_create___200_auth_form_modal_works_fine(self):
        PATH = reverse("base:planer_create")

        world = self.get_world()
        me = self.me()
        profile: Profile = Profile.objects.get(user=me)
        profile.server = None
        profile.save()
        self.login_me()
        assert profile.server_bind is False

        response = self.client.post(
            PATH,
            data={"form2": "", "server": world.server.dns},
        )

        assert response.status_code == 302
        assert response.url == PATH
        profile.refresh_from_db()
        assert profile.server == world.server
        assert profile.server_bind is True
