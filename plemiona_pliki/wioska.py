

from math import sqrt, ceil
from base import models


class Units():
    """ Helps geting proper speed of units """
    def __init__(self):
        self.slownik_jedn_predkosc = {
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

    def speed(self, jednostka: str):
        """ return speed of unit jednostka """
        try:
            return self.slownik_jedn_predkosc[jednostka]
        except Exception:
            raise ValueError("Nie istnieje jednostka: {}".format(jednostka))



class Wioska():
    """ Class used to represent village in game """
    def __init__(self, kord_poprawny_lub_ze_spacjami: str):
        self.kordy = kord_poprawny_lub_ze_spacjami.strip()
        if len(self.kordy) != 7:
            raise ValueError("złe kordy")
        self.x = int(self.kordy[0:3])
        self.y = int(self.kordy[4:7])

    def distance(self, other):
        """ Distance between two villages """
        return sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def time_distance(self, other, jednostka: str, swiat: int):
        """ return distance in hours between two villages """
        unit_speed = Units().speed(jednostka)
        world = self.get_world(swiat)

        return round(
            self.distance(other) / world.speed_world / world.speed_units *
            unit_speed * 60)

    def get_world(self, swiat):
        """ get world instance from database """
        try:
             world = models.World.objects.get(world=swiat)
        except Exception:
            raise Exception('Nie istnieje w bazie świat {}'.format(swiat))
        return world


    def get_village(self, swiat):
        """ get village instance from database """
        try:
            village = models.Village.objects.get(world=swiat, x=self.x, y=self.y)
        except Exception:
            raise Exception('Nie istnieje w bazie wioska {}'.format(self.kordy))
        return village

    def get_player(self, swiat):
        """ get player instance from database """
        try:
            player = models.Player.objects.get(player_id= self.get_village(swiat).player_id)
        except Exception:
            raise Exception(
                "Nie istnieje w bazie właściciel wioski {}".format(self.kordy))

        return player.name

    def get_id_wioski(self, swiat):
        conn = db_pool.getconn()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM data_village where x = %s AND y = %s AND world = %s",
            [self.x, self.y, swiat])
        x = cur.fetchall()
        cur.close()
        db_pool.putconn(conn)
        if x == []:
            raise ValueError("Wioska {} nie istnieje w bazie".format(
                self.kordy))
        else:
            return int(x[0][1])

    def get_punkty_wioski(self, swiat):
        conn = db_pool.getconn()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM data_village where x = %s AND y = %s AND world = %s",
            [self.x, self.y, swiat])
        x = cur.fetchall()
        cur.close()
        db_pool.putconn(conn)
        if x == []:
            raise ValueError("Wioska {} nie istnieje w bazie".format(
                self.kordy))
        else:
            return int(x[0][6])

    def get_player_points(self, swiat):
        conn = db_pool.getconn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM data_player where name = %s and world = %s",
                    [self.get_player(swiat), swiat])
        x = cur.fetchall()
        cur.close()
        db_pool.putconn(conn)
        if x == []:
            raise ValueError("Wioska {} nie istnieje w bazie".format(
                self.kordy))
        else:
            return int(x[0][5])

    def get_map(self, r, center):
        map = Map()
        map.set_r_and_center(r, center)
        return map

    def __str__(self):
        return str(self.kordy)

    def __eq__(self, other):
        return self.kordy == other.kordy


class Wiele_wiosek():
    def __init__(self, wiele_kordow_po_spacji: str):
        wiele_kordow_po_spacji = wiele_kordow_po_spacji.strip()

        lista_wiosek = wiele_kordow_po_spacji.split()

        self.lista_z_wioskami = [Wioska(i) for i in lista_wiosek]


class Map():
    def __init__(self):
        self.map = set()

    def set_r_and_center(self, r, center):
        map = []
        for i in range(-r, r + 1):
            for j in range(-r, r + 1):
                map.append((center[0] + i, center[1] + j))
        self.map = set(map)

    def set_r_and_center_circle(self, r, center):
        t = []
        for x in range(-r, r):
            y_max = ceil(sqrt(r**2 - x**2))
            for y in range(-y_max, y_max):
                t.append((x + center[0], y + center[1]))
        self.map = set(t)

    def sub(self, set_map: set):
        self.map = self.map - set_map


