
""" File with basic classes used in another files """


from math import sqrt, ceil
from base import models


class Units():
    """ helps geting proper speed of units """
    def __init__(self):
        self.dictionary_with_units_speed = {
            "pikinier": 18,
            "miecznik": 22,
            "topornik": 18,
            "łucznik": 18,
            "zwiadowca": 9,
            "lekki kawalerzysta": 10,
            "łucznik na koniu": 10,
            'ciężki kawalerzysta': 11,
            "taran": 30,
            "szlachcic": 35,
            "katapulta": 30
        }

    def speed(self, unit: str):
        """ return speed of unit unit """
        try:
            return self.dictionary_with_units_speed[unit]
        except Exception:
            raise ValueError("Unit doesnt't exits: {}".format(unit))



class Wioska():
    """ class used to represent village in game """
    def __init__(self, kord_poprawny_lub_ze_spacjami: str):
        self.kordy = kord_poprawny_lub_ze_spacjami.strip()
        if len(self.kordy) != 7:
            raise ValueError("złe kordy")
        self.x = int(self.kordy[0:3])
        self.y = int(self.kordy[4:7])

    def distance(self, other):
        """ distance between two villages """
        return sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def time_distance(self, other, unit: str, swiat: int):
        """ return distance in hours between two villages """
        unit_speed = Units().speed(unit)
        world = self.get_world(swiat)

        return round(
            self.distance(other) / world.speed_world / world.speed_units *
            unit_speed * 60)

    def get_world(self, swiat):
        """ get world instance from database """
        try:
            world: models.World = models.World.objects.get(world=swiat)
        except Exception:
            raise Exception('Nie istnieje w bazie świat {}'.format(swiat))
        return world


    def get_village(self, swiat):
        """ get village instance from database """
        try:
            village: models.Village = models.Village.objects.get(world=swiat, x=self.x, y=self.y)
        except Exception:
            raise Exception('Nie istnieje w bazie wioska {}'.format(self.kordy))
        return village

    def get_player(self, swiat):
        """ get player instance from database """
        try:
            player: models.Player = models.Player.objects.get(
                player_id=self.get_village(swiat).player_id)
        except Exception:
            raise Exception(
                "Nie istnieje w bazie właściciel wioski {}".format(self.kordy))

        return player.name

    def get_id_wioski(self, swiat):
        """ get village id from database """
        return self.get_village(swiat).village_id

    def get_punkty_wioski(self, swiat):
        """ get points of village from database """
        return self.get_village(swiat).points

    def get_player_points(self, swiat):
        """ get points of player from database """
        return self.get_player(swiat).points

    def __str__(self):
        return str(self.kordy)

    def __eq__(self, other):
        return self.kordy == other.kordy


class Wiele_wiosek():
    """ Very important class based on Wioska class, implemented
        that way long ago, leaved as it is. """
    def __init__(self, wiele_kordow_po_spacji: str):
        wiele_kordow_po_spacji = wiele_kordow_po_spacji.strip().split()
        self.lista_z_wioskami = [Wioska(i) for i in wiele_kordow_po_spacji]


class Map():
    """ class to represent coordinate system as dictionary of tuples (x,y) """
    def __init__(self):
        self.map = set()

    def set_as_square(self, radius, center):
        """ returns square 2r x 2r with center """
        map_ = []
        for i in range(-radius, radius + 1):
            for j in range(-radius, radius + 1):
                map_.append((center[0] + i, center[1] + j))
        self.map = set(map_)

    def set_as_circle(self, radius, center):
        """ return circle with r and center """
        circle_map = []
        for x_coord in range(-radius, radius):
            y_max = ceil(sqrt(radius**2 - x_coord**2))
            for y_coord in range(-y_max, y_max):
                circle_map.append((x_coord + center[0], y_coord + center[1]))
        self.map = set(circle_map)

    def sub(self, set_map: set):
        """ subs two maps WARNING! very slow, dont use if not necessery """
        self.map = self.map - set_map
