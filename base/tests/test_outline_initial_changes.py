from django.test import TestCase
from django.urls import reverse

from base.tests import initial_setup
from base import models


class InitialAddFirstTest(TestCase):
    def setUp(self):
        initial_setup.create_initial_data()

    def test_add_first_view_correct_behaviour(self):

        outline = models.Outline.objects.get(pk=1)
        target = models.TargetVertex.objects.get(target="500|499", outline=outline)
        weight_max = models.WeightMaximum.objects.get(outline=outline, start="500|500")
        weight = models.WeightModel.objects.get(target=target, start="500|500")

        expected_path = (
            reverse("base:planer_initial_detail", args=[outline.id, target.id])
            + "?page=2&sort=nobleman_left"
        )

        self.client.login(username="user1", password="user1")
        response = self.client.post(
            reverse(
                "base:planer_add_first", args=[outline.id, target.id, weight_max.id]
            )
            + "?page=2&sort=nobleman_left"
        )

        # redirect to target view after the work is done
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, expected_path)
        # testing behaviour
        self.assertEqual(
            models.WeightModel.objects.filter(start="500|500", target=target).count(), 2
        )
        weight_max.refresh_from_db()
        self.assertEqual(weight_max.off_left, 0)
        self.assertEqual(weight_max.off_state, weight_max.off_max)
        self.assertEqual(weight_max.nobleman_left, 0)
        self.assertEqual(weight_max.nobleman_state, weight_max.nobleman_max)

        new_weight = models.WeightModel.objects.filter(
            start="500|500", target=target
        ).last()
        self.assertEqual(new_weight.off, 5000)
        self.assertEqual(new_weight.nobleman, 1)
        self.assertEqual(new_weight.order, -1)

    def test_add_first_off_view_correct_behaviour(self):

        outline = models.Outline.objects.get(pk=1)
        target = models.TargetVertex.objects.get(target="500|499", outline=outline)
        weight_max = models.WeightMaximum.objects.get(outline=outline, start="500|500")
        weight = models.WeightModel.objects.get(target=target, start="500|500")

        expected_path = (
            reverse("base:planer_initial_detail", args=[outline.id, target.id])
            + "?page=2&sort=nobleman_left"
        )

        self.client.login(username="user1", password="user1")
        response = self.client.post(
            reverse(
                "base:planer_add_first_off", args=[outline.id, target.id, weight_max.id]
            )
            + "?page=2&sort=nobleman_left"
        )

        # redirect to target view after the work is done
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, expected_path)
        # testing behaviour
        self.assertEqual(
            models.WeightModel.objects.filter(start="500|500", target=target).count(), 2
        )
        weight_max.refresh_from_db()
        self.assertEqual(weight_max.off_left, 0)
        self.assertEqual(weight_max.off_state, weight_max.off_max)
        self.assertEqual(weight_max.nobleman_left, 1)
        self.assertEqual(weight_max.nobleman_state, 1)

        new_weight = models.WeightModel.objects.filter(
            start="500|500", target=target
        ).last()
        self.assertEqual(new_weight.off, 5000)
        self.assertEqual(new_weight.nobleman, 0)
        self.assertEqual(new_weight.order, -1)

    def test_add_first_view_prevent_access_from_other_user(self):

        outline = models.Outline.objects.get(pk=1)
        target = models.TargetVertex.objects.get(target="500|499", outline=outline)
        weight_max = models.WeightMaximum.objects.get(outline=outline, start="500|500")
        weight = models.WeightModel.objects.get(target=target, start="500|500")

        self.client.login(username="user2", password="user2")
        response = self.client.post(
            reverse(
                "base:planer_add_first", args=[outline.id, target.id, weight_max.id]
            )
            + "?page=2&sort=nobleman_left"
        )
        self.assertEqual(response.status_code, 404)

    def test_add_first_off_view_prevent_access_from_other_user(self):

        outline = models.Outline.objects.get(pk=1)
        target = models.TargetVertex.objects.get(target="500|499", outline=outline)
        weight_max = models.WeightMaximum.objects.get(outline=outline, start="500|500")
        weight = models.WeightModel.objects.get(target=target, start="500|500")

        self.client.login(username="user2", password="user2")
        response = self.client.post(
            reverse(
                "base:planer_add_first_off", args=[outline.id, target.id, weight_max.id]
            )
            + "?page=2&sort=nobleman_left"
        )
        self.assertEqual(response.status_code, 404)

    def test_add_first_fake_noble_view_correct_behaviour(self):

        outline = models.Outline.objects.get(pk=1)
        target = models.TargetVertex.objects.get(target="500|499", outline=outline)
        weight_max = models.WeightMaximum.objects.get(outline=outline, start="500|500")
        weight = models.WeightModel.objects.get(target=target, start="500|500")

        expected_path = (
            reverse("base:planer_initial_detail", args=[outline.id, target.id])
            + "?page=2&sort=nobleman_left"
        )

        self.client.login(username="user1", password="user1")
        response = self.client.post(
            reverse(
                "base:planer_add_first_fake_noble",
                args=[outline.id, target.id, weight_max.id],
            )
            + "?page=2&sort=nobleman_left"
        )

        # redirect to target view after the work is done
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, expected_path)
        # testing behaviour
        self.assertEqual(
            models.WeightModel.objects.filter(start="500|500", target=target).count(), 2
        )
        weight_max.refresh_from_db()
        self.assertEqual(weight_max.off_left, 5000)
        self.assertEqual(weight_max.off_state, 5000)
        self.assertEqual(weight_max.nobleman_left, 0)
        self.assertEqual(weight_max.nobleman_state, 2)

        new_weight = models.WeightModel.objects.filter(
            start="500|500", target=target
        ).last()
        self.assertEqual(new_weight.off, 0)
        self.assertEqual(new_weight.nobleman, 1)
        self.assertEqual(new_weight.order, -1)

    def test_add_first_fake_view_correct_behaviour(self):

        outline = models.Outline.objects.get(pk=1)
        target = models.TargetVertex.objects.get(target="500|499", outline=outline)
        weight_max = models.WeightMaximum.objects.get(outline=outline, start="500|500")
        weight = models.WeightModel.objects.get(target=target, start="500|500")

        expected_path = (
            reverse("base:planer_initial_detail", args=[outline.id, target.id])
            + "?page=2&sort=nobleman_left"
        )

        self.client.login(username="user1", password="user1")
        response = self.client.post(
            reverse(
                "base:planer_add_first_fake",
                args=[outline.id, target.id, weight_max.id],
            )
            + "?page=2&sort=nobleman_left"
        )

        # redirect to target view after the work is done
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, expected_path)
        # testing behaviour
        self.assertEqual(
            models.WeightModel.objects.filter(start="500|500", target=target).count(), 2
        )
        weight_max.refresh_from_db()
        self.assertEqual(weight_max.off_left, 4900)
        self.assertEqual(weight_max.off_state, 5100)
        self.assertEqual(weight_max.nobleman_left, 1)
        self.assertEqual(weight_max.nobleman_state, 1)

        new_weight = models.WeightModel.objects.filter(
            start="500|500", target=target
        ).last()
        self.assertEqual(new_weight.off, 100)
        self.assertEqual(new_weight.nobleman, 0)
        self.assertEqual(new_weight.order, -1)

    def test_add_first_fake_view_prevent_access_from_other_user(self):

        outline = models.Outline.objects.get(pk=1)
        target = models.TargetVertex.objects.get(target="500|499", outline=outline)
        weight_max = models.WeightMaximum.objects.get(outline=outline, start="500|500")
        weight = models.WeightModel.objects.get(target=target, start="500|500")

        self.client.login(username="user2", password="user2")
        response = self.client.post(
            reverse(
                "base:planer_add_first_fake",
                args=[outline.id, target.id, weight_max.id],
            )
            + "?page=2&sort=nobleman_left"
        )
        self.assertEqual(response.status_code, 404)

    def test_add_last_view_correct_behaviour(self):

        outline = models.Outline.objects.get(pk=1)
        target = models.TargetVertex.objects.get(target="500|499", outline=outline)
        weight_max = models.WeightMaximum.objects.get(outline=outline, start="500|500")
        weight = models.WeightModel.objects.get(target=target, start="500|500")

        expected_path = (
            reverse("base:planer_initial_detail", args=[outline.id, target.id])
            + "?page=2&sort=nobleman_left"
        )

        self.client.login(username="user1", password="user1")
        response = self.client.post(
            reverse("base:planer_add_last", args=[outline.id, target.id, weight_max.id])
            + "?page=2&sort=nobleman_left"
        )

        # redirect to target view after the work is done
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, expected_path)
        # testing behaviour
        self.assertEqual(
            models.WeightModel.objects.filter(start="500|500", target=target).count(), 2
        )
        weight_max.refresh_from_db()
        self.assertEqual(weight_max.off_left, 0)
        self.assertEqual(weight_max.off_state, weight_max.off_max)
        self.assertEqual(weight_max.nobleman_left, 0)
        self.assertEqual(weight_max.nobleman_state, weight_max.nobleman_max)

        new_weight = models.WeightModel.objects.filter(
            start="500|500", target=target
        ).last()
        self.assertEqual(new_weight.off, 5000)
        self.assertEqual(new_weight.nobleman, 1)
        self.assertEqual(new_weight.order, 3)

    def test_add_last_view_prevent_access_from_other_user(self):

        outline = models.Outline.objects.get(pk=1)
        target = models.TargetVertex.objects.get(target="500|499", outline=outline)
        weight_max = models.WeightMaximum.objects.get(outline=outline, start="500|500")
        weight = models.WeightModel.objects.get(target=target, start="500|500")

        self.client.login(username="user2", password="user2")
        response = self.client.post(
            reverse("base:planer_add_last", args=[outline.id, target.id, weight_max.id])
            + "?page=2&sort=nobleman_left"
        )
        self.assertEqual(response.status_code, 404)

    def test_add_last_fake_view_correct_behaviour(self):

        outline = models.Outline.objects.get(pk=1)
        target = models.TargetVertex.objects.get(target="500|499", outline=outline)
        weight_max = models.WeightMaximum.objects.get(outline=outline, start="500|500")
        weight = models.WeightModel.objects.get(target=target, start="500|500")

        expected_path = (
            reverse("base:planer_initial_detail", args=[outline.id, target.id])
            + "?page=2&sort=nobleman_left"
        )

        self.client.login(username="user1", password="user1")
        response = self.client.post(
            reverse(
                "base:planer_add_last_fake", args=[outline.id, target.id, weight_max.id]
            )
            + "?page=2&sort=nobleman_left"
        )

        # redirect to target view after the work is done
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, expected_path)
        # testing behaviour
        self.assertEqual(
            models.WeightModel.objects.filter(start="500|500", target=target).count(), 2
        )
        weight_max.refresh_from_db()
        self.assertEqual(weight_max.off_left, 4900)
        self.assertEqual(weight_max.off_state, 5100)
        self.assertEqual(weight_max.nobleman_left, 1)
        self.assertEqual(weight_max.nobleman_state, 1)

        new_weight = models.WeightModel.objects.filter(
            start="500|500", target=target
        ).last()
        self.assertEqual(new_weight.off, 100)
        self.assertEqual(new_weight.nobleman, 0)
        self.assertEqual(new_weight.order, 3)

    def test_add_last_fake_noble_view_correct_behaviour(self):

        outline = models.Outline.objects.get(pk=1)
        target = models.TargetVertex.objects.get(target="500|499", outline=outline)
        weight_max = models.WeightMaximum.objects.get(outline=outline, start="500|500")
        weight = models.WeightModel.objects.get(target=target, start="500|500")

        expected_path = (
            reverse("base:planer_initial_detail", args=[outline.id, target.id])
            + "?page=2&sort=nobleman_left"
        )

        self.client.login(username="user1", password="user1")
        response = self.client.post(
            reverse(
                "base:planer_add_last_fake_noble", args=[outline.id, target.id, weight_max.id]
            )
            + "?page=2&sort=nobleman_left"
        )

        # redirect to target view after the work is done
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, expected_path)
        # testing behaviour
        self.assertEqual(
            models.WeightModel.objects.filter(start="500|500", target=target).count(), 2
        )
        weight_max.refresh_from_db()
        self.assertEqual(weight_max.off_left, 5000)
        self.assertEqual(weight_max.off_state, 5000)
        self.assertEqual(weight_max.nobleman_left, 0)
        self.assertEqual(weight_max.nobleman_state, 2)

        new_weight = models.WeightModel.objects.filter(
            start="500|500", target=target
        ).last()
        self.assertEqual(new_weight.off, 0)
        self.assertEqual(new_weight.nobleman, 1)
        self.assertEqual(new_weight.order, 3)

    def test_add_last_fake_view_prevent_access_from_other_user(self):

        outline = models.Outline.objects.get(pk=1)
        target = models.TargetVertex.objects.get(target="500|499", outline=outline)
        weight_max = models.WeightMaximum.objects.get(outline=outline, start="500|500")
        weight = models.WeightModel.objects.get(target=target, start="500|500")

        self.client.login(username="user2", password="user2")
        response = self.client.post(
            reverse(
                "base:planer_add_last_fake", args=[outline.id, target.id, weight_max.id]
            )
            + "?page=2&sort=nobleman_left"
        )
        self.assertEqual(response.status_code, 404)

    def test_add_last_fake_noble_view_prevent_access_from_other_user(self):

        outline = models.Outline.objects.get(pk=1)
        target = models.TargetVertex.objects.get(target="500|499", outline=outline)
        weight_max = models.WeightMaximum.objects.get(outline=outline, start="500|500")
        weight = models.WeightModel.objects.get(target=target, start="500|500")

        self.client.login(username="user2", password="user2")
        response = self.client.post(
            reverse(
                "base:planer_add_last_fake_noble", args=[outline.id, target.id, weight_max.id]
            )
            + "?page=2&sort=nobleman_left"
        )
        self.assertEqual(response.status_code, 404)

    def test_initial_hide_weight_view_correct_behaviour(self):

        outline = models.Outline.objects.get(pk=1)
        target = models.TargetVertex.objects.get(target="500|499", outline=outline)
        weight_max = models.WeightMaximum.objects.get(outline=outline, start="500|500")
        weight = models.WeightModel.objects.get(target=target, start="500|500")

        expected_path = (
            reverse("base:planer_initial_detail", args=[outline.id, target.id])
            + "?page=2&sort=nobleman_left"
        )

        self.client.login(username="user1", password="user1")
        response = self.client.post(
            reverse(
                "base:planer_hide_weight", args=[outline.id, target.id, weight_max.id]
            )
            + "?page=2&sort=nobleman_left"
        )

        # redirect to target view after the work is done
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, expected_path)
        # testing behaviour

        weight_max.refresh_from_db()
        self.assertEqual(weight_max.hidden, True)

        response2 = self.client.post(
            reverse(
                "base:planer_hide_weight", args=[outline.id, target.id, weight_max.id]
            )
            + "?page=2&sort=nobleman_left"
        )

        self.assertEqual(response2.status_code, 302)
        self.assertEqual(response2.url, expected_path)

        weight_max.refresh_from_db()
        self.assertEqual(weight_max.hidden, False)

    def test_initial_hide_weight_view_prevent_access_from_other_user(self):

        outline = models.Outline.objects.get(pk=1)
        target = models.TargetVertex.objects.get(target="500|499", outline=outline)
        weight_max = models.WeightMaximum.objects.get(outline=outline, start="500|500")
        weight = models.WeightModel.objects.get(target=target, start="500|500")

        self.client.login(username="user2", password="user2")
        response = self.client.post(
            reverse(
                "base:planer_hide_weight", args=[outline.id, target.id, weight_max.id]
            )
            + "?page=2&sort=nobleman_left"
        )
        self.assertEqual(response.status_code, 404)

    def test_initial_move_up_view_correct_behaviour(self):

        outline = models.Outline.objects.get(pk=1)
        target = models.TargetVertex.objects.get(target="500|499", outline=outline)
        weight_max = models.WeightMaximum.objects.get(outline=outline, start="500|500")
        weight0 = models.WeightModel.objects.get(target=target, start="500|500")
        weight1 = models.WeightModel.objects.get(target=target, start="500|501")

        expected_path = (
            reverse("base:planer_initial_detail", args=[outline.id, target.id])
            + "?page=2&sort=nobleman_left"
        )

        self.client.login(username="user1", password="user1")
        response = self.client.post(
            reverse("base:planer_move_up", args=[outline.id, target.id, weight1.id])
            + "?page=2&sort=nobleman_left"
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
            reverse("base:planer_move_up", args=[outline.id, target.id, weight0.id])
            + "?page=2&sort=nobleman_left"
        )

        # redirect to target view after the work is done
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, expected_path)
        # testing behaviour
        weight0.refresh_from_db()
        weight1.refresh_from_db()
        self.assertEqual(weight0.order, 0)
        self.assertEqual(weight1.order, 1)

    def test_initial_move_up_view_prevent_access_from_other_user(self):

        outline = models.Outline.objects.get(pk=1)
        target = models.TargetVertex.objects.get(target="500|499", outline=outline)
        weight_max = models.WeightMaximum.objects.get(outline=outline, start="500|500")
        weight = models.WeightModel.objects.get(target=target, start="500|500")

        self.client.login(username="user2", password="user2")
        response = self.client.post(
            reverse("base:planer_move_up", args=[outline.id, target.id, weight.id])
            + "?page=2&sort=nobleman_left"
        )
        self.assertEqual(response.status_code, 404)

    def test_initial_move_down_view_correct_behaviour(self):

        outline = models.Outline.objects.get(pk=1)
        target = models.TargetVertex.objects.get(target="500|499", outline=outline)
        weight_max = models.WeightMaximum.objects.get(outline=outline, start="500|500")
        weight0 = models.WeightModel.objects.get(target=target, start="500|500")
        weight1 = models.WeightModel.objects.get(target=target, start="500|501")

        expected_path = (
            reverse("base:planer_initial_detail", args=[outline.id, target.id])
            + "?page=2&sort=nobleman_left"
        )

        self.client.login(username="user1", password="user1")
        response = self.client.post(
            reverse("base:planer_move_down", args=[outline.id, target.id, weight0.id])
            + "?page=2&sort=nobleman_left"
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
            reverse("base:planer_move_down", args=[outline.id, target.id, weight1.id])
            + "?page=2&sort=nobleman_left"
        )

        # redirect to target view after the work is done
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, expected_path)
        # testing behaviour
        weight0.refresh_from_db()
        weight1.refresh_from_db()
        self.assertEqual(weight0.order, 0)
        self.assertEqual(weight1.order, 1)

    def test_initial_move_down_view_prevent_access_from_other_user(self):

        outline = models.Outline.objects.get(pk=1)
        target = models.TargetVertex.objects.get(target="500|499", outline=outline)
        weight_max = models.WeightMaximum.objects.get(outline=outline, start="500|500")
        weight = models.WeightModel.objects.get(target=target, start="500|500")

        self.client.login(username="user2", password="user2")
        response = self.client.post(
            reverse("base:planer_move_down", args=[outline.id, target.id, weight.id])
            + "?page=2&sort=nobleman_left"
        )
        self.assertEqual(response.status_code, 404)

    def test_initial_weight_delete_view_correct_behaviour(self):

        outline = models.Outline.objects.get(pk=1)
        target = models.TargetVertex.objects.get(target="500|499", outline=outline)
        weight_max = models.WeightMaximum.objects.get(outline=outline, start="500|500")
        weight = models.WeightModel.objects.get(target=target, start="500|500")

        expected_path = (
            reverse("base:planer_initial_detail", args=[outline.id, target.id])
            + "?page=2&sort=nobleman_left"
        )

        self.client.login(username="user1", password="user1")
        response = self.client.post(
            reverse(
                "base:planer_initial_delete", args=[outline.id, target.id, weight.id]
            )
            + "?page=2&sort=nobleman_left"
        )

        # redirect to target view after the work is done
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, expected_path)
        # testing behaviour

        self.assertEqual(
            models.WeightModel.objects.filter(start="500|500", target=target).exists(),
            False,
        )

    def test_initial_weight_delete_view_prevent_access_from_other_user(self):

        outline = models.Outline.objects.get(pk=1)
        target = models.TargetVertex.objects.get(target="500|499", outline=outline)
        weight_max = models.WeightMaximum.objects.get(outline=outline, start="500|500")
        weight = models.WeightModel.objects.get(target=target, start="500|500")

        self.client.login(username="user2", password="user2")
        response = self.client.post(
            reverse(
                "base:planer_initial_delete", args=[outline.id, target.id, weight.id]
            )
            + "?page=2&sort=nobleman_left"
        )
        self.assertEqual(response.status_code, 404)

    def test_initial_divide_view_correct_behaviour(self):

        outline = models.Outline.objects.get(pk=1)
        target = models.TargetVertex.objects.get(target="500|499", outline=outline)
        weight_max = models.WeightMaximum.objects.get(outline=outline, start="500|500")
        weight = models.WeightModel.objects.get(target=target, start="500|500")

        expected_path = (
            reverse("base:planer_initial_detail", args=[outline.id, target.id])
            + "?page=2&sort=nobleman_left"
        )

        self.client.login(username="user1", password="user1")
        response = self.client.post(
            reverse("base:planer_divide", args=[outline.id, target.id, weight.id, 4])
            + "?page=2&sort=nobleman_left"
        )

        # redirect to target view after the work is done
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, expected_path)
        # testing behaviour

        self.assertEqual(models.WeightModel.objects.filter(target=target).count(), 6)

    def test_initial_divide_view_prevent_access_from_other_user(self):

        outline = models.Outline.objects.get(pk=1)
        target = models.TargetVertex.objects.get(target="500|499", outline=outline)
        weight_max = models.WeightMaximum.objects.get(outline=outline, start="500|500")
        weight = models.WeightModel.objects.get(target=target, start="500|500")

        self.client.login(username="user2", password="user2")
        response = self.client.post(
            reverse("base:planer_divide", args=[outline.id, target.id, weight.id, 2])
            + "?page=2&sort=nobleman_left"
        )
        self.assertEqual(response.status_code, 404)

    def test_initial_divide_view_correct_behaviour(self):

        outline = models.Outline.objects.get(pk=1)
        target = models.TargetVertex.objects.get(target="500|499", outline=outline)
        weight_max = models.WeightMaximum.objects.get(outline=outline, start="500|500")
        weight = models.WeightModel.objects.get(target=target, start="500|500")

        expected_path = (
            reverse("base:planer_initial_detail", args=[outline.id, target.id])
            + "?page=2&sort=nobleman_left"
        )

        self.client.login(username="user1", password="user1")
        response = self.client.post(
            reverse("base:planer_divide", args=[outline.id, target.id, weight.id, 4])
            + "?page=2&sort=nobleman_left"
        )

        # redirect to target view after the work is done
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, expected_path)
        # testing behaviour

        self.assertEqual(models.WeightModel.objects.filter(target=target).count(), 6)

    def test_initial_divide_view_prevent_access_from_other_user(self):

        outline = models.Outline.objects.get(pk=1)
        target = models.TargetVertex.objects.get(target="500|499", outline=outline)
        weight_max = models.WeightMaximum.objects.get(outline=outline, start="500|500")
        weight = models.WeightModel.objects.get(target=target, start="500|500")

        self.client.login(username="user2", password="user2")
        response = self.client.post(
            reverse("base:planer_divide", args=[outline.id, target.id, weight.id, 2])
            + "?page=2&sort=nobleman_left"
        )
        self.assertEqual(response.status_code, 404)

    def test_planer_delete_target_view_correct_behaviour(self):

        outline = models.Outline.objects.get(pk=1)
        target = models.TargetVertex.objects.get(target="500|499", outline=outline)
        weight_max = models.WeightMaximum.objects.get(outline=outline, start="500|500")
        weight = models.WeightModel.objects.get(target=target, start="500|500")

        expected_path = (
            reverse("base:planer_initial", args=[outline.id])
            + "?page=2&mode=add_and_remove"
        )

        self.client.login(username="user1", password="user1")
        response = self.client.post(
            reverse("base:planer_delete_target", args=[outline.id, target.id])
            + "?mode=add_and_remove&page=2"
        )

        # redirect to target view after the work is done
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, expected_path)
        # testing behaviour

        self.assertEqual(
            models.TargetVertex.objects.filter(
                outline=outline, target="500|499"
            ).exists(),
            False,
        )

    def test_planer_delete_target_view_prevent_access_from_other_user(self):

        outline = models.Outline.objects.get(pk=1)
        target = models.TargetVertex.objects.get(target="500|499", outline=outline)
        weight_max = models.WeightMaximum.objects.get(outline=outline, start="500|500")
        weight = models.WeightModel.objects.get(target=target, start="500|500")

        self.client.login(username="user2", password="user2")
        response = self.client.post(
            reverse("base:planer_delete_target", args=[outline.id, target.id])
            + "?mode=add_and_delete&page=2"
        )
        self.assertEqual(response.status_code, 404)
