from django.urls import reverse

from base.models import OutlineTime, TargetVertex, WeightMaximum, WeightModel
from base.tests.test_utils.mini_setup import MiniSetup


class InitialDeleteTime(MiniSetup):
    def test_planer_delete_time___302_not_auth_redirect_login(self):
        outline = self.get_outline()
        outline_time = self.create_outline_time(outline)
        PATH = reverse("base:planer_delete_time", args=[outline_time.pk])

        response = self.client.get(PATH)
        assert response.status_code == 302
        response = self.client.post(PATH)
        assert response.status_code == 302
        assert response.url == self.login_page_path(next=PATH)

    def test_planer_delete_time___404_foreign_user_no_access(self):
        outline = self.get_outline()
        outline_time = self.create_outline_time(outline)
        PATH = reverse("base:planer_delete_time", args=[outline_time.pk])

        self.login_foreign_user()
        response = self.client.get(PATH)
        assert response.status_code == 405

        response = self.client.post(PATH)
        assert response.status_code == 404

    def test_planer_delete_time___302_delete_correct(self):
        outline = self.get_outline()
        outline_time = self.create_outline_time(outline)

        PATH = (
            reverse("base:planer_delete_time", args=[outline_time.pk])
            + "?page=2&mode=time"
        )
        REDIRECT = (
            reverse("base:planer_initial", args=[outline.pk]) + "?page=2&mode=time"
        )

        self.login_me()
        response = self.client.get(PATH)
        assert response.status_code == 405

        response = self.client.post(PATH)
        assert response.status_code == 302
        assert response.url == REDIRECT

        assert not OutlineTime.objects.filter(pk=outline_time.pk).exists()

    def test_planer_delete_time___302_delete_and_change_outline_default_times_id(self):
        outline = self.get_outline()
        outline_time1 = self.create_outline_time(outline)
        outline_time2 = self.create_outline_time(outline)
        outline_time3 = self.create_outline_time(outline)
        outline.default_off_time_id = outline_time1.pk
        outline.default_fake_time_id = outline_time2.pk
        outline.default_ruin_time_id = outline_time3.pk
        outline.save()

        self.login_me()
        REDIRECT = (
            reverse("base:planer_initial", args=[outline.pk]) + "?page=2&mode=time"
        )
        PATH = (
            reverse("base:planer_delete_time", args=[outline_time1.pk])
            + "?page=2&mode=time"
        )

        response = self.client.get(PATH)
        assert response.status_code == 405

        response = self.client.post(PATH)
        assert response.status_code == 302
        assert response.url == REDIRECT

        assert not OutlineTime.objects.filter(pk=outline_time1.pk).exists()
        outline.refresh_from_db()
        assert outline.default_off_time_id == None

        PATH = (
            reverse("base:planer_delete_time", args=[outline_time2.pk])
            + "?page=2&mode=time"
        )

        response = self.client.post(PATH)
        assert response.status_code == 302
        assert response.url == REDIRECT

        assert not OutlineTime.objects.filter(pk=outline_time2.pk).exists()
        outline.refresh_from_db()
        assert outline.default_fake_time_id == None

        PATH = (
            reverse("base:planer_delete_time", args=[outline_time3.pk])
            + "?page=2&mode=time"
        )

        response = self.client.post(PATH)
        assert response.status_code == 302
        assert response.url == REDIRECT

        assert not OutlineTime.objects.filter(pk=outline_time3.pk).exists()
        outline.refresh_from_db()
        assert outline.default_ruin_time_id == None
