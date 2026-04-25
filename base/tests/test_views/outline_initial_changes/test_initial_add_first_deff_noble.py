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

from django.urls import reverse

from base.models import WeightModel
from base.tests.test_views.outline_initial_changes.changes_view_setup import (
    ChangesViewSetup,
)


class InitialAddFirstDeffNoble(ChangesViewSetup):
    def test_planer_add_first_deff_noble(self):
        outline = self.get_outline()
        target = self.get_target(outline)
        target.has_deff_noble = True
        target.deff_noble_order = 4
        target.save(update_fields=["has_deff_noble", "deff_noble_order"])
        weight_max = self.get_weight_max(outline)
        weight_max.deff_left = 700
        weight_max.deff_max = 700
        weight_max.save(update_fields=["deff_left", "deff_max"])
        self.get_weight(target)
        filtr = self.random_lower_string()

        expected_path = (
            reverse("base:planer_initial_detail", args=[outline.pk, target.pk])
            + f"?page=2&sort=nobleman_left&filtr={filtr}"
        )

        self.client.login(username="user1", password="user1")
        response = self.client.post(
            reverse(
                "base:planer_add_first_deff_noble",
                args=[outline.pk, target.pk, weight_max.pk],
            )
            + f"?page=2&sort=nobleman_left&filtr={filtr}"
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(getattr(response, "url"), expected_path)
        self.assertEqual(
            WeightModel.objects.filter(start="500|500", target=target).count(), 2
        )
        weight_max.refresh_from_db()
        self.assertEqual(weight_max.off_left, 5000)
        self.assertEqual(weight_max.off_state, 5000)
        self.assertEqual(weight_max.deff_left, 0)
        self.assertEqual(weight_max.deff_state, 700)
        self.assertEqual(weight_max.nobleman_left, 0)
        self.assertEqual(weight_max.nobleman_state, 2)

        new_weight = WeightModel.objects.filter(start="500|500", target=target).last()
        self.assertEqual(new_weight.off, 0)  # type: ignore
        self.assertEqual(new_weight.deff, 700)  # type: ignore
        self.assertEqual(new_weight.nobleman, 1)  # type: ignore
        self.assertEqual(new_weight.order, -1)  # type: ignore
