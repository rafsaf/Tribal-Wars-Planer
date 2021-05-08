from django.urls import reverse

from base import models
from base.models import Outline, TargetVertex, WeightMaximum, WeightModel
from base.tests.choices_initial import ChoicesInitial


class ChoicesRealAdding(ChoicesInitial):
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

    def test_planer_initial_move_up(self):

        outline = self.get_outline()
        target = self.get_target(outline)
        weight_max = self.get_weight_max(outline)
        weight0 = models.WeightModel.objects.get(target=target, start="500|500")
        weight1 = models.WeightModel.objects.get(target=target, start="500|501")
        filtr = self.random_lower_string()

        expected_path = (
            reverse("base:planer_initial_detail", args=[outline.pk, target.pk])
            + f"?page=2&sort=nobleman_left&filtr={filtr}"
        )

        self.client.login(username="user1", password="user1")
        response = self.client.post(
            reverse("base:planer_move_up", args=[outline.pk, target.pk, weight1.id])
            + f"?page=2&sort=nobleman_left&filtr={filtr}"
        )

        # redirect to target view after the work is done
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, expected_path)
        # testing behaviour
        weight0.refresh_from_db()
        weight1.refresh_from_db()
        self.assertEqual(weight0.order, 1)
        self.assertEqual(weight1.order, 0)
        self.client.login(username="user1", password="user1")
        response = self.client.post(
            reverse("base:planer_move_up", args=[outline.pk, target.pk, weight0.id])
            + f"?page=2&sort=nobleman_left&filtr={filtr}"
        )

        # redirect to target view after the work is done
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, expected_path)
        # testing behaviour
        weight0.refresh_from_db()
        weight1.refresh_from_db()
        self.assertEqual(weight0.order, 0)
        self.assertEqual(weight1.order, 1)

    def test_planer_initial_move_up___prevent_access_from_other_user(self):

        outline = self.get_outline()
        target = self.get_target(outline)
        weight_max = self.get_weight_max(outline)
        weight = self.get_weight(target)

        self.client.login(username="user2", password="user2")
        response = self.client.post(
            reverse("base:planer_move_up", args=[outline.pk, target.pk, weight.pk])
            + "?page=2&sort=nobleman_left"
        )
        self.assertEqual(response.status_code, 404)

    def test_planer_initial_move_down(self):

        outline = self.get_outline()
        target = self.get_target(outline)
        weight_max = self.get_weight_max(outline)
        weight0 = models.WeightModel.objects.get(target=target, start="500|500")
        weight1 = models.WeightModel.objects.get(target=target, start="500|501")
        filtr = self.random_lower_string()

        expected_path = (
            reverse("base:planer_initial_detail", args=[outline.pk, target.pk])
            + f"?page=2&sort=nobleman_left&filtr={filtr}"
        )

        self.client.login(username="user1", password="user1")
        response = self.client.post(
            reverse("base:planer_move_down", args=[outline.pk, target.pk, weight0.id])
            + f"?page=2&sort=nobleman_left&filtr={filtr}"
        )

        # redirect to target view after the work is done
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, expected_path)
        # testing behaviour
        weight0.refresh_from_db()
        weight1.refresh_from_db()
        self.assertEqual(weight0.order, 1)
        self.assertEqual(weight1.order, 0)
        self.client.login(username="user1", password="user1")
        response = self.client.post(
            reverse("base:planer_move_down", args=[outline.pk, target.pk, weight1.id])
            + f"?page=2&sort=nobleman_left&filtr={filtr}"
        )

        # redirect to target view after the work is done
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, expected_path)
        # testing behaviour
        weight0.refresh_from_db()
        weight1.refresh_from_db()
        self.assertEqual(weight0.order, 0)
        self.assertEqual(weight1.order, 1)

    def test_planer_initial_move_down___prevent_access_from_other_user(self):

        outline = self.get_outline()
        target = self.get_target(outline)
        weight_max = self.get_weight_max(outline)
        weight = self.get_weight(target)

        self.client.login(username="user2", password="user2")
        response = self.client.post(
            reverse("base:planer_move_down", args=[outline.pk, target.pk, weight.pk])
            + "?page=2&sort=nobleman_left"
        )
        self.assertEqual(response.status_code, 404)

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
            models.WeightModel.objects.filter(start="500|500", target=target).exists(),
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

    def test_planer_initial_divide(self):

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
            reverse("base:planer_divide", args=[outline.pk, target.pk, weight.pk, 4])
            + f"?page=2&sort=nobleman_left&filtr={filtr}"
        )

        # redirect to target view after the work is done
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, expected_path)
        # testing behaviour

        self.assertEqual(models.WeightModel.objects.filter(target=target).count(), 6)

    def test_planer_initial_divide___prevent_access_from_other_user2(self):

        outline = self.get_outline()
        target = self.get_target(outline)
        weight_max = self.get_weight_max(outline)
        weight = self.get_weight(target)

        self.client.login(username="user2", password="user2")
        response = self.client.post(
            reverse("base:planer_divide", args=[outline.pk, target.pk, weight.pk, 2])
            + "?page=2&sort=nobleman_left"
        )
        self.assertEqual(response.status_code, 404)

    def test_planer_delete_target(self):

        outline = self.get_outline()
        target = self.get_target(outline)
        weight_max = self.get_weight_max(outline)
        weight = self.get_weight(target)

        expected_path = (
            reverse("base:planer_initial", args=[outline.pk])
            + "?page=2&mode=add_and_remove"
        )

        self.client.login(username="user1", password="user1")
        response = self.client.post(
            reverse("base:planer_delete_target", args=[outline.pk, target.pk])
            + "?mode=add_and_remove&page=2"
        )

        # redirect to target view after the work is done
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, expected_path)
        # testing behaviour

        self.assertEqual(
            TargetVertex.objects.filter(outline=outline, target="500|499").exists(),
            False,
        )

    def test_planer_delete_target___prevent_access_from_other_user(self):

        outline = self.get_outline()
        target = self.get_target(outline)
        weight_max = self.get_weight_max(outline)
        weight = self.get_weight(target)

        self.client.login(username="user2", password="user2")
        response = self.client.post(
            reverse("base:planer_delete_target", args=[outline.pk, target.pk])
            + "?mode=add_and_delete&page=2"
        )
        self.assertEqual(response.status_code, 404)
