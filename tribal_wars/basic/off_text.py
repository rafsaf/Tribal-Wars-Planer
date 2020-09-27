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
            + " - WSZYSTKIE W WIOSCE + WSZYSTKIE W DRODZE\r\n"
            + self.full_text()
            + self.full_decription()
        )


class NewDeffFront:
    def __init__(self, name=None):
        self.ins = 0
        self.estimated = 0
        self.villages = 0
        self.out = 0
        self.all_out = 0
        self.name = name
        self.result = ""

    def add_front(self, army, inside):
        self.ins += inside.deff
        self.estimated += army.deff
        self.villages += 1

    def add_out(self, army, inside):
        self.out += inside.deff
        self.all_out += army.deff

    def simplified(self):
        return (
            f"\r\n{self.name}\r\n"
            f"Na froncie {self.villages} wsi, łącznie {self.ins}"
            f" deffa aktualnie w wioskach,"
            f" w tym łącznie {self.estimated} to własny deff.\r\n"
            f"Na zapleczu {self.out} WOLNEGO deffa, zaś {self.all_out} CAŁEGO\r\n"
        )

    def add_user(self, text):
        self.result += text

    def get_result(self):
        text = (
            "Uwaga 1, CK liczone jako x4\r\n"
            "Uwaga 2, Łącznej ilości deffa w wioskach "
            "frontowych może być mniej niż "
            "całkowitej ilości deffa w tych wioskach, "
            "bo ktoś rozesłał wojsko itd.\r\n\r\n"
        )
        return str(text + self.result)

