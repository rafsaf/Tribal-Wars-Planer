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
from base.forms import OutlineForm
from base.tests.test_utils.mini_setup import MiniSetup


class OutlineFormTest(MiniSetup):
    def test_form_pass_when_correct_data(self):
        outline = self.get_outline(test_world=True)
        world: models.World = outline.world

        form: OutlineForm = OutlineForm(
            {
                "name": self.random_lower_string(),
                "date": "2000-05-10",
                "world": f"{world.pk}",
            },
        )
        form.fields["world"].choices = [(f"{world.pk}", world.game_name())]
        assert form.is_valid()

    def test_form_not_pass_when_incorrect_date(self):
        outline = self.get_outline(test_world=True)
        world: models.World = outline.world

        form: OutlineForm = OutlineForm(
            {
                "name": self.random_lower_string(),
                "date": "209-05-10",
                "world": f"{world.pk}",
            },
        )
        form.fields["world"].choices = [(f"{world.pk}", world.game_name())]
        assert not form.is_valid()

        form2: OutlineForm = OutlineForm(
            {
                "name": self.random_lower_string(),
                "date": "20-05-10",
                "world": f"{world.pk}",
            },
        )
        form2.fields["world"].choices = [(f"{world.pk}", world.game_name())]
        assert not form2.is_valid()
