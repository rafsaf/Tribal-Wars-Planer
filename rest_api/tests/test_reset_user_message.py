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

from base.models import Profile
from base.tests.test_utils.mini_setup import MiniSetup


class ResetUserMessage(MiniSetup):
    def test_reset_user_messages___403_not_auth(self):

        PATH = reverse("rest_api:reset_user_messages")

        response = self.client.put(PATH)
        assert response.status_code == 403

    def test_reset_user_messages___200_works_properly(self):
        me = self.me()
        my_profile: Profile = Profile.objects.get(user=me)
        my_profile.messages = 20
        my_profile.save()

        PATH = reverse("rest_api:reset_user_messages")

        self.login_me()

        response = self.client.put(PATH)
        assert response.status_code == 200

        my_profile.refresh_from_db()
        assert my_profile.messages == 0
