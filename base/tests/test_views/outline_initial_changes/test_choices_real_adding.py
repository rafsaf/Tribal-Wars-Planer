from django.urls import reverse

from base.tests.test_views.outline_initial_changes.choices_initial import ChoicesInitial
from base.models import WeightModel


class ChoicesRealAdding(ChoicesInitial):
    def test_planer_add_first_off(self):
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
                "base:planer_add_first_off", args=[outline.pk, target.pk, weight_max.pk]
            )
            + f"?page=2&sort=nobleman_left&filtr={filtr}"
        )

        # redirect to target view after the work is done
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, expected_path)
        # testing behaviour
        self.assertEqual(
            WeightModel.objects.filter(start="500|500", target=target).count(), 2
        )
        weight_max.refresh_from_db()
        self.assertEqual(weight_max.off_left, 0)
        self.assertEqual(weight_max.off_state, weight_max.off_max)
        self.assertEqual(weight_max.nobleman_left, 1)
        self.assertEqual(weight_max.nobleman_state, 1)

        new_weight = WeightModel.objects.filter(start="500|500", target=target).last()
        self.assertEqual(new_weight.off, 5000)
        self.assertEqual(new_weight.nobleman, 0)
        self.assertEqual(new_weight.order, -1)

    def test_planer_add_first_off___prevent_access_from_other_user(self):

        outline = self.get_outline()
        target = self.get_target(outline)
        weight_max = self.get_weight_max(outline)
        weight = self.get_weight(target)

        self.client.login(username="user2", password="user2")
        response = self.client.post(
            reverse(
                "base:planer_add_first_off", args=[outline.pk, target.pk, weight_max.pk]
            )
            + "?page=2&sort=nobleman_left"
        )
        self.assertEqual(response.status_code, 404)

    def test_planer_add_last(self):

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
            reverse("base:planer_add_last", args=[outline.pk, target.pk, weight_max.pk])
            + f"?page=2&sort=nobleman_left&filtr={filtr}"
        )

        # redirect to target view after the work is done
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, expected_path)
        # testing behaviour
        self.assertEqual(
            WeightModel.objects.filter(start="500|500", target=target).count(), 2
        )
        weight_max.refresh_from_db()
        self.assertEqual(weight_max.off_left, 0)
        self.assertEqual(weight_max.off_state, weight_max.off_max)
        self.assertEqual(weight_max.nobleman_left, 0)
        self.assertEqual(weight_max.nobleman_state, weight_max.nobleman_max)

        new_weight = WeightModel.objects.filter(start="500|500", target=target).last()
        self.assertEqual(new_weight.off, 5000)
        self.assertEqual(new_weight.nobleman, 1)
        self.assertEqual(new_weight.order, 3)

    def test_planer_add_last___prevent_access_from_other_user(self):

        outline = self.get_outline()
        target = self.get_target(outline)
        weight_max = self.get_weight_max(outline)
        weight = self.get_weight(target)

        self.client.login(username="user2", password="user2")
        response = self.client.post(
            reverse("base:planer_add_last", args=[outline.pk, target.pk, weight_max.pk])
            + "?page=2&sort=nobleman_left"
        )
        self.assertEqual(response.status_code, 404)

    def test_planer_add_last_off(self):

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
                "base:planer_add_last_off", args=[outline.pk, target.pk, weight_max.pk]
            )
            + f"?page=2&sort=nobleman_left&filtr={filtr}"
        )

        # redirect to target view after the work is done
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, expected_path)
        # testing behaviour
        self.assertEqual(
            WeightModel.objects.filter(start="500|500", target=target).count(), 2
        )
        weight_max.refresh_from_db()
        self.assertEqual(weight_max.off_left, 0)
        self.assertEqual(weight_max.off_state, weight_max.off_max)
        self.assertEqual(weight_max.nobleman_left, 1)
        self.assertEqual(weight_max.nobleman_state, 1)

        new_weight = WeightModel.objects.filter(start="500|500", target=target).last()
        self.assertEqual(new_weight.off, 5000)
        self.assertEqual(new_weight.nobleman, 0)
        self.assertEqual(new_weight.order, 3)

    def test_planer_add_last_off___prevent_access_from_other_user(self):

        outline = self.get_outline()
        target = self.get_target(outline)
        weight_max = self.get_weight_max(outline)
        weight = self.get_weight(target)

        self.client.login(username="user2", password="user2")
        response = self.client.post(
            reverse(
                "base:planer_add_last_off", args=[outline.pk, target.pk, weight_max.pk]
            )
            + "?page=2&sort=nobleman_left"
        )
        self.assertEqual(response.status_code, 404)
