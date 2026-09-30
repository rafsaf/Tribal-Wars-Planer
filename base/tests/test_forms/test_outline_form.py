# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

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
        form.fields["world"].choices = [(f"{world.pk}", world.game_name())]  # type: ignore
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
        form.fields["world"].choices = [(f"{world.pk}", world.game_name())]  # type: ignore
        assert not form.is_valid()

        form2: OutlineForm = OutlineForm(
            {
                "name": self.random_lower_string(),
                "date": "20-05-10",
                "world": f"{world.pk}",
            },
        )
        form2.fields["world"].choices = [(f"{world.pk}", world.game_name())]  # type: ignore
        assert not form2.is_valid()
