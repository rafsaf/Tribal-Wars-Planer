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
        self.initial_outline_minimum_fake_noble_troops = (
            self.outline.initial_outline_minimum_fake_noble_troops
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

        if self.casual_attack_block_ratio is not None:
            self.filters.append(self._casual_attack_block_ratio())

        if self.target.fake:
            self.filters.append(self._minimal_fake_noble_off())
        else:
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
            first_off: int = self._first_off(weight_max, off)

            total_off = first_off + (noble_number - 1) * off

            first_catapult = 0
            catapult = 0

            # if you wonder why we must deal with catapults in this way
            # then i have no good anwser

            # if total off plus all remaining catapults off
            # is more than actually available units in a village...
            if total_off + weight_max.catapult_left * 8 > weight_max.off_left:
                # we need to use some catapults for first attack
                max_first = first_off // 8
                first_catapult = min(weight_max.catapult_left, max_first)
            # if this is still not enough...
            if (
                total_off + (weight_max.catapult_left - first_catapult) * 8
                > weight_max.off_left
            ):
                # we distribute leftovers to other attacks
                max_next = off // 8
                equal_split = (weight_max.catapult_left - first_catapult) // (
                    noble_number - 1
                )
                catapult = min(equal_split, max_next)

            total_catapults = first_catapult + (noble_number - 1) * catapult

            # if this is still not enough...
            if (
                total_off + (weight_max.catapult_left - total_catapults) * 8
                > weight_max.off_left
            ):
                # we give up and just use few less troops
                first_off = first_catapult * 8
                off = catapult * 8
                total_off = first_off + (noble_number - 1) * off

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
                    off=total_off,
                    catapult=total_catapults,
                    noble=noble_number,
                    order=i,
                )
                weights_create_lst.append(weight)

            self._update_weight_max(
                weight_max=weight_max,
                off_used=total_off,
                catapults_used=total_catapults,
                noble_used=noble_number if not self.target.fake else 0,
                fake_noble_used=noble_number if self.target.fake else 0,
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
            village_id=weight_max.village_id,
            player_id=weight_max.player_id,
        )

    @staticmethod
    def _update_weight_max(
        weight_max: FastWeightMaximum,
        off_used: int,
        catapults_used: int,
        noble_used: int = 0,
        fake_noble_used: int = 0,
    ) -> FastWeightMaximum:
        weight_max.off_state += off_used
        weight_max.off_left -= off_used
        weight_max.catapult_state += catapults_used
        weight_max.catapult_left -= catapults_used
        weight_max.nobleman_state += noble_used
        weight_max.nobleman_left -= noble_used
        weight_max.nobles_limit -= noble_used
        weight_max.nobleman_state += fake_noble_used
        weight_max.nobleman_left -= fake_noble_used
        weight_max.fake_nobles_limit -= fake_noble_used

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
                    nobles = weight_max.fake_nobles_allowed_to_use()
                else:
                    nobles = weight_max.nobles_allowed_to_use()

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
        off_left = weight_max.off_left
        if not self.target.fake and (
            off_left
            - weight_max.fake_nobles_allowed_to_use()
            * self.initial_outline_minimum_fake_noble_troops
            > weight_max.nobles_allowed_to_use()
            * self.initial_outline_minimum_noble_troops
        ):
            off_left -= (
                weight_max.fake_nobles_allowed_to_use()
                * self.initial_outline_minimum_fake_noble_troops
            )

        if self.target.fake:
            return self.initial_outline_minimum_fake_noble_troops

        if self.target.mode_division == "divide":
            return off_left // weight_max.nobles_allowed_to_use()

        if self.target.mode_division == "not_divide":
            return self.initial_outline_minimum_noble_troops

        if self.target.mode_division == "separatly":
            return self.initial_outline_minimum_noble_troops

        raise ValueError(
            "impossible configuration: %s: %s", weight_max.pk, self.outline.pk
        )

    def _first_off(self, weight_max: FastWeightMaximum, off: int) -> int:
        off_left = weight_max.off_left
        if not self.target.fake and (
            off_left
            - weight_max.fake_nobles_allowed_to_use()
            * self.initial_outline_minimum_fake_noble_troops
            > weight_max.nobles_allowed_to_use()
            * self.initial_outline_minimum_noble_troops
        ):
            off_left -= (
                weight_max.fake_nobles_allowed_to_use()
                * self.initial_outline_minimum_fake_noble_troops
            )

        if self.target.fake:
            return self.initial_outline_minimum_fake_noble_troops

        if self.target.mode_division == "divide":
            return off_left - (off * (weight_max.nobles_allowed_to_use() - 1))

        if self.target.mode_division == "not_divide":
            return off_left - (off * (weight_max.nobles_allowed_to_use() - 1))

        if self.target.mode_division == "separatly":
            return self.initial_outline_minimum_noble_troops

        raise ValueError(
            "impossible configuration: %s: %s", weight_max.pk, self.outline.pk
        )

    def _morale_query(self) -> Callable[[FastWeightMaximum], bool]:
        def filter_morale(weight_max: FastWeightMaximum) -> bool:
            return weight_max.morale >= self.morale_on_targets_greater_than

        return filter_morale

    def _minimal_noble_off(self) -> Callable[[FastWeightMaximum], bool]:
        def filter_noble_off(weight_max: FastWeightMaximum) -> bool:
            return weight_max.nobles_allowed_to_use() > 0

        return filter_noble_off

    def _minimal_fake_noble_off(self) -> Callable[[FastWeightMaximum], bool]:
        def filter_fake_noble(weight_max: FastWeightMaximum) -> bool:
            return weight_max.fake_nobles_allowed_to_use() > 0

        return filter_fake_noble

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
            return weight_max.distance <= self.initial_outline_target_dist

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
