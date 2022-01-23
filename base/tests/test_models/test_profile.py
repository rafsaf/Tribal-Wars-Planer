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

from datetime import timedelta

from django.conf import settings
from django.utils.timezone import now

from base.models import Profile
from base.tests.test_utils.mini_setup import MiniSetup


class ProfileTest(MiniSetup):
    def test_is_premium__premium_on_validity_null_or_past_is_false(self):
        settings.PREMIUM_ACCOUNT_VALIDATION_ON = True
        user_profile: Profile = Profile.objects.get(user=self.me())
        user_profile.validity_date = None
        assert user_profile.is_premium() is False
        user_profile.validity_date = (now() - timedelta(hours=24)).date()
        assert user_profile.is_premium() is False

    def test_is_premium__premium_on_validity_future_is_true(self):
        settings.PREMIUM_ACCOUNT_VALIDATION_ON = True
        user_profile: Profile = Profile.objects.get(user=self.me())
        user_profile.validity_date = (now() + timedelta(hours=24)).date()
        assert user_profile.is_premium() is True

    def test_is_premium__premium_false_returns_true(self):
        settings.PREMIUM_ACCOUNT_VALIDATION_ON = False
        user_profile: Profile = Profile.objects.get(user=self.me())
        user_profile.validity_date = None
        assert user_profile.is_premium() is True
        user_profile.validity_date = (now() - timedelta(hours=24)).date()
        assert user_profile.is_premium() is True
        user_profile.validity_date = (now() + timedelta(hours=24)).date()
        assert user_profile.is_premium() is True
