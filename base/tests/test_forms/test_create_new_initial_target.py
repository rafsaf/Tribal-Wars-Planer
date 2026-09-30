# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

from django.conf import settings

from base import models
from base.forms import CreateNewInitialTarget
from base.tests.test_utils.mini_setup import MiniSetup


class CreateNewInitialTargetTest(MiniSetup):
    def test_form_pass_when_correct_real_target(self):
        outline = self.get_outline(test_world=True)
        form: CreateNewInitialTarget = CreateNewInitialTarget(
            {"target": "200|200", "target_type": "real"},
            outline=outline,
            is_premium=False,
        )
        assert form.is_valid()

    def test_form_not_pass_when_25_targets_not_premium(self):
        outline = self.get_outline(test_world=True)
        settings.PREMIUM_ACCOUNT_VALIDATION_ON = True
        self.create_target_on_test_world(
            outline, many=settings.PREMIUM_ACCOUNT_MAX_TARGETS_FREE
        )
        form: CreateNewInitialTarget = CreateNewInitialTarget(
            {"target": "200|200", "target_type": "real"},
            outline=outline,
            is_premium=False,
        )
        assert not form.is_valid()

    def test_form_pass_when_25_targets_premium(self):
        outline = self.get_outline(test_world=True)
        settings.PREMIUM_ACCOUNT_VALIDATION_ON = True
        self.create_target_on_test_world(
            outline, many=settings.PREMIUM_ACCOUNT_MAX_TARGETS_FREE
        )
        form: CreateNewInitialTarget = CreateNewInitialTarget(
            {"target": "200|200", "target_type": "real"},
            outline=outline,
            is_premium=True,
        )
        assert form.is_valid()

    def test_form_pass_when_village_barbarian(self):
        outline = self.get_outline(test_world=True)
        village: models.VillageModel = models.VillageModel.objects.get(coord="200|200")
        village.player = None
        village.save()

        form: CreateNewInitialTarget = CreateNewInitialTarget(
            {"target": "200|200", "target_type": "real"},
            outline=outline,
            is_premium=False,
        )
        assert form.is_valid()

    def test_form_not_pass_when_2_villages_in_database(self):
        outline = self.get_outline(test_world=True)
        models.VillageModel.objects.create(
            coord="200|200",
            village_id=1000,
            x_coord=200,
            y_coord=200,
            player=None,
            world=outline.world,
        )

        form: CreateNewInitialTarget = CreateNewInitialTarget(
            {"target": "200|200", "target_type": "real"},
            outline=outline,
            is_premium=False,
        )
        assert not form.is_valid()
