import string

from django.urls import reverse

from base.models import OutlineOverview, Overview
from base.tests.test_views.home.home_view_setup import HomeViewSetup


class OverviewView(HomeViewSetup):
    def test_overview_view___404_when_no_overview_exists(self):
        response = self.client.get(reverse("base:overview", args=["invalid_token"]))
        self.assertEqual(response.status_code, 404)

    def test_overview_view___200_when_overview_exists(self):
        outline_overview: OutlineOverview = OutlineOverview(
            targets_json="{}",
            weights_json="{}",
        )
        outline_overview.save()

        token = self.random_lower_string()
        overview = Overview(
            outline_overview=outline_overview,
            token=token,
            player=self.random_lower_string(),
            table=self.random_lower_string(),
            string=self.random_lower_string(),
        )
        overview.save()

        response = self.client.get(reverse("base:overview", args=[token]))
        self.assertEqual(response.status_code, 200)
