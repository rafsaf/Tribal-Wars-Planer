import datetime

from django.urls import reverse

from base.tests.test_utils.mini_setup import MiniSetup
from shipments.models import Shipment


class TestMyShipmentsView(MiniSetup):
    def test_my_shipments___302_not_auth_redirect_login(self):
        PATH = reverse("shipments:my_shipments")

        response = self.client.get(PATH)
        assert response.status_code == 302
        assert getattr(response, "url") == self.login_page_path(next=PATH)

    def test_my_shipments___200_auth_works_ok(self):
        PATH = reverse("shipments:my_shipments")

        self.login_me()
        response = self.client.get(PATH)
        assert response.status_code == 200

    def test_my_shipments___200_auth_shows_shipments_for_user(self):
        self.login_me()
        PATH = reverse("shipments:my_shipments")
        shipment1 = Shipment.objects.create(
            owner=self.me(),
            name="Shipment 1",
            world=self.get_world(),
            date=datetime.date.today(),
        )
        shipment2 = Shipment.objects.create(
            owner=self.me(),
            name="Shipment 2",
            world=self.get_world(),
            date=datetime.date.today(),
        )
        Shipment.objects.create(
            owner=self.foreign_user(),
            name="Foreign Shipment",
            world=self.get_world(),
            date=datetime.date.today(),
        )
        response = self.client.get(PATH)
        assert response.status_code == 200
        shipments = response.context["shipments"]
        assert len(shipments) == 2
        assert shipment1 in shipments
        assert shipment2 in shipments

    def test_my_shipments___200_auth_hides_hidden_shipments_by_default(self):
        self.login_me()
        PATH = reverse("shipments:my_shipments")
        shipment1 = Shipment.objects.create(
            owner=self.me(),
            name="Shipment 1",
            world=self.get_world(),
            hidden=True,
            date=datetime.date.today(),
        )
        shipment2 = Shipment.objects.create(
            owner=self.me(),
            name="Shipment 2",
            world=self.get_world(),
            hidden=False,
            date=datetime.date.today(),
        )
        response = self.client.get(PATH)
        assert response.status_code == 200
        shipments = response.context["shipments"]
        assert len(shipments) == 1
        assert shipment2 in shipments
        assert shipment1 not in shipments

    def test_my_shipments___200_auth_shows_hidden_shipments_with_show_hidden_param(
        self,
    ):
        self.login_me()
        PATH = reverse("shipments:my_shipments") + "?show-hidden=true"
        shipment1 = Shipment.objects.create(
            owner=self.me(),
            name="Shipment 1",
            world=self.get_world(),
            hidden=True,
            date=datetime.date.today(),
        )
        shipment2 = Shipment.objects.create(
            owner=self.me(),
            name="Shipment 2",
            world=self.get_world(),
            hidden=False,
            date=datetime.date.today(),
        )
        response = self.client.get(PATH)
        assert response.status_code == 200
        shipments = response.context["shipments"]
        assert len(shipments) == 2
        assert shipment1 in shipments
        assert shipment2 in shipments

    def test_my_shipments___200_auth_foreign_user_sees_nothing(self):
        self.login_foreign_user()
        PATH = reverse("shipments:my_shipments")
        Shipment.objects.create(
            owner=self.me(),
            name="Shipment 1",
            world=self.get_world(),
            date=datetime.date.today(),
        )
        response = self.client.get(PATH)
        assert response.status_code == 200
        shipments = response.context["shipments"]
        assert len(shipments) == 0
