# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

import json

from django.urls import reverse

from base.models import TargetVertex
from base.tests.test_utils.mini_setup import MiniSetup
from utils.buildings import BUILDING, BUILDINGS_TRANSLATION


class ChangeWeightModelBuilding(MiniSetup):
    def test_change_weight_building___403_not_auth(self):
        outline = self.get_outline()
        self.create_target_on_test_world(outline)
        target = TargetVertex.objects.get(target="200|200")
        weight_max = self.create_weight_maximum(outline)
        weight = self.create_weight(target=target, weight_max=weight_max)

        PATH = reverse("rest_api:change_weight_building")

        response = self.client.put(
            PATH,
            data=json.dumps(
                {
                    "building": BUILDING.HEADQUARTERS.value,
                    "outline_id": outline.pk,
                    "weight_id": weight.pk,
                }
            ),
            content_type="application/json",
        )
        assert response.status_code == 403

    def test_change_weight_building___404_foreign_user_has_no_access(self):
        outline = self.get_outline()
        self.create_target_on_test_world(outline)
        target = TargetVertex.objects.get(target="200|200")
        weight_max = self.create_weight_maximum(outline)
        weight = self.create_weight(target=target, weight_max=weight_max)

        PATH = reverse("rest_api:change_weight_building")

        self.login_foreign_user()

        response = self.client.put(
            PATH,
            data=json.dumps(
                {
                    "building": BUILDING.HEADQUARTERS.value,
                    "outline_id": outline.pk,
                    "weight_id": weight.pk,
                }
            ),
            content_type="application/json",
        )
        assert response.status_code == 404

    def test_change_weight_building___404_cannot_update_foreign_weight_with_my_outline(
        self,
    ):
        my_outline = self.get_outline()

        foreign_outline = self.create_foreign_outline()
        self.create_target_on_test_world(foreign_outline)
        foreign_target = TargetVertex.objects.get(
            target="200|200", outline=foreign_outline
        )
        foreign_weight_max = self.create_weight_maximum(foreign_outline)
        foreign_weight = self.create_weight(
            target=foreign_target, weight_max=foreign_weight_max
        )

        PATH = reverse("rest_api:change_weight_building")

        self.login_me()

        response = self.client.put(
            PATH,
            data=json.dumps(
                {
                    "building": BUILDING.HEADQUARTERS.value,
                    "outline_id": my_outline.pk,
                    "weight_id": foreign_weight.pk,
                }
            ),
            content_type="application/json",
        )

        assert response.status_code == 404

    def test_change_weight_building___200_building_is_changed_properly(self):
        outline = self.get_outline()
        self.create_target_on_test_world(outline)
        target = TargetVertex.objects.get(target="200|200")
        weight_max = self.create_weight_maximum(outline)
        weight = self.create_weight(target=target, weight_max=weight_max)

        PATH = reverse("rest_api:change_weight_building")

        self.login_me()
        response = self.client.put(
            PATH,
            data=json.dumps(
                {
                    "building": BUILDING.HEADQUARTERS.value,
                    "outline_id": outline.pk,
                    "weight_id": weight.pk,
                }
            ),
            content_type="application/json",
        )
        assert response.json() == {
            "name": BUILDINGS_TRANSLATION[BUILDING.HEADQUARTERS.value]
        }

        assert response.status_code == 200
        weight.refresh_from_db()
        assert weight.building == BUILDING.HEADQUARTERS.value

    def test_change_weight_building___400_building_name_invalid(self):
        outline = self.get_outline()
        self.create_target_on_test_world(outline)
        target = TargetVertex.objects.get(target="200|200")
        weight_max = self.create_weight_maximum(outline)
        weight = self.create_weight(target=target, weight_max=weight_max)

        PATH = reverse("rest_api:change_weight_building")

        self.login_me()
        fake_building_name = self.random_lower_string()
        response = self.client.put(
            PATH,
            data=json.dumps(
                {
                    "building": fake_building_name,
                    "outline_id": outline.pk,
                    "weight_id": weight.pk,
                }
            ),
            content_type="application/json",
        )

        assert response.status_code == 400
        assert response.json() == {
            "building": [f"Invalid building: {fake_building_name}"]
        }
