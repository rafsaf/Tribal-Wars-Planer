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

import math
from collections.abc import Callable
from secrets import SystemRandom

from base.models import Outline, WeightModel
from base.models import TargetVertex as Target
from utils.fast_weight_maximum import FastWeightMaximum


class WriteNobleTarget:
    """
    Single step in making auto outline for given target
    Only NOBLE, NOBLE FAKE

    self.deafult_create_list is list of tuples (FastWeightMaximum, int) which
    represents Villages with number of wirtten out nobles

    1. Quering self.default_query (get FastWeightMaximum, first query)
    Result depend on targets specifications

    2. Then update states (update FastWeightMaximum, second query)

    MODE_DIVISION = [
        "divide", "Divide off with nobles",

        "not_divide", "Dont't divide off",

        "separatly", "Off and nobles separatly",
    ]

    MODE_SPLIT = [
        "together", "Nobles from one village as one command",

        "split", "Nobles from one village as many commands",
    ]

    NOBLE_GUIDELINES = [
        "one", "Try send all nobles to one target",

        "many", "Nobles to one or many targets",

        "single", "Try single nobles from many villages",
    ]

    3. Finally return list[WeightModel] ready to create orders

    """

    def __init__(
        self,
        target: Target,
        outline: Outline,
        weight_max_list: list[FastWeightMaximum],
        random: SystemRandom,
    ):
        self.target: Target = target
        self.outline: Outline = outline
        self.index: int = 0
        self.weight_max_list: list[FastWeightMaximum] = weight_max_list
        self.filters: list[Callable[[FastWeightMaximum], bool]] = []
        self.default_create_list: list[tuple[FastWeightMaximum, int]] = []
        self.random = random

        self.initial_outline_minimum_noble_troops = (
            self.outline.initial_outline_minimum_noble_troops
        )
        self.casual_attack_block_ratio = self.outline.world.casual_attack_block_ratio
        self.morale = self.outline.world.morale
        self.morale_on = self.outline.morale_on
        self.mode_split = self.outline.mode_split
        self.morale_on_targets_greater_than = (
            self.outline.morale_on_targets_greater_than
        )
        self.initial_outline_target_dist = self.outline.initial_outline_target_dist
        self.initial_outline_front_dist = self.outline.initial_outline_front_dist

    def sorted_weights_nobles(self) -> list[FastWeightMaximum]:
        self.filters.append(self._only_closer_than_target_dist())
        self.filters.append(self._noble_query())

        if self.casual_attack_block_ratio is not None:
            self.filters.append(self._casual_attack_block_ratio())

        if not self.target.fake:
            self.filters.append(self._minimal_noble_off())

        if self.morale_on and self.morale > 0:
            self.filters.append(self._morale_query())

        if self.target.mode_noble == "closest":
            self.index = 110000
            return self._closest_weight_lst()

        elif self.target.mode_noble == "close":
            self.filters.append(self._first_line_false_query())
            self.index = 100000
            return self._close_weight_lst()

        elif self.target.mode_noble == "random":
            self.filters.append(self._first_line_false_query())
            self.index = 90000
            return self._random_weight_lst()

        else:  # self.target.mode_off == "far":
            self.filters.append(self._first_line_false_query())
            self.index = 80000
            return self._far_weight_lst()

    def weight_create_list(self) -> list[WeightModel]:
        weights_create_lst: list[WeightModel] = []

        weight_max_list = self.sorted_weights_nobles()

        if self.target.mode_guide == "one":  # (one weight)-(one target) prefer
            self._mode_guide_is_one(weight_max_list)

        elif self.target.mode_guide == "many":  # optimal- one or many
            self._mode_guide_is_many(weight_max_list)

        else:  # self.target.mode_guide == "single" # only single nobles from many weights
            self._mode_guide_is_single(weight_max_list)

        self._order_distance_default_list()

        i: int
        weight_max: FastWeightMaximum
        noble_number: int
        for i, (weight_max, noble_number) in enumerate(self.default_create_list):
            off: int = self._off(weight_max)
            catapult: int = self._catapult(weight_max)
            first_off: int = self._first_off(weight_max, off)
            first_catapult: int = self._first_catapult(weight_max, catapult)
            off_to_left: int = self._off_to_left(weight_max, off, noble_number)
            catapult_to_left: int = self._catapult_to_left(
                weight_max, catapult, noble_number
            )

            if self.mode_split == "split":
                for index in range(noble_number):
                    if index == 0:
                        off_troops = first_off
                        catapult_troops = first_catapult
                    else:
                        off_troops = off
                        catapult_troops = catapult

                    weight: WeightModel = self._weight_model(
                        weight_max=weight_max,
                        off=off_troops,
                        catapult=catapult_troops,
                        noble=1,
                        order=i * 15 + index,
                    )
                    weights_create_lst.append(weight)

            else:  # self.mode_split == "together":
                weight = self._weight_model(
                    weight_max=weight_max,
                    off=first_off + (noble_number - 1) * off,
                    catapult=first_catapult + (noble_number - 1) * catapult,
                    noble=noble_number,
                    order=i,
                )
                weights_create_lst.append(weight)

            self._update_weight_max(
                weight_max, off_to_left, catapult_to_left, noble_number
            )

        return weights_create_lst

    def _weight_model(
        self,
        weight_max: FastWeightMaximum,
        off: int,
        catapult: int,
        noble: int,
        order: int,
    ) -> WeightModel:
        return WeightModel(
            target_id=self.target.pk,
            player=weight_max.player,
            start=weight_max.start,
            state_id=weight_max.pk,
            off=off,
            catapult=catapult,
            distance=weight_max.distance,
            nobleman=noble,
            order=order + self.index,
            first_line=weight_max.first_line,
        )

    @staticmethod
    def _update_weight_max(
        weight_max: FastWeightMaximum,
        off_to_left: int,
        catapult_to_left: int,
        noble_number: int,
    ) -> FastWeightMaximum:
        weight_max.off_state += weight_max.off_left - off_to_left
        weight_max.off_left = off_to_left
        weight_max.catapult_state += weight_max.catapult_left - catapult_to_left
        weight_max.catapult_left = catapult_to_left
        weight_max.nobleman_state += noble_number
        weight_max.nobleman_left = weight_max.nobleman_left - noble_number
        weight_max.nobles_limit -= noble_number

        return weight_max

    def _order_distance_default_list(self) -> None:
        def order_func(weight_tuple: tuple[FastWeightMaximum, int]) -> float:
            return -weight_tuple[0].distance

        self.default_create_list.sort(key=order_func)

    def _fill_default_list(self, sorted_list: list[FastWeightMaximum]) -> None:
        weight_max: FastWeightMaximum
        for weight_max in sorted_list:
            if self.target.required_noble > 0:
                if self.target.mode_guide == "single":
                    nobles: int = 1
                elif self.target.fake:
                    nobles = min(weight_max.nobleman_left, weight_max.nobles_limit)
                else:
                    nobles = weight_max.nobles_allowed_to_use

                if nobles >= self.target.required_noble:
                    self.default_create_list.append(
                        (weight_max, self.target.required_noble)
                    )
                    self.target.required_noble = 0
                else:
                    self.default_create_list.append((weight_max, nobles))
                    self.target.required_noble -= nobles

    def _mode_guide_is_one(self, weight_max_list: list[FastWeightMaximum]) -> None:
        """
        Updates self.default_create_list attribute

        This case represents ONE weight - ONE target prefer
        Best fit is weight_max with exact number of (required nobles) nobles
        Then we use weight_max with (required nobles +1) nobles and so on (+2, +3...)
        Then we use weight_max with (required nobles -1) nobles and so on (-2, -3...)
        """

        def sort_func(weight_max: FastWeightMaximum) -> tuple[int, float, int, int]:
            fit: int = abs(weight_max.nobleman_left - self.target.required_noble)
            distance: float = float(weight_max.distance)
            off: int = -int(weight_max.off_left)
            number: int = -int(weight_max.nobleman_left)
            return (fit, distance, off, number)

        sorted_weight_max_lst: list[FastWeightMaximum] = sorted(
            weight_max_list, key=sort_func
        )
        self._fill_default_list(sorted_weight_max_lst)

    def _mode_guide_is_many(self, weight_max_list: list[FastWeightMaximum]) -> None:
        """
        Updates self.default_create_list attribute

        This case represents OPTIMAL FIT, depend of off troops and distance
        """

        def sort_func(weight_max: FastWeightMaximum) -> tuple[float, int]:
            off: int = -int(weight_max.off_left)
            distance: float = float(weight_max.distance)
            return (distance, off)

        sorted_weight_max_lst: list[FastWeightMaximum] = sorted(
            weight_max_list, key=sort_func
        )
        self._fill_default_list(sorted_weight_max_lst)

    def _mode_guide_is_single(self, weight_max_list: list[FastWeightMaximum]) -> None:
        """
        Updates self.default_create_list attribute

        This case represents FROM MANY case, depend of off troops and distance
        Later we decide to use only one noble from every village
        """

        def sort_func(weight_max: FastWeightMaximum) -> tuple[float, int]:
            off: int = -int(weight_max.off_left)
            distance: float = float(weight_max.distance)
            return (distance, off)

        sorted_weight_max_lst: list[FastWeightMaximum] = sorted(
            weight_max_list, key=sort_func
        )
        self._fill_default_list(sorted_weight_max_lst)

    def _off(self, weight_max: FastWeightMaximum) -> int:
        if self.target.fake:
            return 0

        elif weight_max.off_left < 200 * weight_max.nobles_allowed_to_use:
            return weight_max.off_left // weight_max.nobles_allowed_to_use

        elif self.target.mode_division == "divide":
            return weight_max.off_left // weight_max.nobles_allowed_to_use

        elif self.target.mode_division == "not_divide":
            return 200

        else:  # self.target.mode_division == "separatly"
            return 200

    def _first_off(self, weight_max: FastWeightMaximum, off: int) -> int:
        if self.target.fake:
            return 0

        elif weight_max.off_left < 200 * weight_max.nobles_allowed_to_use:
            return weight_max.off_left - (off * (weight_max.nobles_allowed_to_use - 1))

        elif self.target.mode_division == "divide":
            return weight_max.off_left - (off * (weight_max.nobles_allowed_to_use - 1))

        elif self.target.mode_division == "not_divide":
            return weight_max.off_left - (off * (weight_max.nobles_allowed_to_use - 1))

        else:  # self.target.mode_division == "separatly"
            return 200

    def _catapult(self, weight_max: FastWeightMaximum) -> int:
        if self.target.fake:
            return 0

        elif weight_max.off_left < 200 * weight_max.nobles_allowed_to_use:
            return weight_max.catapult_left // weight_max.nobles_allowed_to_use

        elif self.target.mode_division == "divide":
            return weight_max.catapult_left // weight_max.nobles_allowed_to_use

        elif self.target.mode_division == "not_divide":
            return 0

        else:  # self.target.mode_division == "separatly"
            return 0

    def _first_catapult(self, weight_max: FastWeightMaximum, catapult: int) -> int:
        if self.target.fake:
            return 0

        elif weight_max.off_left < 200 * weight_max.nobles_allowed_to_use:
            return weight_max.catapult_left - (
                catapult * (weight_max.nobles_allowed_to_use - 1)
            )

        elif self.target.mode_division == "divide":
            return weight_max.catapult_left - (
                catapult * (weight_max.nobles_allowed_to_use - 1)
            )

        elif self.target.mode_division == "not_divide":
            return weight_max.catapult_left

        else:  # self.target.mode_division == "separatly"
            return 0

    def _off_to_left(  # noqa: PLR0911
        self, weight_max: FastWeightMaximum, off: int, noble: int
    ) -> int:
        if self.target.fake:
            return weight_max.off_left

        elif weight_max.off_left < 200 * weight_max.nobles_allowed_to_use:
            if weight_max.nobles_allowed_to_use > noble:
                return off * (weight_max.nobles_allowed_to_use - noble)
            return 0

        elif self.target.mode_division == "divide":
            if weight_max.nobles_allowed_to_use > noble:
                return off * (weight_max.nobles_allowed_to_use - noble)
            return 0

        elif self.target.mode_division == "not_divide":
            if weight_max.nobles_allowed_to_use > noble:
                return 200 * (weight_max.nobles_allowed_to_use - noble)
            return 0

        else:  # self.target.mode_division == "separatly"
            return weight_max.off_left - (off * (noble))

    def _catapult_to_left(  # noqa: PLR0911
        self, weight_max: FastWeightMaximum, catapult: int, noble: int
    ) -> int:
        if self.target.fake:
            return weight_max.catapult_left

        elif weight_max.off_left < 200 * weight_max.nobles_allowed_to_use:
            if weight_max.nobles_allowed_to_use > noble:
                return catapult * (weight_max.nobles_allowed_to_use - noble)
            return 0

        elif self.target.mode_division == "divide":
            if weight_max.nobles_allowed_to_use > noble:
                return catapult * (weight_max.nobles_allowed_to_use - noble)
            return 0

        elif self.target.mode_division == "not_divide":
            return 0

        else:  # self.target.mode_division == "separatly"
            return weight_max.catapult_left

    def _morale_query(self) -> Callable[[FastWeightMaximum], bool]:
        def filter_morale(weight_max: FastWeightMaximum) -> bool:
            return weight_max.morale >= self.morale_on_targets_greater_than

        return filter_morale

    def _noble_query(self) -> Callable[[FastWeightMaximum], bool]:
        def filter_noble(weight_max: FastWeightMaximum) -> bool:
            return weight_max.nobleman_left >= 1 and weight_max.nobles_limit >= 1

        return filter_noble

    def _minimal_noble_off(self) -> Callable[[FastWeightMaximum], bool]:
        def filter_noble(weight_max: FastWeightMaximum) -> bool:
            return weight_max.off_left >= self.initial_outline_minimum_noble_troops

        return filter_noble

    def _casual_attack_block_ratio(self) -> Callable[[FastWeightMaximum], bool]:
        if self.casual_attack_block_ratio is None:
            raise RuntimeError("expected world casual_attack_block_ratio to be int")
        world_ratio = (100 + self.casual_attack_block_ratio) / 100

        def filter_casual_attack_block_ratio(weight_max: FastWeightMaximum) -> bool:
            if self.target.player == "":
                # special case barbarians
                return True
            smaller_points = min(weight_max.points, self.target.points)
            bigger_points = max(weight_max.points, self.target.points)
            max_possible = math.floor(world_ratio * smaller_points)
            return bigger_points <= max_possible

        return filter_casual_attack_block_ratio

    def _get_filtered_weight_max_list(self) -> list[FastWeightMaximum]:
        def filter_func(weight_max: FastWeightMaximum) -> bool:
            for filter_func in self.filters:
                if not filter_func(weight_max):
                    return False
            return True

        return [
            weight for weight in self.weight_max_list if filter_func(weight_max=weight)
        ]

    def _only_closer_than_target_dist(self) -> Callable[[FastWeightMaximum], bool]:
        def filter_close_than_target_dist(weight_max: FastWeightMaximum) -> bool:
            return weight_max.distance <= self.outline.initial_outline_target_dist

        return filter_close_than_target_dist

    def _first_line_false_query(self) -> Callable[[FastWeightMaximum], bool]:
        def filter_first_line_false(weight_max: FastWeightMaximum) -> bool:
            return (
                not weight_max.first_line
                and weight_max.distance >= self.initial_outline_front_dist
            )

        return filter_first_line_false

    def _closest_weight_lst(self) -> list[FastWeightMaximum]:
        filtered_weight_max = self._get_filtered_weight_max_list()
        filtered_weight_max.sort(key=lambda weight: weight.distance)

        weight_list: list[FastWeightMaximum] = filtered_weight_max[:15]
        return weight_list

    def _close_weight_lst(self) -> list[FastWeightMaximum]:
        filtered_weight_max = self._get_filtered_weight_max_list()
        filtered_weight_max.sort(key=lambda weight: weight.distance)

        weight_list: list[FastWeightMaximum] = filtered_weight_max[:15]
        return weight_list

    def _random_weight_lst(self) -> list[FastWeightMaximum]:
        filtered_weight_max = self._get_filtered_weight_max_list()
        weight_list: list[FastWeightMaximum] = self.random.sample(
            filtered_weight_max, min(15, len(filtered_weight_max))
        )

        return sorted(
            weight_list,
            key=lambda item: item.distance,
        )

    def _far_weight_lst(self) -> list[FastWeightMaximum]:
        filtered_weight_max = self._get_filtered_weight_max_list()
        filtered_weight_max.sort(key=lambda weight: -weight.distance)

        weight_list: list[FastWeightMaximum] = filtered_weight_max[:15]
        return sorted(
            weight_list,
            key=lambda item: item.distance,
        )
