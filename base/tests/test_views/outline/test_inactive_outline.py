from django.urls import reverse

from base.tests.test_utils.mini_setup import MiniSetup


class InactiveOutline(MiniSetup):
    def test_planer_status___302_not_auth_redirect_login(self):
        outline = self.get_outline()
        PATH = reverse("base:planer_status", args=[outline.pk])

        response = self.client.get(PATH)
        assert response.status_code == 302
        assert response.url == self.login_page_path(next=PATH)

        response = self.client.post(PATH)
        assert response.status_code == 302
        assert response.url == self.login_page_path(next=PATH)

    def test_planer_status___404_foreign_user_no_access(self):
        outline = self.get_outline()
        PATH = reverse("base:planer_status", args=[outline.pk])

        self.login_foreign_user()
        response = self.client.get(PATH)
        assert response.status_code == 405

        response = self.client.post(PATH)
        assert response.status_code == 404

    def test_planer_status___302_auth_works_ok_status_active(self):
        outline = self.get_outline()
        outline.status = "active"
        outline.save()

        PATH = reverse("base:planer_status", args=[outline.pk])
        REDIRECT = reverse("base:planer")

        self.login_me()
        response = self.client.get(PATH)
        assert response.status_code == 405

        response = self.client.post(PATH)
        assert response.status_code == 302
        assert response.url == REDIRECT

        outline.refresh_from_db()
        assert outline.status == "inactive"

    def test_planer_status___302_auth_works_ok_status_inactive(self):
        outline = self.get_outline()
        outline.status = "inactive"
        outline.save()

        PATH = reverse("base:planer_status", args=[outline.pk])
        REDIRECT = reverse("base:planer_all")

        self.login_me()
        response = self.client.get(PATH)
        assert response.status_code == 405

        response = self.client.post(PATH)
        assert response.status_code == 302
        assert response.url == REDIRECT

        outline.refresh_from_db()
        assert outline.status == "active"
