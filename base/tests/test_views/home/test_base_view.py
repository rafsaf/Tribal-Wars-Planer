from django.urls import reverse

from base.tests.test_views.home.home_view_setup import HomeViewSetup


class BaseView(HomeViewSetup):
    def test_base(self):
        response = self.client.get(reverse("base:base"))
        self.assertEqual(response.status_code, 200)
