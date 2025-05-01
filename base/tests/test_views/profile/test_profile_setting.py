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

from base.forms import ChangeProfileForm
from base.models import Outline, Profile
from base.tests.test_utils.mini_setup import MiniSetup


class OutlineProfileSettings(MiniSetup):
    def test_settings___302_not_auth_redirect_login(self):
        PATH = reverse("base:settings")

        response = self.client.get(PATH)
        assert response.status_code == 302
        assert getattr(response, "url") == self.login_page_path(next=PATH)

    def test_settings___200_foreign_user_works_ok(self):
        self.login_foreign_user()
        PATH = reverse("base:settings")

        response = self.client.get(PATH)
        assert response.status_code == 200

    def test_settings___200_auth_works_ok(self):
        PATH = reverse("base:settings")

        self.login_me()
        response = self.client.get(PATH)
        assert response.status_code == 200

    def test_settings___200_form_nonsense_errors(self):
        PATH = reverse("base:settings")

        self.login_me()
        response = self.client.post(
            PATH,
            data={
                "server": "xaxaxa",
                "form1": "",
                "default_morale_on": True,
                "input_data_type": Outline.DEFF_COLLECTION,
                "currency": "PLN",
                "sending_option": "default",
                "send_message_with_url": True,
                "feature_flag_shipments": True,
            },
        )
        assert response.status_code == 200
        form1: ChangeProfileForm = response.context["form1"]
        assert len(form1.errors) == 1
        assert "server" in form1.errors

    def test_settings___302_form_works_correct(self):
        PATH = reverse("base:settings")
        self.get_world()

        me = self.me()
        profile: Profile = Profile.objects.get(user=me)
        profile.default_morale_on = True
        profile.feature_flag_shipments = True
        profile.server = None
        profile.input_data_type = Outline.ARMY_COLLECTION
        profile.save()

        self.login_me()
        response = self.client.post(
            PATH,
            data={
                "server": "nottestserver",
                "currency": "EUR",
                "input_data_type": Outline.DEFF_COLLECTION,
                "default_morale_on": False,
                "feature_flag_shipments": False,
                "sending_option": "extended",
                "send_message_with_url": False,
                "form1": "",
            },
        )
        assert response.status_code == 302
        assert getattr(response, "url") == PATH

        profile_2: Profile = Profile.objects.get(user=me)
        assert profile_2.input_data_type == Outline.DEFF_COLLECTION
        assert profile_2.server is not None
        assert profile_2.server.dns == "nottestserver"
        assert not profile_2.default_morale_on
        assert not profile_2.feature_flag_shipments
        assert profile_2.sending_option == "extended"
        assert not profile_2.send_message_with_url
