import datetime

from django.urls import reverse
from django.utils.translation import activate

from base.models.outline_overview import OutlineOverview
from base.models.overview import Overview
from base.tests.test_utils.mini_setup import MiniSetup
from shipments.models import Shipment


class TestAddEditShipmentView(MiniSetup):
    def test_add_shipment___302_not_auth_redirect_login(self):
        PATH = reverse("shipments:add_shipment")

        response = self.client.get(PATH)
        assert response.status_code == 302
        assert getattr(response, "url") == self.login_page_path(next=PATH)

    def test_add_shipment___200_auth_works_ok(self):
        self.login_me()
        PATH = reverse("shipments:add_shipment")

        response = self.client.get(PATH)
        assert response.status_code == 200

    def test_edit_shipment___302_not_auth_redirect_login(self):
        shipment = Shipment.objects.create(
            owner=self.me(),
            name="Shipment 1",
            world=self.get_world(),
            date=datetime.date.today(),
        )
        PATH = reverse("shipments:edit_shipment", args=[shipment.pk])

        response = self.client.get(PATH)
        assert response.status_code == 302
        assert getattr(response, "url") == self.login_page_path(next=PATH)

    def test_edit_shipment___200_auth_works_ok(self):
        self.login_me()
        shipment = Shipment.objects.create(
            owner=self.me(),
            name="Shipment 1",
            world=self.get_world(),
            date=datetime.date.today(),
        )
        PATH = reverse("shipments:edit_shipment", args=[shipment.pk])

        response = self.client.get(PATH)
        assert response.status_code == 200

    def test_edit_shipment___404_foreign_user_no_access(self):
        self.login_foreign_user()
        shipment = Shipment.objects.create(
            owner=self.me(),
            name="Shipment 1",
            world=self.get_world(),
            date=datetime.date.today(),
        )
        PATH = reverse("shipments:edit_shipment", args=[shipment.pk])

        response = self.client.get(PATH)
        assert response.status_code == 404

    def test_add_shipment___valid_data___shipment_created(self):
        self.login_me()
        PATH = reverse("shipments:add_shipment")

        outline = self.get_outline()
        outline_overview = OutlineOverview.objects.create(
            outline=outline,
            targets_json='{"1": {"target": "500|500"}}',
            weights_json='{"1": [{"player": "test", "off": 100,"nobleman":0,"distance":1}]}',
            world_json={"id": self.get_world().pk},
            outline_json={"date": str(datetime.date(2024, 1, 4))},
        )
        Overview.objects.create(
            outline_overview=outline_overview,
            token="testtoken",
            outline=outline,
            player="test",
            table="test",
            string="test",
        )

        data = {
            "name": "New Shipment",
            "form-TOTAL_FORMS": 1,
            "form-INITIAL_FORMS": 0,
            "form-MIN_NUM_FORMS": 1,
            "form-MAX_NUM_FORMS": 10,
            "form-0-token": "testtoken",
        }

        response = self.client.post(PATH, data)
        assert response.status_code == 302
        assert Shipment.objects.count() == 1
        shipment = Shipment.objects.first()
        assert shipment is not None
        assert shipment.name == "New Shipment"
        assert shipment.overviews.count() == 1

    def test_add_shipment___valid_data___shipment_created_for_2_overviews(self):
        self.login_me()
        PATH = reverse("shipments:add_shipment")

        outline = self.get_outline()
        outline_overview = OutlineOverview.objects.create(
            outline=outline,
            targets_json='{"1": {"target": "500|500"}}',
            weights_json='{"1": [{"player": "test", "off": 100,"nobleman":0,"distance":1}]}',
            world_json={"id": self.get_world().pk},
            outline_json={"date": str(datetime.date(2024, 1, 4))},
        )
        Overview.objects.create(
            outline_overview=outline_overview,
            token="testtoken",
            outline=outline,
            player="test",
            table="test",
            string="test",
        )
        outline2 = self.get_outline()
        outline_overview2 = OutlineOverview.objects.create(
            outline=outline2,
            targets_json='{"1": {"target": "500|500"}}',
            weights_json='{"1": [{"player": "test", "off": 100,"nobleman":0,"distance":1}]}',
            world_json={"id": self.get_world().pk},
            outline_json={"date": str(datetime.date(2024, 1, 4))},
        )
        Overview.objects.create(
            outline_overview=outline_overview2,
            token="testtoken2",
            outline=outline,
            player="test",
            table="test",
            string="test",
        )

        data = {
            "name": "New Shipment",
            "form-TOTAL_FORMS": 2,
            "form-INITIAL_FORMS": 0,
            "form-MIN_NUM_FORMS": 1,
            "form-MAX_NUM_FORMS": 10,
            "form-0-token": "testtoken",
            "form-1-token": "testtoken2",
        }

        response = self.client.post(PATH, data)
        assert response.status_code == 302
        assert Shipment.objects.count() == 1
        shipment = Shipment.objects.first()
        assert shipment is not None
        assert shipment.name == "New Shipment"
        assert shipment.overviews.count() == 2

    def test_edit_shipment___valid_data___shipment_edited(self):
        activate("en")
        self.login_me()
        world = self.get_world()
        shipment = Shipment.objects.create(
            owner=self.me(),
            name="Shipment 1",
            world=world,
            date=datetime.date.today(),
        )

        outline = self.get_outline()
        outline_overview = OutlineOverview.objects.create(
            outline=outline,
            targets_json='{"1": {"target": "500|500"}}',
            weights_json='{"1": [{"player": "test", "off": 100,"nobleman":0,"distance":1}]}',
            world_json={"id": self.get_world().pk},
            outline_json={"date": str(datetime.date(2024, 1, 4))},
        )
        Overview.objects.create(
            outline_overview=outline_overview,
            token="testtoken",
            outline=outline,
            player="test",
            table="test",
            string="test",
        )

        PATH = reverse("shipments:edit_shipment", args=[shipment.pk])
        data = {
            "name": "Shipment 1",
            "form-TOTAL_FORMS": 1,
            "form-INITIAL_FORMS": 0,
            "form-MIN_NUM_FORMS": 1,
            "form-MAX_NUM_FORMS": 10,
            "form-0-token": "testtoken",
        }

        response = self.client.post(PATH, data)
        assert response.status_code == 302
        shipment = Shipment.objects.get(pk=shipment.pk)
        assert shipment.overviews.count() == 1

    def test_add_shipment___valid_data___no_shipment_created_long_name(self):
        self.login_me()
        PATH = reverse("shipments:add_shipment")

        outline = self.get_outline()
        outline_overview = OutlineOverview.objects.create(
            outline=outline,
            targets_json='{"1": {"target": "500|500"}}',
            weights_json='{"1": [{"player": "test", "off": 100,"nobleman":0,"distance":1}]}',
            world_json={"id": self.get_world().pk},
            outline_json={"date": str(datetime.date(2024, 1, 4))},
        )
        Overview.objects.create(
            outline_overview=outline_overview,
            token="testtoken",
            outline=outline,
            player="test",
            table="test",
            string="test",
        )

        data = {
            "name": "New Shipment" * 10,
            "form-TOTAL_FORMS": 1,
            "form-INITIAL_FORMS": 0,
            "form-MIN_NUM_FORMS": 1,
            "form-MAX_NUM_FORMS": 10,
            "form-0-token": "testtoken",
        }

        response = self.client.post(PATH, data)
        assert response.status_code == 200
        assert Shipment.objects.count() == 0
        form = response.context["form"]
        assert form.errors == {
            "name": ["Ensure this value has at most 24 characters (it has 120)."],
        }
        formset = response.context["formset"]
        assert formset.errors == [{}]
        assert formset._non_form_errors == []

    def test_add_shipment___valid_data___no_shipment_created_long_token(self):
        self.login_me()
        PATH = reverse("shipments:add_shipment")

        outline = self.get_outline()
        outline_overview = OutlineOverview.objects.create(
            outline=outline,
            targets_json='{"1": {"target": "500|500"}}',
            weights_json='{"1": [{"player": "test", "off": 100,"nobleman":0,"distance":1}]}',
            world_json={"id": self.get_world().pk},
            outline_json={"date": str(datetime.date(2024, 1, 4))},
        )
        Overview.objects.create(
            outline_overview=outline_overview,
            token="testtoken",
            outline=outline,
            player="test",
            table="test",
            string="test",
        )

        data = {
            "name": "New Shipment",
            "form-TOTAL_FORMS": 1,
            "form-INITIAL_FORMS": 0,
            "form-MIN_NUM_FORMS": 1,
            "form-MAX_NUM_FORMS": 10,
            "form-0-token": "testtoken" * 50,
        }

        response = self.client.post(PATH, data)
        assert response.status_code == 200
        assert Shipment.objects.count() == 0
        form = response.context["form"]
        assert form.errors == {}
        formset = response.context["formset"]
        assert formset.errors == [
            {"token": ["Ensure this value has at most 100 characters (it has 450)."]}
        ]
        assert formset._non_form_errors == []

    def test_add_shipment___valid_data___no_shipment_created_duplicate_tokens(self):
        self.login_me()
        PATH = reverse("shipments:add_shipment")

        outline = self.get_outline()
        outline_overview = OutlineOverview.objects.create(
            outline=outline,
            targets_json='{"1": {"target": "500|500"}}',
            weights_json='{"1": [{"player": "test", "off": 100,"nobleman":0,"distance":1}]}',
            world_json={"id": self.get_world().pk},
            outline_json={"date": str(datetime.date(2024, 1, 4))},
        )
        Overview.objects.create(
            outline_overview=outline_overview,
            token="testtoken",
            outline=outline,
            player="test",
            table="test",
            string="test",
        )

        data = {
            "name": "New Shipment",
            "form-TOTAL_FORMS": 2,
            "form-INITIAL_FORMS": 0,
            "form-MIN_NUM_FORMS": 1,
            "form-MAX_NUM_FORMS": 10,
            "form-0-token": "testtoken",
            "form-1-token": "testtoken",
        }

        response = self.client.post(PATH, data)
        assert response.status_code == 200
        assert Shipment.objects.count() == 0
        form = response.context["form"]
        assert form.errors == {}
        formset = response.context["formset"]
        assert formset.errors == [{}, {}]
        assert formset._non_form_errors == [
            "Duplicate overview tokens are not allowed."
        ]

    def test_add_shipment___valid_data___no_shipment_2_empty_formsets(self):
        self.login_me()
        PATH = reverse("shipments:add_shipment")

        data = {
            "name": "New Shipment",
            "form-TOTAL_FORMS": 2,
            "form-INITIAL_FORMS": 0,
            "form-MIN_NUM_FORMS": 1,
            "form-MAX_NUM_FORMS": 10,
        }

        response = self.client.post(PATH, data)
        assert response.status_code == 200
        assert Shipment.objects.count() == 0
        form = response.context["form"]
        assert form.errors == {}
        formset = response.context["formset"]
        assert formset.errors == [
            {"token": ["This field is required."]},
            {},
        ]
        assert formset._non_form_errors == ["Please submit at least 1 form."]

    def test_add_shipment___valid_data___no_shipment_1_empty_formsets(self):
        self.login_me()
        PATH = reverse("shipments:add_shipment")

        data = {
            "name": "New Shipment",
            "form-TOTAL_FORMS": 1,
            "form-INITIAL_FORMS": 0,
            "form-MIN_NUM_FORMS": 1,
            "form-MAX_NUM_FORMS": 10,
        }

        response = self.client.post(PATH, data)
        assert response.status_code == 200
        assert Shipment.objects.count() == 0
        form = response.context["form"]
        assert form.errors == {}
        formset = response.context["formset"]
        assert formset.errors == [{"token": ["This field is required."]}]
        assert formset._non_form_errors == ["Please submit at least 1 form."]

    def test_add_shipment___valid_data___no_shipment_0_formset(self):
        activate("en")
        self.login_me()
        PATH = reverse("shipments:add_shipment")

        data = {
            "name": "New Shipment",
            "form-TOTAL_FORMS": 0,
            "form-INITIAL_FORMS": 0,
            "form-MIN_NUM_FORMS": 1,
            "form-MAX_NUM_FORMS": 10,
        }

        response = self.client.post(PATH, data)
        assert response.status_code == 200
        assert Shipment.objects.count() == 0
        form = response.context["form"]
        assert form.errors == {}
        formset = response.context["formset"]
        assert formset.errors == []
        assert formset._non_form_errors == ["Please submit at least 1 form."]

    def test_add_shipment___valid_data___no_shipment_11_formset(self):
        self.login_me()
        PATH = reverse("shipments:add_shipment")

        data = {
            "name": "New Shipment",
            "form-TOTAL_FORMS": 11,
            "form-INITIAL_FORMS": 0,
            "form-MIN_NUM_FORMS": 1,
            "form-MAX_NUM_FORMS": 10,
            "form-0-token": "testtoken",
            "form-1-token": "testtoken1",
            "form-2-token": "testtoken2",
            "form-3-token": "testtoken3",
            "form-4-token": "testtoken4",
            "form-5-token": "testtoken5",
            "form-6-token": "testtoken6",
            "form-7-token": "testtoken7",
            "form-8-token": "testtoken8",
            "form-9-token": "testtoken9",
            "form-10-token": "testtoken10",
        }

        response = self.client.post(PATH, data)
        assert response.status_code == 200
        assert Shipment.objects.count() == 0
        form = response.context["form"]
        assert form.errors == {}
        formset = response.context["formset"]
        assert formset.errors == [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}]
        assert formset._non_form_errors == ["Please submit at most 10 forms."]

    def test_add_shipment___invalid_overview___no_shipment_created(self):
        activate("en")
        self.login_me()
        PATH = reverse("shipments:add_shipment")

        data = {
            "name": "New Shipment",
            "form-TOTAL_FORMS": 1,
            "form-INITIAL_FORMS": 0,
            "form-MIN_NUM_FORMS": 1,
            "form-MAX_NUM_FORMS": 10,
            "form-0-token": "invalidtoken",
        }

        response = self.client.post(PATH, data)
        assert response.status_code == 200
        assert Shipment.objects.count() == 0
        assert "formset" in response.context
        formset = response.context["formset"]
        assert formset.errors == [{"token": [""]}]
        assert formset._non_form_errors == ["Invalid overview token: invalidtoken"]

    def test_add_shipment___different_world___error_raised(self):
        activate("en")
        self.login_me()
        PATH = reverse("shipments:add_shipment")

        outline1 = self.get_outline(name="1")
        outline_overview1 = OutlineOverview.objects.create(
            outline=outline1,
            targets_json='{"1": {"target": "500|500"}}',
            weights_json='{"1": [{"player": "test", "off": 100,"nobleman":0,"distance":1}]}',
            world_json={"id": self.get_world().pk},
            outline_json={"date": str(datetime.date(2024, 1, 4))},
        )
        Overview.objects.create(
            outline_overview=outline_overview1,
            token="testtoken1",
            outline=outline1,
            player="test",
            table="test",
            string="test",
        )

        outline2 = self.get_outline(name="2", test_world=True)
        outline_overview2 = OutlineOverview.objects.create(
            outline=outline2,
            targets_json='{"1": {"target": "500|500"}}',
            weights_json='{"1": [{"player": "test", "off": 100,"nobleman":0,"distance":1}]}',
            world_json={"id": self.get_world(test_world=True).pk},
            outline_json={"date": str(datetime.date(2024, 1, 4))},
        )
        Overview.objects.create(
            outline_overview=outline_overview2,
            token="testtoken2",
            outline=outline2,
            player="test",
            table="test",
            string="test",
        )

        data = {
            "name": "New Shipment",
            "form-TOTAL_FORMS": 2,
            "form-INITIAL_FORMS": 0,
            "form-MIN_NUM_FORMS": 1,
            "form-MAX_NUM_FORMS": 10,
            "form-0-token": "testtoken1",
            "form-1-token": "testtoken2",
        }

        response = self.client.post(PATH, data)
        assert response.status_code == 200
        formset = response.context["formset"]
        assert formset._non_form_errors == [
            "All overviews must belong to the same world."
        ]

    def test_add_shipment___different_player___error_raised(self):
        activate("en")
        self.login_me()
        PATH = reverse("shipments:add_shipment")

        outline1 = self.get_outline(name="1")
        outline_overview1 = OutlineOverview.objects.create(
            outline=outline1,
            targets_json='{"1": {"target": "500|500"}}',
            weights_json='{"1": [{"player": "test", "off": 100,"nobleman":0,"distance":1}]}',
            world_json={"id": self.get_world().pk},
            outline_json={"date": str(datetime.date(2024, 1, 4))},
        )
        Overview.objects.create(
            outline_overview=outline_overview1,
            token="testtoken1",
            outline=outline1,
            player="test",
            table="test",
            string="test",
        )

        outline2 = self.get_outline(name="2")
        outline_overview2 = OutlineOverview.objects.create(
            outline=outline2,
            targets_json='{"1": {"target": "500|500"}}',
            weights_json='{"1": [{"player": "test2", "off": 100,"nobleman":0,"distance":1}]}',
            world_json={"id": self.get_world().pk},
            outline_json={"date": str(datetime.date(2024, 1, 5))},
        )
        Overview.objects.create(
            outline_overview=outline_overview2,
            token="testtoken2",
            outline=outline2,
            player="test2",
            table="test",
            string="test",
        )

        data = {
            "name": "New Shipment",
            "form-TOTAL_FORMS": 2,
            "form-INITIAL_FORMS": 0,
            "form-MIN_NUM_FORMS": 1,
            "form-MAX_NUM_FORMS": 10,
            "form-0-token": "testtoken1",
            "form-1-token": "testtoken2",
        }

        response = self.client.post(PATH, data)
        assert response.status_code == 200
        formset = response.context["formset"]
        assert formset._non_form_errors == [
            "All overviews must be for the same player.",
            "test",
            "does not match",
            "test2",
        ]
