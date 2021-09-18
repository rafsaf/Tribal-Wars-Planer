from django.urls import reverse

from base.models import OutlineOverview, Overview, Stats
from base.tests.test_utils.mini_setup import MiniSetup


class OverviewView(MiniSetup):
    def test_overview_view___404_when_no_overview_exists(self):
        response = self.client.get(reverse("base:overview", args=["invalid_token"]))
        self.assertEqual(response.status_code, 404)

    def test_overview_view___200_when_overview_exists_outline_exists(self):
        outline = self.get_outline()
        outline.create_stats()
        outline_overview: OutlineOverview = OutlineOverview(
            targets_json="{}",
            weights_json="{}",
        )
        outline_overview.save()

        token = self.random_lower_string()
        overview = Overview(
            outline_overview=outline_overview,
            token=token,
            outline=outline,
            player=self.random_lower_string(),
            table=self.random_lower_string(),
            string=self.random_lower_string(),
        )
        overview.save()

        response = self.client.get(reverse("base:overview", args=[token]))
        self.assertEqual(response.status_code, 200)
        stats: Stats = Stats.objects.get(outline=outline)
        assert stats.overview_visited == 1

    def test_overview_view___200_when_overview_exists_outline_is_none(self):
        outline = self.get_outline()
        outline.create_stats()
        outline_overview: OutlineOverview = OutlineOverview(
            targets_json="{}",
            weights_json="{}",
        )
        outline_overview.save()

        token = self.random_lower_string()
        overview = Overview(
            outline_overview=outline_overview,
            token=token,
            outline=None,
            player=self.random_lower_string(),
            table=self.random_lower_string(),
            string=self.random_lower_string(),
        )
        overview.save()

        response = self.client.get(reverse("base:overview", args=[token]))
        self.assertEqual(response.status_code, 200)
        stats: Stats = Stats.objects.get(outline=outline)
        assert stats.overview_visited == 0
