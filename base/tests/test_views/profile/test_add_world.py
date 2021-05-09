from django.urls import reverse
from base.tests.utils.mini_setup import MiniSetup


class OutlineAddWorld(MiniSetup):
    def test_add_world___302_not_auth_redirect_login(self):
        PATH = reverse("base:add_world")

        response = self.client.get(PATH)
        assert response.status_code == 302
        assert response.url == self.login_page_path(next=PATH)

    def test_add_world___200_foreign_user_works_ok(self):
        self.login_foreign_user()
        PATH = reverse("base:add_world")

        response = self.client.get(PATH)
        assert response.status_code == 200

    def test_add_world___200_auth_works_ok(self):
        PATH = reverse("base:add_world")

        self.login_me()
        response = self.client.get(PATH)
        assert response.status_code == 200
