from base.models import Outline
from django.urls import reverse
from base.tests.utils.mini_setup import MiniSetup


class InactiveOutline(MiniSetup):
    def test_paypal___1(self):
        outline = self.get_outline()
        PATH = reverse("paypal-ipn")

        response = self.client.get(PATH)
        self.assertEqual(response.status_code, 405)

        response = self.client.post(
            PATH, content_type="application/x-www-form-urlencoded"
        )
        print(response)
        self.assertEqual(response.status_code, 200)
