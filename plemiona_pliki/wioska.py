from math import sqrt
from plemiona_pliki.db_pool import db_pool
import plemiona_pliki.swiat_i_jednostki as swiat_i_jednostki
from math import sqrt, floor, ceil

jednostki = swiat_i_jednostki.Jednostki()

class Wioska():
    def __init__(self, kord_poprawny_lub_ze_spacjami:str):
        self.kordy = kord_poprawny_lub_ze_spacjami.strip()
        if len(self.kordy) != 7:
            raise ValueError("złe kordy")
        self.x = int(self.kordy[0:3])
        self.y = int(self.kordy[4:7])

    def distance(self, other):
        return sqrt((self.x - other.x)**2+(self.y-other.y)**2)

    def time_distance(self, other, jednostka:str, swiat:int):
        if not jednostka in jednostki.slownik_jedn_predkosc:
            raise ValueError("Zła jednostka")
        sw = swiat_i_jednostki.Swiat(swiat)
        return round(self.distance(other) / sw.predkosc_swiata /
              sw.predkosc_jednostek * jednostki.slownik_jedn_predkosc[jednostka] * 60)

    def get_player(self,swiat):
        conn = db_pool.getconn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM data_player JOIN data_village as v USING(player_id) WHERE v.x = %s AND v.y = %s "
                    "AND v.world = %s", [self.x, self.y, swiat])
        x = cur.fetchall()
        cur.close()
        db_pool.putconn(conn)
        if x == []:
            raise ValueError("Nie istnieje w bazie właściciel wioski {}".format(self.kordy))
        if type(x) == list:
            return str(x[-1][2])
        else:
            raise ValueError("Błąd wioska {}".format(self.kordy))
    def get_id_wioski(self, swiat):
        conn = db_pool.getconn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM data_village where x = %s AND y = %s AND world = %s", [self.x, self.y, swiat])
        x = cur.fetchall()
        cur.close()
        db_pool.putconn(conn)
        if x == []:
            raise ValueError("Wioska {} nie istnieje w bazie".format(self.kordy))
        else:
            return int(x[0][1])
    def get_punkty_wioski(self, swiat):
        conn = db_pool.getconn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM data_village where x = %s AND y = %s AND world = %s", [self.x, self.y, swiat])
        x = cur.fetchall()
        cur.close()
        db_pool.putconn(conn)
        if x == []:
            raise ValueError("Wioska {} nie istnieje w bazie".format(self.kordy))
        else:
            return int(x[0][6])

    def get_player_points(self, swiat):
        conn = db_pool.getconn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM data_player where name = %s and world = %s",[self.get_player(swiat), swiat])
        x = cur.fetchall()
        cur.close()
        db_pool.putconn(conn)
        if x == []:
            raise ValueError("Wioska {} nie istnieje w bazie".format(self.kordy))
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
    def __init__(self, wiele_kordow_po_spacji:str):
        wiele_kordow_po_spacji = wiele_kordow_po_spacji.strip()

        lista_wiosek = wiele_kordow_po_spacji.split()

        self.lista_z_wioskami = [Wioska(i) for i in lista_wiosek]


class Map():
    def __init__(self):
        self.map = set()

    def set_r_and_center(self, r, center):
        map = []
        for i in range(-r, r + 1):
            for j in range(-r, r+1):
                map.append((center[0]+i,center[1]+j))
        self.map = set(map)

    def set_r_and_center_circle(self, r, center):
        t = []
        for x in range(-r, r):
            y_max = ceil(sqrt(r ** 2 - x**2))
            for y in range(- y_max, y_max):
                t.append((x+center[0],y+center[1]))
        self.map = set(t)

    def sub(self, set_map: set):
        self.map = self.map - set_map






