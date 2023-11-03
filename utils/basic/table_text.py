# Copyright 2021 Rafał Safin (rafsaf). All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

import re

from django.utils.translation import gettext as _

from base import models


class TableText:
    NEXT_LINE = "\r\n"
    NEXT_LINE_DOUBLE = "\r\n\r\n"
    POSTFIX = "[/table]"

    def __init__(self, world: models.World):
        self.PREFIX = _(
            "[table][**][||]SEND[||]OFF[||]NOBLE[||]SENDING[||]ENTER[||]FROM[||]TARGET[/**]"
        )
        self.result = {}
        self.table_result = {}
        self.string_result = {}
        self.deputy_result = {}
        self.extended_result = {}

        self.weight_table = {}
        self.weight_string = {}
        self.weight_deputy = {}
        self.weight_extended = {}

        self.world = world

    def __link(
        self,
        ally_village_id,
        enemy_village_id,
        fake,
        ruin=False,
        deputy=None,
        noble=False,
    ):
        if deputy is not None:
            t = f"&t={deputy}"
        else:
            t = ""
        if fake:
            send = _("Send fake")
        elif ruin:
            send = _("Send ruin")
        elif not noble:
            send = _("Send OFF")
        else:
            send = _("Send NOBLE")
        return (
            f"[url={self.world.link_to_game()}/game.php?"
            f"village={ally_village_id}&screen=place&"
            f"target={enemy_village_id}{t}]{send}[/url]"
        )

    def __date_table(self, datetime1, datetime2):
        date_part = datetime1.date()

        t1_part = datetime1.time()
        t2_part = datetime2.time()

        return (
            f"{date_part}"
            f"\n"
            f"[b][color=#0e5e5e]{t1_part}[/color][/b]-"
            f"[b][color=#ff0000]{t2_part}[/color][/b]"
        )

    def __date_string(self, datetime1, datetime2):
        date_part = datetime1.date()

        t1_part = datetime1.time()
        t2_part = datetime2.time()

        return (
            f"\r\n[b]{date_part} [color=#ff0000]{t1_part} " f"- {t2_part}[/color][/b]"
        )

    def __weight_table(
        self,
        weight: models.WeightModel,
        ally_id,
        enemy_id,
        fake,
        deputy=None,
    ):
        if fake and weight.nobleman > 0:
            send = _("fake noble")
        elif fake and weight.nobleman == 0:
            send = _("fake")
        elif weight.ruin:
            send = _("Catapults-")
            if weight.building is not None:
                building = "- " + weight.get_building_display()  # type: ignore
            else:
                building = ""
            send = f"{send}{weight.catapult}{building}"
        else:
            send = f"{weight.off}"

        return (
            f"[|]{self.__link(ally_id, enemy_id, fake, weight.ruin, deputy=deputy)}"
            f"[|]{send}[|]{weight.nobleman}"
            f"[|]{self.__date_table(weight.sh_t1, weight.sh_t2)}"  # type: ignore
            f"[|]{self.__date_table(weight.t1, weight.t2)}"
            f"[|][coord]{weight.start}[/coord][|][coord]{weight.target.target}[/coord]"
        )

    def __weight_string(
        self,
        weight: models.WeightModel,
        ally_id,
        enemy_id,
        fake,
        deputy=None,
        simple=False,
    ):
        nobles = _("Nobles-")
        from_village = _("from village")
        to = _("to ")
        if fake and weight.nobleman > 0:
            text = _("[color=#00a500][b]Send fake noble[/b][/color] (1 noble)")
            send = f"{text}"
        elif fake and weight.nobleman == 0:
            text = _("[color=#00a500][b]Send fake[/b][/color]")
            send = f"{text}"
        elif weight.ruin:
            text = _("[color=#0e0eff][b]Ruin[/b][/color] (Catapults-")
            if weight.building is not None:
                building = "[b]" + weight.get_building_display() + "[/b]"  # type: ignore
            else:
                building = ""
            send = f"{text}{weight.catapult} {building})"
        else:
            if weight.nobleman == 0:
                text = _("[size=12][b]OFF[/b][/size] (Off-")
                send = f"{text}{weight.off})"
            else:
                text = _("[color=#a500a5][size=12][b]NOBLE[/b][/size][/color]")
                send = f"{text} (Off-{weight.off}, {nobles}{weight.nobleman}) "

        if simple:
            own_and_enemy_villages = ""
        else:
            own_and_enemy_villages = (
                f" {from_village} {weight.start} {to}{weight.target.target}"
            )
        return (
            f"{send}"
            f"{own_and_enemy_villages}"
            f"{self.__date_string(weight.sh_t1, weight.sh_t2)}\n"  # type: ignore
            f"{self.__link(ally_id, enemy_id, fake, weight.ruin, deputy=deputy)}"
        )

    def add_weight(
        self, weight: models.WeightModel, ally_id, enemy_id, fake, deputy=None
    ):
        self.weight_table[weight] = str(
            self.__weight_table(weight, ally_id, enemy_id, fake)
        )

        self.weight_string[weight] = str(
            self.__weight_string(weight, ally_id, enemy_id, fake, simple=True)
        )

        self.weight_extended[weight] = str(
            self.__weight_string(weight, ally_id, enemy_id, fake)
        )

        self.weight_deputy[weight] = str(
            self.__weight_string(weight, ally_id, enemy_id, fake, deputy=deputy)
        )
        try:
            self.result[weight.player].append(weight)

        except KeyError:
            self.result[weight.player] = [weight]

    def __sort_weights(self):
        for lst in self.result.values():
            lst.sort(
                key=lambda weight: (weight.sh_t1, weight.start, weight.target.target)
            )

    def __create_table(self):
        for player, lst in self.result.items():
            table = str(self.NEXT_LINE + self.NEXT_LINE + self.PREFIX)
            for i, weight in enumerate(lst):
                table += f"[*]{i + 1}" + self.weight_table[weight]
                if i % 31 == 0 and i != 0:
                    table += (
                        self.POSTFIX
                        + self.NEXT_LINE_DOUBLE
                        + self.NEXT_LINE_DOUBLE
                        + self.NEXT_LINE_DOUBLE
                        + self.PREFIX
                    )

            table += self.POSTFIX
            self.table_result[player] = table

    def __create_string(self):
        for player, lst in self.result.items():
            text = str(self.NEXT_LINE + self.NEXT_LINE)
            for i, weight in enumerate(lst):
                text += (
                    f"{i + 1}. " + self.weight_string[weight] + self.NEXT_LINE_DOUBLE
                )

            self.string_result[player] = text

    def __create_deputy(self):
        for player, lst in self.result.items():
            text = str(self.NEXT_LINE + self.NEXT_LINE)
            for i, weight in enumerate(lst):
                text += (
                    f"{i + 1}. " + self.weight_deputy[weight] + self.NEXT_LINE_DOUBLE
                )

            self.deputy_result[player] = text

    def __create_extended(self):
        for player, lst in self.result.items():
            text = str(self.NEXT_LINE + self.NEXT_LINE)
            for i, weight in enumerate(lst):
                text += (
                    f"{i + 1}. " + self.weight_extended[weight] + self.NEXT_LINE_DOUBLE
                )

            self.extended_result[player] = text

    def get_full_result(self):
        result = ""
        for player in self.string_result:
            result += player
            result += self.NEXT_LINE
            result += self.string_result[player]
            result += self.NEXT_LINE_DOUBLE
            result = re.sub(r"\[size=12\]|\[/size\]", "", result)
        return result

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.__sort_weights()
        self.__create_table()
        self.__create_string()
        self.__create_deputy()
        self.__create_extended()

    def iterate_over(self):
        for player in self.result:
            yield (
                player,
                self.table_result[player],
                self.string_result[player],
                self.deputy_result[player],
                self.extended_result[player],
            )
