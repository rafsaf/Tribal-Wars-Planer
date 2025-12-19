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

from django.urls import reverse

from base.tests.test_utils.mini_setup import MiniSetup
from shipments.models import Shipment


class TestShipmentHideView(MiniSetup):
    def test_shipment_hide___302_not_auth_redirect_login(self):
        shipment = Shipment.objects.create(
            owner=self.me(),
            name="Shipment 1",
            world=self.get_world(),
            date=datetime.date.today(),
        )
        PATH = reverse("shipments:shipment_hide", args=[shipment.pk])

        response = self.client.post(PATH)
        assert response.status_code == 302
        assert getattr(response, "url") == self.login_page_path(next=PATH)

    def test_shipment_hide___302_auth_works_ok(self):
        self.login_me()
        shipment = Shipment.objects.create(
            owner=self.me(),
            name="Shipment 1",
            world=self.get_world(),
            date=datetime.date.today(),
        )
        PATH = reverse("shipments:shipment_hide", args=[shipment.pk])
        REDIRECT = reverse("shipments:my_shipments") + "?show-hidden=false"

        response = self.client.post(PATH)
        assert response.status_code == 302
        assert getattr(response, "url") == REDIRECT

    def test_shipment_hide___404_foreign_user_no_access(self):
        self.login_foreign_user()
        shipment = Shipment.objects.create(
            owner=self.me(),
            name="Shipment 1",
            world=self.get_world(),
            date=datetime.date.today(),
        )
        PATH = reverse("shipments:shipment_hide", args=[shipment.pk])

        response = self.client.post(PATH)
        assert response.status_code == 404

    def test_shipment_hide___hides_and_unhides_shipment(self):
        self.login_me()
        shipment = Shipment.objects.create(
            owner=self.me(),
            name="Shipment 1",
            world=self.get_world(),
            date=datetime.date.today(),
            hidden=False,
        )
        PATH = reverse("shipments:shipment_hide", args=[shipment.pk])

        self.client.post(PATH)
        shipment.refresh_from_db()
        assert shipment.hidden

        self.client.post(PATH)
        shipment.refresh_from_db()
        assert not shipment.hidden
