from django.urls import reverse
from django.conf import settings
from base.models import OutlineTime, Profile, TargetVertex, WeightMaximum, WeightModel
from base.tests.utils.mini_setup import MiniSetup


class StripeWebhook(MiniSetup):
    def test_stripe_webhook___live_for_not_auth_but_return_400(self):

        PATH = reverse("rest_api:stripe_webhook")

        response = self.client.get(PATH)
        assert response.status_code == 405
        response = self.client.delete(PATH)
        assert response.status_code == 405
        response = self.client.put(PATH)
        assert response.status_code == 405

        response = self.client.post(PATH)
        assert response.status_code == 400
