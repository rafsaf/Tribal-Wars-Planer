from django.conf import settings
from django.urls import reverse

from base.tests.utils.mini_setup import MiniSetup


class StripeConfig(MiniSetup):
    def test_stripe_key___403_not_auth(self):

        PATH = reverse("rest_api:stripe_key")

        response = self.client.get(PATH)
        assert response.status_code == 403
        response = self.client.post(PATH)
        assert response.status_code == 403
        response = self.client.delete(PATH)
        assert response.status_code == 403
        response = self.client.put(PATH)
        assert response.status_code == 403

    def test_stripe_key___200_works_properly(self):

        PATH = reverse("rest_api:stripe_key")

        self.login_me()
        response = self.client.get(PATH)
        assert response.status_code == 200
        result = response.json()
        assert result["publicKey"] == settings.STRIPE_PUBLISHABLE_KEY

        response = self.client.post(PATH)
        assert response.status_code == 405

        response = self.client.delete(PATH)
        assert response.status_code == 405

        response = self.client.put(PATH)
        assert response.status_code == 405
