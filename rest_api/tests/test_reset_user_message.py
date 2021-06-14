from django.urls import reverse

from base.models import Profile
from base.tests.test_utils.mini_setup import MiniSetup


class ResetUserMessage(MiniSetup):
    def test_reset_user_messages___403_not_auth(self):

        PATH = reverse("rest_api:reset_user_messages")

        response = self.client.get(PATH)
        assert response.status_code == 403
        response = self.client.post(PATH)
        assert response.status_code == 403
        response = self.client.delete(PATH)
        assert response.status_code == 403
        response = self.client.put(PATH)
        assert response.status_code == 403

    def test_reset_user_messages___200_works_properly(self):
        me = self.me()
        my_profile: Profile = Profile.objects.get(user=me)
        my_profile.messages = 20
        my_profile.save()

        PATH = reverse("rest_api:reset_user_messages")

        self.login_me()
        response = self.client.get(PATH)
        assert response.status_code == 405

        response = self.client.post(PATH)
        assert response.status_code == 405

        response = self.client.delete(PATH)
        assert response.status_code == 405

        response = self.client.put(PATH)
        assert response.status_code == 200

        my_profile.refresh_from_db()
        assert my_profile.messages == 0
