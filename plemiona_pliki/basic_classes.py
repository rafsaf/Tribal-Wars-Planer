
""" File with basic classes used in another files """

import random
import datetime
from math import sqrt, ceil
from base import models


class Unit():
    """ helps geting proper speed of units """
    def __init__(self, name):
        self.dictionary_with_units_speed = {
            "pikinier": 18,
            "miecznik": 22,
            "topornik": 18,
            "łucznik": 18,
            "zwiadowca": 9,
            "lekki kawalerzysta": 10,
            "łucznik na koniu": 10,
            "ciężki kawalerzysta": 11,
            "taran": 30,
            "szlachcic": 35,
            "katapulta": 30
        }
        if not name in self.dictionary_with_units_speed:
            raise ValueError("Unit doesnt't exist: {}".format(name))
        self.name = name

    def get_speed(self):
        """ return speed of unit """
        return self.dictionary_with_units_speed[self.name]

    def get_name(self):
        """ return name """
        return self.name

    def __str__(self):
        return self.name



class Wioska():
    """ class used to represent village in game """
    def __init__(self, kord_poprawny_lub_ze_spacjami: str):
        try:
            self.kordy = kord_poprawny_lub_ze_spacjami.strip()
        except Exception:
            raise ValueError("Nieprawidłowe kordy: {}".format(kord_poprawny_lub_ze_spacjami))
        if len(self.kordy) != 7:
            raise ValueError("Nieprawidłowe kordy: {}".format(kord_poprawny_lub_ze_spacjami))

        if not self.kordy[0:3].isnumeric() and self.kordy[4:7].isnumeric() and self.kordy[3]=="|":
            raise ValueError("Nieprawidłowe kordy: {}".format(kord_poprawny_lub_ze_spacjami))

        self.x = int(self.kordy[0:3])
        self.y = int(self.kordy[4:7])

    def distance(self, other):
        """ distance between two villages """
        return sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def time_distance(self, other, unit: str, swiat: int):
        """ return distance in seconds between two villages """
        unit_speed = Unit(unit).get_speed()
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
        """ get player instance from database, NOT nickname """
        try:
            player: models.Player = models.Player.objects.get(
                player_id=self.get_village(swiat).player_id, world=swiat)
        except Exception:
            raise Exception(
                "Nie istnieje w bazie właściciel wioski {}".format(self.kordy))

        return player

    def get_id_wioski(self, swiat):
        """ get village id from database """
        return self.get_village(swiat).village_id

    def get_village_points(self, swiat):
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
    """ class based on Wioska class, implemented
        that way long ago, leaved as it is. """
    def __init__(self, wiele_kordow_po_spacji: str):
        self.wiele_kordow_po_spacji = wiele_kordow_po_spacji.strip().split()
        self.lista_z_wioskami = [Wioska(i) for i in self.wiele_kordow_po_spacji]
    
    def __str__(self):
        return self.wiele_kordow_po_spacji


class Map():
    """ class to represent coordinate system as list of tuples [(x,y), ...] """
    def __init__(self):
        self.map = []

    def add_vertex(self, x_coord, y_coord):
        """ add new to map """
        self.map.append((x_coord, y_coord))

    def set_as_square(self, radius, center):
        """ returns square 2r x 2r with center """
        map_ = []
        for i in range(-radius, radius + 1):
            for j in range(-radius, radius + 1):
                map_.append((center[0] + i, center[1] + j))
        self.map = map_

    def set_as_circle(self, radius, center):
        """ return circle with r and center """
        circle_map = []
        for x_coord in range(-radius, radius + 1):
            y_max = ceil(sqrt(radius**2 - x_coord**2))
            for y_coord in range(-y_max, y_max + 1):
                circle_map.append((x_coord + center[0], y_coord + center[1]))
        self.map = circle_map

    def __sub__(self, other):
        """ subs two maps WARNING! may be very slow, dont use if not necessery """
        return set(self.map) - set(other.map)


class Type_of_attack():
    """ type of attack for example offoszlachta deffoszlachta, off, fejk. """
    def __init__(self):
        self.off = "OFF PRĘDKOŚĆ TARANA"
        self.offoszlachta = "OFFOSZLACHTA"
        self.fejk_taran = "FEJK Z PRĘDKOŚCIĄ TARANA"
        self.fejk_gruby = "FEJK GRUBY"
        self.deffoszlachta = "DEFFOSZLACHTA"

        self.type = None
        self.speed = None
        self.unit = None


    def set_off(self):
        self.type = self.off
        self.unit = "taran"
        self.speed = Unit(self.unit).get_speed()

    def set_offoszlachta(self):
        self.type = self.offoszlachta
        self.unit = "szlachcic"
        self.speed = Unit(self.unit).get_speed()

    def set_fejk_taran(self):
        self.type = self.fejk_taran
        self.unit = "taran"
        self.speed = Unit(self.unit).get_speed()

    def set_fejk_gruby(self):
        self.type = self.fejk_gruby
        self.unit = "szlachcic"
        self.speed = Unit(self.unit).get_speed()

    def set_deffoszlachta(self):
        self.type = self.deffoszlachta
        self.unit = "szlachcic"
        self.speed = Unit(self.unit).get_speed()


class Czas_wejscia():
    def __init__(self, data_wejscia: datetime.datetime, maksymalna_data_wejscia: datetime.datetime,
                 rodzaj_ataku: Type_of_attack):
        self.data_wejscia = data_wejscia.replace(tzinfo=None)
        self.maksymalna_data_wejscia = maksymalna_data_wejscia.replace(tzinfo=None)
        self.predkosc_jednostki = rodzaj_ataku.speed
        self.unit = rodzaj_ataku.unit

        self.czas_wejscia()

    def czas_wejscia(self):
        if self.data_wejscia != self.maksymalna_data_wejscia:
            diffrence = self.maksymalna_data_wejscia - self.data_wejscia
            diffrence = diffrence.total_seconds()
            delta = datetime.timedelta(seconds=random.randint(0, diffrence))
            self.data_wejscia = self.data_wejscia + delta

    def czas_wyjscia_ataku(self, moja_wioska: Wioska, cel_wioska: Wioska):
        odleglosc_sekundy = moja_wioska.time_distance(cel_wioska, self.unit, moja_wioska.get_world().world)
        return self.data_wejscia - datetime.timedelta(seconds=odleglosc_sekundy)
