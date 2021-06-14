from django.urls import reverse

from base.models import OutlineTime, TargetVertex, WeightMaximum, WeightModel
from base.tests.test_utils.mini_setup import MiniSetup


class OverviewStateHideUpdate(MiniSetup):
    def test_hide_state_update___403_not_auth(self):
        outline = self.get_outline()
        overview = self.create_overview(outline)

        PATH = reverse("rest_api:hide_state_update", args=[outline.pk, overview.token])

        response = self.client.get(PATH)
        assert response.status_code == 403
        response = self.client.post(PATH)
        assert response.status_code == 403
        response = self.client.delete(PATH)
        assert response.status_code == 403
        response = self.client.put(PATH)
        assert response.status_code == 403

    def test_hide_state_update___404_foreign_user_has_no_access(self):
        outline = self.get_outline()
        overview = self.create_overview(outline)

        PATH = reverse("rest_api:hide_state_update", args=[outline.pk, overview.token])

        self.login_foreign_user()
        response = self.client.get(PATH)
        assert response.status_code == 405

        response = self.client.post(PATH)
        assert response.status_code == 405

        response = self.client.delete(PATH)
        assert response.status_code == 405

        response = self.client.put(PATH)
        assert response.status_code == 404

    def test_hide_state_update___200_target_is_deleted_properly(self):
        outline = self.get_outline()
        overview = self.create_overview(outline)

        PATH = reverse("rest_api:hide_state_update", args=[outline.pk, overview.token])

        self.login_me()
        response = self.client.get(PATH)
        assert response.status_code == 405

        response = self.client.post(PATH)
        assert response.status_code == 405

        response = self.client.delete(PATH)
        assert response.status_code == 405

        response = self.client.put(PATH)
        assert response.status_code == 200

        overview.refresh_from_db()
        assert overview.show_hidden == True
        result = response.json()
        assert result["name"] == "True"
        assert result["class"] == "btn btn-light btn-light-no-border md-blue"

        response = self.client.put(PATH)
        assert response.status_code == 200

        overview.refresh_from_db()
        assert overview.show_hidden == False
        result = response.json()
        assert result["name"] == "False"
        assert result["class"] == "btn btn-light btn-light-no-border md-error"
