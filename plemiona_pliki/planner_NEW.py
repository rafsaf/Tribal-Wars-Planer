from plemiona_pliki.swiat_i_jednostki import Swiat, Jednostki
from plemiona_pliki.db_pool import db_pool
from plemiona_pliki.wioska import Wiele_wiosek, Wioska
import datetime
import random
from plemiona_pliki.cele_masowo import ranodmize_cele_masowe, check_data
#
# Dążymy do uzupełnienia tabeli planner_baza_celi informacjami z planner_cele_recznie
#
jednostka = Jednostki()
swiat = Swiat(150)
swiat.predkosc()





def dodaj_do_bazy_celi(nazwa_gracza: str, x_wioski: int, y_wioski: int, id_wioski: int, x_celu: int, y_celu: int,
                       id_celu: int,
                       data_wyjscia: datetime.datetime, data_wejscia: datetime.datetime, jednostka: str):
    conn = db_pool.getconn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO planner_baza_celi(nazwa_gracza,x_wioski,y_wioski,id_wioski,x_celu,y_celu,id_celu,data_wyjscia,"
        "data_wejscia,jednostka) VALUES (%s, %s,%s, %s,%s, %s,%s, %s,%s, %s)",
        [nazwa_gracza, x_wioski, y_wioski, id_wioski, x_celu, y_celu, id_celu, data_wyjscia, data_wejscia, jednostka])
    conn.commit()
    cur.close()
    db_pool.putconn(conn)


def uzupelnij_planner_baza_celi():
    conn = db_pool.getconn()
    cur = conn.cursor()
    cur.execute("DELETE FROM planner_baza_celi;")
    conn.commit()

    cur.execute("SELECT * FROM planner_cele_recznie;")
    wszystkie_cele = cur.fetchall()

    cur.execute("SELECT * FROM planner_cele_masowo_robocze_tylko_wewnatrz;")
    wszystkie_cele2 = cur.fetchall()


    wszystkie_cele = wszystkie_cele + wszystkie_cele2



    for cel in wszystkie_cele:
        wioska_cel = Wioska(cel[1])
        wioski_jeden_gruby:list = Wiele_wiosek(cel[8]).lista_z_wioskami

        wioski_taran_fejk:list = Wiele_wiosek(cel[6]).lista_z_wioskami
        wioski_taran_off:list = Wiele_wiosek(cel[7]).lista_z_wioskami
        wioski_jeden_gruby_fejk:list = Wiele_wiosek(cel[9]).lista_z_wioskami
        wioski_deffoszlachta:list = Wiele_wiosek(cel[10]).lista_z_wioskami
        for wioska in wioski_jeden_gruby:
            if wioska.x != None:

                number = (wioski_jeden_gruby.count(wioska))


                rozkaz = Rodzaj_ataku()
                rozkaz.set_offoszlachta()
                czas = Czas_wejscia(cel[4], cel[5], rozkaz)
                for i in range(number):
                    dodaj_do_bazy_celi(wioska.get_player(swiat.number), wioska.x, wioska.y, wioska.get_id_wioski(swiat.number),
                                   wioska_cel.x, wioska_cel.y, wioska_cel.get_id_wioski(swiat.number),
                                   czas.czas_wyjscia_ataku(wioska, wioska_cel), czas.data_wejscia, rozkaz.rodzaj)
                if number > 1:
                    for i in range(len(wioski_jeden_gruby)):
                        if wioski_jeden_gruby[i] == wioska:
                            wioski_jeden_gruby[i].x = None

        for wioska in wioski_taran_off:
            rozkaz = Rodzaj_ataku()
            rozkaz.set_off()
            czas = Czas_wejscia(cel[2], cel[3], rozkaz)

            dodaj_do_bazy_celi(wioska.get_player(swiat.number),wioska.x, wioska.y,wioska.get_id_wioski(swiat.number),
                               wioska_cel.x, wioska_cel.y, wioska_cel.get_id_wioski(swiat.number),
                               czas.czas_wyjscia_ataku(wioska, wioska_cel), czas.data_wejscia, rozkaz.rodzaj)
        for wioska in wioski_taran_fejk:
            rozkaz = Rodzaj_ataku()
            rozkaz.set_fejk_taran()
            czas = Czas_wejscia(cel[2], cel[3], rozkaz)

            dodaj_do_bazy_celi(wioska.get_player(swiat.number),wioska.x, wioska.y,wioska.get_id_wioski(swiat.number),
                               wioska_cel.x, wioska_cel.y, wioska_cel.get_id_wioski(swiat.number),
                               czas.czas_wyjscia_ataku(wioska, wioska_cel), czas.data_wejscia, rozkaz.rodzaj)
        for wioska in wioski_jeden_gruby_fejk:
            if wioska.x != None:

                number = (wioski_jeden_gruby_fejk.count(wioska))


                rozkaz = Rodzaj_ataku()
                rozkaz.set_fejk_gruby()
                czas = Czas_wejscia(cel[4], cel[5], rozkaz)
                for i in range(number):
                    dodaj_do_bazy_celi(wioska.get_player(swiat.number), wioska.x, wioska.y, wioska.get_id_wioski(swiat.number),
                                   wioska_cel.x, wioska_cel.y, wioska_cel.get_id_wioski(swiat.number),
                                   czas.czas_wyjscia_ataku(wioska, wioska_cel), czas.data_wejscia, rozkaz.rodzaj)
                if number > 1:
                    for i in range(len(wioski_jeden_gruby_fejk)):
                        if wioski_jeden_gruby_fejk[i] == wioska:
                            wioski_jeden_gruby_fejk[i].x = None



        for wioska in wioski_deffoszlachta:
            rozkaz = Rodzaj_ataku()
            rozkaz.set_deffoszlachta()
            czas = Czas_wejscia(cel[4], cel[5], rozkaz)

            dodaj_do_bazy_celi(wioska.get_player(swiat.number),wioska.x, wioska.y,wioska.get_id_wioski(swiat.number),
                               wioska_cel.x, wioska_cel.y, wioska_cel.get_id_wioski(swiat.number),
                               czas.czas_wyjscia_ataku(wioska, wioska_cel), czas.data_wejscia, rozkaz.rodzaj)
    conn.commit()
    rodzaj1 = Rodzaj_ataku()
    rodzaj2 = Rodzaj_ataku()
    rodzaj1.set_off()

    cur.execute("select count(*), id_wioski from planner_baza_celi where jednostka = %s group by id_wioski;", [rodzaj1.rodzaj])
    lista = cur.fetchall()
    for i in lista:
        if i[0] > 1:
            cur.execute("select x_celu, y_celu from planner_baza_celi where id_wioski = %s and jednostka = %s", [i[1], rodzaj1.rodzaj])
            kordy = " ".join([str(i[0])+"|"+str(i[1]) for i in cur.fetchall()])
            raise ValueError("powtorzony off {} razy w wiosce plemiennej o id {}".format(i[0],i[1]), " kordy celi: {}".format(kordy))

    cur.close()
    db_pool.putconn(conn)
    #KONIEC


def get_output_results(text):

    output_text = ""

    conn = db_pool.getconn()
    cur = conn.cursor()
    cur.execute('SELECT DISTINCT nazwa_gracza FROM planner_baza_celi')
    all_players = cur.fetchall()

    gracze = []
    for i in all_players:
        gracze.append(i[0])


    for gracz in gracze:
        cur.execute('SELECT DISTINCT * FROM planner_baza_celi WHERE nazwa_gracza = %s ORDER BY data_wyjscia', [gracz])
        dane = cur.fetchall()
        output_text += "{} \r\r".format(gracz)
        output_text += text
        output_text += "\r[spoiler][code][table][**]Rodzaj Ataku[||]Źródło[||]Cel[||]Czas wyjścia[||]Czas wejścia[||]Rozkaz[/**]"

        for i in dane:
            output_text += "[*]{}[|] {}|{} [|] {}|{} [|] {} [|] {} [|] [" \
                           "url=https://pl150.plemiona.pl/game.php?village={}&screen=place&target={}]Wykonaj".format(
                i[10],i[2],i[3],i[5],i[6],i[8],i[9],i[4],i[7])
        output_text += '[/table]' # Koniec tabeli



        cur.execute("SELECT DISTINCT nazwa_gracza FROM planner_baza_celi WHERE id_celu IN(SELECT id_celu FROM "
                    "planner_baza_celi where nazwa_gracza = %s AND jednostka = 'OFFOSZLACHTA') AND"
                    " nazwa_gracza != %s;", [gracz, gracz])
        komendy = cur.fetchall()


        output_text += '\rONI mają udostępnić Ci komendy:\r'
        for i in komendy:
            output_text += '[player]'+i[0]+"[/player]\r"

        cur.execute("SELECT DISTINCT nazwa_gracza FROM planner_baza_celi WHERE id_celu IN(SELECT id_celu FROM "
                    "planner_baza_celi where nazwa_gracza = %s AND jednostka = 'CAŁY OFF PRĘDKOŚĆ TARANA KATAPULTY KUŹNIA') "
                    "AND nazwa_gracza != "
                    "%s AND jednostka = 'OFFOSZLACHTA';", [gracz, gracz])
        komendy = cur.fetchall()
        output_text += '\rTY masz IM mają udostępnić komendy:\r'
        for i in komendy:
            output_text += '[player]'+i[0]+"[/player]\r"
        output_text += "[/code][/spoiler]\r\r"

    conn.commit()

    cur.close()
    db_pool.putconn(conn)
    return output_text


def planner_NEW(text):
    check_data()
    ranodmize_cele_masowe()
    uzupelnij_planner_baza_celi()
    return get_output_results(text)
