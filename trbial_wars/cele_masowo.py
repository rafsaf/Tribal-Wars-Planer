from tribal_wars.db_pool import db_pool
from tribal_wars.wioska import many_villages
import random


def check_data():
    conn = db_pool.getconn()
    cur = conn.cursor()

    cur.execute("SELECT * FROM planner_cele_masowo;")
    wszystkie_cele1 = cur.fetchall()

    cur.execute("SELECT * FROM planner_cele_recznie;")
    wszystkie_cele2 = cur.fetchall()

    wszystkie_cele = wszystkie_cele1 + wszystkie_cele2

    gruby, off, gruby_fejk, taran_fejk = [], [], [], []
    for cel in wszystkie_cele:
        gruby += [i for i in many_villages(cel[8]).village_list]
        off += [i for i in many_villages(cel[7]).village_list]
        gruby_fejk += [i for i in many_villages(cel[9]).village_list]

    while off != []:
        i = off.pop()

        if i in off:
            raise ValueError("Powtórzone offy: {}".format(i.coord))
    conn.commit()
    cur.close()
    db_pool.putconn(conn)

def ranodmize_cele_masowe():
    conn = db_pool.getconn()
    cur = conn.cursor()
    cur.execute("DELETE FROM planner_cele_masowo_robocze_tylko_wewnatrz;")
    conn.commit()

    cur.execute("SELECT * FROM planner_cele_masowo;")
    wszystkie_cele = cur.fetchall()
    for cel in wszystkie_cele:
        wioski_cele = many_villages(cel[1]).village_list



        wioski_jeden_gruby:list = [i.coord for i  in many_villages(cel[8]).village_list]



        wioski_taran_fejk:list = [i.coord for i in many_villages(cel[6]).village_list]
        random.shuffle(wioski_taran_fejk)


        wioski_taran_off:list = [i.coord for i in many_villages(cel[7]).village_list]



        wioski_jeden_gruby_fejk:list = [i.coord for i in many_villages(cel[9]).village_list]


        dlugosc1:int = len(wioski_taran_fejk) // len(wioski_cele)
        dlugosc2:int = len(wioski_taran_off) // len(wioski_cele)
        dlugosc3:int = len(wioski_jeden_gruby) // len(wioski_cele)
        dlugosc4:int = len(wioski_jeden_gruby_fejk) // len(wioski_cele)
        for i in range(len(wioski_cele)):

            cur.execute("INSERT INTO planner_cele_masowo_robocze_tylko_wewnatrz(kordy_celu, data_wejscia_taranow, "
                        "koncowa_data_wejscia_taranow, "
                        "data_wejscia_grubych, koncowa_data_wejscia_grubych, kordy_taran_fejk, kordy_taran_off, "
                        "kordy_jeden_gruby, kordy_jeden_gruby_fejk, kordy_deffoszlachta) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",
                        [wioski_cele[i].coord, cel[2], cel[3], cel[4], cel[5],
                         " ".join(wioski_taran_fejk[i*dlugosc1: (i+1)*dlugosc1]),
                         " ".join(wioski_taran_off[i*dlugosc2: (i+1)*dlugosc2]),
                         " ".join(wioski_jeden_gruby[i*dlugosc3: (i+1)*dlugosc3]),
                         " ".join(wioski_jeden_gruby_fejk[i*dlugosc4: (i+1)*dlugosc4]),
                         cel[10]


                         ])

            conn.commit()
    cur.close()
    db_pool.putconn(conn)



