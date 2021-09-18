import json

from django.urls import reverse

from base.models import TargetVertex
from base.tests.test_utils.mini_setup import MiniSetup


class ChangeWeightModelBuilding(MiniSetup):
    def test_change_weight_building___403_not_auth(self):
        outline = self.get_outline()
        self.create_target_on_test_world(outline)
        target = TargetVertex.objects.get(target="200|200")
        weight_max = self.create_weight_maximum(outline)
        weight = self.create_weight(target=target, weight_max=weight_max)

        PATH = reverse("rest_api:change_weight_building", args=[outline.pk, weight.pk])

        response = self.client.get(PATH)
        assert response.status_code == 403
        response = self.client.post(PATH)
        assert response.status_code == 403
        response = self.client.delete(PATH)
        assert response.status_code == 403
        response = self.client.put(PATH)
        assert response.status_code == 403

    def test_change_weight_building___404_foreign_user_has_no_access(self):
        outline = self.get_outline()
        self.create_target_on_test_world(outline)
        target = TargetVertex.objects.get(target="200|200")
        weight_max = self.create_weight_maximum(outline)
        weight = self.create_weight(target=target, weight_max=weight_max)

        PATH = reverse("rest_api:change_weight_building", args=[outline.pk, weight.pk])

        self.login_foreign_user()
        response = self.client.get(PATH)
        assert response.status_code == 405

        response = self.client.post(PATH)
        assert response.status_code == 405

        response = self.client.delete(PATH)
        assert response.status_code == 405

        response = self.client.put(PATH)
        assert response.status_code == 404

    def test_change_weight_building___200_building_is_changed_properly(self):
        outline = self.get_outline()
        self.create_target_on_test_world(outline)
        target = TargetVertex.objects.get(target="200|200")
        weight_max = self.create_weight_maximum(outline)
        weight = self.create_weight(target=target, weight_max=weight_max)

        PATH = reverse("rest_api:change_weight_building", args=[outline.pk, weight.pk])

        self.login_me()
        response = self.client.get(PATH)
        assert response.status_code == 405

        response = self.client.post(PATH)
        assert response.status_code == 405

        response = self.client.delete(PATH)
        assert response.status_code == 405

        response = self.client.put(
            PATH,
            data=json.dumps({"building": "headquarters"}),
            content_type="application/json",
        )
        assert response.json() == {"name": "Ratusz"}

        assert response.status_code == 200
        weight.refresh_from_db()
        assert weight.building == "headquarters"

        response = self.client.put(
            PATH,
            data=json.dumps({"building": self.random_lower_string()}),
            content_type="application/json",
        )

        assert response.status_code == 404
