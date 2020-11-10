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
        description = (
            "Przetestowane. LEGENDA:\r\n"
            "CK liczone jako x4 a nie x6, zwiad NIE jest liczony.\r\n"
            "W WIOSKACH = swój w wiosce + cudzy z stałych.\r\n"
            "CAŁY SWÓJ = swój w wiosce + swój poza wioską.\r\n\r\n"
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
        return (
            f"\r\n{self.name}\r\n"
            f"Na froncie {self.front_villages} wsi, "
            f"{self.sumary_info['player_front_deff_inside']} "
            f"deffa W WIOSKACH, "
            f"zaś {self.sumary_info['player_front_deff_own']} "
            "CAŁEGO SWOJEGO.\r\n"
            f"Na zapleczu {self.back_villages} wsi, "
            f"{self.sumary_info['player_back_deff_inside']} "
            f"deffa W WIOSKACH, "
            f"zaś {self.sumary_info['player_back_deff_own']} "
            f"CAŁEGO SWOJEGO.\r\n"
        )

    def add_back_village(self, deff_instance, army_instance):
        self.back_villages += 1
        coord = deff_instance.coord
        inside_army = deff_instance.deff
        if army_instance is not None:
            own_army = army_instance.deff
            self.sumary_info["player_back_deff_own"] += own_army
        else:
            own_army = "brak podglądu"

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
            own_army = "brak podglądu"

        village_info_object = VillageDeffInfo(coord, own_army, inside_army)
        self.player_front_villages.append(village_info_object)
        self.sumary_info["player_front_deff_inside"] += inside_army

    def __str__(self):
        text = "\r\n\r\n" + self.name + "\r\n---------FRONT---------" + "\r\n"
        for village_info in self.player_front_villages:
            text += str(village_info)
        text += "---------ZAPLECZE---------" + "\r\n"
        for village_info in self.player_back_villages:
            text += str(village_info)
        return text


class VillageDeffInfo:
    def __init__(self, coord, own_army, inside_army):
        self.coord = coord
        self.own_army = own_army
        self.inside_army = inside_army

    def __str__(self):
        return (
            f"{self.coord}- W wiosce- {self.inside_army}  "
            f"(CAŁY własny deff [ {self.own_army} ])\r\n"
        )
