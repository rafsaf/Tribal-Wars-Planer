import json

from django.urls import reverse

from base.tests.test_utils.mini_setup import MiniSetup
from shipments.models import Shipment

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


class TestShipmentAddToSendLst(MiniSetup):
    def setUp(self):
        super().setUp()
        self.shipment = Shipment.objects.create(
            name="Test Shipment",
            owner=self.me(),
            date="2024-01-01",
            world=self.get_world(),
        )

    def test_add_to_send_lst___403_not_auth(self):
        PATH = reverse(
            "rest_api:shipment_add_to_send_lst", kwargs={"pk": self.shipment.pk}
        )
        response = self.client.post(
            PATH, data=json.dumps({"id": 123}), content_type="application/json"
        )
        assert response.status_code == 403

    def test_add_to_send_lst___404_foreign_user_has_no_access(self):
        PATH = reverse(
            "rest_api:shipment_add_to_send_lst", kwargs={"pk": self.shipment.pk}
        )
        self.login_foreign_user()
        response = self.client.post(
            PATH, data=json.dumps({"id": 123}), content_type="application/json"
        )
        assert response.status_code == 404

    def test_add_to_send_lst___200_add_id_to_sent_lst(self):
        PATH = reverse(
            "rest_api:shipment_add_to_send_lst", kwargs={"pk": self.shipment.pk}
        )
        self.login_me()
        response = self.client.post(
            PATH, data=json.dumps({"id": 123}), content_type="application/json"
        )
        assert response.status_code == 200
        self.shipment.refresh_from_db()
        assert self.shipment.sent_lst == [123]

    def test_add_to_send_lst___200_add_multiple_ids_to_sent_lst(self):
        self.shipment.sent_lst = [1, 2, 3]
        self.shipment.save()
        PATH = reverse(
            "rest_api:shipment_add_to_send_lst", kwargs={"pk": self.shipment.pk}
        )
        self.login_me()
        response = self.client.post(
            PATH, data=json.dumps({"id": 4}), content_type="application/json"
        )
        assert response.status_code == 200
        self.shipment.refresh_from_db()
        assert self.shipment.sent_lst == [1, 2, 3, 4]

    def test_add_to_send_lst___400_invalid_id(self):
        PATH = reverse(
            "rest_api:shipment_add_to_send_lst", kwargs={"pk": self.shipment.pk}
        )
        self.login_me()
        response = self.client.post(
            PATH, data=json.dumps({"id": "abc"}), content_type="application/json"
        )
        assert response.status_code == 400
        assert response.json() == {"id": ["A valid integer is required."]}

    def test_add_to_send_lst___400_missing_id(self):
        PATH = reverse(
            "rest_api:shipment_add_to_send_lst", kwargs={"pk": self.shipment.pk}
        )
        self.login_me()
        response = self.client.post(
            PATH, data=json.dumps({}), content_type="application/json"
        )
        assert response.status_code == 400
        assert response.json() == {"id": ["This field is required."]}
