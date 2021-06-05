import json
from django.urls import reverse
from base.models import OutlineTime, TargetVertex, WeightMaximum, WeightModel
from base.tests.utils.mini_setup import MiniSetup


class ChangeBuildingsArray(MiniSetup):
    def test_change_buildings_array___403_not_auth(self):
        outline = self.get_outline()

        PATH = reverse("rest_api:change_buildings_array", args=[outline.pk])

        response = self.client.get(PATH)
        assert response.status_code == 403
        response = self.client.post(PATH)
        assert response.status_code == 403
        response = self.client.delete(PATH)
        assert response.status_code == 403
        response = self.client.put(PATH)
        assert response.status_code == 403

    def test_change_buildings_array___404_foreign_user_has_no_access(self):
        outline = self.get_outline()

        PATH = reverse("rest_api:change_buildings_array", args=[outline.pk])

        self.login_foreign_user()
        response = self.client.get(PATH)
        assert response.status_code == 405

        response = self.client.post(PATH)
        assert response.status_code == 405

        response = self.client.delete(PATH)
        assert response.status_code == 405

        response = self.client.put(PATH)
        assert response.status_code == 404

    def test_change_buildings_array___200_target_is_deleted_properly(self):
        outline = self.get_outline()

        PATH = reverse("rest_api:change_buildings_array", args=[outline.pk])

        self.login_me()
        response = self.client.get(PATH)
        assert response.status_code == 405

        response = self.client.post(PATH)
        assert response.status_code == 405

        response = self.client.delete(PATH)
        assert response.status_code == 405

        response = self.client.put(
            PATH,
            data=json.dumps({"buildings": ["stable", "workshop", "academy", "smithy"]}),
            content_type="application/json",
        )

        assert response.status_code == 200
        outline.refresh_from_db()
        assert outline.initial_outline_buildings == [
            "stable",
            "workshop",
            "academy",
            "smithy",
        ]
