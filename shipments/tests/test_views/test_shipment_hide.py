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
