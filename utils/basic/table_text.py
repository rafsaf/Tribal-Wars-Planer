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
from collections import defaultdict

from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy

from base import models
from base.models.weight_model import WeightModel


class TableText:
    NEXT_LINE = "\r\n"
    NEXT_LINE_DOUBLE = "\r\n\r\n"
    POSTFIX = "[/table]"
    WEEKDAY_PAUZES = "-" * 16
    WEEKDAYS = {
        0: gettext_lazy("Monday"),
        1: gettext_lazy("Tuesday"),
        2: gettext_lazy("Wednesday"),
        3: gettext_lazy("Thursday"),
        4: gettext_lazy("Friday"),
        5: gettext_lazy("Saturday"),
        6: gettext_lazy("Sunday"),
    }

    def __init__(self, outline: models.Outline):
        self.PREFIX = _(
            "[table][**][||]SEND[||]OFF[||]NOBLE[||]SENDING[||]ENTER[||]FROM[||]TARGET[/**]"
        )
        self.result: defaultdict[str, list[WeightModel]] = defaultdict(list)
        self.table_result = {}
        self.string_result = {}
        self.deputy_result = {}
        self.extended_result = {}
        self.new_extended_result = {}

        self.weight_table = {}
        self.weight_string = {}
        self.weight_string = {}
        self.weight_deputy = {}
        self.weight_extended = {}
        self.new_weight_extended = {}

        self.world = outline.world
        self.outline = outline
        self.weights: defaultdict[str, list[WeightModel]] = defaultdict(list)

    def create_weights(self, weight_lst: list[WeightModel]):
        for weight in weight_lst:
            self.weights[weight.start].append(weight)
        for weights in self.weights.values():
            weights.sort(key=lambda weight: weight.sh_t1)

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

    def __new_weight_string(
        self,
        weight: models.WeightModel,
        ally_id,
        enemy_id,
        fake,
        deputy=None,
    ):
        if deputy is not None:
            deputy_link_part = f"&t={deputy}"
        else:
            deputy_link_part = ""

        data = {
            "noble_number": weight.nobleman,
            "off_number": weight.off,
            "catapults_number": weight.catapult,
            "date": self.__date_string(weight.sh_t1, weight.sh_t2),
            "start_coord": weight.start,
            "target_coord": weight.target.target,
            "game_url": self.world.link_to_game(),
            "ally_id": ally_id,
            "enemy_id": enemy_id,
            "deputy_link_part": deputy_link_part,
            "building": weight.get_building_display().upper()
            if weight.building
            else None,
        }
        if fake and weight.nobleman > 0:
            all_weights_from_this_village = [
                w
                for w in self.weights[weight.start]
                if w.target.fake and weight.nobleman > 0
            ]
            data["weight_count"] = all_weights_from_this_village.index(weight) + 1
            data["weight_count_all"] = len(all_weights_from_this_village)
            return (
                _(
                    "[b][color=#00a500]Send FAKE NOBLE[%(noble_number)s noble][/color] (%(weight_count)s of %(weight_count_all)s)[/b]\r\n"
                    "%(date)s\r\n"
                    "%(start_coord)s [b]->[/b] %(target_coord)s\r\n"
                    "[url=%(game_url)s/game.php?"
                    "village=%(ally_id)s&screen=place&"
                    "target=%(enemy_id)s%(deputy_link_part)s]Send FAKE NOBLE[/url]"
                )
                % data
            )
        elif fake and weight.nobleman == 0:
            all_weights_from_this_village = [
                w
                for w in self.weights[weight.start]
                if w.target.fake and weight.nobleman == 0
            ]
            data["weight_count"] = all_weights_from_this_village.index(weight) + 1
            data["weight_count_all"] = len(all_weights_from_this_village)
            return (
                _(
                    "[b][color=#00a500]Send FAKE[%(off_number)s off][/color] (%(weight_count)s of %(weight_count_all)s)[/b]\r\n"
                    "%(date)s\r\n"
                    "%(start_coord)s [b]->[/b] %(target_coord)s\r\n"
                    "[url=%(game_url)s/game.php?"
                    "village=%(ally_id)s&screen=place&"
                    "target=%(enemy_id)s%(deputy_link_part)s]Send FAKE[/url]"
                )
                % data
            )
        elif weight.ruin:
            all_weights_from_this_village = [
                w for w in self.weights[weight.start] if w.ruin
            ]
            data["weight_count"] = all_weights_from_this_village.index(weight) + 1
            data["weight_count_all"] = len(all_weights_from_this_village)
            return (
                _(
                    "[b][color=#0e0eff]Send RUIN[%(catapults_number)sc on %(building)s][/color] "
                    "(%(weight_count)s of %(weight_count_all)s)[/b]\r\n"
                    "%(date)s\r\n"
                    "%(start_coord)s [b]->[/b] %(target_coord)s\r\n"
                    "[url=%(game_url)s/game.php?"
                    "village=%(ally_id)s&screen=place&"
                    "target=%(enemy_id)s%(deputy_link_part)s]Send RUIN[/url]"
                )
                % data
            )
        elif weight.nobleman > 0:
            all_weights_from_this_village = [
                w
                for w in self.weights[weight.start]
                if not w.ruin and not w.target.fake and w.nobleman > 0
            ]
            data["weight_count"] = all_weights_from_this_village.index(weight) + 1
            data["weight_count_all"] = len(all_weights_from_this_village)
            return (
                _(
                    "[b][color=#a500a5]Send NOBLE[%(off_number)s off + %(noble_number)s noble][/color] "
                    "(%(weight_count)s of %(weight_count_all)s)[/b]\r\n"
                    "%(date)s\r\n"
                    "%(start_coord)s [b]->[/b] %(target_coord)s\r\n"
                    "[url=%(game_url)s/game.php?"
                    "village=%(ally_id)s&screen=place&"
                    "target=%(enemy_id)s%(deputy_link_part)s]Send NOBLE[/url]"
                )
                % data
            )
        else:
            all_weights_from_this_village = [
                w
                for w in self.weights[weight.start]
                if not w.ruin and not w.target.fake and w.nobleman == 0
            ]
            data["weight_count"] = all_weights_from_this_village.index(weight) + 1
            data["weight_count_all"] = len(all_weights_from_this_village)
            return (
                _(
                    "[b][color=#a50000]Send OFF[%(off_number)s off][/color] "
                    "(%(weight_count)s of %(weight_count_all)s)[/b]\r\n"
                    "%(date)s\r\n"
                    "%(start_coord)s [b]->[/b] %(target_coord)s\r\n"
                    "[url=%(game_url)s/game.php?"
                    "village=%(ally_id)s&screen=place&"
                    "target=%(enemy_id)s%(deputy_link_part)s]Send OFF[/url]"
                )
                % data
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
                building = "[b]" + weight.get_building_display() + "[/b]"
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

        self.new_weight_extended[weight] = str(
            self.__new_weight_string(weight, ally_id, enemy_id, fake)
        )

        self.weight_deputy[weight] = str(
            self.__new_weight_string(weight, ally_id, enemy_id, fake, deputy=deputy)
        )

        self.result[weight.player].append(weight)

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
            day_split_used: set[str] = set()
            text = str(self.NEXT_LINE + self.NEXT_LINE)
            for i, weight in enumerate(lst):
                date = str(weight.sh_t1.date())
                if date not in day_split_used:
                    day_split_used.add(date)
                    text += (
                        "[b]"
                        + self.WEEKDAY_PAUZES
                        + date
                        + f" ({self.WEEKDAYS[weight.sh_t1.weekday()]})"
                        + self.WEEKDAY_PAUZES
                        + "[/b]"
                        + self.NEXT_LINE
                    )
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

    def __create_new_extended(self):
        for player, lst in self.result.items():
            day_split_used: set[str] = set()
            text = str(self.NEXT_LINE + self.NEXT_LINE)
            for i, weight in enumerate(lst):
                date = str(weight.sh_t1.date())
                if date not in day_split_used:
                    day_split_used.add(date)
                    text += (
                        "[b]"
                        + self.WEEKDAY_PAUZES
                        + date
                        + f" ({self.WEEKDAYS[weight.sh_t1.weekday()]})"
                        + self.WEEKDAY_PAUZES
                        + "[/b]"
                        + self.NEXT_LINE
                    )
                text += (
                    f"{i + 1}. "
                    + self.new_weight_extended[weight]
                    + self.NEXT_LINE_DOUBLE
                )

            self.new_extended_result[player] = text

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
        self.__create_new_extended()

    def iterate_over(self):
        for player in self.result:
            yield (
                player,
                self.table_result[player],
                self.string_result[player],
                self.deputy_result[player],
                self.extended_result[player],
                self.new_extended_result[player],
            )
