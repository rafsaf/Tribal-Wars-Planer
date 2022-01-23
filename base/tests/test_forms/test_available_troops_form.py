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

from base.forms import AvailableTroopsForm
from base.tests.test_utils.mini_setup import MiniSetup


class AvailableTroopsFormTest(MiniSetup):
    def test_form_pass_when_correct_data(self):
        form: AvailableTroopsForm = AvailableTroopsForm(
            {
                "initial_outline_min_off": 10,
                "initial_outline_max_off": 15,
                "initial_outline_front_dist": 15,
                "initial_outline_maximum_front_dist": 150,
                "initial_outline_target_dist": 100,
                "initial_outline_excluded_coords": "500|500",
            },
        )
        assert form.is_valid()

    def test_form_not_valid_when_min_radius_gt_max(self):
        form: AvailableTroopsForm = AvailableTroopsForm(
            {
                "initial_outline_min_off": 10,
                "initial_outline_max_off": 15,
                "initial_outline_front_dist": 150,
                "initial_outline_maximum_front_dist": 15,
                "initial_outline_target_dist": 100,
                "initial_outline_excluded_coords": "500|500",
            },
        )
        assert not form.is_valid()

    def test_form_not_valid_when_invalid_excluded_coords(self):
        form: AvailableTroopsForm = AvailableTroopsForm(
            {
                "initial_outline_min_off": 10,
                "initial_outline_max_off": 15,
                "initial_outline_front_dist": 15,
                "initial_outline_maximum_front_dist": 150,
                "initial_outline_target_dist": 100,
                "initial_outline_excluded_coords": "500XD500",
            },
        )
        assert not form.is_valid()

    def test_form_not_valid_when_invalid_max_off_is_greater_than_min(self):
        form: AvailableTroopsForm = AvailableTroopsForm(
            {
                "initial_outline_min_off": 15,
                "initial_outline_max_off": 10,
                "initial_outline_front_dist": 15,
                "initial_outline_maximum_front_dist": 25,
                "initial_outline_target_dist": 100,
                "initial_outline_excluded_coords": "500|500",
            },
        )
        assert not form.is_valid()

    def test_not_valid_when_empty_fields(self):
        form: AvailableTroopsForm = AvailableTroopsForm(
            {
                "initial_outline_min_off": "",
                "initial_outline_max_off": "",
                "initial_outline_front_dist": "",
                "initial_outline_maximum_front_dist": "",
                "initial_outline_target_dist": "",
                "initial_outline_excluded_coords": "",
            },
        )
        assert not form.is_valid()
