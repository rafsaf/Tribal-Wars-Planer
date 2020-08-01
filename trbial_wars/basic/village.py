""" Village, Unit, Map classes """

from math import sqrt, ceil
from base import models

class Unit:
    """ Unit in the game with its speed """

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
        """ Speed of unit """
        return self.dictionary_with_units_speed[self.name]

    def __str__(self):
        return self.name


class VillageError(Exception):
    """ Village Exception """


class Village:
    """ Represent village in game """

    def __init__(self, coord: str, validate=True, x_coord=None, y_coord=None):
        self.coord = coord
        self.x_coord = x_coord
        self.y_coord = y_coord
        if validate:
            self.coord_validation()

    def coord_validation(self):
        """ Validate coord """
        coord = self.coord
        if not coord:
            raise VillageError("Kordy są puste!")
        if not isinstance(coord, str):
            if len(coord) > 20:
                coord = f"{coord}..."
            raise VillageError(f"{coord}: Nie jest typu napisem!")
        coord = coord.strip()
        if len(coord) != 7:
            if len(coord) > 20:
                coord = f"{coord}..."
            raise VillageError(f"{coord}: Nie jest prawidłowej długości!")
        if not coord[0:3].isnumeric():
            raise VillageError(f"{coord}: '{coord[0:4]}' Nie jest liczbą!")
        if not coord[4:7].isnumeric():
            raise VillageError(f"{coord}: '{coord[4:7]}' Nie jest liczbą!")
        if not coord[3] == "|":
            raise VillageError(f"{coord}: Znak '{coord[3]}' ie jest '|'!")
        self.coord = coord
        self.x_coord = int(coord[0:3])
        self.y_coord = int(coord[4:7])

    @classmethod
    def from_coordinates(cls, x_coord: int, y_coord: int):
        """ From x_coord and y_coord """
        return cls(
            coord=f"{x_coord}|{y_coord}",
            validate=False,
            x_coord=x_coord,
            y_coord=y_coord,
        )

    @staticmethod
    def from_village_model(village_model: models.VillageModel):
        """ From VillageModel """
        return Village.from_coordinates(
            x_coord=village_model.x_coord, y_coord=village_model.y_coord
        )

    def distance(self, other):
        """ Distance between two villages """
        return sqrt(
            (self.x_coord - other.x_coord) ** 2 + (self.y_coord - other.y_coord) ** 2
        )

    def time_distance(self, other, unit: str, world: models.World):
        """ Time in seconds for given unit between two villages """
        unit_speed = Unit(name=unit).speed
        return round(
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
    """ List of Villages """
    coord_many = coord_many.strip().split()
    return [Village(i) for i in coord_many]


def yield_circle(radius, center):
    """ Return circle with r and center """
    for x_coord in range(-radius, radius + 1):
        y_max = ceil(sqrt(radius ** 2 - x_coord ** 2))
        for y_coord in range(-y_max, y_max + 1):
            yield (x_coord + center[0], y_coord + center[1])


def yield_four_circle_ends(radius, center):
    for x_coord in range(radius + 1):
        y_coord = radius - x_coord
        yield (x_coord + center[0], y_coord + center[1])
        yield (x_coord + center[0], - y_coord + center[1])
        yield (- x_coord + center[0], y_coord + center[1])
        yield (- x_coord + center[0], - y_coord + center[1])
