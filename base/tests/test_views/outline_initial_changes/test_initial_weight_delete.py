from django.urls import reverse

from base.models import WeightModel
from base.tests.test_views.outline_initial_changes.changes_view_setup import \
    ChangesViewSetup


class InitialWeightDelete(ChangesViewSetup):
    def test_planer_initial_weight_delete(self):

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
                "base:planer_initial_delete", args=[outline.pk, target.pk, weight.pk]
            )
            + f"?page=2&sort=nobleman_left&filtr={filtr}"
        )

        # redirect to target view after the work is done
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, expected_path)
        # testing behaviour

        self.assertEqual(
            WeightModel.objects.filter(start="500|500", target=target).exists(),
            False,
        )

    def test_planer_initial_weight_delete___prevent_access_from_other_user(self):

        outline = self.get_outline()
        target = self.get_target(outline)
        weight_max = self.get_weight_max(outline)
        weight = self.get_weight(target)

        self.client.login(username="user2", password="user2")
        response = self.client.post(
            reverse(
                "base:planer_initial_delete", args=[outline.pk, target.pk, weight.pk]
            )
            + "?page=2&sort=nobleman_left"
        )
        self.assertEqual(response.status_code, 404)
        response = self.client.get(
            reverse(
                "base:planer_initial_delete", args=[outline.pk, target.pk, weight.pk]
            )
            + "?page=2&sort=nobleman_left"
        )
        self.assertEqual(response.status_code, 405)
