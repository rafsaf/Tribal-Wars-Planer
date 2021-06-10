from django.urls import reverse

from base.tests.test_utils.mini_setup import MiniSetup


class StripeCheckoutSession(MiniSetup):
    def test_stripe_session___403_not_auth(self):

        PATH = reverse("rest_api:stripe_session", args=[30])

        response = self.client.get(PATH)
        assert response.status_code == 403
        response = self.client.post(PATH)
        assert response.status_code == 403
        response = self.client.delete(PATH)
        assert response.status_code == 403
        response = self.client.put(PATH)
        assert response.status_code == 403

    def test_stripe_session___200_works_properly(self):
        self.login_me()
        PATH = reverse("rest_api:stripe_session", args=[33])

        response = self.client.get(PATH)
        assert response.status_code == 400

        PATH = reverse("rest_api:stripe_session", args=[80])

        response = self.client.get(PATH)
        assert response.status_code == 400

        response = self.client.post(PATH)
        assert response.status_code == 405

        response = self.client.delete(PATH)
        assert response.status_code == 405

        response = self.client.put(PATH)
        assert response.status_code == 405
