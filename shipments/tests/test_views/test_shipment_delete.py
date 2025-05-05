import datetime

from django.urls import reverse

from base.tests.test_utils.mini_setup import MiniSetup
from shipments.models import Shipment


class TestShipmentDeleteView(MiniSetup):
    def test_shipment_delete___302_not_auth_redirect_login(self):
        shipment = Shipment.objects.create(
            owner=self.me(),
            name="Shipment 1",
            world=self.get_world(),
            date=datetime.date.today(),
        )
        PATH = reverse("shipments:shipment_delete", args=[shipment.pk])

        response = self.client.post(PATH)
        assert response.status_code == 302
        assert getattr(response, "url") == self.login_page_path(next=PATH)

    def test_shipment_delete___302_auth_works_ok(self):
        self.login_me()
        shipment = Shipment.objects.create(
            owner=self.me(),
            name="Shipment 1",
            world=self.get_world(),
            date=datetime.date.today(),
        )
        PATH = reverse("shipments:shipment_delete", args=[shipment.pk])
        REDIRECT = reverse("shipments:my_shipments") + "?show-hidden=false"

        response = self.client.post(PATH)
        assert response.status_code == 302
        assert getattr(response, "url") == REDIRECT
        assert Shipment.objects.count() == 0

    def test_shipment_delete___404_foreign_user_no_access(self):
        self.login_foreign_user()
        shipment = Shipment.objects.create(
            owner=self.me(),
            name="Shipment 1",
            world=self.get_world(),
            date=datetime.date.today(),
        )
        PATH = reverse("shipments:shipment_delete", args=[shipment.pk])

        response = self.client.post(PATH)
        assert response.status_code == 404
        assert Shipment.objects.count() == 1
