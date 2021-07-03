from django.urls import reverse
from django.utils import timezone

from base import forms
from base.models import TargetVertex, WeightMaximum
from base.tests.test_utils.mini_setup import MiniSetup
from utils import basic


class InitialPlaner(MiniSetup):
    def test_planer_initial___302_not_auth_redirect_login(self):
        outline = self.get_outline(written="active")
        PATH = reverse("base:planer_initial", args=[outline.pk])

        response = self.client.get(PATH)
        assert response.status_code == 302
        assert response.url == self.login_page_path(next=PATH)

        response = self.client.post(PATH)
        assert response.status_code == 302
        assert response.url == self.login_page_path(next=PATH)

    def test_planer_initial___404_foreign_user_no_access(self):
        outline = self.get_outline(written="active")
        PATH = reverse("base:planer_initial", args=[outline.pk])

        self.login_foreign_user()
        response = self.client.get(PATH)
        assert response.status_code == 404

        response = self.client.post(PATH)
        assert response.status_code == 404

    def test_planer_initial___404_when_not_written(self):
        outline = self.get_outline(written="inactive")
        PATH = reverse("base:planer_initial", args=[outline.pk])

        self.login_me()
        response = self.client.get(PATH)
        assert response.status_code == 404

        response = self.client.post(PATH)
        assert response.status_code == 404

    def test_planer_initial___200_filter_form_correct_initials(self):
        outline = self.get_outline(written="active")
        outline.filter_targets_number = 15
        outline.simple_textures = True
        outline.save()

        PATH = (
            reverse("base:planer_initial", args=[outline.pk])
            + "?mode=ruin&page=5&filtr=xxx"
        )

        self.login_me()
        response = self.client.get(PATH)
        assert response.status_code == 200
        filter_form: forms.SetTargetsMenuFilters = response.context["filter_form"]
        assert filter_form.fields["filter_targets_number"].initial == 15
        assert filter_form.fields["simple_textures"].initial == True

    def test_planer_initial___200_correct_GET_params(self):
        outline = self.get_outline(written="active")
        outline.save()
        self.login_me()

        PATH = reverse("base:planer_initial", args=[outline.pk])

        response = self.client.get(PATH + "?mode=ruin&page=5&filtr=xxx")
        assert response.status_code == 200
        mode: basic.Mode = response.context["mode"]
        filtr: str = response.context["filtr"]
        assert mode.is_ruin
        assert filtr == "xxx"

        response = self.client.get(PATH + "?mode=time&page=5&filtr=yyy")
        assert response.status_code == 200
        mode: basic.Mode = response.context["mode"]
        filtr: str = response.context["filtr"]
        assert mode.is_time
        assert filtr == "yyy"

        response = self.client.get(PATH + "?mode=add_and_remove&page=5&filtr=yyy")
        assert response.status_code == 200
        mode: basic.Mode = response.context["mode"]
        filtr: str = response.context["filtr"]
        assert mode.is_add_and_remove
        assert filtr == "yyy"

        response = self.client.get(PATH + "?mode=menu&page=5&filtr=yyy")
        assert response.status_code == 200
        mode: basic.Mode = response.context["mode"]
        filtr: str = response.context["filtr"]
        assert mode.is_menu
        assert filtr == "yyy"

        response = self.client.get(PATH + "?mode=fake&page=5&filtr=yyy")
        assert response.status_code == 200
        mode: basic.Mode = response.context["mode"]
        filtr: str = response.context["filtr"]
        assert mode.is_fake
        assert filtr == "yyy"

    def test_planer_initial___302_go_back_button(self):
        outline = self.get_outline(written="active", add_result=True)
        outline_time = self.create_outline_time(outline)
        outline.written = "active"
        outline.avaiable_offs = [155, 5555, 1111, 100]
        outline.avaiable_offs_near = [123, 123, 5, 0]
        outline.avaiable_nobles = [1, 2, 3, 7]
        outline.avaiable_nobles_near = [55, 33, 3, 5]
        outline.avaiable_ruins = 6661
        outline.filter_weights_min = 150005
        outline.filter_weights_max = 150015
        outline.filter_card_number = 15
        outline.filter_targets_number = 8
        outline.filter_hide_front = "back"
        outline.choice_sort = "-distance"
        outline.default_off_time_id = outline_time.pk
        outline.default_fake_time_id = outline_time.pk
        outline.default_ruin_time_id = outline_time.pk
        outline.save()
        self.login_me()

        PATH = reverse("base:planer_initial", args=[outline.pk])
        REDIRECT = reverse("base:planer_initial_form", args=[outline.pk])

        response = self.client.post(PATH, data={"form1": ""})
        assert response.status_code == 302
        assert response.url == REDIRECT

        outline.refresh_from_db()
        assert outline.written == "inactive"
        assert outline.avaiable_offs == []
        assert outline.avaiable_offs_near == []
        assert outline.avaiable_nobles == []
        assert outline.avaiable_nobles_near == []
        assert outline.avaiable_ruins == None
        assert outline.filter_weights_min == 0
        assert outline.filter_weights_max == 30000
        assert outline.filter_card_number == 12
        assert outline.filter_targets_number == 12
        assert outline.filter_hide_front == "all"
        assert outline.choice_sort == "distance"
        assert outline.default_off_time_id == None
        assert outline.default_fake_time_id == None
        assert outline.default_ruin_time_id == None

    def test_planer_initial___filter_form_works_ok(self):
        outline = self.get_outline(written="active")
        outline.filter_targets_number = 5
        outline.simple_textures = False
        outline.save()
        self.login_me()

        PATH = reverse("base:planer_initial", args=[outline.pk])

        response = self.client.post(
            PATH,
            data={
                "form-filter-targets": "",
                "filter_targets_number": 15,
                "simple_textures": "on",
            },
        )
        assert response.status_code == 302
        assert response.url == PATH + "?page=None&mode=menu&filtr="
        outline.refresh_from_db()
        assert outline.simple_textures == True
        assert outline.filter_targets_number == 15

    def test_planer_initial___create_form_works_ok(self):
        outline = self.get_outline(written="active", test_world=True)
        self.login_me()

        PATH = reverse("base:planer_initial", args=[outline.pk])

        response = self.client.post(
            PATH,
            data={
                "create": "",
                "target_type": "real",
                "target": "200|200",
            },
        )
        assert response.status_code == 302
        assert response.url == PATH + "?page=None&mode=menu&filtr="

        response = self.client.post(
            PATH,
            data={
                "create": "",
                "target_type": "fake",
                "target": "200|200",
            },
        )
        assert response.status_code == 302
        assert response.url == PATH + "?page=None&mode=menu&filtr="

        response = self.client.post(
            PATH,
            data={
                "create": "",
                "target_type": "ruin",
                "target": "200|200",
            },
        )
        assert response.status_code == 302
        assert response.url == PATH + "?page=None&mode=menu&filtr="

        assert TargetVertex.objects.filter(fake=False, ruin=False).count() == 1
        assert TargetVertex.objects.filter(fake=True, ruin=False).count() == 1
        assert TargetVertex.objects.filter(fake=False, ruin=True).count() == 1