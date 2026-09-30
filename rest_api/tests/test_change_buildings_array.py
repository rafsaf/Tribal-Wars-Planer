# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

import json

from django.urls import reverse

from base.tests.test_utils.mini_setup import MiniSetup
from utils.buildings import BUILDING


class ChangeBuildingsArray(MiniSetup):
    def test_change_buildings_array___403_not_auth(self):
        outline = self.get_outline()

        PATH = reverse("rest_api:change_buildings_array")
        response = self.client.put(
            PATH,
            data=json.dumps(
                {
                    "buildings": [
                        BUILDING.STABLE.value,
                        BUILDING.WORKSHOP.value,
                        BUILDING.ACADEMY.value,
                        BUILDING.SMITHY.value,
                    ],
                    "outline_id": outline.pk,
                }
            ),
            content_type="application/json",
        )
        assert response.status_code == 403

    def test_change_buildings_array___404_foreign_user_has_no_access(self):
        outline = self.get_outline()

        PATH = reverse("rest_api:change_buildings_array")

        self.login_foreign_user()
        response = self.client.put(
            PATH,
            data=json.dumps(
                {
                    "buildings": [
                        BUILDING.STABLE.value,
                        BUILDING.WORKSHOP.value,
                        BUILDING.ACADEMY.value,
                        BUILDING.SMITHY.value,
                    ],
                    "outline_id": outline.pk,
                }
            ),
            content_type="application/json",
        )
        assert response.status_code == 404

    def test_change_buildings_array___200_target_is_deleted_properly(self):
        outline = self.get_outline()

        PATH = reverse("rest_api:change_buildings_array")

        self.login_me()
        response = self.client.put(
            PATH,
            data=json.dumps(
                {
                    "buildings": [
                        BUILDING.STABLE.value,
                        BUILDING.WORKSHOP.value,
                        BUILDING.ACADEMY.value,
                        BUILDING.SMITHY.value,
                    ],
                    "outline_id": outline.pk,
                }
            ),
            content_type="application/json",
        )

        assert response.status_code == 200
        outline.refresh_from_db()
        assert outline.initial_outline_buildings == [
            BUILDING.STABLE.value,
            BUILDING.WORKSHOP.value,
            BUILDING.ACADEMY.value,
            BUILDING.SMITHY.value,
        ]

    def test_change_buildings_array___400_invalid_building_name(self):
        outline = self.get_outline()
        fake_building_name = self.random_lower_string()

        PATH = reverse("rest_api:change_buildings_array")

        self.login_me()

        response = self.client.put(
            PATH,
            data=json.dumps(
                {
                    "buildings": [fake_building_name],
                    "outline_id": outline.pk,
                }
            ),
            content_type="application/json",
        )

        assert response.status_code == 400
        assert response.json() == {
            "buildings": [f"Invalid building: {fake_building_name}"]
        }

    def test_change_buildings_array___400_double_building_name(self):
        outline = self.get_outline()

        PATH = reverse("rest_api:change_buildings_array")

        self.login_me()

        response = self.client.put(
            PATH,
            data=json.dumps(
                {
                    "buildings": [BUILDING.STABLE.value, BUILDING.STABLE.value],
                    "outline_id": outline.pk,
                }
            ),
            content_type="application/json",
        )

        assert response.status_code == 400
        assert response.json() == {
            "buildings": ["Building occured more than once: stable"]
        }

    def test_change_buildings_array___400_empty_list(self) -> None:
        outline = self.get_outline()

        PATH = reverse("rest_api:change_buildings_array")

        self.login_me()

        response = self.client.put(
            PATH,
            data=json.dumps(
                {
                    "buildings": [],
                    "outline_id": outline.pk,
                }
            ),
            content_type="application/json",
        )

        assert response.status_code == 400
        assert response.json() == {"buildings": ["Buildings list is empty"]}
