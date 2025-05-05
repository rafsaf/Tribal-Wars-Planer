import datetime

from django.urls import reverse

from base.tests.test_utils.mini_setup import MiniSetup
from shipments.models import Shipment


class TestShipmentSendView(MiniSetup):
    def test_shipment_send___302_not_auth_redirect_login(self):
        shipment = Shipment.objects.create(
            owner=self.me(),
            name="Shipment 1",
            world=self.get_world(),
            date=datetime.date.today(),
        )
        PATH = reverse("shipments:shipment", args=[shipment.pk])

        response = self.client.get(PATH)
        assert response.status_code == 302
        assert getattr(response, "url") == self.login_page_path(next=PATH)

    def test_shipment_send___200_auth_works_ok(self):
        self.login_me()
        shipment = Shipment.objects.create(
            owner=self.me(),
            name="Shipment 1",
            world=self.get_world(),
            date=datetime.date.today(),
        )
        PATH = reverse("shipments:shipment", args=[shipment.pk])

        response = self.client.get(PATH)
        assert response.status_code == 200

    def test_shipment_send___404_foreign_user_no_access(self):
        self.login_foreign_user()
        shipment = Shipment.objects.create(
            owner=self.me(),
            name="Shipment 1",
            world=self.get_world(),
            date=datetime.date.today(),
        )
        PATH = reverse("shipments:shipment", args=[shipment.pk])

        response = self.client.get(PATH)
        assert response.status_code == 404
