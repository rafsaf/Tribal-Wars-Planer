from django.urls import reverse

from base.models import OutlineTime, TargetVertex, WeightMaximum, WeightModel
from base.tests.test_utils.mini_setup import MiniSetup


class TargetTimeUpdate(MiniSetup):
    def test_target_time_update___403_not_auth(self):
        outline = self.get_outline()
        self.create_target_on_test_world(outline)
        target: TargetVertex = TargetVertex.objects.get(target="200|200")
        outline_time = self.create_outline_time(outline)

        PATH = reverse("rest_api:target_time_update", args=[target.pk, outline_time.pk])

        response = self.client.get(PATH)
        assert response.status_code == 403
        response = self.client.post(PATH)
        assert response.status_code == 403
        response = self.client.delete(PATH)
        assert response.status_code == 403
        response = self.client.put(PATH)
        assert response.status_code == 403

    def test_target_time_update___404_foreign_user_has_no_access(self):
        outline = self.get_outline()
        self.create_target_on_test_world(outline)
        target: TargetVertex = TargetVertex.objects.get(target="200|200")
        outline_time = self.create_outline_time(outline)

        PATH = reverse("rest_api:target_time_update", args=[target.pk, outline_time.pk])

        self.login_foreign_user()
        response = self.client.get(PATH)
        assert response.status_code == 405

        response = self.client.post(PATH)
        assert response.status_code == 405

        response = self.client.delete(PATH)
        assert response.status_code == 405

        response = self.client.put(PATH)
        assert response.status_code == 404

    def test_target_time_update___200_target_updated_correct_target_no_time(self):
        outline = self.get_outline()
        self.create_target_on_test_world(outline)
        target: TargetVertex = TargetVertex.objects.get(target="200|200")
        outline_time = self.create_outline_time(outline)

        PATH = reverse("rest_api:target_time_update", args=[target.pk, outline_time.pk])

        self.login_me()
        response = self.client.get(PATH)
        assert response.status_code == 405

        response = self.client.post(PATH)
        assert response.status_code == 405

        response = self.client.delete(PATH)
        assert response.status_code == 405

        response = self.client.put(PATH)
        assert response.status_code == 200

        result = response.json()
        assert result["new"] == f"{target.pk}-time-{outline_time.pk}"
        assert result["old"] == "none"
        target.refresh_from_db()
        assert target.outline_time == outline_time

    def test_target_time_update___200_target_updated_correct_target_with_time(self):
        outline = self.get_outline()
        self.create_target_on_test_world(outline)
        target: TargetVertex = TargetVertex.objects.get(target="200|200")
        outline_time_old = self.create_outline_time(outline)
        target.outline_time = outline_time_old
        target.save()
        outline_time_new = self.create_outline_time(outline)

        PATH = reverse(
            "rest_api:target_time_update", args=[target.pk, outline_time_new.pk]
        )

        self.login_me()
        response = self.client.get(PATH)
        assert response.status_code == 405

        response = self.client.post(PATH)
        assert response.status_code == 405

        response = self.client.delete(PATH)
        assert response.status_code == 405

        response = self.client.put(PATH)
        assert response.status_code == 200

        result = response.json()
        assert result["new"] == f"{target.pk}-time-{outline_time_new.pk}"
        assert result["old"] == f"{target.pk}-time-{outline_time_old.pk}"
        target.refresh_from_db()
        assert target.outline_time == outline_time_new
