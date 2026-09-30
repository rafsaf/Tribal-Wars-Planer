# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

from base.forms import AvailableTroopsForm
from base.tests.test_utils.mini_setup import MiniSetup


class AvailableTroopsFormTest(MiniSetup):
    def test_form_pass_when_correct_data(self):
        form: AvailableTroopsForm = AvailableTroopsForm(
            {
                "initial_outline_min_off": 10,
                "initial_outline_max_off": 15,
                "initial_outline_front_dist": 15,
                "initial_outline_target_dist": 100,
                "initial_outline_maximum_off_dist": 111,
                "initial_outline_excluded_coords": "500|500",
            },
            instance=self.get_outline(),
        )
        assert form.is_valid()

    def test_form_not_valid_when_invalid_excluded_coords(self):
        form: AvailableTroopsForm = AvailableTroopsForm(
            {
                "initial_outline_min_off": 10,
                "initial_outline_max_off": 15,
                "initial_outline_front_dist": 15,
                "initial_outline_target_dist": 100,
                "initial_outline_maximum_off_dist": 111,
                "initial_outline_excluded_coords": "500XD500",
            },
            instance=self.get_outline(),
        )
        assert not form.is_valid()

    def test_form_not_valid_when_invalid_max_off_is_greater_than_min(self):
        form: AvailableTroopsForm = AvailableTroopsForm(
            {
                "initial_outline_min_off": 15,
                "initial_outline_max_off": 10,
                "initial_outline_front_dist": 15,
                "initial_outline_target_dist": 100,
                "initial_outline_maximum_off_dist": 111,
                "initial_outline_excluded_coords": "500|500",
            },
            instance=self.get_outline(),
        )
        assert not form.is_valid()

    def test_not_valid_when_empty_fields(self):
        form: AvailableTroopsForm = AvailableTroopsForm(
            {
                "initial_outline_min_off": "",
                "initial_outline_max_off": "",
                "initial_outline_front_dist": "",
                "initial_outline_target_dist": "",
                "initial_outline_maximum_off_dist": "",
                "initial_outline_excluded_coords": "",
            },
            instance=self.get_outline(),
        )
        assert not form.is_valid()
