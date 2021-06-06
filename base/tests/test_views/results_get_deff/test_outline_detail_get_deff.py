from django.urls import reverse

from base.tests.utils.mini_setup import MiniSetup


class OutlineDetailGetDeff(MiniSetup):
    def test_planer_detail_get_deff___302_not_auth_redirect_login(self):
        outline = self.get_outline()
        outline_time = self.create_outline_time(outline)
        PATH = reverse("base:planer_detail_get_deff", args=[outline_time.pk])

        response = self.client.get(PATH)
        assert response.status_code == 302
        response = self.client.post(PATH)
        assert response.status_code == 302
        assert response.url == self.login_page_path(next=PATH)

    def test_planer_detail_get_deff___404_foreign_user_no_access(self):
        outline = self.get_outline(add_result=True)
        PATH = reverse("base:planer_detail_get_deff", args=[outline.pk])

        self.login_foreign_user()
        response = self.client.get(PATH)
        assert response.status_code == 404

        response = self.client.post(PATH)
        assert response.status_code == 404

    def test_planer_detail_get_deff___404_when_result_not_exists(self):
        outline = self.get_outline()
        PATH = reverse("base:planer_detail_get_deff", args=[outline.pk])
        self.login_me()

        response = self.client.get(PATH)
        assert response.status_code == 404

    def test_planer_detail_get_deff___302_redirect_when_no_deff_or_off_troops(self):
        outline = self.get_outline(add_result=True)
        PATH = reverse("base:planer_detail_get_deff", args=[outline.pk])
        REDIRECT = reverse("base:planer_detail", args=[outline.pk])
        self.login_me()

        outline.deff_troops = ""
        outline.off_troops = self.random_lower_string()
        outline.save()

        response = self.client.get(PATH)
        assert response.status_code == 302
        assert response.url == REDIRECT

        outline.refresh_from_db()
        outline.deff_troops = self.random_lower_string()
        outline.off_troops = ""
        outline.save()

        response = self.client.get(PATH)
        assert response.status_code == 302
        assert response.url == REDIRECT

        outline.refresh_from_db()
        outline.deff_troops = self.random_lower_string()
        outline.off_troops = self.random_lower_string()
        outline.save()

        response = self.client.get(PATH)
        assert response.status_code == 200

    def test_planer_detail_get_deff___302_form_work_ok_data(self):
        outline = self.get_outline(test_world=True, add_result=True)
        PATH = reverse("base:planer_detail_get_deff", args=[outline.pk])
        REDIRECT_BAD = reverse("base:planer_detail", args=[outline.pk])
        REDIRECT_OK = (
            reverse("base:planer_detail_results", args=[outline.pk]) + "?tab=deff"
        )
        self.login_me()

        outline.off_troops = "102|102,100,100,7002,0,100,2802,0,0,350,100,0,0,0,0,0,"
        outline.deff_troops = (
            "100|100,w wiosce,100,100,7000,0,100,2800,0,0,350,100,0,0,0,0,"
        )
        outline.save()

        response = self.client.post(
            PATH, data={"form": "", "radius": 10, "excluded": "500|500"}
        )
        assert response.status_code == 302
        assert response.url == REDIRECT_OK

        response = self.client.post(
            PATH,
            data={"form": "", "radius": 10, "excluded": self.random_lower_string()},
        )
        assert response.status_code == 200

        outline.refresh_from_db()
        outline.off_troops = self.random_lower_string()
        outline.save()

        response = self.client.post(
            PATH,
            data={"form": "", "radius": 10, "excluded": ""},
        )
        assert response.status_code == 302
        assert response.url == REDIRECT_BAD
