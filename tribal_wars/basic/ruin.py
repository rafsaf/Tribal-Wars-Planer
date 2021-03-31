from typing import Dict, List, Tuple
from base import models

BuildingCount = Tuple[str, int]


class RuinHandle:
    def __init__(self, outline: models.Outline) -> None:
        self.outline: models.Outline = outline
        self.catapult: int = outline.initial_outline_catapult_default
        self.buildings: List[BuildingCount] = []
        if self.outline.initial_outline_average_ruining_points == "big":
            self.levels: Dict[str, int] = {
                "headquarters": 20,
                "barracks": 25,
                "stable": 20,
                "workshop": 10,
                "academy": 1,
                "smithy": 20,
                "rally_point": 1,
                "timber_camp": 30,
                "clay_pit": 30,
                "iron_mine": 30,
                "farm": 30,
                "warehouse": 30,
                "wall": 0,
            }
        else:
            self.levels: Dict[str, int] = {
                "headquarters": 20,
                "barracks": 18,
                "stable": 10,
                "workshop": 5,
                "academy": 1,
                "smithy": 20,
                "rally_point": 1,
                "timber_camp": 25,
                "clay_pit": 25,
                "iron_mine": 25,
                "farm": 25,
                "warehouse": 24,
                "wall": 0,
            }

        self.catapult_destroy_levels: CatapultDestroyLevels = CatapultDestroyLevels()
        if self.outline.initial_outline_ruining_order == "first":
            self.destroying_order: List[str] = [
                "farm",
                "headquarters",
                "smithy",
                "barracks",
                "clay_pit",
                "timber_camp",
                "iron_mine",
                "warehouse",
                "stable",
            ]
        elif self.outline.initial_outline_ruining_order == "second":
            self.destroying_order: List[str] = [
                "farm",
                "headquarters",
                "warehouse",
                "smithy",
                "clay_pit",
                "timber_camp",
                "iron_mine",
                "barracks",
                "stable",
            ]

    def next_level(self, level: int) -> int:
        return self.catapult_destroy_levels.level_after_destroy(self.catapult, level)

    def yield_building(self):
        building: str
        for building in self.destroying_order:
            level: int = self.levels[building]
            while True:
                next_level: int = self.next_level(level)
                if next_level <= 5:
                    yield building
                    break
                else:
                    yield building
                    level = next_level


class CatapultDestroyLevels:
    def __init__(self) -> None:
        self.main_level_dictionary: Dict[Tuple[int, int], int] = {
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
        }

    def level_after_destroy(self, catapult_number: int, building_level: int) -> int:
        return self.main_level_dictionary[(catapult_number, building_level)]
