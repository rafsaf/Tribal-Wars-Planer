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

""" Army and Defence tools"""
from functools import cached_property
from typing import NamedTuple

from base import models
from utils import basic


class WorldEvidence(NamedTuple):
    paladin: bool
    archer: bool
    militia: bool


def world_evidence(world: models.World) -> WorldEvidence:
    """For world return [T/F, .. , ..] [paladin, archer, militia]"""
    if world.paladin == "active":
        paladin = True
    else:
        paladin = False
    if world.archer == "active":
        archer = True
    else:
        archer = False
    if world.militia == "active":
        militia = True
    else:
        militia = False

    return WorldEvidence(paladin, archer, militia)


class ArmyError(Exception):
    """Army and Defence base error"""


class Army:
    """Off line in off troops for calculation purposes.

    It perfectly calculate off/deff for village

    Note it can be used for defence line also, by using from_defence_line param,
    every off/deff calculations will be precise, but clean_init method won't
    pass for defence line.
    """

    EVIDENCE_DICTIONARY: dict[tuple[int, int, int], set[int]] = {
        (1, 1, 1): {16, 17},
        (1, 1, 0): {15, 16},
        (0, 1, 1): {15, 16},
        (1, 0, 1): {14, 15},
        (1, 0, 0): {13, 14},
        (0, 0, 1): {13, 14},
        (0, 1, 0): {14, 15},
        (0, 0, 0): {12, 13},
    }
    # (paladin, archer, militia)

    def __init__(
        self, text_army: str, evidence: WorldEvidence, from_defence_line: bool = False
    ):
        self._original_text = text_army
        self.text_army = text_army.split(",")
        self.world_evidence = evidence
        if from_defence_line:
            # remove second "in village" / "enroute" place
            del self.text_army[1]

    def clean_init(self, player_dictionary):
        """Text army validation"""

        text_army_length = len(self.text_army)

        if text_army_length not in Army.EVIDENCE_DICTIONARY[self.world_evidence]:
            raise ArmyError(f"Length: {text_army_length} is not correct")
        if len(self.text_army[0]) != 7:
            raise ArmyError("Length must be equal to 7")
        try:
            village = basic.Village(self.text_army[0])
        except basic.VillageError as identifier:
            raise ArmyError(identifier)
        else:
            if village.coord not in player_dictionary:
                raise ArmyError(f"{village.coord} is not in any valid tribe")
        for army_element in self.text_army[1:-1]:
            if not army_element.isnumeric():
                raise ArmyError(f"{army_element} is not a number")
        if self.text_army[-1] != "":
            raise ArmyError(f"Syntax error in {self.text_army[-1]}")

    @property
    def coord(self) -> str:
        """Coords of village"""
        return self.text_army[0]

    @cached_property
    def nobleman(self):
        """Number of nobleman"""
        if not self.world_evidence.archer:
            if not self.world_evidence.paladin:
                return int(self.text_army[9])
            return int(self.text_army[10])
        if not self.world_evidence.paladin:
            return int(self.text_army[11])
        return int(self.text_army[12])

    @cached_property
    def catapult(self):
        """Literal Number of catapult"""
        # no heavy cavalery
        if not self.world_evidence.archer:  # no archers
            return int(self.text_army[8])
        return int(self.text_army[10])

    def _raw_deff(self):
        # no heavy cavalery
        if not self.world_evidence.archer:  # no archers
            return (
                int(self.text_army[1])
                + int(self.text_army[2])
                + int(self.text_army[4]) * 2
                + int(self.text_army[8]) * 8
            )
        return (  # with archers
            int(self.text_army[1])
            + int(self.text_army[2])
            + int(self.text_army[4])
            + int(self.text_army[5]) * 2
            + int(self.text_army[10]) * 8
        )

    def _off_scout(self):
        if not self.world_evidence.archer:
            scouts = int(self.text_army[4])
        else:
            scouts = int(self.text_army[5])
        if scouts >= 200:
            return 400
        return scouts * 2

    def _raw_off(self):
        # no heavy cavalery
        if not self.world_evidence.archer:  # no archers
            return (
                int(self.text_army[3])
                + self._off_scout()
                + int(self.text_army[5]) * 4
                + int(self.text_army[7]) * 5
                + int(self.text_army[8]) * 8
            )
        return (  # with archers
            int(self.text_army[3])
            + self._off_scout()
            + int(self.text_army[6]) * 4
            + int(self.text_army[7]) * 5
            + int(self.text_army[9]) * 5
            + int(self.text_army[10]) * 8
        )

    @cached_property
    def off(self):
        """Number of off"""
        raw_deff = self._raw_deff()
        raw_off = self._raw_off()

        if raw_off > raw_deff:
            if not self.world_evidence.archer:  # no archers
                return raw_off + int(self.text_army[6]) * 6
            return raw_off + int(self.text_army[8]) * 6  # with archers
        return raw_off - self._off_scout()

    @cached_property
    def deff(self):
        """Number of deff"""
        if not self.world_evidence.archer:  # no archers
            return (
                int(self.text_army[1])
                + int(self.text_army[2])
                + int(self.text_army[6]) * 4
            )
        return (  # with archers
            int(self.text_army[1])
            + int(self.text_army[2])
            + int(self.text_army[4])
            + int(self.text_army[8]) * 4
        )


class DefenceError(Exception):
    """Defence Error"""


class Defence:
    """Deff line in deff troops"""

    EVIDENCE_DICTIONARY: dict[tuple[int, int, int], set[int]] = {
        (1, 1, 1): {16, 17},
        (1, 1, 0): {15, 16},
        (0, 1, 1): {15, 16},
        (1, 0, 1): {14, 15},
        (1, 0, 0): {13, 14},
        (0, 0, 1): {13, 14},
        (0, 1, 0): {14, 15},
        (0, 0, 0): {12, 13},
    }

    def __init__(self, text_army: str, evidence):
        self.text_army = text_army.split(",")
        self.world_evidence = evidence

    def clean_init(self, player_dictionary):
        """Text army validation"""

        text_army_length = len(self.text_army)

        if text_army_length not in Defence.EVIDENCE_DICTIONARY[self.world_evidence]:
            raise DefenceError(f"Length: {text_army_length} is not correct")
        if len(self.text_army[0]) != 7:
            raise DefenceError("Length must be equal to 7")
        try:
            village = basic.Village(self.text_army[0])
        except basic.VillageError as identifier:
            raise DefenceError(identifier)
        else:
            if village.coord not in player_dictionary:
                raise DefenceError(f"{village.coord} is not in any valid tribe")
        for army_element in self.text_army[2:-1]:
            if not army_element.isnumeric():
                raise DefenceError(f"{army_element} is not a number")
        if not isinstance(self.text_army[1], str):
            raise DefenceError("Second element must be a string")
        if self.text_army[-1] != "":
            raise DefenceError(f"Invalid syntax in {self.text_army[-1]}")

    @cached_property
    def coord(self):
        """Coords of village"""
        return self.text_army[0]

    @cached_property
    def nobleman(self):
        """Number of nobleman"""
        if self.world_evidence[1] == 0:
            if self.world_evidence[0] == 0:
                return int(self.text_army[10])
            return int(self.text_army[11])
        if self.world_evidence[0] == 0:
            return int(self.text_army[12])
        return int(self.text_army[13])

    @cached_property
    def off(self):
        """Number of off"""
        if self.world_evidence[1] == 0:
            return (
                int(self.text_army[4])
                + int(self.text_army[6]) * 4
                + int(self.text_army[8]) * 5
                + int(self.text_army[9]) * 8
            )
        return (
            int(self.text_army[4])
            + int(self.text_army[7]) * 4
            + int(self.text_army[8]) * 5
            + int(self.text_army[10]) * 5
            + int(self.text_army[11]) * 8
        )

    @cached_property
    def deff(self):
        """Number of deff"""
        if self.world_evidence[1] == 0:
            return (
                int(self.text_army[2])
                + int(self.text_army[3])
                + int(self.text_army[7]) * 4
            )
        return (
            int(self.text_army[2])
            + int(self.text_army[3])
            + int(self.text_army[5])
            + int(self.text_army[9]) * 4
        )
