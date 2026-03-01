# Copyright 2021 Rafał Safin (rafsaf). All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from django.contrib.auth.models import User
from django.urls import reverse

from base.models import Outline, TargetVertex, WeightMaximum, WeightModel
from base.tests.test_views.outline_initial_changes.changes_view_setup import (
    ChangesViewSetup,
)


class InitialMoveDown(ChangesViewSetup):
    def test_planer_initial_move_down(self):
        outline = self.get_outline()
        target = self.get_target(outline)
        self.get_weight_max(outline)
        weight0: WeightModel = WeightModel.objects.get(target=target, start="500|500")
        weight1: WeightModel = WeightModel.objects.get(target=target, start="500|501")
        filtr = self.random_lower_string()

        expected_path = (
            reverse("base:planer_initial_detail", args=[outline.pk, target.pk])
            + f"?page=2&sort=nobleman_left&filtr={filtr}"
        )

        self.client.login(username="user1", password="user1")
        response = self.client.post(
            reverse("base:planer_move_down", args=[outline.pk, target.pk, weight0.pk])
            + f"?page=2&sort=nobleman_left&filtr={filtr}"
        )

        # redirect to target view after the work is done
        self.assertEqual(response.status_code, 302)
        self.assertEqual(getattr(response, "url"), expected_path)
        # testing behaviour
        weight0.refresh_from_db()
        weight1.refresh_from_db()
        self.assertEqual(weight0.order, 1)
        self.assertEqual(weight1.order, 0)
        self.client.login(username="user1", password="user1")
        response = self.client.post(
            reverse("base:planer_move_down", args=[outline.pk, target.pk, weight1.pk])
            + f"?page=2&sort=nobleman_left&filtr={filtr}"
        )

        # redirect to target view after the work is done
        self.assertEqual(response.status_code, 302)
        self.assertEqual(getattr(response, "url"), expected_path)
        # testing behaviour
        weight0.refresh_from_db()
        weight1.refresh_from_db()
        self.assertEqual(weight0.order, 0)
        self.assertEqual(weight1.order, 1)

    def test_planer_initial_move_down___prevent_access_from_other_user(self):
        outline = self.get_outline()
        target = self.get_target(outline)
        self.get_weight_max(outline)
        weight = self.get_weight(target)

        self.client.login(username="user2", password="user2")
        response = self.client.post(
            reverse("base:planer_move_down", args=[outline.pk, target.pk, weight.pk])
            + "?page=2&sort=nobleman_left"
        )
        self.assertEqual(response.status_code, 404)
        response = self.client.get(
            reverse("base:planer_move_down", args=[outline.pk, target.pk, weight.pk])
            + "?page=2&sort=nobleman_left"
        )
        self.assertEqual(response.status_code, 405)

    def test_planer_initial_move_down___404_mixed_ids_weight_must_match_target_and_outline(
        self,
    ):
        outline = self.get_outline()
        target = self.get_target(outline)

        foreign_user = User.objects.get(username="user2")
        foreign_outline = Outline.objects.create(
            id=102,
            owner=foreign_user,
            date=outline.date,
            name="foreign-outline-move",
            world=outline.world,
        )
        foreign_target = TargetVertex.objects.create(
            outline=foreign_outline,
            target="502|499",
            player="foreign-player",
        )
        foreign_weight_max = WeightMaximum.objects.create(
            outline=foreign_outline,
            start="502|500",
            player="foreign-player",
            off_max=1000,
            off_left=500,
            nobleman_max=2,
            nobleman_left=1,
            ram_max=10,
            ram_left=10,
        )
        foreign_weight = WeightModel.objects.create(
            target=foreign_target,
            state=foreign_weight_max,
            start="502|500",
            village_id=1,
            off=100,
            distance=1.0,
            nobleman=0,
            catapult=0,
            ruin=False,
            order=0,
            player="foreign-player",
            player_id=1,
            first_line=True,
        )

        self.client.login(username="user1", password="user1")
        response = self.client.post(
            reverse(
                "base:planer_move_down",
                args=[outline.pk, target.pk, foreign_weight.pk],
            )
            + "?page=1&sort=nobleman_left"
        )

        self.assertEqual(response.status_code, 404)
