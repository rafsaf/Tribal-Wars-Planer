from base.models import Outline
from django.urls import reverse
from base.tests.utils.mini_setup import MiniSetup


class InactiveOutline(MiniSetup):
    def test_planer_detail___302_not_auth_redirect_login(self):
        outline = self.get_outline()
        PATH = reverse("base:planer_detail", args=[outline.pk])

        response = self.client.get(PATH)
        assert response.status_code == 302
        assert response.url == self.login_page_path(next=PATH)

    def test_planer_detail___404_foreign_user_no_access(self):
        outline = self.get_outline(editable="inactive")
        PATH = reverse("base:planer_detail", args=[outline.pk])

        self.login_foreign_user()
        response = self.client.get(PATH)
        assert response.status_code == 404

    def test_planer_detail___404_auth_editable_is_removed_do_not_touch_others(self):
        outline = self.get_outline()
        foreign_outline = self.create_foreign_outline()
        PATH = reverse("base:planer_detail", args=[outline.pk])

        self.login_me()
        assert Outline.objects.count() == 2
        response = self.client.get(PATH)
        assert Outline.objects.count() == 1
        assert response.status_code == 404

    def test_planer_detail___200_auth_works_ok(self):
        outline = self.get_outline(editable="inactive")

        PATH = reverse("base:planer_detail", args=[outline.pk])

        self.login_me()
        response = self.client.get(PATH)
        assert response.status_code == 200

    def test_planer_detail___302_auth_works_ok_on_Test_world_army_troops(self):
        outline = self.get_outline(editable="inactive", test_world=True)
        assert outline.ally_tribe_tag == ["ALLY"]

        PATH = reverse("base:planer_detail", args=[outline.pk])
        TROOPS = "100|100,100,100,7000,0,100,2800,0,0,350,100,0,0,0,0,0,"
        self.login_me()
        response = self.client.post(
            PATH,
            data={
                "form-1": "",
                "off_troops": TROOPS,
            },
        )
        assert response.status_code == 302
        assert response.url == PATH

        outline.refresh_from_db()
        assert outline.off_troops == TROOPS

    def test_planer_detail___302_auth_works_ok_on_Test_world_deff_troops(self):
        outline = self.get_outline(editable="inactive", test_world=True)

        PATH = reverse("base:planer_detail", args=[outline.pk])
        DEFF = "101|101,w wiosce,100,100,7001,0,100,2801,0,0,350,100,0,0,0,0,"
        self.login_me()
        response = self.client.post(
            PATH,
            data={
                "form-2": "",
                "deff_troops": DEFF,
            },
        )
        assert response.status_code == 302
        assert response.url == PATH

        outline.refresh_from_db()
        assert outline.deff_troops == DEFF

    def test_planer_detail___200_auth_form_error_when_nonsense(self):
        outline = self.get_outline(editable="inactive", test_world=True)

        PATH = reverse("base:planer_detail", args=[outline.pk])
        DEFF = "101|101,some_big_nonsene"
        self.login_me()
        response = self.client.post(
            PATH,
            data={
                "form-2": "",
                "deff_troops": DEFF,
            },
        )
        assert response.status_code == 200
        deff_troops = response.context["deff_troops"]
        assert len(deff_troops.errors) == 1

        outline.refresh_from_db()
        assert outline.deff_troops == ""
