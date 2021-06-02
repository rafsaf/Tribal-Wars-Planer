from django.urls import reverse

from base.models import Outline, WeightMaximum
from base.tests.utils.mini_setup import MiniSetup


class InitialForm(MiniSetup):
    def test_planer_initial_form___302_not_auth_redirect_login(self):
        outline = self.get_outline()
        PATH = reverse("base:planer_initial_form", args=[outline.pk])

        response = self.client.get(PATH)
        assert response.status_code == 302
        assert response.url == self.login_page_path(next=PATH)

    def test_planer_initial_form___404_foreign_user_no_access(self):
        outline = self.get_outline()
        PATH = reverse("base:planer_initial_form", args=[outline.pk])

        self.login_foreign_user()
        response = self.client.get(PATH)
        assert response.status_code == 404

        response = self.client.post(PATH)
        assert response.status_code == 404

    def test_planer_initial_form___302_redirect_when_off_troops_empty(self):
        outline = self.get_outline()
        PATH = reverse("base:planer_initial_form", args=[outline.pk])
        REDIRECT = reverse("base:planer_detail", args=[outline.pk])
        self.login_me()
        response = self.client.get(PATH)
        assert response.status_code == 302
        assert response.url == REDIRECT

    def test_planer_initial_form___302_redirect_when_invalid_off_troops(self):
        outline = self.get_outline()
        outline.off_troops = self.random_lower_string()
        outline.save()
        PATH = reverse("base:planer_initial_form", args=[outline.pk])
        REDIRECT = reverse("base:planer_detail", args=[outline.pk])

        self.login_me()
        response = self.client.get(PATH)
        assert response.status_code == 302
        assert response.url == REDIRECT

    def test_planer_initial_form___302_redirect_when_written(self):
        outline = self.get_outline(written="active")
        outline.off_troops = self.random_lower_string()
        outline.save()
        PATH = reverse("base:planer_initial_form", args=[outline.pk])
        REDIRECT = reverse("base:planer_initial", args=[outline.pk])

        self.login_me()
        response = self.client.get(PATH)
        assert response.status_code == 302
        assert response.url == REDIRECT

    def test_planer_initial_form___200_off_troops_correct_and_creating_weights(self):
        outline = self.get_outline(test_world=True)
        outline.off_troops = "102|102,100,100,7002,0,100,2802,0,0,350,100,0,0,0,0,0,"
        outline.save()
        PATH = reverse("base:planer_initial_form", args=[outline.pk])

        self.login_me()
        response = self.client.get(PATH)
        assert response.status_code == 200
        assert (
            WeightMaximum.objects.filter(outline=outline, start="102|102").count() == 1
        )
        assert response.context.get("premium_error") == False
        assert response.context.get("")
