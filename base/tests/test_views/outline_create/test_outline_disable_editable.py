from django.urls import reverse
from base.tests.utils.mini_setup import MiniSetup


class OutlinePlanerDisableEditable(MiniSetup):
    def test_planer_disable_editable___302_not_auth_redirect_login(self):
        PATH = reverse("base:planer_disable_editable", args=[1])

        response = self.client.get(PATH)
        assert response.status_code == 405

        response = self.client.post(PATH)
        assert response.status_code == 302
        assert response.url == self.login_page_path(next=PATH)

    def test_planer_disable_editable___404_foreign_user(self):
        self.login_foreign_user()
        outline = self.get_outline()
        PATH = reverse("base:planer_disable_editable", args=[outline.pk])

        response = self.client.get(PATH)
        assert response.status_code == 405
        response = self.client.post(PATH)
        assert response.status_code == 404

    def test_planer_disable_editable___302_auth_works_ok(self):
        outline = self.get_outline()
        PATH = reverse("base:planer_disable_editable", args=[outline.pk])
        REDIRECT = reverse("base:planer")

        self.login_me()
        response = self.client.get(PATH)
        assert response.status_code == 405

        outline.editable = "active"
        outline.save()

        response = self.client.post(PATH)
        assert response.status_code == 302
        assert response.url == REDIRECT

        outline.refresh_from_db()
        assert outline.editable == "inactive"
