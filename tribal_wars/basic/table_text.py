import datetime
from base import models


class TableText:
    def __init__(self, world_num: int):
        self.__next_line = "\r\n"
        self.__next_line_double = "\r\n\r\n"
        self.__prefix = (
            "[table][**]NR[||]WYŚLIJ[||]OFF[||]GRUBE[||]WYSYŁKA[||]WEJŚCIE[||]Z WIOSKI[||]CEL[/**]"
        )
        self.__postfix = "[/table]"
        self.result = {}
        self.table_result = {}
        self.string_result = {}
        self.weight_table = {}
        self.weight_string = {}
        self.world = world_num
        world_instance = models.World.objects.get(world=self.world)
        if world_instance.classic:
            self.name_prefix = 'cl'
        else:
            self.name_prefix = 'pl'

    def __link(self, ally_village_id, enemy_village_id):
        return (
            f"[url=https://{self.name_prefix}{self.world}.plemiona.pl/game.php?"
            f"village={ally_village_id}&screen=place&"
            f"target={enemy_village_id}]Wyślij[/url]"
        )

    def __date_table(self, datetime1, datetime2):
        date_part = datetime1.date()

        t1_part = datetime1.time()
        t2_part = datetime2.time()

        return (
            f'{date_part}'
            f'\n'
            f'[b][color=#00a500]{t1_part}[/color][/b]-'
            f'[b][color=#ff0000]{t2_part}[/color][/b]'
        )

    def __date_string(self, datetime1, datetime2):
        date_part = datetime1.date()

        t1_part = datetime1.time()
        t2_part = datetime2.time()

        return (
            f"dnia {date_part} od {t1_part} "
            f"do {t2_part}."
        ) 

    def __weight_table(self, weight: models.WeightModel, ally_id, enemy_id):
        return (
            f"[|]{self.__link(ally_id, enemy_id)}"
            f"[|]{weight.off}[|]{weight.nobleman}"
            f"[|]{self.__date_table(weight.sh_t1, weight.sh_t2)}"
            f"[|]{self.__date_table(weight.t1, weight.t2)}"
            f"[|][coord]{weight.start}[/coord][|][coord]{weight.target.target}[/coord]"
        )

    def __weight_string(self, weight: models.WeightModel, ally_id, enemy_id):
        return (
            f"Wyślij atak (Off-{weight.off}, Grubych-{weight.nobleman}) "
            f"z wioski {weight.start} na wioskę {weight.target.target} "
            f"{self.__date_string(weight.sh_t1, weight.sh_t2)}\n"
            f"{self.__link(ally_id, enemy_id)}"
        )

    def add_weight(self, weight: models.WeightModel, ally_id, enemy_id):
        
        self.weight_table[weight] = str(
            self.__weight_table(weight, ally_id, enemy_id)
        )

        self.weight_string[weight] = str(
            self.__weight_string(weight, ally_id, enemy_id)
        )
        try:
            self.result[weight.player].append(weight)

        except KeyError:
            self.result[weight.player] = [weight]

    def __sort_weights(self):
        for lst in self.result.values():
            lst.sort(key=lambda weight: (weight.sh_t1, weight.start, weight.target.target))
            
    def __create_table(self):
        for player, lst in self.result.items():
            table = str(
                self.__next_line
                + player
                + self.__next_line
                + self.__prefix
            )
            for i, weight in enumerate(lst):
                table += f"[*]{i+1}" + self.weight_table[weight]
            
            table += self.__postfix
            self.table_result[player] = table

    def __create_string(self):
        for player, lst in self.result.items():
            text = str(
                self.__next_line
                + player
                + self.__next_line
            )
            for i, weight in enumerate(lst):
                text += f"{i+1}. " + self.weight_string[weight] + self.__next_line_double

            self.string_result[player] = text

    def get_full_result(self):
        return self.__next_line_double.join(self.table_result.values())

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.__sort_weights()
        self.__create_table()
        self.__create_string()

    def iterate_over(self):
        for player in self.result:
            yield (player, self.table_result[player], self.string_result[player])
