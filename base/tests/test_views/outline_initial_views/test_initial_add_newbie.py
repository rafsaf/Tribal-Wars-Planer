# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

from datetime import timedelta

from django.urls import reverse
from django.utils.timezone import now

from base.models import TargetVertex, WeightMaximum, WeightModel
from base.tests.test_utils.mini_setup import MiniSetup

ADD_URL_NAMES = [
    "planer_add_first",
    "planer_add_first_off",
    "planer_add_first_ruin",
    "planer_add_first_fake",
    "planer_add_first_fake_noble",
    "planer_add_last_fake",
    "planer_add_last_fake_noble",
    "planer_add_last_ruin",
    "planer_add_last",
    "planer_add_last_off",
]


class InitialAddNewbie(MiniSetup):
    def setup_data(
        self,
        ratio: int,
        target_points: int,
        weight_points: int,
        target_age_days: int = 10,
        weight_age_days: int = 100,
    ) -> tuple[TargetVertex, WeightMaximum]:
        outline = self.get_outline(test_world=True)
        outline.world.newbie_ratio = ratio
        outline.world.newbie_ratio_days = 60
        outline.world.save()
        self.create_target_on_test_world(outline=outline)
        target = TargetVertex.objects.get(outline=outline)
        target.points = target_points
        target.player_created_at = now() - timedelta(days=target_age_days)
        target.save()
        weight = self.create_weight_maximum(outline=outline)
        weight.points = weight_points
        weight.player_created_at = now() - timedelta(days=weight_age_days)
        weight.save()
        self.login_me()
        return target, weight

    def post(self, name: str, target: TargetVertex, weight: WeightMaximum):
        path = reverse(f"base:{name}", args=[target.outline_id, target.pk, weight.pk])
        return self.client.post(path + "?page=1&sort=&filtr=")

    def test_add___blocked_when_attacker_too_big_for_newbie_target(self):
        target, weight = self.setup_data(
            ratio=20, target_points=5000, weight_points=200_000
        )
        redirect = reverse(
            "base:planer_initial_detail", args=[target.outline_id, target.pk]
        )
        for name in ADD_URL_NAMES:
            response = self.post(name, target, weight)
            assert response.status_code == 302, name
            assert getattr(response, "url").startswith(redirect), name
            assert "Newbie protection" in self.client.session["error"], name
            assert not WeightModel.objects.filter(target=target).exists(), name
            weight.refresh_from_db()
            assert weight.off_left == 1500, name

    def test_add___blocked_when_newbie_attacker_too_small_for_target(self):
        target, weight = self.setup_data(
            ratio=20,
            target_points=200_000,
            weight_points=5000,
            target_age_days=100,
            weight_age_days=10,
        )
        for name in ADD_URL_NAMES:
            self.post(name, target, weight)
            assert not WeightModel.objects.filter(target=target).exists(), name

    def test_add___allowed_when_in_ratio(self):
        target, weight = self.setup_data(
            ratio=20, target_points=5000, weight_points=90_000
        )
        self.post("planer_add_first_off", target, weight)
        assert WeightModel.objects.filter(target=target).count() == 1

    def test_add___allowed_when_player_not_newbie_anymore(self):
        target, weight = self.setup_data(
            ratio=20, target_points=5000, weight_points=200_000, target_age_days=61
        )
        self.post("planer_add_first_off", target, weight)
        assert WeightModel.objects.filter(target=target).count() == 1

    def test_add___allowed_when_ratio_disabled(self):
        target, weight = self.setup_data(
            ratio=0, target_points=5000, weight_points=200_000
        )
        self.post("planer_add_first_off", target, weight)
        assert WeightModel.objects.filter(target=target).count() == 1
