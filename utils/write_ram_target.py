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

from collections.abc import Callable, Generator
from secrets import SystemRandom
from statistics import mean

from base.models import Outline, WeightMaximum, WeightModel
from base.models import TargetVertex as Target
from utils.basic.ruin import RuinHandle


class WriteRamTarget:
    """
    Single step in making auto outline for given target
    Only OFF, FAKE OFF, RUIN ATTACK

    if self.ruin is True, we assume that ONLY ruin attacks are there

    1. Quering self.default_query (get WeightMaximum, first query)
    Result depend on targets specifications

    2. Then update states (update WeightMaximum, second query)

    3. Finally return list[WeightModel] ready to create orders
    """

    def __init__(
        self,
        target: Target,
        outline: Outline,
        weight_max_list: list[WeightMaximum],
        random: SystemRandom,
        ruin: bool = False,
    ):
        self.target: Target = target
        self.outline: Outline = outline
        self.index: int = 0
        self.weight_max_list: list[WeightMaximum] = weight_max_list
        self.filters: list[Callable[[WeightMaximum], bool]] = []
        self.ruin: bool = ruin
        self.ruin_handle: RuinHandle | None = None
        self.building_generator: Generator | None = None

        self.random = random
        self.avg_dist: float = mean((self.target.enter_t1, self.target.enter_t2))
        self.interval_dist = self.target.enter_t2 - self.avg_dist
        self.dividier = (
            self.outline.world.speed_world * self.outline.world.speed_units * 2
        )

    def sorted_weights_offs(self, catapults: int = 50) -> list[WeightMaximum]:
        self.filters.append(self._only_closer_than_maximum_off_dist())

        if self.target.fake:
            self.filters.append(self._fake_query())
        elif self.ruin:
            self.filters.append(self._ruin_query(catapults=catapults))
        else:
            self.filters.append(self._off_query())

        if self.outline.morale_on and self.outline.world.morale > 0:
            self.filters.append(self._morale_query())

        if self.target.mode_off == "closest":
            self.index = 30000
            if self.ruin:
                self.index += 40000
            return self._closest_weight_lst()

        elif self.target.mode_off == "close":
            self.filters.append(self._first_line_false_query())
            self.index = 20000
            if self.ruin:
                self.index += 40000
            return self._close_weight_lst()

        elif self.target.mode_off == "random":
            self.filters.append(self._first_line_false_query())
            self.index = 10000
            if self.ruin:
                self.index += 40000
            return self._random_weight_lst()

        else:  # self.target.mode_off == "far":
            self.filters.append(self._first_line_false_query())
            self.index = 0
            if self.ruin:
                self.index += 40000
            return self._far_weight_lst()

    def weight_create_list(self) -> list[WeightModel]:
        weights_create_lst: list[WeightModel] = []
        self._set_building_generator()
        if self.ruin:
            ruins_set: set[WeightMaximum] = set()
            for catapult_val in [200, 150, 100, 75, 50, 25]:
                if (
                    self.outline.initial_outline_catapult_min_value
                    <= catapult_val
                    <= self.outline.initial_outline_catapult_max_value
                ):
                    ruins_set |= set(self.sorted_weights_offs(catapult_val))
                    self.filters = []
                    if len(ruins_set) >= self.target.required_off:
                        break

            off_lst: list[WeightMaximum] = list(ruins_set)

            off_lst.sort(key=lambda weight: -weight.catapult_left)
            off_lst = off_lst[: self.target.required_off]
            off_lst.sort(key=lambda weight: -weight.distance)
        else:
            off_lst: list[WeightMaximum] = self.sorted_weights_offs()
        i: int
        weight_max: WeightMaximum
        for i, weight_max in enumerate(off_lst):
            try:
                catapult: int = self._catapult(weight_max)
            except StopIteration:
                break
            off: int = self._off(weight_max, catapult)
            building: str | None = self._building()
            fake_limit: int = self._fake_limit()

            weight = self._weight_model(weight_max, off, catapult, building, i)
            weights_create_lst.append(weight)

            self._update_weight_max(weight_max, off, catapult, fake_limit)

        return weights_create_lst

    def _set_building_generator(self) -> None:
        if self.ruin and len(self.outline.initial_outline_buildings) > 0:
            ruin_handle: RuinHandle = RuinHandle(outline=self.outline)
            self.ruin_handle = ruin_handle

    def _building(self) -> str | None:
        if self.ruin_handle is not None:
            building: str = self.ruin_handle.building()
            return building
        return None

    def _off(self, weight_max: WeightMaximum, catapult: int) -> int:
        if self.target.fake:
            return 100
        elif self.ruin:
            return catapult * 8
        else:  # real
            return weight_max.off_left

    def _fake_limit(self) -> int:
        if self.target.fake:
            return 1
        else:
            return 0

    def _catapult(self, weight_max: WeightMaximum) -> int:
        if self.target.fake:
            return 0
        elif self.ruin:
            if self.ruin_handle is None:
                raise ValueError("ruin handle var is none")
            return self.ruin_handle.best_catapult(weight_max)
        else:  # real
            return weight_max.catapult_left

    def _weight_model(
        self,
        weight_max: WeightMaximum,
        off: int,
        catapult: int,
        building: str | None,
        order: int,
    ) -> WeightModel:
        return WeightModel(
            target=self.target,
            player=weight_max.player,
            start=weight_max.start,
            state=weight_max,
            off=off,
            catapult=catapult,
            ruin=self.ruin,
            building=building,
            distance=weight_max.distance,  # type: ignore
            nobleman=0,
            order=order + self.index,
            first_line=weight_max.first_line,
        )

    @staticmethod
    def _update_weight_max(
        weight_max: WeightMaximum, off: int, catapult: int, fake_limit: int
    ) -> WeightMaximum:
        weight_max.off_state += off
        weight_max.off_left -= off
        weight_max.catapult_state += catapult
        weight_max.catapult_left -= catapult
        weight_max.fake_limit -= fake_limit

        return weight_max

    def _get_filtered_weight_max_list(self) -> list[WeightMaximum]:
        return [
            weight
            for weight in self.weight_max_list
            if all(filter_func(weight) for filter_func in self.filters)
        ]

    def _only_closer_than_maximum_off_dist(self) -> Callable[[WeightMaximum], bool]:
        def filter_closer_than_maximum_off_dist(weight_max: WeightMaximum) -> bool:
            return (
                getattr(weight_max, "distance")
                <= self.outline.initial_outline_maximum_off_dist
            )

        return filter_closer_than_maximum_off_dist

    def _fake_query(self) -> Callable[[WeightMaximum], bool]:
        def filter_fake(weight_max: WeightMaximum) -> bool:
            if self.outline.initial_outline_fake_mode == "off":
                return (
                    weight_max.fake_limit >= 1
                    and weight_max.off_left >= self.outline.initial_outline_min_off
                    and weight_max.off_left <= self.outline.initial_outline_max_off
                )
            else:
                return (
                    weight_max.fake_limit >= 1
                    and weight_max.off_left >= 100 + weight_max.catapult_left * 8
                )

        return filter_fake

    def _ruin_query(self, catapults: int = 50) -> Callable[[WeightMaximum], bool]:
        def filter_ruin(weight_max: WeightMaximum) -> bool:
            return (
                weight_max.catapult_left >= catapults
                and (
                    weight_max.off_left < self.outline.initial_outline_min_off
                    or weight_max.off_left > self.outline.initial_outline_max_off
                )
            ) or (
                weight_max.catapult_left
                >= (catapults + self.outline.initial_outline_off_left_catapult)
                and weight_max.off_left >= self.outline.initial_outline_min_off
                and weight_max.off_left <= self.outline.initial_outline_max_off
            )

        return filter_ruin

    def _morale_query(self) -> Callable[[WeightMaximum], bool]:
        def filter_morale(weight_max: WeightMaximum) -> bool:
            return weight_max.morale >= self.outline.morale_on_targets_greater_than

        return filter_morale

    def _off_query(self) -> Callable[[WeightMaximum], bool]:
        def filter_off(weight_max: WeightMaximum) -> bool:
            return (
                weight_max.off_left >= self.outline.initial_outline_min_off
                and weight_max.off_left <= self.outline.initial_outline_max_off
            )

        return filter_off

    def _add_night_bonus_annotations(self, weight_lst: list[WeightMaximum]) -> None:
        for weight_max in weight_lst:
            time_hours: int = getattr(weight_max, "distance") / self.dividier
            time_mod = time_hours % 24
            night_score = (self.avg_dist - time_mod + 24) % 24
            if (
                night_score >= 7 + self.interval_dist
                and night_score <= 24 - self.interval_dist
            ):
                score = 3
            elif (night_score >= 7 and night_score <= 24) or night_score == 0:
                score = 2
            else:
                score = 1
            setattr(weight_max, "night_bool", score)

    def _first_line_false_query(self) -> Callable[[WeightMaximum], bool]:
        def filter_first_line_false(weight_max: WeightMaximum) -> bool:
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
        filtered_weight_max.sort(key=lambda weigth: weigth.distance)  # type: ignore
        weight_list = filtered_weight_max[: 1 * self.target.required_off]
        weight_list.sort(key=lambda weight: -weight.distance)  # type: ignore
        return weight_list

    def _close_weight_lst(self) -> list[WeightMaximum]:
        filtered_weight_max = self._get_filtered_weight_max_list()
        if self.target.night_bonus:
            self._add_night_bonus_annotations(filtered_weight_max)
            filtered_weight_max.sort(
                key=lambda i: (-getattr(i, "night_bool"), getattr(i, "distance"))
            )
        else:
            filtered_weight_max.sort(key=lambda i: getattr(i, "distance"))

        weight_list: list[WeightMaximum] = list(
            filtered_weight_max[: 2 * self.target.required_off]
        )

        if len(weight_list) < self.target.required_off:
            required: int = len(weight_list)
        else:
            required: int = self.target.required_off

        sampled_weight_lst: list[WeightMaximum] = self.random.sample(
            weight_list, required
        )

        return sorted(
            sampled_weight_lst,
            key=lambda item: item.distance,  # type: ignore
            reverse=True,
        )

    def _random_query(
        self, weight_max_lst: list[WeightMaximum], night_bool: int | None
    ):
        def filter_night_bool(weight_max: WeightMaximum):
            if getattr(weight_max, "night_bool") == night_bool:
                return True
            return False

        if night_bool is not None:
            filtered_list = [i for i in weight_max_lst if filter_night_bool(i)]
        else:
            filtered_list = weight_max_lst
        self.random.shuffle(filtered_list)
        return filtered_list

    def _random_weight_lst(self) -> list[WeightMaximum]:
        filtered_weight_max = self._get_filtered_weight_max_list()
        if self.target.night_bonus:
            self._add_night_bonus_annotations(filtered_weight_max)
            result_lst: list[WeightMaximum] = []
            left_offs: int = self.target.required_off

            weight_list_3: list[WeightMaximum] = list(
                self._random_query(filtered_weight_max, night_bool=3)[:left_offs]
            )

            result_lst += weight_list_3
            left_offs -= len(weight_list_3)

            if left_offs > 0:
                weight_list_2: list[WeightMaximum] = list(
                    self._random_query(filtered_weight_max, night_bool=2)[:left_offs]
                )

                result_lst += weight_list_2
                left_offs -= len(weight_list_2)

                if left_offs > 0:
                    weight_list_1: list[WeightMaximum] = list(
                        self._random_query(filtered_weight_max, night_bool=1)[
                            :left_offs
                        ]
                    )

                    result_lst += weight_list_1
                    left_offs -= len(weight_list_1)

        else:
            result_lst: list[WeightMaximum] = list(
                self._random_query(filtered_weight_max, night_bool=None)[
                    : self.target.required_off
                ]
            )

        return sorted(
            result_lst,
            key=lambda item: item.distance,  # type: ignore
            reverse=True,
        )

    def _far_weight_lst(self) -> list[WeightMaximum]:
        filtered_weight_max = self._get_filtered_weight_max_list()

        if self.target.night_bonus:
            self._add_night_bonus_annotations(filtered_weight_max)
            filtered_weight_max.sort(
                key=lambda i: (-getattr(i, "night_bool"), -getattr(i, "distance"))
            )
        else:
            filtered_weight_max.sort(key=lambda i: -getattr(i, "distance"))

        weight_list: list[WeightMaximum] = list(
            filtered_weight_max[: 3 * self.target.required_off]
        )
        if len(weight_list) < self.target.required_off:
            required: int = len(weight_list)
        else:
            required: int = self.target.required_off

        sampled_weight_lst: list[WeightMaximum] = self.random.sample(
            weight_list, required
        )

        return sorted(
            sampled_weight_lst,
            key=lambda item: item.distance,  # type: ignore
            reverse=True,
        )
