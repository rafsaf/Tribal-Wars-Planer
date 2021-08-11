from base import forms
from django.urls import reverse

from base.tests.test_utils.mini_setup import MiniSetup


class OutlineDetailResults(MiniSetup):
    def test_planer_detail_results___302_not_auth_redirect_login(self):
        outline = self.get_outline(add_result=True)
        outline_time = self.create_outline_time(outline)
        PATH = reverse("base:planer_detail_results", args=[outline_time.pk])

        response = self.client.get(PATH)
        assert response.status_code == 302
        response = self.client.post(PATH)
        assert response.status_code == 302
        assert response.url == self.login_page_path(next=PATH)

    def test_planer_detail_results___404_foreign_user_no_access(self):
        outline = self.get_outline(add_result=True)
        PATH = reverse("base:planer_detail_results", args=[outline.pk])

        self.login_foreign_user()
        response = self.client.get(PATH)
        assert response.status_code == 404

        response = self.client.post(PATH)
        assert response.status_code == 404

    def test_planer_detail_results___404_initial_form_works_properly(self):
        outline = self.get_outline(add_result=True)
        outline.default_show_hidden = False
        outline.title_message = self.random_lower_string()
        outline.text_message = self.random_lower_string()
        outline.save()

        PATH = reverse("base:planer_detail_results", args=[outline.pk])
        self.login_me()

        response = self.client.get(PATH)
        assert response.status_code == 200
        form: forms.SettingMessageForm = response.context["form1"]
        assert form.fields["default_show_hidden"].initial == outline.default_show_hidden
        assert form.fields["title_message"].initial == outline.title_message
        assert form.fields["text_message"].initial == outline.text_message

    def test_planer_detail_results___302_form_redirect_works_ok(self):
        outline = self.get_outline(add_result=True)
        overview = self.create_overview(outline)
        overview.show_hidden = False
        overview.removed = False
        overview.save()

        PATH = reverse("base:planer_detail_results", args=[outline.pk])
        self.login_me()

        response = self.client.get(PATH)
        assert response.status_code == 200

        TITLE = self.random_lower_string()
        TEXT = self.random_lower_string()
        assert outline.sending_option == "default"

        response = self.client.post(
            PATH,
            data={
                "form1": "",
                "default_show_hidden": "on",
                "title_message": TITLE,
                "text_message": TEXT,
                "sending_option": "table",
            },
        )
        assert response.status_code == 302
        assert response.url == PATH

        outline.refresh_from_db()

        assert outline.default_show_hidden == True
        assert outline.title_message == TITLE
        assert outline.text_message == TEXT
        assert outline.sending_option == "table"

        overview.refresh_from_db()
        assert overview.show_hidden == True
