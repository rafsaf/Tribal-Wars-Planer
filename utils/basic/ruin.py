from typing import Dict, Iterator, Optional, Tuple

from base.models import Outline, WeightMaximum


class RuinHandle:
    BIG_LEVELS: Dict[str, int] = {
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
    SMALL_LEVELS: Dict[str, int] = {
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
    LEVEL_DICTIONARY: Dict[Tuple[int, int], int] = {
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
        (20, 1): 0,
    }

    def __init__(self, outline: Outline) -> None:
        self.outline: Outline = outline
        self.building_is_not_set = True
        self.current_level: Optional[int] = None
        self.current_building: Optional[str] = None
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

    def best_catapult(self, weight_max: WeightMaximum) -> int:
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
        elif self.current_level <= 8 or available_cats < 75:
            best = 50
        elif self.current_level <= 11 or available_cats < 100:
            best = 75
        elif self.current_level <= 13 or available_cats < 150:
            best = 100
        elif self.current_level <= 16 or available_cats < 200:
            best = 150
        else:
            best = 200
        if best > self.outline.initial_outline_catapult_default:
            best = self.outline.initial_outline_catapult_default

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
