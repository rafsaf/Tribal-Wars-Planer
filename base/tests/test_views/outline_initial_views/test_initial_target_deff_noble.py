from django.urls import reverse

from base.models import TargetVertex
from base.tests.test_utils.mini_setup import MiniSetup


class InitialTargetDeffNoble(MiniSetup):
    def test_planer_initial_detail_renders_manual_deff_noble_controls(self):
        outline = self.get_outline(test_world=True, written="active")
        self.create_target_on_test_world(outline)
        target = TargetVertex.objects.get(target="200|200", outline=outline)
        target.has_deff_noble = True
        target.deff_noble_order = 4
        target.save(update_fields=["has_deff_noble", "deff_noble_order"])
        weight_max = self.create_weight_maximum(outline=outline)
        weight_max.off_left = 0
        weight_max.off_max = 0
        weight_max.deff_left = 500
        weight_max.deff_max = 500
        weight_max.save(update_fields=["off_left", "off_max", "deff_left", "deff_max"])
        self.create_weight(target=target, weight_max=weight_max)

        path = reverse("base:planer_initial_detail", args=[outline.pk, target.pk])
        self.login_me()
        response = self.client.get(path)

        assert response.status_code == 200
        assert (
            reverse(
                "base:planer_add_first_deff_noble",
                args=[outline.pk, target.pk, weight_max.pk],
            )
            in response.content.decode()
        )
        assert "images/spear" in response.content.decode()
