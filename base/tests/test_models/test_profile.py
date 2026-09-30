# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

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
