from django.urls import reverse

from base.forms import ChangeServerForm
from base.models import Profile
from base.tests.test_utils.mini_setup import MiniSetup


class OutlineProfileSettings(MiniSetup):
    def test_settings___302_not_auth_redirect_login(self):
        PATH = reverse("base:settings")

        response = self.client.get(PATH)
        assert response.status_code == 302
        assert response.url == self.login_page_path(next=PATH)

    def test_settings___200_foreign_user_works_ok(self):
        self.login_foreign_user()
        PATH = reverse("base:settings")

        response = self.client.get(PATH)
        assert response.status_code == 200

    def test_settings___200_auth_works_ok(self):
        PATH = reverse("base:settings")

        self.login_me()
        response = self.client.get(PATH)
        assert response.status_code == 200

    def test_settings___200_form_nonsense_errors(self):
        PATH = reverse("base:settings")

        self.login_me()
        response = self.client.post(PATH, data={"server": "xaxaxa", "form1": ""})
        assert response.status_code == 200
        form1: ChangeServerForm = response.context["form1"]
        assert len(form1.errors) == 1
        assert "server" in form1.errors

    def test_settings___302_form_works_correct(self):
        PATH = reverse("base:settings")
        world = self.get_world()

        me = self.me()
        profile: Profile = Profile.objects.get(user=me)
        profile.server = None
        profile.save()

        self.login_me()
        response = self.client.post(PATH, data={"server": "nottestserver", "form1": ""})
        assert response.status_code == 302
        assert response.url == PATH

        profile.refresh_from_db()
        assert profile.server is not None
