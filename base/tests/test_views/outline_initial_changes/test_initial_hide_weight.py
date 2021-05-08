from django.urls import reverse

from base.tests.test_views.outline_initial_changes.changes_view_setup import (
    ChangesViewSetup,
)
from base.models import WeightModel


class InitialHideWeight(ChangesViewSetup):
    def test_planer_initial_hide_weight(self):

        outline = self.get_outline()
        target = self.get_target(outline)
        weight_max = self.get_weight_max(outline)
        weight = self.get_weight(target)
        filtr = self.random_lower_string()

        expected_path = (
            reverse("base:planer_initial_detail", args=[outline.pk, target.pk])
            + f"?page=2&sort=nobleman_left&filtr={filtr}"
        )

        self.client.login(username="user1", password="user1")
        response = self.client.post(
            reverse(
                "base:planer_hide_weight", args=[outline.pk, target.pk, weight_max.pk]
            )
            + f"?page=2&sort=nobleman_left&filtr={filtr}"
        )

        # redirect to target view after the work is done
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, expected_path)
        # testing behaviour

        weight_max.refresh_from_db()
        self.assertEqual(weight_max.hidden, True)

        response2 = self.client.post(
            reverse(
                "base:planer_hide_weight", args=[outline.pk, target.pk, weight_max.pk]
            )
            + f"?page=2&sort=nobleman_left&filtr={filtr}"
        )

        self.assertEqual(response2.status_code, 302)
        self.assertEqual(response2.url, expected_path)

        weight_max.refresh_from_db()
        self.assertEqual(weight_max.hidden, False)

    def test_planer_initial_hide_weight___prevent_access_from_other_user(self):

        outline = self.get_outline()
        target = self.get_target(outline)
        weight_max = self.get_weight_max(outline)
        weight = self.get_weight(target)

        self.client.login(username="user2", password="user2")
        response = self.client.post(
            reverse(
                "base:planer_hide_weight", args=[outline.pk, target.pk, weight_max.pk]
            )
            + "?page=2&sort=nobleman_left"
        )
        self.assertEqual(response.status_code, 404)
        response = self.client.get(
            reverse(
                "base:planer_hide_weight", args=[outline.pk, target.pk, weight_max.pk]
            )
            + "?page=2&sort=nobleman_left"
        )
        self.assertEqual(response.status_code, 405)
