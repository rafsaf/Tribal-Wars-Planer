import datetime
from base import models


class TableText:
    def __init__(self, world_num: int):
        self.__next_line = "\r\n"
        self.__next_line_double = "\r\n\r\n"
        self.__prefix = (
            "[table][**]WYŚLIJ[||]OFF[||]GRUBE[||]WYSYŁKA[||]WEJŚCIE[||]Z WIOSKI[||]CEL[/**]"
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

    def __data_color_column(self, datetime1: datetime.datetime, datetime2:datetime.datetime):
        date_part = datetime1.date()

        t1_part = datetime1.time()
        t2_part = datetime2.time()

        return (
            f'{date_part}'
            f'\n'
            f'[b][color=#00a500]{t1_part}[/color][/b]-'
            f'[b][color=#ff0000]{t2_part}[/color][/b]'
        )

    def __weight_string(self, weight: models.WeightModel, ally_id, enemy_id):
        return (
            f"[*][url={self.__link(self.world, ally_id, enemy_id)}]Wyślij[/url]"
            f"[|]{weight.off}[|]{weight.nobleman}"
            f"[|]{self.__data_color_column(weight.sh_t1, weight.sh_t2)}"
            f"[|]{self.__data_color_column(weight.t1, weight.t2)}"
            f"[|][coord]{weight.start}[/coord][|][coord]{weight.target.target}[/coord]"
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
