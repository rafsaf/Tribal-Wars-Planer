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

"""Army and Defence tools"""

from functools import cached_property
from typing import Any, Literal, NamedTuple, TypedDict

from django.utils.translation import gettext

from base import models
from utils import basic

TROOPS_TYPES = [
    "spear",
    "swordsman",
    "axeman",
    "archer",
    "scout",
    "light",
    "mounted_archer",
    "heavy",
    "ram",
    "catapult",
    "paladin",
    "nobleman",
    "militia",
]


class WorldEvidence(NamedTuple):
    paladin: int
    archer: int
    militia: int


class ArmyIndexDict(TypedDict):
    spear: int
    swordsman: int
    axeman: int
    archer: int | None
    scout: int
    light: int
    mounted_archer: int | None
    heavy: int
    ram: int
    catapult: int
    paladin: int | None
    nobleman: int
    militia: int | None


class TroopsIndex:
    def __init__(self, army: Literal["army", "defence"]) -> None:
        self.result_mapping: dict[WorldEvidence, dict[str, int | None]] = {
            WorldEvidence(1, 1, 1): {},
            WorldEvidence(1, 1, 0): {},
            WorldEvidence(0, 1, 1): {},
            WorldEvidence(1, 0, 1): {},
            WorldEvidence(1, 0, 0): {},
            WorldEvidence(0, 0, 1): {},
            WorldEvidence(0, 1, 0): {},
            WorldEvidence(0, 0, 0): {},
        }
        for evidence in self.result_mapping:
            if army == "army":
                start_index = 2
            else:
                start_index = 3
            troops_indexes = self.result_mapping[evidence]
            for troop in TROOPS_TYPES:
                if not evidence.archer and troop in {"archer", "mounted_archer"}:
                    troops_indexes[troop] = None
                    continue
                if not evidence.paladin and troop == "paladin":
                    troops_indexes[troop] = None
                    continue
                if not evidence.militia and troop == "militia":
                    troops_indexes[troop] = None
                    continue
                troops_indexes[troop] = start_index
                start_index += 1

    def get_index_dict(self, evidence: WorldEvidence) -> ArmyIndexDict:
        return self.result_mapping[evidence]  # type: ignore


ARMY_INDEX = TroopsIndex("army")
DEFENCE_INDEX = TroopsIndex("defence")


def world_evidence(world: models.World):
    """For world return [T/F, .. , ..] [paladin, archer, militia]"""
    if world.paladin == "active":
        paladin = 1
    else:
        paladin = 0
    if world.archer == "active":
        archer = 1
    else:
        archer = 0
    if world.militia == "active":
        militia = 1
    else:
        militia = 0

    return WorldEvidence(paladin, archer, militia)


class ArmyError(Exception):
    """Army and Defence base error"""

    def __init__(self, *args: object, coord: str | None = None) -> None:
        super().__init__(*args)
        self.coord = coord


class Army:
    """Off line in off troops"""

    EVIDENCE_DICTIONARY: dict[tuple[int, int, int], set[int]] = {
        (1, 1, 1): {17, 18},
        (1, 1, 0): {16, 17},
        (0, 1, 1): {16, 17},
        (1, 0, 1): {15, 16},
        (1, 0, 0): {14, 15},
        (0, 0, 1): {14, 15},
        (0, 1, 0): {15, 16},
        (0, 0, 0): {13, 14},
    }

    def __init__(self, text_army: str, evidence: WorldEvidence):
        self.text_army = text_army.split(",")
        self.world_evidence = evidence
        self.index_dict = ARMY_INDEX.get_index_dict(self.world_evidence)

    def clean_init(
        self,
        player_dictionary: set[str] | dict[str, Any],
        ally_tribes: list[str] | None = None,
    ):
        """Text army validation"""

        text_army_length = len(self.text_army)

        if text_army_length not in Army.EVIDENCE_DICTIONARY[self.world_evidence]:
            raise ArmyError(
                gettext(
                    "Invalid number of elements in line: %(len)s is not correct, expected %(expected)s"
                )
                % {
                    "len": text_army_length,
                    "expected": Army.EVIDENCE_DICTIONARY[self.world_evidence],
                }
            )
        if len(self.text_army[0]) != 7:
            raise ArmyError(
                gettext("Length of coord at first postition must be equal to 7")
            )
        try:
            village = basic.Village(self.text_army[0])
        except basic.VillageError as identifier:
            raise ArmyError(identifier)
        else:
            if village.coord not in player_dictionary:
                raise ArmyError(
                    gettext(
                        "Coord: %(coord)s does not exist or is not in any of valid tribes: %(tribes)s"
                    )
                    % {"coord": village.coord, "tribes": ally_tribes},
                    coord=village.coord,
                )
        for army_element in self.text_army[2:-1]:
            if not army_element.isnumeric():
                raise ArmyError(
                    gettext("One of line elements is not a number: %s") % army_element
                )
        if self.text_army[-1] != "":
            raise ArmyError(
                gettext("Last element in line must be empty string, currently: %s")
                % self.text_army[-1]
            )

    def army_value(self, index: int | None):
        if index is None:
            return 0
        return int(self.text_army[index])

    @property
    def coord(self) -> str:
        """Coords of village"""
        return self.text_army[0]

    @cached_property
    def nobleman(self):
        """Number of nobleman"""
        return self.army_value(self.index_dict["nobleman"])

    @cached_property
    def catapult(self):
        """Literal Number of catapult"""
        return self.army_value(self.index_dict["catapult"])

    def _raw_deff(self):
        # no heavy cavalery
        return (
            self.army_value(self.index_dict["spear"])
            + self.army_value(self.index_dict["swordsman"])
            + self.army_value(self.index_dict["scout"]) * 2
            + self.army_value(self.index_dict["archer"])
            + self.army_value(self.index_dict["catapult"]) * 8
        )

    def _off_scouts(self):
        scouts = self.army_value(self.index_dict["scout"])
        if scouts >= 200:
            return 400
        return scouts * 2

    def _raw_off(self):
        # no heavy cavalery
        return (
            self.army_value(self.index_dict["axeman"])
            + self._off_scouts()
            + self.army_value(self.index_dict["light"]) * 4
            + self.army_value(self.index_dict["mounted_archer"]) * 5
            + self.army_value(self.index_dict["ram"]) * 5
            + self.army_value(self.index_dict["catapult"]) * 8
        )

    @cached_property
    def off(self):
        """Number of off"""
        raw_deff = self._raw_deff()
        raw_off = self._raw_off()

        if raw_off > raw_deff:
            return raw_off + self.army_value(self.index_dict["heavy"]) * 6
        return raw_off - self._off_scouts()

    @cached_property
    def deff(self):
        """Number of deff"""
        return (
            self.army_value(self.index_dict["spear"])
            + self.army_value(self.index_dict["swordsman"])
            + self.army_value(self.index_dict["archer"])
            + self.army_value(self.index_dict["heavy"]) * 4
        )


class DefenceError(Exception):
    """Defence Error"""

    def __init__(self, *args: object, coord: str | None = None) -> None:
        super().__init__(*args)
        self.coord = coord


class Defence(Army):
    """Deff line in deff troops"""

    EVIDENCE_DICTIONARY: dict[tuple[int, int, int], set[int]] = {
        (1, 1, 1): {17, 18},
        (1, 1, 0): {16, 17},
        (0, 1, 1): {16, 17},
        (1, 0, 1): {15, 16},
        (1, 0, 0): {14, 15},
        (0, 0, 1): {14, 15},
        (0, 1, 0): {15, 16},
        (0, 0, 0): {13, 14},
    }

    def __init__(self, text_army: str, evidence):
        self.text_army = text_army.split(",")
        self.world_evidence = evidence
        self.index_dict = DEFENCE_INDEX.get_index_dict(self.world_evidence)

    @property
    def deff_collection_text(self) -> str:
        return self.text_army[1]

    def clean_init(self, player_dictionary, ally_tribes: list[str] | None = None):
        """Text army validation"""

        text_army_length = len(self.text_army)

        if text_army_length not in Defence.EVIDENCE_DICTIONARY[self.world_evidence]:
            raise DefenceError(
                gettext(
                    "Invalid number of elements in line: %(len)s is not correct, expected %(expected)s"
                )
                % {
                    "len": text_army_length,
                    "expected": Defence.EVIDENCE_DICTIONARY[self.world_evidence],
                }
            )
        if len(self.text_army[0]) != 7:
            raise DefenceError(
                gettext("Length of coord at first postition must be equal to 7")
            )
        try:
            village = basic.Village(self.text_army[0])
        except basic.VillageError as identifier:
            raise DefenceError(identifier)
        else:
            if village.coord not in player_dictionary:
                raise DefenceError(
                    gettext(
                        "Coord: %(coord)s does not exist or is not in any of valid tribes: %(tribes)s"
                    )
                    % {"coord": village.coord, "tribes": ally_tribes},
                    coord=village.coord,
                )
        for army_element in self.text_army[3:-1]:
            if not army_element.isnumeric():
                raise DefenceError(
                    gettext("One of line elements is not a number: %s") % army_element
                )
        if not all(chr.isalpha() or chr.isspace() for chr in self.text_army[2]):
            raise DefenceError(
                gettext("Third element of line must be a text: %s") % self.text_army[1],
            )
        if self.text_army[-1] != "":
            raise DefenceError(
                gettext("Last element in line must be empty string, currently: %s")
                % self.text_army[-1]
            )
