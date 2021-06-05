from django.urls import reverse

from base.models import OutlineTime, TargetVertex, WeightMaximum, WeightModel
from base.tests.utils.mini_setup import MiniSetup


class TargetTimeUpdate(MiniSetup):
    def test_target_delete___403_not_auth(self):
        outline = self.get_outline()
        self.create_target_on_test_world(outline)
        target: TargetVertex = TargetVertex.objects.get(target="200|200")

        PATH = reverse("rest_api:target_delete", args=[target.pk])

        response = self.client.get(PATH)
        assert response.status_code == 403
        response = self.client.post(PATH)
        assert response.status_code == 403
        response = self.client.delete(PATH)
        assert response.status_code == 403
        response = self.client.put(PATH)
        assert response.status_code == 403

    def test_target_delete___404_foreign_user_has_no_access(self):
        outline = self.get_outline()
        self.create_target_on_test_world(outline)
        target: TargetVertex = TargetVertex.objects.get(target="200|200")

        PATH = reverse("rest_api:target_delete", args=[target.pk])

        self.login_foreign_user()
        response = self.client.get(PATH)
        assert response.status_code == 405

        response = self.client.post(PATH)
        assert response.status_code == 405

        response = self.client.delete(PATH)
        assert response.status_code == 404

        response = self.client.put(PATH)
        assert response.status_code == 405

    def test_target_delete___200_target_is_deleted_properly(self):
        outline = self.get_outline()
        self.create_target_on_test_world(outline)
        target: TargetVertex = TargetVertex.objects.get(target="200|200")

        PATH = reverse("rest_api:target_delete", args=[target.pk])

        self.login_me()
        response = self.client.get(PATH)
        assert response.status_code == 405

        response = self.client.post(PATH)
        assert response.status_code == 405

        response = self.client.put(PATH)
        assert response.status_code == 405

        response = self.client.delete(PATH)
        assert response.status_code == 204

        assert not TargetVertex.objects.filter(target="200|200").exists()
