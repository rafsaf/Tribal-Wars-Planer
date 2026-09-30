# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

from django.urls import reverse

from base.tests.test_utils.mini_setup import MiniSetup


class InactiveOutline(MiniSetup):
    def test_planer_status___302_not_auth_redirect_login(self):
        outline = self.get_outline()
        PATH = reverse("base:planer_status", args=[outline.pk])

        response = self.client.get(PATH)
        assert response.status_code == 302
        assert getattr(response, "url") == self.login_page_path(next=PATH)

        response = self.client.post(PATH)
        assert response.status_code == 302
        assert getattr(response, "url") == self.login_page_path(next=PATH)

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

        PATH = reverse("base:planer_status", args=[outline.pk]) + "?show-hidden=true"
        REDIRECT = reverse("base:planer") + "?show-hidden=true"

        self.login_me()
        response = self.client.get(PATH)
        assert response.status_code == 405

        response = self.client.post(PATH)
        assert response.status_code == 302
        assert getattr(response, "url") == REDIRECT

        outline.refresh_from_db()
        assert outline.status == "inactive"

    def test_planer_status___302_auth_works_ok_status_inactive(self):
        outline = self.get_outline()
        outline.status = "inactive"
        outline.save()

        PATH = reverse("base:planer_status", args=[outline.pk])
        REDIRECT = reverse("base:planer") + "?show-hidden=false"

        self.login_me()
        response = self.client.get(PATH)
        assert response.status_code == 405

        response = self.client.post(PATH)
        assert response.status_code == 302
        assert getattr(response, "url") == REDIRECT

        outline.refresh_from_db()
        assert outline.status == "active"
