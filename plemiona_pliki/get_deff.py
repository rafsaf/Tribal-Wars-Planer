"""
 Model contains functions to convert text
 from script Obrona to nice good looking version, also prining only villages in center
"""

from base import models
from .basic_classes import (
    Wioska,
    Map,
    Wiele_wiosek,
    Defence,
    Parent_Army_Defence_World_Evidence,
)


def get_deff(
    new_Outline: models.New_Outline,
    radius: int,
    ally_name_list=None,
    enemy_name_list=None,
    excluded_villages="",
):
    """
    Args is instance of New_Outline, WARNING! be sure to use CORRECT
    data in instance, returns text with deff results.
    """
    if ally_name_list is None:
        ally_name_list = []
    if enemy_name_list is None:
        enemy_name_list = []

    if new_Outline.zbiorka_obrona == "":
        return ""
    # napisać funkcję która sprawdza dokładnie poprawność przed pojsciem dalej
    # lub wcześniej w forms.py to zrobić
    my_tribe = new_Outline.moje_plemie_skrot.split(", ")
    my_tribe_id = [
        tribe.tribe_id
        for tribe in models.Tribe.objects.all().filter(
            world=new_Outline.swiat, tag__in=my_tribe
        )
    ]

    enemy_tribe = new_Outline.przeciwne_plemie_skrot.split(", ")

    my_tribe_villages = models.Village.objects.all().filter(
        world=new_Outline.swiat,
        player_id__in=[
            player.player_id
            for player in models.Player.objects.all().filter(
                tribe_id__in=my_tribe_id, world=new_Outline.swiat,
            )
        ]
        + [
            player.player_id
            for player in models.Player.objects.all().filter(name__in=ally_name_list)
        ],
    )

    if not excluded_villages == "":
        excluded_villages = Wiele_wiosek(excluded_villages).lista_z_wioskami

        my_tribe_villages = my_tribe_villages.exclude(
            village_id__in=[
                village.get_id_wioski(new_Outline.swiat)
                for village in excluded_villages
            ]
        )

    enemy_tribe_villages = models.Village.objects.all().filter(
        world=new_Outline.swiat,
        player_id__in=[
            player.player_id
            for player in models.Player.objects.all().filter(
                tribe_id__in=[
                    tribe.tribe_id
                    for tribe in models.Tribe.objects.all().filter(
                        world=new_Outline.swiat, tag__in=enemy_tribe
                    )
                ]
                + [
                    player.player_id
                    for player in models.Player.objects.all().filter(
                        name__in=enemy_name_list
                    )
                ],
                world=new_Outline.swiat,
            )
        ],
    )
    # to get context coord : owner
    player_dictionary = {}
    village_dictionary = {}

    players = models.Player.objects.all().filter(
        tribe_id__in=my_tribe_id, world=new_Outline.swiat
    )

    for player_model in players:
        player_dictionary[player_model.player_id] = player_model.name

    for v in my_tribe_villages:
        village_dictionary[str(v.x) + "|" + str(v.y)] = player_dictionary[v.player_id]

    return deff_text(
        my_tribe_villages,
        enemy_tribe_villages,
        radius,
        new_Outline.zbiorka_obrona,
        int(new_Outline.swiat),
        village_dictionary,
    )


def get_legal_coords(ally_villages, enemy_villages, radius):
    """ create map with ally_vill without enemy_vill """
    enemy_villages_map = Map()
    ally_villages_map = Map()

    for village in ally_villages:
        ally_villages_map.add_vertex(village.x, village.y)

    for village in enemy_villages:
        map_instance = Map()
        map_instance.set_as_circle(radius, (village.x, village.y))
        enemy_villages_map.map += map_instance.map

    return ally_villages_map - enemy_villages_map


def get_list_of_villages(ally_villages, enemy_villages, radius):
    """ get list of legal villages from ally villages"""
    result_villages = []
    legal_cords = get_legal_coords(ally_villages, enemy_villages, radius)
    for i in ally_villages:
        if (i.x, i.y) in legal_cords:
            result_villages.append(Wioska("{}|{}".format(i.x, i.y)))

    return result_villages


def deff_text(
    ally_villages, enemy_villages, radius, text_obrona, world, village_dictionary
):
    """
    uses get_list_of_villages to get legal villages in legal area,
    from text_obrona get numbers of units finaly returns text with results
    """

    lista_wiosek = get_list_of_villages(ally_villages, enemy_villages, radius)

    context_all: dict = {}
    context_details: dict = {}
    if text_obrona == "":
        return ""
    index = 0
    for i in text_obrona.split("\r\n"):
        if index % 2 == 1:
            index += 1
            continue
        index += 1
        # classes from basic_classes.py !
        parent_world_evidence = Parent_Army_Defence_World_Evidence(world_number=world)
        #
        deff_instance = Defence(text_army=i, parent_army_object=parent_world_evidence)
        #
        wioska = deff_instance.get_village()
        if wioska not in lista_wiosek:
            continue
        owner = village_dictionary[wioska.kordy]
        if owner not in context_all:
            # sprawdzic czy "?" w deff_instance ???
            if deff_instance.get_deff_units() > 0:

                context_all[owner] = deff_instance.get_deff_units()
                context_details[owner] = (
                    "\r\n"
                    + owner
                    + "\r\n"
                    + wioska.kordy
                    + " Piki - "
                    + str(deff_instance.get_pikinier())
                    + ", Miecze - "
                    + str(deff_instance.get_miecznik())
                    + ", CK - "
                    + str(deff_instance.get_ck())
                )
        else:
            if deff_instance.get_deff_units() > 0:
                context_all[owner] += deff_instance.get_deff_units()
                context_details[owner] += (
                    "\r\n"
                    + wioska.kordy
                    + " Piki - "
                    + str(deff_instance.get_pikinier())
                    + ", Miecze - "
                    + str(deff_instance.get_miecznik())
                    + ", CK - "
                    + str(deff_instance.get_ck())
                )

    output = ""
    for i in context_details:

        context_details[i] += (
            "\r\nŁącznie - "
            + str(context_all[i])
            + " - miejsc w zagrodzie, CK liczone jako x4\r\n"
        )

        output += context_details[i]

    return output
