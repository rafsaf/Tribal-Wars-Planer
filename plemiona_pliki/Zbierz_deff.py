from plemiona_pliki.wioska import Wioska, Map, Wiele_wiosek
from data.models import Village
from django.utils import timezone


def parse_to_Wioska(village):
    return Wioska('{}|{}'.format(village.x, village.y))


def get_map(list_of_Villages_objects, r):
    result_map = Map()
    set_x = set()
    result_map.set_as_square(300, (500, 500))
    for i in list_of_Villages_objects:
        map = Map()
        map.set_as_circle(r, (i.x, i.y))
        set_x.update(map.map)

    result_map.sub(set_x)


    return result_map


def zaplecze_lista_wiosek(enemy_villages, friendly_villages, r):
    result_villages = []

    map = get_map(enemy_villages, r).map

    for i in friendly_villages:
        if (i.x, i.y) in map:

            result_villages.append(parse_to_Wioska(i))
    print(result_villages[1])
    return result_villages


def zbierz_deff(enemy_villages, friendly_villages, r, text_obrona):

    lista_wiosek = zaplecze_lista_wiosek(enemy_villages, friendly_villages, r)

    context_all: dict = {}
    context_details: dict = {}
    if text_obrona == "":
        return ''
    n = 0
    for i in text_obrona.split("\r\n"):
        if n % 2 == 0:
            n += 1
            continue
        else:
            n += 1
        i = i.split(',')
        try:
            wioska = Wioska(i[0])
        except ValueError:
            print(i[0])
            continue

        if not wioska in lista_wiosek:

            continue

        owner = wioska.get_player(150)

        if owner not in context_all:
            if i[2] == '?':
                continue
            if int(i[2]) + int(i[3]) + 4 * int(i[7]) > 0:
                context_all[owner] = int(i[2]) + int(i[3]) + 4 * int(i[7])
                context_details[
                    owner] = '\r\r' + owner + '\r' + wioska.kordy + " Piki - " + i[
                        2] + ", Miecze - " + i[3] + ", CK - " + i[7]
        else:
            if int(i[2]) + int(i[3]) + 4 * int(i[7]) > 0:
                context_all[owner] += int(i[2]) + int(i[3]) + 4 * int(i[7])
                context_details[owner] += '\r' + wioska.kordy + " Piki - " + i[
                    2] + ", Miecze - " + i[3] + ", CK - " + i[7]

    output = ""
    for i in context_details:

        context_details[i] += "\rŁącznie - " + str(
            context_all[i]) + " - miejsc w zagrodzie, CK liczone jako x4"

        output += context_details[i]

    return output