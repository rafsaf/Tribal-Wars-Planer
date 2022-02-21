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

from secrets import SystemRandom
from typing import Callable

from base.models import Outline
from base.models import TargetVertex as Target
from base.models import WeightMaximum, WeightModel


class WriteNobleTarget:
    """
    Single step in making auto outline for given target
    Only NOBLE, NOBLE FAKE

    self.deafult_create_list is list of tuples (WeightMaximum, int) which
    represents Villages with number of wirtten out nobles

    1. Quering self.default_query (get WeightMaximum, first query)
    Result depend on targets specifications

    2. Then update states (update WeightMaximum, second query)

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
        weight_max_list: list[WeightMaximum],
        random: SystemRandom,
    ):
        self.target: Target = target
        self.outline: Outline = outline
        self.index: int = 0
        self.weight_max_list: list[WeightMaximum] = weight_max_list
        self.filters: list[Callable[[WeightMaximum], bool]] = []
        self.default_create_list: list[tuple[WeightMaximum, int]] = []
        self.random = random

    def sorted_weights_nobles(self) -> list[WeightMaximum]:
        self.filters.append(self._noble_query())
        self.filters.append(self._only_closer_than_target_dist())

        if self.outline.morale_on and self.outline.world.morale > 0:
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

    def weight_create_list(self) -> tuple[list[WeightModel], list[WeightMaximum]]:
        weights_max_update_lst: list[WeightMaximum] = []
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
        weight_max: WeightMaximum
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

            if self.outline.mode_split == "split":
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

            else:  # self.outline.mode_split == "together":
                weight: WeightModel = self._weight_model(
                    weight_max=weight_max,
                    off=first_off + (noble_number - 1) * off,
                    catapult=first_catapult + (noble_number - 1) * catapult,
                    noble=noble_number,
                    order=i,
                )
                weights_create_lst.append(weight)

            weights_max_update_lst.append(
                self._updated_weight_max(
                    weight_max, off_to_left, catapult_to_left, noble_number
                )
            )

        return weights_create_lst, weights_max_update_lst

    def _weight_model(
        self,
        weight_max: WeightMaximum,
        off: int,
        catapult: int,
        noble: int,
        order: int,
    ) -> WeightModel:

        return WeightModel(
            target=self.target,
            player=weight_max.player,
            start=weight_max.start,
            state=weight_max,
            off=off,
            catapult=catapult,
            distance=weight_max.distance,  # type: ignore
            nobleman=noble,
            order=order + self.index,
            first_line=weight_max.first_line,
        )

    @staticmethod
    def _updated_weight_max(
        weight_max: WeightMaximum,
        off_to_left: int,
        catapult_to_left: int,
        noble_number: int,
    ) -> WeightMaximum:
        weight_max.off_state += weight_max.off_left - off_to_left
        weight_max.off_left = off_to_left
        weight_max.catapult_state += weight_max.catapult_left - catapult_to_left
        weight_max.catapult_left = catapult_to_left
        weight_max.nobleman_state += noble_number
        weight_max.nobleman_left = weight_max.nobleman_left - noble_number

        return weight_max

    def _order_distance_default_list(self) -> None:
        def order_func(weight_tuple: tuple[WeightMaximum, int]) -> int:
            weight_max: WeightMaximum = weight_tuple[0]
            return -weight_max.distance  # type: ignore

        self.default_create_list.sort(key=order_func)

    def _fill_default_list(
        self, sorted_list: list[WeightMaximum], single: bool = False
    ) -> None:
        weight_max: WeightMaximum
        for weight_max in sorted_list:
            if self.target.required_noble > 0:
                if single:
                    nobles: int = 1
                else:
                    nobles: int = weight_max.nobleman_left

                if nobles >= self.target.required_noble:
                    self.default_create_list.append(
                        (weight_max, self.target.required_noble)
                    )
                    self.target.required_noble = 0
                else:
                    self.default_create_list.append((weight_max, nobles))
                    self.target.required_noble -= nobles

    def _mode_guide_is_one(self, weight_max_list: list[WeightMaximum]) -> None:
        """
        Updates self.default_create_list attribute

        This case represents ONE weight - ONE target prefer
        Best fit is weight_max with exact number of (required nobles) nobles
        Then we use weight_max with (required nobles +1) nobles and so on (+2, +3...)
        Then we use weight_max with (required nobles -1) nobles and so on (-2, -3...)
        """

        def sort_func(weight_max: WeightMaximum) -> tuple[int, float, int, int]:
            fit: int = abs(weight_max.nobleman_left - self.target.required_noble)
            distance: float = float(weight_max.distance)  # type: ignore
            off: int = -int(weight_max.off_left)
            number: int = -int(weight_max.nobleman_left)
            return (fit, distance, off, number)

        sorted_weight_max_lst: list[WeightMaximum] = sorted(
            weight_max_list, key=sort_func
        )
        self._fill_default_list(sorted_weight_max_lst)

    def _mode_guide_is_many(self, weight_max_list: list[WeightMaximum]) -> None:
        """
        Updates self.default_create_list attribute

        This case represents OPTIMAL FIT, depend of off troops and distance
        """

        def sort_func(weight_max: WeightMaximum) -> tuple[float, int]:
            off: int = -int(weight_max.off_left)
            distance: float = float(weight_max.distance)  # type: ignore
            return (distance, off)

        sorted_weight_max_lst: list[WeightMaximum] = sorted(
            weight_max_list, key=sort_func
        )
        self._fill_default_list(sorted_weight_max_lst)

    def _mode_guide_is_single(self, weight_max_list: list[WeightMaximum]) -> None:
        """
        Updates self.default_create_list attribute

        This case represents FROM MANY case, depend of off troops and distance
        Later we decide to use only one noble from every village by using single=True
        """

        def sort_func(weight_max: WeightMaximum) -> tuple[float, int]:
            off: int = -int(weight_max.off_left)
            distance: float = float(weight_max.distance)  # type: ignore
            return (distance, off)

        sorted_weight_max_lst: list[WeightMaximum] = sorted(
            weight_max_list, key=sort_func
        )
        self._fill_default_list(sorted_weight_max_lst, single=True)

    def _off(self, weight_max: WeightMaximum) -> int:
        if self.target.fake:
            return 0

        elif weight_max.off_left < 200 * weight_max.nobleman_left:
            return weight_max.off_left // weight_max.nobleman_left

        elif self.target.mode_division == "divide":
            return weight_max.off_left // weight_max.nobleman_left

        elif self.target.mode_division == "not_divide":
            return 200

        else:  # self.target.mode_division == "separatly"
            return 200

    def _first_off(self, weight_max: WeightMaximum, off: int) -> int:
        if self.target.fake:
            return 0

        elif weight_max.off_left < 200 * weight_max.nobleman_left:
            return weight_max.off_left - (off * (weight_max.nobleman_left - 1))

        elif self.target.mode_division == "divide":
            return weight_max.off_left - (off * (weight_max.nobleman_left - 1))

        elif self.target.mode_division == "not_divide":
            return weight_max.off_left - (off * (weight_max.nobleman_left - 1))

        else:  # self.target.mode_division == "separatly"
            return 200

    def _catapult(self, weight_max: WeightMaximum) -> int:
        if self.target.fake:
            return 0

        elif weight_max.off_left < 200 * weight_max.nobleman_left:
            return weight_max.catapult_left // weight_max.nobleman_left

        elif self.target.mode_division == "divide":
            return weight_max.catapult_left // weight_max.nobleman_left

        elif self.target.mode_division == "not_divide":
            return 0

        else:  # self.target.mode_division == "separatly"
            return 0

    def _first_catapult(self, weight_max: WeightMaximum, catapult: int) -> int:
        if self.target.fake:
            return 0

        elif weight_max.off_left < 200 * weight_max.nobleman_left:
            return weight_max.catapult_left - (
                catapult * (weight_max.nobleman_left - 1)
            )

        elif self.target.mode_division == "divide":
            return weight_max.catapult_left - (
                catapult * (weight_max.nobleman_left - 1)
            )

        elif self.target.mode_division == "not_divide":
            return weight_max.catapult_left

        else:  # self.target.mode_division == "separatly"
            return 0

    def _off_to_left(self, weight_max: WeightMaximum, off: int, noble: int) -> int:
        if self.target.fake:
            return weight_max.off_left

        elif weight_max.off_left < 200 * weight_max.nobleman_left:
            if weight_max.nobleman_left > noble:
                return off * (weight_max.nobleman_left - noble)
            return 0

        elif self.target.mode_division == "divide":
            if weight_max.nobleman_left > noble:
                return off * (weight_max.nobleman_left - noble)
            return 0

        elif self.target.mode_division == "not_divide":
            if weight_max.nobleman_left > noble:
                return 200 * (weight_max.nobleman_left - noble)
            return 0

        else:  # self.target.mode_division == "separatly"
            return weight_max.off_left - (off * (noble))

    def _catapult_to_left(
        self, weight_max: WeightMaximum, catapult: int, noble: int
    ) -> int:
        if self.target.fake:
            return weight_max.catapult_left

        elif weight_max.off_left < 200 * weight_max.nobleman_left:
            if weight_max.nobleman_left > noble:
                return catapult * (weight_max.nobleman_left - noble)
            return 0

        elif self.target.mode_division == "divide":
            if weight_max.nobleman_left > noble:
                return catapult * (weight_max.nobleman_left - noble)
            return 0

        elif self.target.mode_division == "not_divide":
            return 0

        else:  # self.target.mode_division == "separatly"
            return weight_max.catapult_left

    def _morale_query(self):
        def filter_morale(weight_max: WeightMaximum):
            if weight_max.morale >= self.outline.morale_on_targets_greater_than:
                return True
            return False

        return filter_morale

    def _noble_query(self):
        def filter_noble(weight_max: WeightMaximum):
            if (
                weight_max.nobleman_left >= 1
                and weight_max.off_left >= 200 + weight_max.catapult_left * 8
            ):
                return True
            return False

        return filter_noble

    def _only_closer_than_target_dist(self):
        def filter_close_than_target_dist(weight_max: WeightMaximum) -> bool:
            return (
                getattr(weight_max, "distance")
                <= self.outline.initial_outline_target_dist
            )

        return filter_close_than_target_dist

    def _get_filtered_weight_max_list(self):
        def all_filters_match(weight_max: WeightMaximum):
            for filter_func in self.filters:
                if not filter_func(weight_max):
                    return False
            return True

        return [weight for weight in self.weight_max_list if all_filters_match(weight)]

    def _first_line_false_query(self):
        def filter_first_line_false(weight_max: WeightMaximum):
            if (
                not weight_max.first_line
                and getattr(weight_max, "distance")
                >= self.outline.initial_outline_front_dist
            ):
                return True
            return False

        return filter_first_line_false

    def _closest_weight_lst(self) -> list[WeightMaximum]:
        filtered_weight_max = self._get_filtered_weight_max_list()
        filtered_weight_max.sort(key=lambda weight: getattr(weight, "distance"))

        weight_list: list[WeightMaximum] = filtered_weight_max[:15]
        return weight_list

    def _close_weight_lst(self) -> list[WeightMaximum]:
        filtered_weight_max = self._get_filtered_weight_max_list()
        filtered_weight_max.sort(key=lambda weight: getattr(weight, "distance"))

        weight_list: list[WeightMaximum] = filtered_weight_max[:15]
        return weight_list

    def _random_weight_lst(self) -> list[WeightMaximum]:
        filtered_weight_max = self._get_filtered_weight_max_list()
        self.random.shuffle(filtered_weight_max)

        weight_list: list[WeightMaximum] = filtered_weight_max[:15]
        return sorted(
            weight_list,
            key=lambda item: item.distance,  # type: ignore
        )

    def _far_weight_lst(self) -> list[WeightMaximum]:
        filtered_weight_max = self._get_filtered_weight_max_list()
        filtered_weight_max.sort(key=lambda weight: -getattr(weight, "distance"))

        weight_list: list[WeightMaximum] = filtered_weight_max[:15]
        return sorted(
            weight_list,
            key=lambda item: item.distance,  # type: ignore
        )
