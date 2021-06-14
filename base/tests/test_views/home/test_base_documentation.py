from django.urls import reverse

from base.tests.test_utils.mini_setup import MiniSetup


class BaseDocumentation(MiniSetup):
    def test_base(self):
        response = self.client.get(reverse("base:documentation"))
        self.assertEqual(response.status_code, 200)
