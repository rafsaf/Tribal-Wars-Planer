from base.models import Outline
from django.urls import reverse
from base.tests.utils.mini_setup import MiniSetup


class OutlineList(MiniSetup):
    def test_planer___302_not_auth_redirect_login(self):
        PATH = reverse("base:planer")

        response = self.client.get(PATH)
        assert response.status_code == 302
        assert response.url == self.login_page_path(next=PATH)

    def test_planer___200_foreign_user_works_ok(self):
        self.login_foreign_user()
        PATH = reverse("base:planer")

        response = self.client.get(PATH)
        assert response.status_code == 200

    def test_planer___200_auth_works_ok(self):
        PATH = reverse("base:planer")

        self.login_me()
        response = self.client.get(PATH)
        assert response.status_code == 200

    def test_planer___200_auth_remove_editable_outline_leave_foreign_outline(self):
        PATH = reverse("base:planer")
        foreign_outline = self.create_foreign_outline()
        outline = self.get_outline()
        self.login_me()
        assert Outline.objects.count() == 2
        response = self.client.get(PATH)
        assert response.status_code == 200
        query = response.context["object_list"]
        assert len(query) == 0
        assert Outline.objects.count() == 1

    def test_planer___200_auth_show_active_outline(self):
        PATH = reverse("base:planer")
        outline = self.get_outline()
        outline.status = "active"
        outline.editable = "inactive"
        outline.save()

        self.login_me()
        response = self.client.get(PATH)
        assert response.status_code == 200
        query = response.context["object_list"]
        assert len(query) == 1
        assert Outline.objects.count() == 1

    def test_planer___200_auth_not_show_inactive_outline(self):
        PATH = reverse("base:planer")
        outline = self.get_outline()
        outline.status = "inactive"
        outline.editable = "inactive"
        outline.save()

        self.login_me()
        response = self.client.get(PATH)
        assert response.status_code == 200
        query = response.context["object_list"]
        assert len(query) == 0
        assert Outline.objects.count() == 1