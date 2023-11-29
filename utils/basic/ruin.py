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

from collections.abc import Iterator

from base.models import Outline, WeightMaximum


class RuinHandle:
    BIG_LEVELS: dict[str, int] = {
        "headquarters": 20,
        "barracks": 25,
        "stable": 20,
        "workshop": 10,
        "academy": 1,
        "smithy": 20,
        "market": 22,
        "statue": 1,
        "rally_point": 1,
        "timber_camp": 30,
        "clay_pit": 30,
        "iron_mine": 30,
        "farm": 30,
        "warehouse": 30,
        "wall": 20,
    }
    SMALL_LEVELS: dict[str, int] = {
        "headquarters": 20,
        "barracks": 18,
        "stable": 10,
        "workshop": 5,
        "academy": 1,
        "smithy": 20,
        "market": 15,
        "statue": 1,
        "rally_point": 1,
        "timber_camp": 25,
        "clay_pit": 25,
        "iron_mine": 25,
        "farm": 25,
        "warehouse": 24,
        "wall": 20,
    }
    LEVEL_DICTIONARY: dict[tuple[int, int], int] = {
        (20, 1): 0,
        (25, 30): 29,
        (25, 29): 28,
        (25, 28): 27,
        (25, 27): 26,
        (25, 26): 25,
        (25, 25): 24,
        (25, 24): 23,
        (25, 23): 22,
        (25, 22): 21,
        (25, 21): 20,
        (25, 20): 19,
        (25, 19): 17,
        (25, 18): 16,
        (25, 17): 15,
        (25, 16): 14,
        (25, 15): 13,
        (25, 14): 12,
        (25, 13): 10,
        (25, 12): 9,
        (25, 11): 8,
        (25, 10): 6,
        (25, 9): 5,
        (25, 8): 4,
        (25, 7): 2,
        (25, 6): 1,
        (25, 5): 0,
        (25, 4): 0,
        (25, 3): 0,
        (25, 2): 0,
        (25, 1): 0,
        (25, 0): 0,
        (50, 30): 29,
        (50, 29): 28,
        (50, 28): 27,
        (50, 27): 25,
        (50, 26): 24,
        (50, 25): 23,
        (50, 24): 22,
        (50, 23): 21,
        (50, 22): 19,
        (50, 21): 18,
        (50, 20): 17,
        (50, 19): 16,
        (50, 18): 14,
        (50, 17): 13,
        (50, 16): 12,
        (50, 15): 10,
        (50, 14): 9,
        (50, 13): 8,
        (50, 12): 6,
        (50, 11): 5,
        (50, 10): 3,
        (50, 9): 1,
        (50, 8): 0,
        (50, 7): 0,
        (50, 6): 0,
        (50, 5): 0,
        (50, 4): 0,
        (50, 3): 0,
        (50, 2): 0,
        (50, 1): 0,
        (50, 0): 0,
        (75, 30): 28,
        (75, 29): 27,
        (75, 28): 26,
        (75, 27): 25,
        (75, 26): 23,
        (75, 25): 22,
        (75, 24): 21,
        (75, 23): 20,
        (75, 22): 18,
        (75, 21): 17,
        (75, 20): 16,
        (75, 19): 14,
        (75, 18): 13,
        (75, 17): 11,
        (75, 16): 10,
        (75, 15): 8,
        (75, 14): 7,
        (75, 13): 5,
        (75, 12): 3,
        (75, 11): 1,
        (75, 10): 0,
        (75, 9): 0,
        (75, 8): 0,
        (75, 7): 0,
        (75, 6): 0,
        (75, 5): 0,
        (75, 4): 0,
        (75, 3): 0,
        (75, 2): 0,
        (75, 1): 0,
        (75, 0): 0,
        (100, 30): 27,
        (100, 29): 26,
        (100, 28): 25,
        (100, 27): 24,
        (100, 26): 22,
        (100, 25): 21,
        (100, 24): 20,
        (100, 23): 18,
        (100, 22): 17,
        (100, 21): 16,
        (100, 20): 14,
        (100, 19): 13,
        (100, 18): 11,
        (100, 17): 9,
        (100, 16): 8,
        (100, 15): 6,
        (100, 14): 4,
        (100, 13): 2,
        (100, 12): 0,
        (100, 11): 0,
        (100, 10): 0,
        (100, 9): 0,
        (100, 8): 0,
        (100, 7): 0,
        (100, 6): 0,
        (100, 5): 0,
        (100, 4): 0,
        (100, 3): 0,
        (100, 2): 0,
        (100, 1): 0,
        (100, 0): 0,
        (150, 30): 26,
        (150, 29): 25,
        (150, 28): 24,
        (150, 27): 22,
        (150, 26): 21,
        (150, 25): 19,
        (150, 24): 18,
        (150, 23): 16,
        (150, 22): 14,
        (150, 21): 13,
        (150, 20): 11,
        (150, 19): 9,
        (150, 18): 7,
        (150, 17): 5,
        (150, 16): 3,
        (150, 15): 1,
        (150, 14): 0,
        (150, 13): 0,
        (150, 12): 0,
        (150, 11): 0,
        (150, 10): 0,
        (150, 9): 0,
        (150, 8): 0,
        (150, 7): 0,
        (150, 6): 0,
        (150, 5): 0,
        (150, 4): 0,
        (150, 3): 0,
        (150, 2): 0,
        (150, 1): 0,
        (150, 0): 0,
        (200, 30): 25,
        (200, 29): 24,
        (200, 28): 22,
        (200, 27): 20,
        (200, 26): 19,
        (200, 25): 17,
        (200, 24): 16,
        (200, 23): 14,
        (200, 22): 12,
        (200, 21): 10,
        (200, 20): 8,
        (200, 19): 6,
        (200, 18): 4,
        (200, 17): 2,
        (200, 16): 0,
        (200, 15): 0,
        (200, 14): 0,
        (200, 13): 0,
        (200, 12): 0,
        (200, 11): 0,
        (200, 10): 0,
        (200, 9): 0,
        (200, 8): 0,
        (200, 7): 0,
        (200, 6): 0,
        (200, 5): 0,
        (200, 4): 0,
        (200, 3): 0,
        (200, 2): 0,
        (200, 1): 0,
        (200, 0): 0,
    }

    def __init__(self, outline: Outline) -> None:
        self.outline: Outline = outline
        self.building_is_not_set = True
        self.current_level: int | None = None
        self.current_building: str | None = None
        self.destroying_order: Iterator[str] = iter(
            self.outline.initial_outline_buildings
        )

        if self.outline.initial_outline_average_ruining_points == "big":
            self.levels = self.BIG_LEVELS
        else:
            self.levels = self.SMALL_LEVELS

    def _next_level(self, catapults: int) -> int:
        if self.current_level is None:
            raise ValueError("Current level cannot be none")
        return self.LEVEL_DICTIONARY[(catapults, self.current_level)]

    def best_catapult(self, weight_max: WeightMaximum) -> int:  # noqa: PLR0912
        """
        For given weight_max match best catapult number possible
        Also take care about current levels and building name
        """
        if self.building_is_not_set:
            self.current_building = next(self.destroying_order)
            self.building_is_not_set = False
            self.current_level = self.levels[self.current_building]

        best: int
        available_cats: int = weight_max.catapult_left
        if self.current_level is None:
            raise ValueError("current level is None")
        if self.current_level == 1:
            best = 20
        elif self.current_level <= 7 or available_cats < 50:
            best = 25
        elif self.current_level <= 10 or available_cats < 75:
            best = 50
        elif self.current_level <= 12 or available_cats < 100:
            best = 75
        elif self.current_level <= 14 or available_cats < 150:
            best = 100
        elif self.current_level <= 16 or available_cats < 200:
            best = 150
        else:
            best = 200
        if best > self.outline.initial_outline_catapult_max_value:
            best = self.outline.initial_outline_catapult_max_value
        elif best < self.outline.initial_outline_catapult_min_value:
            best = self.outline.initial_outline_catapult_min_value

        next_level: int = self._next_level(best)
        if next_level <= 3:
            self.building_is_not_set = True
        else:
            self.current_level = next_level

        return best

    def building(self) -> str:
        """For cats number return building name, always actual"""
        if self.current_building is None:
            raise ValueError("Building cannot be None")
        return self.current_building
