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

"""Village, Unit, Map classes"""

from math import ceil, sqrt

from django.utils.translation import gettext as _

from base import models


def dist(coord1, coord2):
    x_coord1 = int(coord1[0:3])
    y_coord1 = int(coord1[4:7])
    x_coord2 = int(coord2[0:3])
    y_coord2 = int(coord2[4:7])
    return sqrt((x_coord1 - x_coord2) ** 2 + (y_coord1 - y_coord2) ** 2)


class Unit:
    """Unit in the game with its speed"""

    def __init__(self, name):
        self.dictionary_with_units_speed = {
            "spear": 18,
            "swordsman": 22,
            "axeman": 18,
            "archer": 18,
            "scout": 9,
            "light": 10,
            "mounted archer": 10,
            "heavy": 11,
            "ram": 30,
            "nobleman": 35,
            "catapult": 30,
            "paladin": 10,
        }
        if name not in self.dictionary_with_units_speed:
            raise KeyError(name)
        self.name = name

    @property
    def speed(self):
        """Speed of unit"""
        return self.dictionary_with_units_speed[self.name]

    def __str__(self):
        return self.name


class VillageError(Exception):
    """Village Exception"""


class Village:
    """Represent village in game"""

    def __init__(self, coord: str, validate=True, x_coord=None, y_coord=None):
        self.coord = coord
        self.x_coord = x_coord
        self.y_coord = y_coord
        if validate:
            self.coord_validation()
        else:
            self.x_coord = int(coord[0:3])
            self.y_coord = int(coord[4:7])

    def coord_validation(self):
        """Validate coord"""
        coord = self.coord
        if not coord:
            raise VillageError(_("Coords are empty!"))
        if not isinstance(coord, str):
            if len(coord) > 20:
                coord = f"{coord}..."
            not_string = _(": Is not string type!")
            raise VillageError(f"{coord}{not_string}")
        coord = coord.strip()
        if len(coord) != 7:
            if len(coord) > 20:
                coord = f"{coord}..."
            too_long = _(": Is not the correct length!")
            raise VillageError(f"{coord}{too_long}")
        if not coord[0:3].isnumeric():
            not_number = _("Is not a number")
            raise VillageError(f"{coord}: '{coord[0:4]}' {not_number}")
        if not coord[4:7].isnumeric():
            not_number = _("Is not a number")
            raise VillageError(f"{coord}: '{coord[4:7]}' {not_number}")
        if not coord[3] == "|":
            symbol = _("Symbol")
            not_equal = _("Is not equal to '|'!")
            raise VillageError(f"{coord}: {symbol} '{coord[3]}' {not_equal}")
        self.coord = coord
        self.x_coord = int(coord[0:3])
        self.y_coord = int(coord[4:7])

    @classmethod
    def from_coordinates(cls, x_coord: int, y_coord: int):
        """From x_coord and y_coord"""
        return cls(
            coord=f"{x_coord}|{y_coord}",
            validate=False,
            x_coord=x_coord,
            y_coord=y_coord,
        )

    @staticmethod
    def from_village_model(village_model: models.VillageModel):
        """From VillageModel"""
        return Village.from_coordinates(
            x_coord=village_model.x_coord, y_coord=village_model.y_coord
        )

    def distance(self, other):
        """Distance between two villages"""
        return sqrt(
            (self.x_coord - other.x_coord) ** 2 + (self.y_coord - other.y_coord) ** 2
        )

    def time_distance(self, other, unit: str, world: models.World) -> float:
        """Time in seconds for given unit between two villages"""
        unit_speed = Unit(name=unit).speed
        return (
            self.distance(other)
            / world.speed_world
            / world.speed_units
            * unit_speed
            * 60
        )

    def __str__(self):
        return str(self.coord)

    def __eq__(self, other):
        return self.coord == other.coord


def many_villages(coord_many: str):
    """List of Villages"""
    coords = coord_many.strip().split()
    return [Village(i) for i in coords]


def yield_circle(radius, center):
    """Return circle with r and center"""
    for x_coord in range(-radius, radius + 1):
        y_max = ceil(sqrt(radius**2 - x_coord**2))
        for y_coord in range(-y_max, y_max + 1):
            yield (x_coord + center[0], y_coord + center[1])


def yield_four_circle_ends(radius, center):
    for x_coord in range(radius + 1):
        y_coord = radius - x_coord
        yield (x_coord + center[0], y_coord + center[1])
        yield (x_coord + center[0], -y_coord + center[1])
        yield (-x_coord + center[0], y_coord + center[1])
        yield (-x_coord + center[0], -y_coord + center[1])
