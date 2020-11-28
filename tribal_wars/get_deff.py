"""
Model contains functions to convert text

From script Obrona to nice good looking version

Also prining only villages in center

"""
from math import ceil

from django.db.models import F, IntegerField, ExpressionWrapper

from base import models
from . import basic


def get_deff(
    outline: models.Outline,
    radius: int,
    deff=True,
    ally_name_list=None,
    enemy_name_list=None,
    excluded_villages="",
):
    """
    Args is instance of Outline, WARNING! be sure to use CORRECT
    data in instance, returns text with deff results.
    """
    if ally_name_list is None:
        ally_name_list = []
    if enemy_name_list is None:
        enemy_name_list = []

    if outline.deff_troops == "":
        return ""

    my_tribe = outline.ally_tribe_tag
    ally_tribe_pk = [f"{tag}::{outline.world}" for tag in my_tribe]
    enemy_tribe = outline.enemy_tribe_tag

    my_tribe_id = [
        tribe.tribe_id
        for tribe in models.Tribe.objects.all().filter(id__in=ally_tribe_pk)
    ]
    ally_players = models.Player.objects.all().filter(
        tribe_id__in=my_tribe_id, world=outline.world
    )

    my_tribe_villages = models.VillageModel.objects.all().filter(
        world=outline.world,
        player_id__in=[player.player_id for player in ally_players]
        + [
            player.player_id
            for player in models.Player.objects.all().filter(
                name__in=ally_name_list, world=outline.world
            )
        ],
    )

    if excluded_villages != "":
        excluded_villages = basic.many_villages(excluded_villages)

        my_tribe_villages = my_tribe_villages.exclude(
            id__in=[
                f"{village.coord}-{outline.world}"
                for village in excluded_villages
            ]
        )

    enemy_tribe_villages = models.VillageModel.objects.all().filter(
        world=outline.world,
        player_id__in=[
            player.player_id
            for player in models.Player.objects.all().filter(
                tribe_id__in=[
                    tribe.tribe_id
                    for tribe in models.Tribe.objects.all().filter(
                        world=outline.world, tag__in=enemy_tribe
                    )
                ]
                + [
                    player.player_id
                    for player in models.Player.objects.all().filter(
                        name__in=enemy_name_list
                    )
                ],
                world=outline.world,
            )
        ],
    )

    village_dictionary = {}
    player_dictionary = {}

    for player in ally_players:
        player_dictionary[player.player_id] = player.name
    for village_model in my_tribe_villages:
        village_dictionary[
            f"{village_model.x_coord}|{village_model.y_coord}"
        ] = player_dictionary[village_model.player_id]

    if deff:
        return deff_text2(
            my_tribe_villages,
            enemy_tribe_villages,
            radius,
            outline.off_troops,
            outline.deff_troops,
            int(outline.world),
            village_dictionary,
        )
    else:
        return off_text(
            my_tribe_villages,
            enemy_tribe_villages,
            radius,
            outline.off_troops,
            outline.deff_troops,
            int(outline.world),
            village_dictionary,
        )

def get_legal_coords(ally_villages, enemy_villages, radius, p=0.4):
    """ Create set with ally_vill without enemy_vill closer than radius """
    # ally_villages_ids = [village.pk for village in ally_villages]
# 
    # query = models.VillageModel.objects.filter(pk__in=ally_villages_ids)
# 
    # for i, village in enumerate(enemy_villages):
    #     if not i % 10 == 0:
    #         continue
    #     left_right = [village.x_coord - radius, village.x_coord + radius]
    #     up_down = [village.y_coord + radius, village.y_coord - radius]
# 
    #     query = query.exclude(x_coord__gte=left_right[0], x_coord__lte=left_right[1],
    #                 y_coord__lte=up_down[0], y_coord__gte=up_down[1])
    #     
    #     if i % 1000 == 0 and i != 0:
    #         ally_villages_ids = [village.pk for village in query]
    #         query = models.VillageModel.objects.filter(pk__in=ally_villages_ids)
    # 
    # ally_set = set()
    # for village in query:
    #     ally_set.add((village.x_coord, village.y_coord))
    # return ally_set
    enemy_count = enemy_villages.count()
    instance_number = ceil(enemy_count * (p) + 1000)

    banned_coords = set()
    ally_set = set()
    for village in ally_villages:
        ally_set.add((village.x_coord, village.y_coord))
    for village in enemy_villages.order_by("?")[:instance_number]:
        pass_bool = False
        if (village.x_coord, village.y_coord) in banned_coords:
            for coord in basic.yield_four_circle_ends(
                radius, (village.x_coord, village.y_coord)
            ):
                if coord in banned_coords:
                    break
                pass_bool = True
        if not pass_bool:
            for coord in basic.yield_circle(
                radius, (village.x_coord, village.y_coord)
            ):
                if coord not in banned_coords:
                    banned_coords.add(coord)

    return ally_set - banned_coords


def get_set_of_villages(ally_villages, enemy_villages, radius):
    """ get list of legal villages from ally villages"""
    result_villages = set()
    legal_cords = get_legal_coords(ally_villages, enemy_villages, radius)
    for i in ally_villages:
        if (i.x_coord, i.y_coord) in legal_cords:
            result_villages.add(f"{i.x_coord}|{i.y_coord}")
    
    return result_villages


def deff_text(
    ally_villages,
    enemy_villages,
    radius,
    text_obrona,
    world,
    village_dictionary,
):
    """
    uses get_list_of_villages to get legal villages in legal area,
    from text_obrona get numbers of units finaly returns text with results
    """

    lista_wiosek = get_set_of_villages(ally_villages, enemy_villages, radius)

    context_all: dict = {}
    context_details: dict = {}
    if text_obrona == "":
        return ""

    world_evidence = basic.world_evidence(world_number=world)

    for i, line in enumerate(text_obrona.strip().split("\r\n")):

        if i % 2 == 1:
            continue

        deff_instance = basic.Defence(text_army=line, evidence=world_evidence)
        try:
            owner = village_dictionary[deff_instance.coord]
        except KeyError:
            raise KeyError()
        if deff_instance.coord not in lista_wiosek:
            continue
        deff = deff_instance.deff
        if deff <= 0:
            continue

        if owner not in context_all:
            context_all[owner] = deff
            context_details[
                owner
            ] = f"\r\n{owner}\r\n{deff_instance.coord} - {deff}"
        else:
            context_all[owner] += deff
            context_details[owner] += f"\r\n{deff_instance.coord} - {deff}"

    output = ""
    for i in context_details:

        context_details[
            i
        ] += f"\r\nŁącznie - {context_all[i]} - miejsc w zagrodzie, CK liczone jako x4\r\n"

        output += context_details[i]

    return output


def off_text(
    ally_villages,
    enemy_villages,
    radius,
    text_off,
    text_deff,
    world,
    village_dictionary,
):
    """
    uses get_list_of_villages to get legal villages in legal area,
    from text_obrona get numbers of units finaly returns text with results
    """

    not_in_front = get_set_of_villages(ally_villages, enemy_villages, radius)

    in_village: dict = {}
    outside_village: dict = {}
    context_all: dict = {}

    world_evidence = basic.world_evidence(world_number=world)

    for i, line in enumerate(text_deff.strip().split("\r\n")):

        deff_instance = basic.Defence(text_army=line, evidence=world_evidence)
        try:
            owner = village_dictionary[deff_instance.coord]
        except KeyError:
            raise KeyError()

        if i % 2 == 1:
            outside_village[deff_instance.coord] = deff_instance
        else:
            in_village[deff_instance.coord] = deff_instance

    for line in text_off.strip().split("\r\n"):
        off_instance = basic.Army(text_army=line, evidence=world_evidence)
        try:
            owner = village_dictionary[off_instance.coord]
        except KeyError:
            raise KeyError()

        if owner not in context_all:
            context_all[owner] = [off_instance]
        else:
            context_all[owner].append(off_instance)

    all_off_text = basic.NewOffsText()

    output = ""
    for owner, lst in context_all.items():
        new_off = basic.NewOffsText(name=owner)
        all_string = "\r\n\r\n"
        text = ""
        lst.sort(key=lambda army: army.off, reverse=True)

        front = [army for army in lst if army.coord not in not_in_front]
        not_front = [army for army in lst if army.coord in not_in_front]

        text += "\r\n---------FRONT---------" + "\r\n"
        for army in front:
            all_off_text.add_army_front(army)
            new_off.add_army_front(army)
            try:
                inside = in_village[army.coord]
                away_off = army.off - inside.off
                away_nob = army.nobleman - inside.nobleman
            except KeyError:
                away_off = "brak danych"
                away_nob = "brak danych"

            text += (
                f"{army.coord}- Off- {army.off} Gruby- {army.nobleman}  "
                f"(Poza wioską [ {away_off} , {away_nob} ])\r\n"
            )
        text += "---------ZAPLECZE---------" + "\r\n"
        for army in not_front:
            all_off_text.add_army_out(army)
            new_off.add_army_out(army)

            try:
                inside = in_village[army.coord]
                away_off = army.off - inside.off
                away_nob = army.nobleman - inside.nobleman
            except KeyError:
                away_off = "brak danych"
                away_nob = "brak danych"

            text += (
                f"{army.coord} Off- {army.off} Gruby- {army.nobleman}  "
                f"(Poza wioską [ {away_off} , {away_nob} ])\r\n"
            )

        all_off_text.add_user(new_off.simplified())
        all_string += new_off.simplified() + text
        output += all_string

    return str(all_off_text.text() + output)


def deff_text2(
    ally_villages,
    enemy_villages,
    radius,
    text_off,
    text_deff,
    world,
    village_dictionary,
):
    """
    uses get_list_of_villages to get legal villages in legal area,
    from text_obrona get numbers of units finaly returns text with results
    """

    not_in_front = get_set_of_villages(ally_villages, enemy_villages, radius)
    deff_in_village_back: dict = {}
    deff_in_village_front: dict = {}
    deff_own_from_village_back: dict = {}
    deff_own_from_village_front: dict = {}

    world_evidence = basic.world_evidence(world_number=world)

    for i, line in enumerate(text_deff.strip().split("\r\n")):
        if i % 2 == 1:
            continue

        deff_instance = basic.Defence(text_army=line, evidence=world_evidence)
        try:
            owner = village_dictionary[deff_instance.coord]
        except KeyError:
            raise basic.DeffException()

        if deff_instance.coord in not_in_front:
            deff_in_village_back[deff_instance.coord] = deff_instance
        else:
            deff_in_village_front[deff_instance.coord] = deff_instance

    for line in text_off.strip().split("\r\n"):
        army_instance = basic.Army(text_army=line, evidence=world_evidence)
        try:
            owner = village_dictionary[army_instance.coord]
        except KeyError:
            raise basic.DeffException()

        if army_instance.coord in not_in_front:
            deff_own_from_village_back[army_instance.coord] = army_instance
        else:
            deff_own_from_village_front[army_instance.coord] = army_instance

    all_deff_text = basic.NewDeffText()

    for coord, deff_instance in deff_in_village_back.items():
        try:
            army_instance = deff_own_from_village_back[coord]
        except KeyError:
            army_instance = None
        owner = village_dictionary[coord]
        all_deff_text.add_back_village(owner, deff_instance, army_instance)

    for coord, deff_instance in deff_in_village_front.items():
        try:
            army_instance = deff_own_from_village_front[coord]
        except KeyError:
            army_instance = None
        owner = village_dictionary[coord]
        all_deff_text.add_front_village(owner, deff_instance, army_instance)

    return str(all_deff_text)
