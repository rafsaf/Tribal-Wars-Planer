from base import models
from .basic_classes import Wioska, Map, Wiele_wiosek


def get_deff_text(New_Outline: models.New_Outline, radius, excluded_villages):
    """
    Args is instance of New_Outline, WARNING! be sure to use CORRECT
    data in instance, returns text with deff results.
    """

    # napisać funkcję która sprawdza dokładnie poprawność przed pojsciem dalej
    # lub wcześniej w forms.py to zrobić
    my_tribe = New_Outline.moje_plemie_skrot.split(', ')
    enemy_tribe = New_Outline.przeciwne_plemie_skrot.split(', ')

    my_tribe_villages = models.Village.objects.all().filter(
        world=New_Outline.swiat,
        player_id__in=[
            player.player_id for player in models.Player.objects.all().filter(
                tribe_id__in=[
                    tribe.tribe_id
                    for tribe in models.Tribe.objects.all().filter(
                        world=New_Outline.swiat, tag__in=my_tribe)
                ],
                world=New_Outline.swiat)
        ])

    if not excluded_villages == '':
        excluded_villages = Wiele_wiosek(excluded_villages).lista_z_wioskami

        my_tribe_villages = my_tribe_villages.exclude(village_id__in=[
            village.get_id_wioski(New_Outline.swiat)
            for village in excluded_villages
        ])

    enemy_tribe_villages = models.Village.objects.all().filter(
        world=New_Outline.swiat,
        player_id__in=[
            player.player_id for player in models.Player.objects.all().filter(
                tribe_id__in=[
                    tribe.tribe_id
                    for tribe in models.Tribe.objects.all().filter(
                        world=New_Outline.swiat, tag__in=enemy_tribe)
                ],
                world=New_Outline.swiat)
        ])
    return get_deff(my_tribe_villages, enemy_tribe_villages, radius, New_Outline.zbiorka_obrona)



def get_legal_coords(ally_villages, enemy_villages, radius):
    """ create map with ally_vill without enemy_vill """
    enemy_villages_map = Map()
    ally_villages_map = Map()

    for village in enemy_villages:
        enemy_villages_map.add_vertex(village.x, village.y)

    for village in ally_villages:
        map_instance = Map()
        map_instance.set_as_circle(radius, (village.x, village.y))
        ally_villages_map.map += map_instance.map

    return ally_villages_map - enemy_villages_map


def get_list_of_villages(ally_villages, enemy_villages, radius):
    """ get list of legal villages from ally villages"""
    result_villages = []
    legal_cords = get_legal_coords(ally_villages, enemy_villages, radius)

    for i in ally_villages:
        if (i.x, i.y) in legal_cords:
            result_villages.append(Wioska("{}|{}".format(i.x, i.y)))

    return result_villages


def get_deff(ally_villages, enemy_villages, radius, text_obrona):
    """
    uses get_list_of_villages to get legal villages in legal area,
    from text_obrona get numbers of units finaly returns text with results
    """
    lista_wiosek = get_list_of_villages(ally_villages, enemy_villages, radius)

    context_all: dict = {}
    context_details: dict = {}
    if text_obrona == "":
        return ''
    index = 0
    for i in text_obrona.split("\r\n"):
        if index % 2 == 0:
            index += 1
            continue
        index += 1
        i = i.split(',')
        wioska = Wioska(i[0])
        if wioska not in lista_wiosek:
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