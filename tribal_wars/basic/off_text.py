from django.utils.translation import gettext as _


class NewOffsText:
    def __init__(self, name=None):
        self.ins = {"1": 0, "3/4": 0, "1/2": 0, "1/4": 0}
        self.out = {"1": 0, "3/4": 0, "1/2": 0, "1/4": 0}
        self.name = name
        self.newline = "\r\n"
        self.results = ""

    def add_army_front(self, army):
        if army.off >= 20000:
            self.ins["1"] += 1
        elif army.off >= 15000:
            self.ins["3/4"] += 1
        elif army.off >= 10000:
            self.ins["1/2"] += 1
        elif army.off >= 5000:
            self.ins["1/4"] += 1

    def add_army_out(self, army):
        if army.off >= 20000:
            self.out["1"] += 1
        elif army.off >= 15000:
            self.out["3/4"] += 1
        elif army.off >= 10000:
            self.out["1/2"] += 1
        elif army.off >= 5000:
            self.out["1/4"] += 1

    def full_text(self):
        return (
            f"\r\n---FRONT---\r\n"
            f"Pełne : {self.ins['1']},\r\n"
            f"3/4 : {self.ins['3/4']},\r\n"
            f"1/2 : {self.ins['1/2']},\r\n"
            f"1/4 : {self.ins['1/4']},\r\n"
            f"---ZAPLECZE---\r\n"
            f"Pełne : {self.out['1']},\r\n"
            f"3/4 : {self.out['3/4']},\r\n"
            f"1/2 : {self.out['1/2']},\r\n"
            f"1/4 : {self.out['1/4']},\r\n"
        )

    def simplified(self):
        return (
            f"{self.name}    "
            f"({self.ins['1']},{self.ins['3/4']},{self.ins['1/2']},{self.ins['1/4']})   "
            f"({self.out['1']},{self.out['3/4']},{self.out['1/2']},{self.out['1/4']})"
        )

    def add_user(self, simplified):
        self.results += simplified + self.newline

    def full_decription(self):
        return "\r\nNICK, FRONT, ZAPLECZE\r\n" f"{self.results}"

    def text(self):
        return str(
            "Uwaga 1, Pełny off to 20k, 3/4 to 15k itd.\r\n"
            + "Uwaga 2, np. -500 jednostek poza wioską to nie błąd,"
            + " oznacza to że gracz ma 500 nie swoich toporników w "
            + "wiosce LUB inne takie sytuacje!\r\n"
            + "WOJSKA POZA WIOSKĄ = WSZYSTKIE WŁASNE"
            + " - WSZYSTKIE W WIOSCE\r\n"
            + self.full_text()
            + self.full_decription()
        )


class DeffException(Exception):
    pass


class NewDeffText:
    def __init__(self):
        self.users = {}

    def add_back_village(self, user, deff_instance, army_instance):
        if user in self.users:
            self.users[user].add_back_village(deff_instance, army_instance)
        else:
            self.users[user] = UserDeffInfo(user)
            self.users[user].add_back_village(deff_instance, army_instance)

    def add_front_village(self, user, deff_instance, army_instance):
        if user in self.users:
            self.users[user].add_front_village(deff_instance, army_instance)
        else:
            self.users[user] = UserDeffInfo(user)
            self.users[user].add_front_village(deff_instance, army_instance)

    def __str__(self):
        description = _(
            "Tested. LEGEND: \r\n"
            "HEAVY counted as x4 and not x6, scouts are NOT counted.\r\n"
            "IN VILLAGES = troops in the village + everyone else's troops.\r\n"
            "ALL OWN = troops in the village + troops outside the village.\r\n\r\n"
        )
        text = ""
        for user_info in self.users.values():
            description += user_info.user_description()
            text += str(user_info)
        return description + text


class UserDeffInfo:
    def __init__(self, username: str):
        self.name = username
        self.back_villages = 0
        self.front_villages = 0
        self.sumary_info = {
            "player_back_deff_inside": 0,
            "player_back_deff_own": 0,
            "player_front_deff_inside": 0,
            "player_front_deff_own": 0,
        }
        self.player_back_villages = []
        self.player_front_villages = []

    def user_description(self):
        on_front = _("On front")
        villages = _("villages,")
        deff_inside = _("deff IN VILLAGE and")
        all_own = _("ALL OWN")
        on_back = _("On back")
        return (
            f"\r\n{self.name}\r\n"
            f"{on_front} {self.front_villages} {villages} "
            f"{self.sumary_info['player_front_deff_inside']} "
            f"{deff_inside}"
            f" {self.sumary_info['player_front_deff_own']} "
            f"{all_own}.\r\n"
            f"{on_back} {self.back_villages} {villages} "
            f"{self.sumary_info['player_back_deff_inside']} "
            f"{deff_inside}"
            f" {self.sumary_info['player_back_deff_own']} "
            f"{all_own}.\r\n"
        )

    def add_back_village(self, deff_instance, army_instance):
        self.back_villages += 1
        coord = deff_instance.coord
        inside_army = deff_instance.deff
        if army_instance is not None:
            own_army = army_instance.deff
            self.sumary_info["player_back_deff_own"] += own_army
        else:
            own_army = _("No preview")

        village_info_object = VillageDeffInfo(coord, own_army, inside_army)
        self.player_back_villages.append(village_info_object)
        self.sumary_info["player_back_deff_inside"] += inside_army

    def add_front_village(self, deff_instance, army_instance):
        self.front_villages += 1
        coord = deff_instance.coord
        inside_army = deff_instance.deff
        if army_instance is not None:
            own_army = army_instance.deff
            self.sumary_info["player_front_deff_own"] += own_army
        else:
            own_army = _("No preview")

        village_info_object = VillageDeffInfo(coord, own_army, inside_army)
        self.player_front_villages.append(village_info_object)
        self.sumary_info["player_front_deff_inside"] += inside_army

    def __str__(self):
        text = "\r\n\r\n" + self.name + "\r\n---------FRONT---------" + "\r\n"
        for village_info in self.player_front_villages:
            text += str(village_info)
        text += _("---------BACK---------") + "\r\n"
        for village_info in self.player_back_villages:
            text += str(village_info)
        return text


class VillageDeffInfo:
    def __init__(self, coord, own_army, inside_army):
        self.coord = coord
        self.own_army = own_army
        self.inside_army = inside_army

    def __str__(self):
        inside = _("- In village- ")
        all_troops = _("(All deff")
        return (
            f"{self.coord}{inside}{self.inside_army}  "
            f"{all_troops} [ {self.own_army} ])\r\n"
        )
