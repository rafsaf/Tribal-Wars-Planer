from base import models


class TableText:
    def __init__(self, world_num: int):
        self.__next_line = "\r\n"
        self.__next_line_double = "\r\n\r\n"
        self.__prefix = (
            "[table][**]LINK[||]Z WIOSKI[||]CEL[||]PRĘDKOŚĆ"
            "[||]OFF[||]SZLACHTA[||]MIN WYSYŁKA[||]MAX WYSYŁKA"
            "[||]MIN WEJŚCIE[||]MAX WEJŚCIE[/**]"
        )
        self.__postfix = "[/table]"
        self.result = {}
        self.world = world_num

    def __link(self, world, ally_village_id, enemy_village_id):
        return (
            f"https://pl{world}.plemiona.pl/game.php?"
            f"village={ally_village_id}&screen=place&"
            f"target={enemy_village_id}"
        )

    def __weight_string(self, weight: models.WeightModel, ally_id, enemy_id):
        if weight.nobleman > 0:
            unit = "noble"
        else:
            unit = "ram"

        return (
            f"[*][url={self.__link(self.world, ally_id, enemy_id)}]Link[/url]"
            f"[|][coord]{weight.start}[/coord]"
            f"[|][coord]{weight.target.target}[/coord][|]{unit}"
            f"[|]{weight.off}[|]{weight.nobleman}[|]{weight.sh_t1}"
            f"[|]{weight.sh_t2}[|]{weight.t1}[|]{weight.t2}"
        )

    def add_weight(self, weight: models.WeightModel, ally_id, enemy_id):
        try:
            self.result[weight.player] += str(
                self.__weight_string(weight, ally_id, enemy_id)
            )

        except KeyError:
            self.result[weight.player] = str(
                weight.player
                + self.__next_line
                + self.__prefix
                + self.__weight_string(weight, ally_id, enemy_id)
            )

    def get_full_result(self):
        return self.__next_line_double.join(self.result.values())

    def result(self, player: str):
        return self.result[player]

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, exc_traceback):
        for player, text in self.result.items():
            self.result[player] = text + self.__postfix

    def __iter__(self):
        return iter(self.result.items())
