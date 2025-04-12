# Copyright 2024 Rafał Safin (rafsaf). All Rights Reserved.
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

from typing import Any

import cython

from base.models.outline import Outline
from base.models.weight_maximum import WeightMaximum


class FastWeightMaximum:
    """
    Why this class exists?

    This class is used to speed up the process of calculating the outline.
    It is used in the outline_complete.py file, where the outline is calculated.

    The outline calculation is a very time-consuming process.
    Worst part was related to access to getable fields in the WeightMaximum model.
    It's very magic how field __get__ and __set__ methods are resolved in Django ORM,
    and it's really slow. It's completely not designed for such a high number of accesses.
    """

    def __init__(self, weight_max: WeightMaximum, index: int, outline: Outline) -> None:
        # index is a list index in the outline list of real WeightMaximum objects
        # so they can be updated in the same place after calculations
        self.index: cython.int = index

        self.pk = weight_max.pk
        self.start = weight_max.start
        self.coord_tuple: tuple[int, int] = (weight_max.x_coord, weight_max.y_coord)
        self.player = weight_max.player
        self.points: int = weight_max.points
        self.off_state: int = weight_max.off_state
        self.off_left: int = weight_max.off_left
        self.nobleman_state: int = weight_max.nobleman_state
        self.nobleman_left: int = weight_max.nobleman_left
        self.catapult_state: int = weight_max.catapult_state
        self.catapult_left: int = weight_max.catapult_left
        self.first_line: bool = weight_max.first_line
        self.fake_limit: int = weight_max.fake_limit
        self.nobles_limit: int = weight_max.nobles_limit
        self.distance: float = 0
        self.night_bool: int = 0
        self.morale: int = 0
        self.initial_outline_minimum_noble_troops: int = (
            outline.initial_outline_minimum_noble_troops
        )
        self.initial_outline_minimum_fake_noble_troops: int = (
            outline.initial_outline_minimum_fake_noble_troops
        )
        self.village_id: int = weight_max.village_id
        self.player_id: int = weight_max.player_id

    def __eq__(self, other: Any) -> bool:
        return self.pk == other.pk

    def __hash__(self) -> int:
        return hash(self.pk)

    def nobles_allowed_to_use(self) -> int:
        if self.initial_outline_minimum_noble_troops == 0:
            possible_nobles_by_min_off = self.nobleman_left
        else:
            possible_nobles_by_min_off = (
                self.off_left
            ) // self.initial_outline_minimum_noble_troops
        return min(self.nobleman_left, self.nobles_limit, possible_nobles_by_min_off)

    def fake_nobles_allowed_to_use(self) -> int:
        if self.initial_outline_minimum_fake_noble_troops == 0:
            possible_nobles_by_min_off = self.nobleman_left
        else:
            possible_nobles_by_min_off = (
                self.off_left
            ) // self.initial_outline_minimum_fake_noble_troops
        return min(self.nobleman_left, self.nobles_limit, possible_nobles_by_min_off)
