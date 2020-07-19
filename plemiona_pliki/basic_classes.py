""" File with basic classes used in another files """

import random
import datetime
from math import sqrt, ceil
from base import models
from .timing import timing

class Unit:
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
            "katapulta": 30,
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


class Wioska:
    """ class used to represent village in game """

    def __init__(self, kord_poprawny_lub_ze_spacjami: str):
        try:
            self.kordy = kord_poprawny_lub_ze_spacjami.strip()
        except Exception:
            raise ValueError(
                "Nieprawidłowe kordy: {}".format(kord_poprawny_lub_ze_spacjami)
            )
        if len(self.kordy) != 7:
            raise ValueError(
                "Nieprawidłowe kordy: {}".format(kord_poprawny_lub_ze_spacjami)
            )

        if (
            not self.kordy[0:3].isnumeric()
            and self.kordy[4:7].isnumeric()
            and self.kordy[3] == "|"
        ):
            raise ValueError(
                "Nieprawidłowe kordy: {}".format(kord_poprawny_lub_ze_spacjami)
            )

        self.x = int(self.kordy[0:3])
        self.y = int(self.kordy[4:7])
    
    @classmethod
    def from_coords(cls, x_coord:int, y_coord:int):
        return cls(str(x_coord)+"|"+str(y_coord))

    @classmethod
    def from_Village_class(cls, village):
        return cls.from_coords(village.x, village.y)

    def distance(self, other):
        """ distance between two villages """
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def time_distance(self, other, unit: str, swiat: int):
        """ return distance in seconds between two villages """
        unit_speed = Unit(unit).get_speed()
        world = self.get_world(swiat)
        return round(
            self.distance(other)
            / world.speed_world
            / world.speed_units
            * unit_speed
            * 60
        )

    def get_world(self, swiat:int):
        """ get world instance from database """
        try:
            world: models.World = models.World.objects.get(world=swiat)
        except Exception:
            raise Exception("Nie istnieje w bazie świat {}".format(swiat))
        return world

    def get_village(self, swiat:int):
        """ get village instance from database """
        try:
            village: models.Village = models.Village.objects.get(
                world=swiat, x=self.x, y=self.y
            )
        except Exception:
            raise Exception("Nie istnieje w bazie wioska {}".format(self.kordy))
        return village
    
    def get_player(self, swiat:int):
        """ get player instance from database, NOT nickname """
        try:
            player: models.Player = models.Player.objects.get(
                player_id=self.get_village(swiat).player_id, world=swiat
            )
        except Exception:
            raise Exception(
                "Nie istnieje w bazie właściciel wioski {}".format(self.kordy)
            )

        return player

    def get_id_wioski(self, swiat:int):
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


class Wiele_wiosek:
    """ class based on Wioska class, implemented
        that way long ago, leaved as it is. """

    def __init__(self, wiele_kordow_po_spacji: str):
        self.wiele_kordow_po_spacji = wiele_kordow_po_spacji.strip().split()
        self.lista_z_wioskami = [Wioska(i) for i in self.wiele_kordow_po_spacji]

    def __str__(self):
        return self.wiele_kordow_po_spacji


class Map:
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
            y_max = ceil(sqrt(radius ** 2 - x_coord ** 2))
            for y_coord in range(-y_max, y_max + 1):
                circle_map.append((x_coord + center[0], y_coord + center[1]))
        self.map = circle_map

    def __sub__(self, other):
        """ subs two maps WARNING! may be very slow, dont use if not necessery """
        return set(self.map) - set(other.map)

# brak testow
class Type_of_attack:
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

#brak testow
class Czas_wejscia:
    def __init__(
        self,
        data_wejscia: datetime.datetime,
        maksymalna_data_wejscia: datetime.datetime,
        rodzaj_ataku: Type_of_attack,
    ):
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
        odleglosc_sekundy = moja_wioska.time_distance(
            cel_wioska, self.unit, moja_wioska.get_world().world
        )
        return self.data_wejscia - datetime.timedelta(seconds=odleglosc_sekundy)


class Parent_Army_Defence_World_Evidence:
    """ Class representing worlds_evidence
    
    for given worlds value self.results is 3-element list with 0-1 values(T/F) 
    
    1- active, 0- inactive on world
        
    first 0/1 - paladin
        
    second 0/1 - archer
        
    third 0/1 - militia"""
    def __init__(self, world_number: int):
        self.world_number = world_number
        self.result: list = []
        self.set_data_about_world()

    def get_world(self):
        """ returning instance of World model for given int in constructor """
        return models.World.objects.get(world=self.world_number)

    def set_data_about_world(self):
        """ set self.result as 3-element list with 0-1 numbers

        1- active, 0- inactive on world
        
        first 0/1 - paladin
        
        second 0/1 - archer
        
        third 0/1 - militia"""
        world = self.get_world()
        result = []
        if world.paladin == "active":
            result.append(1)
        else:
            result.append(0)
        if world.archer == "active":
            result.append(1)
        else:
            result.append(0)
        if world.militia == "active":
            result.append(1)
        else:
            result.append(0)
        self.result = result
        # [RYCERZ, ŁUCZNICY, CHŁOPI]
        return result


class Army:
    """ 
    twin for Defence, class used when iterating over zbiorka_wojsko text of New_Outline class works properly for all types of world(with no archers or with archers etc.) args:
    \n text_army: str - from script zbiorka_wojsko after split('\ r\ n')
    \n parent_army_object: Parent_Army_Defence_World_Evidence - which determines type of world

    method clean_init(self) used only for form Wojsko_Outline_Form forms.py

    method get_village retruns Wioska instance of text[0]

    methods get_*unit*() return INT with number of units

    methods get_deff_units()/get_off_units() return INT with number of deff/off units

    methods [off/deff]_greater_than(value:INT) return TRUE/FALSE if units greater than *value*

    method have_szlachcic() return TRUE/FALSE if village have snob or doesn't
    """

    def __init__(
        self, text_army: str, parent_army_object: Parent_Army_Defence_World_Evidence
    ):
        self.text_army = text_army.split(",")
        self.world_evidence = parent_army_object.result

    def clean_init(self):
        """ 
        used ONLY in form to check user's input in Wojsko_Outline_Form forms.py
        not recomended to use method in any other situation(AFTER it's used in form)
         """
        # dokonczyc, uzyc to w forms.py clean_zbiorka_wojsko jako test, dodac world do **kwargs.
        wioska = Wioska(self.text_army[0])
        ev = self.world_evidence
        # all units
        if ev == [1, 1, 1] and len(self.text_army) not in {16, 17}:
            raise ValueError("Nieprawidłowe dane dla wybranego świata")
        # no militia
        if ev == [1, 1, 0] and len(self.text_army) not in {15, 16}:
            raise ValueError("Nieprawidłowe dane dla wybranego świata")
        # no paladin
        if ev == [0, 1, 1] and len(self.text_army) not in {15, 16}:
            raise ValueError("Nieprawidłowe dane dla wybranego świata")
        # no archers
        if ev == [1, 0, 1] and len(self.text_army) not in {14, 15}:
            raise ValueError("Nieprawidłowe dane dla wybranego świata")
        # no archers no militia
        if ev == [1, 0, 0] and len(self.text_army) not in {13, 14}:
            raise ValueError("Nieprawidłowe dane dla wybranego świata")
        # no archers no paladin
        if ev == [0, 0, 1] and len(self.text_army) not in {13, 14}:
            raise ValueError("Nieprawidłowe dane dla wybranego świata")
        # no militia no paladin
        if ev == [0, 1, 0] and len(self.text_army) not in {14, 15}:
            raise ValueError("Nieprawidłowe dane dla wybranego świata")
        # no archers no paladin no archers
        if ev == [0, 0, 0] and len(self.text_army) not in {12, 13}:
            raise ValueError("Nieprawidłowe dane dla wybranego świata")

    
    @property
    def coords_string(self):
        """ return kordy of village """
        return self.get_village().kordy

    def get_village(self):
        """ return Wioska instance of text[0] """
        return Wioska(self.text_army[0])

    def get_pikinier(self):
        """Pikinier always 1 element """
        return int(self.text_army[1])

    def get_miecznik(self):
        """MIecznik always 2 element """
        return int(self.text_army[2])

    def get_topornik(self):
        """Topornik, always 3 element """
        return int(self.text_army[3])

    def get_lucznik(self):
        """Łucznik if no archers, ValueError, 4 element otherwise """
        if self.world_evidence[1] == 0:
            raise ValueError("Łucznicy nie występują na tym świecie")
        return int(self.text_army[4])

    def get_zwiadowca(self):
        """Zwiadowca, If no archers, 4 element, 5 otherwise """
        if self.world_evidence[1] == 0:
            return int(self.text_army[4])
        return int(self.text_army[5])

    def get_lk(self):
        """LK, If no archers, 5 element, 6 otherwise """
        if self.world_evidence[1] == 0:
            return int(self.text_army[5])
        return int(self.text_army[6])

    def get_lucznik_konny(self):
        """Łucznik Konny if no archers, ValueError, 7 element otherwise """
        if self.world_evidence[1] == 0:
            raise ValueError("Łucznicy Konni nie występują na tym świecie")
        return int(self.text_army[7])

    def get_ck(self):
        """CK, If no archers, 6 element, 8 otherwise """
        if self.world_evidence[1] == 0:
            return int(self.text_army[6])
        return int(self.text_army[8])

    def get_taran(self):
        """Taran, If no archers, 7 element, 9 otherwise """
        if self.world_evidence[1] == 0:
            return int(self.text_army[7])
        return int(self.text_army[9])

    def get_katapulta(self):
        """Katapulta, If no archers, 8 element, 10 otherwise """
        if self.world_evidence[1] == 0:
            return int(self.text_army[8])
        return int(self.text_army[10])

    def get_szlachcic(self):
        """Szlachcic, depence of archers and paladin, could be 9,10,11,12 element """
        if self.world_evidence[1] == 0:
            if self.world_evidence[0] == 0:
                return int(self.text_army[9])
            return int(self.text_army[10])
        if self.world_evidence[0] == 0:
            return int(self.text_army[11])
        return int(self.text_army[12])
    
    def get_off_units(self):
        """ return number of offensive units(all that exists) 
        
        katapulta x8 taran x5 lk x4 topornik x1 łk x5
        """
        number = 0
        number += self.get_topornik() + self.get_lk() * 4 + self.get_taran() * 5 + self.get_katapulta() * 8
        try:
            value = self.get_lucznik_konny() * 5
            number += value
        except ValueError:
            return number
        return number

    def get_deff_units(self):
        """ return number of deff units(all that exists) 
        
        pik x1 miecz 1x łuk 1x ck x4
        """
        number = 0
        number += self.get_pikinier() + self.get_miecznik() + self.get_ck() * 4
        try:
            value = self.get_lucznik()
            number += value
        except ValueError:
            return number
        return number
    
    def off_greater_than(self, value:int):
        """ try off units > value, return bool """
        if not type(value) == int:
            raise ValueError("Incorrect value")
        return self.get_off_units() > value

    def deff_greater_than(self, value:int):
        """ try deff units > value, return bool """
        if not type(value) == int:
            raise ValueError("Incorrect value")
        return self.get_deff_units() > value

    def have_szlachcic(self):
        """ try village have snobs, return bool """
        return self.get_szlachcic() > 0


class Defence:
    """ 
    twin for Army, class used when iterating over zbiorka_obrona text of New_Outline class works properly for all types of world(with no archers or with archers etc.) args:
    \n text_army: str - from script zbiorka_wojsko after split('\ r\ n')
    \n parent_army_object: Parent_Army_Defence_World_Evidence - which determines type of world

    method clean_init(self) used only for form Obrona_Outline_Form forms.py

    method get_village retruns Wioska instance of text[0]

    methods get_*unit*() return INT with number of units

    methods get_deff_units()/get_off_units() return INT with number of deff/off units

    methods [off/deff]_greater_than(value:INT) return TRUE/FALSE if units greater than *value*

    method have_szlachcic() return TRUE/FALSE if village have snob or doesn't
    """

    def __init__(
        self, text_army: str, parent_army_object: Parent_Army_Defence_World_Evidence
    ):
        self.text_army = text_army.split(",")
        self.world_evidence = parent_army_object.result

    def get_village(self):
        """ return Wioska instance of text[0] """
        return Wioska(self.text_army[0])

    def get_pikinier(self):
        """Pikinier always 2 element """
        return int(self.text_army[2])

    def get_miecznik(self):
        """MIecznik always 3 element """
        return int(self.text_army[3])

    def get_topornik(self):
        """Topornik, always 4 element """
        return int(self.text_army[4])

    def get_lucznik(self):
        """Łucznik if no archers, ValueError, 5 element otherwise """
        if self.world_evidence[1] == 0:
            raise ValueError("Łucznicy nie występują na tym świecie")
        return int(self.text_army[5])

    def get_zwiadowca(self):
        """Zwiadowca, If no archers, 5 element, 6 otherwise """
        if self.world_evidence[1] == 0:
            return int(self.text_army[5])
        return int(self.text_army[6])

    def get_lk(self):
        """LK, If no archers, 6 element, 7 otherwise """
        if self.world_evidence[1] == 0:
            return int(self.text_army[6])
        return int(self.text_army[7])

    def get_lucznik_konny(self):
        """Łucznik Konny if no archers, ValueError, 8 element otherwise """
        if self.world_evidence[1] == 0:
            raise ValueError("Łucznicy Konni nie występują na tym świecie")
        return int(self.text_army[8])

    def get_ck(self):
        """CK, If no archers, 7 element, 9 otherwise """
        if self.world_evidence[1] == 0:
            return int(self.text_army[7])
        return int(self.text_army[9])

    def get_taran(self):
        """Taran, If no archers, 8 element, 10 otherwise """
        if self.world_evidence[1] == 0:
            return int(self.text_army[8])
        return int(self.text_army[10])

    def get_katapulta(self):
        """Katapulta, If no archers, 9 element, 11 otherwise """
        if self.world_evidence[1] == 0:
            return int(self.text_army[9])
        return int(self.text_army[11])

    def get_szlachcic(self):
        """Szlachcic, depence of archers and paladin, could be 10,11,12,13 element """
        if self.world_evidence[1] == 0:
            if self.world_evidence[0] == 0:
                return int(self.text_army[10])
            return int(self.text_army[11])
        if self.world_evidence[0] == 0:
            return int(self.text_army[12])
        return int(self.text_army[13])
    
    def get_off_units(self):
        """ return number of offensive units(all that exists) 
        
        katapulta x8 taran x5 lk x4 topornik x1 łk x5
        """
        number = 0
        number += self.get_topornik() + self.get_lk() * 4 + self.get_taran() * 5 + self.get_katapulta() * 8
        try:
            value = self.get_lucznik_konny() * 5
            number += value
        except ValueError:
            return number
        return number

    def get_deff_units(self):
        """ return number of deff units(all that exists) 
        
        pik x1 miecz 1x łuk 1x ck x4
        """
        number = 0
        number += self.get_pikinier() + self.get_miecznik() + self.get_ck() * 4
        try:
            value = self.get_lucznik()
            number += value
        except ValueError:
            return number
        return number
    
    def off_greater_than(self, value:int):
        """ try off units > value, return bool """
        if not type(value) == int:
            raise ValueError("Incorrect value")
        return self.get_off_units() > value

    def deff_greater_than(self, value:int):
        """ try deff units > value, return bool """
        if not type(value) == int:
            raise ValueError("Incorrect value")
        return self.get_deff_units() > value

    def have_szlachcic(self):
        """ try village has snob, return bool """
        return self.get_szlachcic() > 0
