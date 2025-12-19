# Copyright 2025 Rafał Safin (rafsaf). All Rights Reserved.
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

import datetime
import json

from django.core.serializers.json import DjangoJSONEncoder
from django.urls import reverse
from rest_framework import status

from base.models.outline import Outline
from base.models.outline_overview import OutlineOverview
from base.models.overview import Overview
from base.tests.test_utils.mini_setup import MiniSetup
from shipments.models import Shipment


class TestShipmentOverviews(MiniSetup):
    def setUp(self):
        super().setUp()
        self.world = self.get_world()
        self.shipment = Shipment.objects.create(
            name="Test Shipment",
            owner=self.me(),
            date="2024-01-01",
            world=self.world,
        )
        self.outline = Outline.objects.create(
            owner=self.me(),
            name="Test Outline",
            world=self.world,
        )
        self.outline_overview = OutlineOverview.objects.create(
            outline=self.outline,
            targets_json=json.dumps(
                {
                    "1": {
                        "id": 1,
                        "target": "500|500",
                        "player": "target-player",
                        "fake": False,
                        "ruin": False,
                        "village_id": 100,
                        "player_id": 500,
                    }
                },
                cls=DjangoJSONEncoder,
            ),
            weights_json=json.dumps(
                {
                    "1": [
                        {
                            "id": 50,
                            "start": "501|501",
                            "player": "weight-test",
                            "off": 100,
                            "nobleman": 0,
                            "catapult": 0,
                            "ruin": False,
                            "distance": 1,
                            "time_seconds": 1,
                            "t1": datetime.time(1, 1, 1, 0),
                            "t2": datetime.time(1, 1, 1, 0),
                            "building": "stable",
                            "delivery_t1": datetime.datetime(
                                2022, 1, 5, 1, 1, 1, 1, tzinfo=datetime.UTC
                            ),
                            "delivery_t2": datetime.datetime(
                                2022, 1, 5, 1, 1, 1, 1, tzinfo=datetime.UTC
                            ),
                            "shipment_t1": datetime.datetime(
                                2021, 1, 5, 1, 1, 1, 1, tzinfo=datetime.UTC
                            ),
                            "shipment_t2": datetime.datetime(
                                2021, 1, 5, 1, 1, 1, 1, tzinfo=datetime.UTC
                            ),
                            "village_id": 444,
                            "player_id": 444,
                            "send_url": "http://example.com",
                            "send_url_text": "Send OFF",
                        },
                        {
                            "id": 100,
                            "start": "501|900",
                            "player": "other",
                            "off": 100,
                            "nobleman": 0,
                            "catapult": 0,
                            "ruin": False,
                            "distance": 1,
                            "time_seconds": 1,
                            "t1": datetime.time(1, 1, 1, 0),
                            "t2": datetime.time(1, 1, 1, 0),
                            "building": "stable",
                            "delivery_t1": datetime.datetime(
                                2022, 1, 5, 1, 1, 1, 1, tzinfo=datetime.UTC
                            ),
                            "delivery_t2": datetime.datetime(
                                2022, 1, 5, 1, 1, 1, 1, tzinfo=datetime.UTC
                            ),
                            "shipment_t1": datetime.datetime(
                                2021, 1, 5, 1, 1, 1, 1, tzinfo=datetime.UTC
                            ),
                            "shipment_t2": datetime.datetime(
                                2021, 1, 5, 1, 1, 1, 1, tzinfo=datetime.UTC
                            ),
                            "village_id": 4444,
                            "player_id": 4444,
                            "send_url": "http://example.com",
                            "send_url_text": "Send OFF",
                        },
                    ]
                },
                cls=DjangoJSONEncoder,
            ),
            world_json={
                "id": self.world.pk,
                "name": "pl180",
                "server": "server name",
                "full_game_name": "world name",
                "speed_units": 5.2,
                "speed_world": 5.2,
            },
            outline_json={"date": "2024-01-01", "id": self.outline.pk},
        )
        self.overview = Overview.objects.create(
            outline_overview=self.outline_overview,
            token="testtoken",
            outline=self.outline,
            player="weight-test",
            table="test",
            string="test",
        )
        self.shipment.overviews.add(self.overview)
        self.PATH = reverse(
            "rest_api:shipment_overviews", kwargs={"pk": self.shipment.pk}
        )

    def test_shipment_overviews___403_not_authenticated(self):
        response = self.client.get(self.PATH)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_shipment_overviews___404_foreign_user_no_access(self):
        self.login_foreign_user()
        response = self.client.get(self.PATH)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_shipment_overviews___200_one_overview(self):
        self.login_me()
        with self.assertNumQueries(5):
            response = self.client.get(self.PATH)
        assert response.status_code == status.HTTP_200_OK, response.content
        data = json.loads(response.content)
        assert data["outline"]["date"] == "2024-01-01", data
        assert data["world"]["id"] == self.world.pk
        assert len(data["targets"]) == 1
        assert data["targets"][0]["target"]["id"] == 1
        assert len(data["targets"][0]["my_orders"]) == 1
        assert data["targets"][0]["my_orders"][0]["id"] == 50
        assert data["targets"][0]["my_orders"][0]["off"] == 100
        assert data["targets"][0]["my_orders"][0]["nobleman"] == 0
        assert data["targets"][0]["my_orders"][0]["distance"] == 1

    def test_shipment_overviews___200_two_overviews(self):
        outline_overview2 = OutlineOverview.objects.create(
            outline=self.outline,
            targets_json=json.dumps(
                {
                    "6": {
                        "id": 6,
                        "target": "500|499",
                        "player": "target-player",
                        "fake": False,
                        "ruin": False,
                        "village_id": 100,
                        "player_id": 500,
                    }
                },
                cls=DjangoJSONEncoder,
            ),
            weights_json=json.dumps(
                {
                    "6": [
                        {
                            "id": 500,
                            "start": "505|505",
                            "player": "weight-test",
                            "off": 200,
                            "nobleman": 1,
                            "catapult": 0,
                            "ruin": False,
                            "distance": 2,
                            "time_seconds": 1,
                            "t1": datetime.time(1, 1, 1, 0),
                            "t2": datetime.time(1, 1, 1, 0),
                            "building": "stable",
                            "delivery_t1": datetime.datetime(
                                2022, 1, 5, 1, 1, 1, 1, tzinfo=datetime.UTC
                            ),
                            "delivery_t2": datetime.datetime(
                                2022, 1, 5, 1, 1, 1, 1, tzinfo=datetime.UTC
                            ),
                            "shipment_t1": datetime.datetime(
                                2021, 1, 5, 1, 1, 1, 1, tzinfo=datetime.UTC
                            ),
                            "shipment_t2": datetime.datetime(
                                2021, 1, 5, 1, 1, 1, 1, tzinfo=datetime.UTC
                            ),
                            "village_id": 444,
                            "player_id": 444,
                            "send_url": "http://example.com",
                            "send_url_text": "Send OFF",
                        },
                        {
                            "id": 5000,
                            "start": "510|505",
                            "player": "weight-test2",
                            "off": 200,
                            "nobleman": 0,
                            "catapult": 0,
                            "ruin": False,
                            "distance": 1,
                            "time_seconds": 1,
                            "t1": datetime.time(1, 1, 1, 0),
                            "t2": datetime.time(1, 1, 1, 0),
                            "building": "stable",
                            "delivery_t1": datetime.datetime(
                                2022, 1, 5, 1, 1, 1, 1, tzinfo=datetime.UTC
                            ),
                            "delivery_t2": datetime.datetime(
                                2022, 1, 5, 1, 1, 1, 1, tzinfo=datetime.UTC
                            ),
                            "shipment_t1": datetime.datetime(
                                2021, 1, 5, 1, 1, 1, 1, tzinfo=datetime.UTC
                            ),
                            "shipment_t2": datetime.datetime(
                                2021, 1, 5, 1, 1, 1, 1, tzinfo=datetime.UTC
                            ),
                            "village_id": 44466,
                            "player_id": 44466,
                            "send_url": "http://example.com",
                            "send_url_text": "Send OFF",
                        },
                    ]
                },
                cls=DjangoJSONEncoder,
            ),
            world_json={
                "id": self.world.pk,
                "name": "pl180",
                "server": "server name",
                "full_game_name": "world name",
                "speed_units": 5.2,
                "speed_world": 5.2,
            },
            outline_json={"date": "2024-02-02", "id": self.outline.pk},
        )
        overview2 = Overview.objects.create(
            outline_overview=outline_overview2,
            token="testtoken2",
            outline=self.outline,
            player="weight-test",
            table="test2",
            string="test2",
        )
        self.shipment.overviews.add(overview2)

        self.login_me()
        with self.assertNumQueries(5):
            response = self.client.get(self.PATH)
        assert response.status_code == status.HTTP_200_OK
        data = json.loads(response.content)

        assert data["outline"]["date"] == "2024-01-01"
        assert data["world"]["id"] == self.world.pk
        assert len(data["targets"]) == 2
        assert data["targets"][0]["target"]["id"] == 1
        assert len(data["targets"][0]["my_orders"]) == 1
        assert data["targets"][0]["my_orders"][0]["id"] == 50
        assert data["targets"][0]["my_orders"][0]["off"] == 100
        assert data["targets"][0]["my_orders"][0]["nobleman"] == 0
        assert data["targets"][0]["my_orders"][0]["distance"] == 1

        assert data["targets"][1]["target"]["id"] == 6
        assert len(data["targets"][1]["my_orders"]) == 1
        assert data["targets"][1]["my_orders"][0]["id"] == 500
        assert data["targets"][1]["my_orders"][0]["off"] == 200
        assert data["targets"][1]["my_orders"][0]["nobleman"] == 1
        assert data["targets"][1]["my_orders"][0]["distance"] == 2

    def test_shipment_overviews___200_no_overviews(self):
        self.shipment.overviews.clear()
        self.login_me()
        response = self.client.get(self.PATH)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_shipment_overviews___invalid_language___defaults_to_english(self):
        self.login_me()
        PATH = (
            reverse("rest_api:shipment_overviews", kwargs={"pk": self.shipment.pk})
            + "?language=invalid"
        )
        response = self.client.get(PATH)
        assert response.status_code == status.HTTP_200_OK
        # Add assertions to check if the response is in English (or the default language)
