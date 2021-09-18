from django.urls import reverse

from base.forms import EnemyTribeTagForm, MyTribeTagForm
from base.tests.test_utils.mini_setup import MiniSetup


class NewOutlineCreateSelect(MiniSetup):
    def test_planer_create_select___302_not_auth_redirect_login(self):
        PATH = reverse("base:planer_create_select", args=[1])

        response = self.client.get(PATH)

        assert response.status_code == 302
        assert response.url == self.login_page_path(next=PATH)

    def test_planer_create_select___404_foreign_user(self):
        self.login_foreign_user()
        outline = self.get_outline()
        PATH = reverse("base:planer_create_select", args=[outline.pk])

        response = self.client.get(PATH)
        assert response.status_code == 404

    def test_planer_create_select___200_auth(self):
        self.login_me()
        outline = self.get_outline()
        PATH = reverse("base:planer_create_select", args=[outline.pk])

        response = self.client.get(PATH)

        assert response.status_code == 200
        form1: MyTribeTagForm = response.context["form1"]
        form2: EnemyTribeTagForm = response.context["form2"]
        assert len(form1.errors) == 0
        assert len(form2.errors) == 0

    def test_planer_create_select___200_auth_nonsense_post(self):
        self.login_me()
        outline = self.get_outline()
        PATH = reverse("base:planer_create_select", args=[outline.pk])

        response = self.client.post(PATH, data={"nonsense": 5})

        assert response.status_code == 200
        form1: MyTribeTagForm = response.context["form1"]
        form2: EnemyTribeTagForm = response.context["form2"]
        assert len(form1.errors) == 0
        assert len(form2.errors) == 0

    def test_planer_create_select___302_correct_create_ally_tribe(self):
        self.login_me()
        outline = self.get_outline()
        self.create_tribe("ally")
        PATH = reverse("base:planer_create_select", args=[outline.pk])

        response = self.client.post(PATH, data={"tribe1": "ally"})

        assert response.status_code == 302
        assert response.url == PATH
        outline.refresh_from_db()
        assert outline.ally_tribe_tag == ["ally"]

    def test_planer_create_select___200_correct_error_invalid_ally_tag(self):
        self.login_me()
        outline = self.get_outline()
        PATH = reverse("base:planer_create_select", args=[outline.pk])

        response = self.client.post(PATH, data={"tribe1": "some_ally"})

        assert response.status_code == 200
        form1: MyTribeTagForm = response.context["form1"]
        assert len(form1.errors) == 1
        assert "tribe1" in form1.errors

    def test_planer_create_select___302_correct_create_enemy_tribe(self):
        self.login_me()
        outline = self.get_outline()
        self.create_tribe("enemy")
        PATH = reverse("base:planer_create_select", args=[outline.pk])

        response = self.client.post(PATH, data={"tribe2": "enemy"})

        assert response.status_code == 302
        assert response.url == PATH
        outline.refresh_from_db()
        assert outline.enemy_tribe_tag == ["enemy"]

    def test_planer_create_select___200_correct_error_invalid_enemy_tag(self):
        self.login_me()
        outline = self.get_outline()
        PATH = reverse("base:planer_create_select", args=[outline.pk])

        response = self.client.post(PATH, data={"tribe2": "some_ally"})

        assert response.status_code == 200
        form2: EnemyTribeTagForm = response.context["form2"]
        assert len(form2.errors) == 1
        assert "tribe2" in form2.errors
