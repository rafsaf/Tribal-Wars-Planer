# Copyright 2021 Rafał Safin (rafsaf). All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

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
        self.create_target_on_test_world(outline, many=25)
        form: CreateNewInitialTarget = CreateNewInitialTarget(
            {"target": "200|200", "target_type": "real"},
            outline=outline,
            is_premium=False,
        )
        assert not form.is_valid()

    def test_form_pass_when_25_targets_premium(self):
        outline = self.get_outline(test_world=True)
        self.create_target_on_test_world(outline, many=25)
        form: CreateNewInitialTarget = CreateNewInitialTarget(
            {"target": "200|200", "target_type": "real"},
            outline=outline,
            is_premium=True,
        )
        assert form.is_valid()

    def test_form_not_pass_when_village_barbarian(self):
        outline = self.get_outline(test_world=True)
        village: models.VillageModel = models.VillageModel.objects.get(coord="200|200")
        village.player = None
        village.save()

        form: CreateNewInitialTarget = CreateNewInitialTarget(
            {"target": "200|200", "target_type": "real"},
            outline=outline,
            is_premium=False,
        )
        assert not form.is_valid()

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
