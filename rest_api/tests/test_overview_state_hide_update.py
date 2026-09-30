# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

import json

from django.urls import reverse

from base.tests.test_utils.mini_setup import MiniSetup


class OverviewStateHideUpdate(MiniSetup):
    def test_hide_state_update___403_not_auth(self):
        outline = self.get_outline()
        overview = self.create_overview(outline)

        PATH = reverse("rest_api:hide_state_update")

        response = self.client.put(
            PATH,
            data=json.dumps(
                {
                    "outline_id": outline.pk,
                    "token": overview.token,
                }
            ),
            content_type="application/json",
        )
        assert response.status_code == 403

    def test_hide_state_update___404_foreign_user_has_no_access(self):
        outline = self.get_outline()
        overview = self.create_overview(outline)

        PATH = reverse("rest_api:hide_state_update")

        self.login_foreign_user()

        response = self.client.put(
            PATH,
            data=json.dumps(
                {
                    "outline_id": outline.pk,
                    "token": overview.token,
                }
            ),
            content_type="application/json",
        )
        assert response.status_code == 404

    def test_hide_state_update___404_cannot_use_foreign_token_with_my_outline(self):
        my_outline = self.get_outline()
        foreign_outline = self.create_foreign_outline()
        foreign_overview = self.create_overview(foreign_outline)

        PATH = reverse("rest_api:hide_state_update")

        self.login_me()

        response = self.client.put(
            PATH,
            data=json.dumps(
                {
                    "outline_id": my_outline.pk,
                    "token": foreign_overview.token,
                }
            ),
            content_type="application/json",
        )
        assert response.status_code == 404

        foreign_overview.refresh_from_db()
        assert foreign_overview.show_hidden is False

    def test_hide_state_update___400_invalid_payload_types(self):
        outline = self.get_outline()
        overview = self.create_overview(outline)

        PATH = reverse("rest_api:hide_state_update")

        self.login_me()

        response = self.client.put(
            PATH,
            data=json.dumps(
                {
                    "outline_id": "text",
                    "token": overview.token,
                }
            ),
            content_type="application/json",
        )
        assert response.status_code == 400
        assert response.json() == {"outline_id": ["A valid integer is required."]}

    def test_hide_state_update___200_overview_properly_state_changed(self):
        outline = self.get_outline()
        overview = self.create_overview(outline)

        PATH = reverse("rest_api:hide_state_update")

        self.login_me()

        response = self.client.put(
            PATH,
            data=json.dumps(
                {
                    "outline_id": outline.pk,
                    "token": overview.token,
                }
            ),
            content_type="application/json",
        )
        assert response.status_code == 200

        overview.refresh_from_db()
        assert overview.show_hidden is True
        result = response.json()
        assert result["name"] == "True"
        assert result["class"] == "btn btn-light btn-light-no-border md-blue"

        response = self.client.put(
            PATH,
            data=json.dumps(
                {
                    "outline_id": outline.pk,
                    "token": overview.token,
                }
            ),
            content_type="application/json",
        )
        assert response.status_code == 200

        overview.refresh_from_db()
        assert overview.show_hidden is False
        result = response.json()
        assert result["name"] == "False"
        assert result["class"] == "btn btn-light btn-light-no-border md-error"
