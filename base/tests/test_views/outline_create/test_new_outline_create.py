import datetime

from django.urls import reverse

from base.forms import OutlineForm
from base.models import Outline, Result, Stats
from base.tests.test_utils.mini_setup import MiniSetup


class NewOutlineCreate(MiniSetup):
    def test_planer_create___302_not_auth_redirect_login(self):
        PATH = reverse("base:planer_create")

        response = self.client.get(PATH)

        assert response.status_code == 302
        assert response.url == self.login_page_path(next=PATH)

    def test_planer_create___200_auth(self):
        PATH = reverse("base:planer_create")

        self.login_me()
        response = self.client.get(PATH)
        form: OutlineForm = response.context["form1"]

        assert response.status_code == 200
        assert len(form.errors) == 0

    def test_planer_create___200_auth_form_not_work_world_invalid(self):
        PATH = reverse("base:planer_create")

        self.login_me()
        response = self.client.post(
            PATH,
            data={
                "name": "name",
                "date": datetime.date.today(),
                "world": "xxxx",
            },
        )
        form: OutlineForm = response.context["form1"]

        assert response.status_code == 200
        assert len(form.errors) == 1
        assert "world" in form.errors

    def test_planer_create___200_auth_form_create_outline_and_redirect(self):
        PATH = reverse("base:planer_create")

        world = self.get_world()

        self.login_me()
        response = self.client.post(
            PATH,
            data={
                "name": "name",
                "date": datetime.date.today(),
                "world": world.pk,
            },
        )

        assert response.status_code == 302
        assert Outline.objects.filter(name="name").count() == 1
        assert Result.objects.all().count() == 1
        assert Stats.objects.all().count() == 1

        outline: Outline = Outline.objects.get(name="name")
        REDIRECT = reverse("base:planer_create_select", args=[outline.pk])

        assert response.url == REDIRECT
        assert outline.name == "name"
        assert outline.date == datetime.date.today()
        assert outline.world == world
        assert outline.owner == self.me()

        result: Result = Result.objects.get(outline=outline)

        assert result.results_export == ""
        assert result.results_get_deff == ""
        assert result.results_players == ""
        assert result.results_outline == ""
        assert result.results_sum_up == ""

        stats: Stats = Stats.objects.get(outline=outline)

        assert stats.outline_pk == outline.pk
        assert stats.premium_user is False
        assert stats.owner_name == self.me().username
        assert stats.world == str(outline.world)
