from django.urls import reverse
from base.tests.utils.mini_setup import MiniSetup


class OutlineDeleteEnemyTags(MiniSetup):
    def test_planer_delete_enemy_tags___302_not_auth_redirect_login(self):
        PATH = reverse("base:planer_delete_enemy_tags", args=[1])

        response = self.client.get(PATH)
        assert response.status_code == 405

        response = self.client.post(PATH)
        assert response.status_code == 302
        assert response.url == self.login_page_path(next=PATH)

    def test_planer_delete_enemy_tags___404_foreign_user(self):
        self.login_foreign_user()
        outline = self.get_outline()
        PATH = reverse("base:planer_delete_enemy_tags", args=[outline.pk])

        response = self.client.get(PATH)
        assert response.status_code == 405
        response = self.client.post(PATH)
        assert response.status_code == 404

    def test_planer_delete_enemy_tags___302_auth_works_ok(self):
        outline = self.get_outline()
        PATH = reverse("base:planer_delete_enemy_tags", args=[outline.pk])
        REDIRECT = reverse("base:planer_create_select", args=[outline.pk])

        self.login_me()
        response = self.client.get(PATH)
        assert response.status_code == 405

        outline.enemy_tribe_tag = ["tag1", "tag2"]
        outline.save()

        response = self.client.post(PATH)
        assert response.status_code == 302
        assert response.url == REDIRECT

        outline.refresh_from_db()
        assert outline.enemy_tribe_tag == []
