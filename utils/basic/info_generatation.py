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

from __future__ import annotations

from django.db.models.query import QuerySet
from django.utils.translation import get_language
from django.utils.translation import gettext as _

from base import models
from utils import basic


class OutlineInfo:
    evidence_dictionary: dict[tuple[int, int, int], int] = {
        (1, 1, 1): 16,
        (1, 1, 0): 15,
        (0, 1, 1): 15,
        (1, 0, 1): 14,
        (1, 0, 0): 13,
        (0, 0, 1): 13,
        (0, 1, 0): 14,
        (0, 0, 0): 12,
    }

    def __init__(self, outline: models.Outline) -> None:
        """
        Generate basic informations about outline like targets coords
        and players nicks.
        """
        self.outline: models.Outline = outline
        self.targets: QuerySet = models.TargetVertex.objects.filter(outline=outline)
        self.target_message: str = _("Targets:") + "\r\n"
        self.fake_message: str = _("Fakes:") + "\r\n"
        self.ruin_message: str = _("Ruins:") + "\r\n"
        self.world_evidence: tuple[int, int, int] = basic.world_evidence(
            self.outline.world
        )
        self.order_counter = {
            "ruins": 0,
            "fakes": 0,
            "offs": 0,
            "nobles": 0,
        }

    def generate_nicks(self) -> str:
        result: str = _("Nicknames: ") + "\r\n\r\n"
        unique_weights = (
            models.WeightModel.objects.filter(target__outline=self.outline)
            .distinct("player")
            .values_list("player", flat=True)
        )
        counter: int = 1
        player: str
        for player in unique_weights:
            if counter == 50:
                counter = 0
                result += "\r\n\r\n"
            counter += 1
            result += f"{player};"
        return result

    def add_target_info(self, target_info: TargetCount) -> None:
        line = target_info.line_with_ally_nick
        if target_info.target_type == "real":
            self.target_message += line
        elif target_info.target_type == "fake":
            self.fake_message += line
        else:
            self.ruin_message += line

        for ruin in target_info.ally_players_ruins.values():
            self.order_counter["ruins"] += ruin
        for off in target_info.ally_players_offs.values():
            self.order_counter["offs"] += off
        for noble in target_info.ally_players_nobles.values():
            self.order_counter["nobles"] += noble
        for fake in target_info.ally_players_fakes.values():
            self.order_counter["fakes"] += fake

    def get_outline_time_text(self) -> str:
        outline_times = self.outline.get_outline_times()

        headers = [
            _("Time"),
            _("Mode"),
            _("Unit"),
            _("From"),
            _("To"),
            _("Min. time"),
            _("Max. time"),
        ]
        i = 0
        table_data = []
        for outline_time, periods in outline_times.items():
            i += 1
            for period in periods:
                unit = period.get_unit_display()  # type: ignore
                mode = period.get_status_display()  # type: ignore
                row = [
                    i,
                    mode,
                    unit,
                    period.from_number or "",
                    period.to_number or "",
                    period.from_time,
                    period.to_time,
                ]
                table_data.append(row)

        table = basic.draw_table(headers, table_data)
        return f"[code]\r\n{table}\r\n[/code]"

    def show_sum_up(self):
        sum_text = _(
            "SUM: %(offs_count)s offs, %(nobles_count)s nobles, "
            "%(ruins_count)s ruins and %(fakes_count)s fakes"
        ) % {
            "offs_count": self.order_counter["offs"],
            "nobles_count": self.order_counter["nobles"],
            "ruins_count": self.order_counter["ruins"],
            "fakes_count": self.order_counter["fakes"],
        }
        left_text = _(
            "LEFT: %(offs_count)s offs, %(nobles_count)s nobles, "
            "%(catapults_count)s catapults"
        ) % {
            "offs_count": self.outline.count_off(),
            "nobles_count": self.outline.count_noble(),
            "catapults_count": self.outline.count_catapults(),
        }
        return (
            str(self.outline)
            + "\r\n"
            + _("Date")
            + f": {self.outline.date}"
            + "\r\n"
            + sum_text
            + "\r\n"
            + left_text
            + "\r\n\r\n"
            + self.get_outline_time_text()
            + "\r\n\r\n"
            + self.target_message
            + "\r\n\r\n"
            + self.fake_message
            + "\r\n\r\n"
            + self.ruin_message
        )

    @staticmethod
    def parse_weight_to_army_line(
        weight_max: models.WeightMaximum,
        line_lst: list[str],
        noble_index: int,
        catapult_index: int,
    ) -> str:
        line_lst[0] = str(weight_max.start) + ","
        line_lst[3] = str(weight_max.off_left - weight_max.catapult_left * 8) + ","
        line_lst[noble_index] = str(weight_max.nobleman_left) + ","
        line_lst[catapult_index] = str(weight_max.catapult_left) + ","
        return "".join(line_lst)

    def show_export_troops(self) -> str:
        sum_text: str = ""
        line_length: int = self.evidence_dictionary[self.world_evidence]

        line_lst: list[str] = ["0," for _ in range(line_length)]

        catapult_index: int
        noble_index: int

        if self.world_evidence[1] == 0:
            catapult_index = 8
            if self.world_evidence[0] == 0:
                noble_index = 9
            else:
                noble_index = 10
        elif self.world_evidence[0] == 0:
            catapult_index = 10
            noble_index = 11
        else:
            catapult_index = 10
            noble_index = 12

        for weight_max in models.WeightMaximum.objects.filter(
            outline=self.outline
        ).iterator():
            sum_text += self.parse_weight_to_army_line(
                weight_max, line_lst, noble_index, catapult_index
            )
            sum_text += "\r\n"
        return sum_text


class TargetCount:
    def __init__(
        self, target: models.TargetVertex, weight_lst: list[models.WeightModel]
    ) -> None:
        self.target: models.TargetVertex = target
        self.weight_lst = weight_lst
        self.ally_players_offs = {weight.player: 0 for weight in self.weight_lst}
        self.ally_players_nobles = {player: 0 for player in self.ally_players_offs}
        self.ally_players_fakes = {player: 0 for player in self.ally_players_offs}
        self.ally_players_ruins = {player: 0 for player in self.ally_players_offs}
        lang = get_language()
        if lang == "pl":
            self.troops_shortcuts = {
                "offs": "o",
                "noble": "s",
                "ruin": "b",
                "fake": "f",
            }
        else:
            self.troops_shortcuts = {
                "offs": "o",
                "noble": "n",
                "ruin": "r",
                "fake": "f",
            }

    @property
    def line(self) -> str:
        if self.target.fake:
            fakes_string: str = _("fakes")
            fake_nobles_string: str = _("fake nobles")

            fakes = 0
            fake_nobles = 0
            for weight in self.weight_lst:
                if weight.nobleman:
                    fake_nobles += weight.nobleman
                    self.ally_players_nobles[weight.player] += weight.nobleman
                else:
                    self.ally_players_fakes[weight.player] += 1
                    fakes += 1

            return f"\r\n{self.target.target} - {fakes} {fakes_string} - {fake_nobles} {fake_nobles_string}"

        elif self.target.ruin:
            offs_string: str = _("offs")
            ruins_string: str = _("ruins")

            ruins = 0
            offs = 0
            for weight in self.weight_lst:
                if weight.ruin:
                    ruins += 1
                    self.ally_players_ruins[weight.player] += 1
                else:
                    offs += 1
                    self.ally_players_offs[weight.player] += 1

            return f"\r\n{self.target.target} - {offs} {offs_string} - {ruins} {ruins_string}"

        else:
            offs_string: str = _("offs")
            nobles_string: str = _("nobles")

            nobles = 0
            offs = 0
            for weight in self.weight_lst:
                if weight.nobleman:
                    nobles += weight.nobleman
                    self.ally_players_nobles[weight.player] += weight.nobleman
                else:
                    self.ally_players_offs[weight.player] += 1
                    offs += 1
            return f"\r\n{self.target.target} - {offs} {offs_string} - {nobles} {nobles_string}"

    @property
    def line_with_ally_nick(self):
        base_line = self.line

        ally_players_details = {player: "" for player in self.ally_players_offs}
        for player, count in self.ally_players_offs.items():
            if count:
                ally_players_details[
                    player
                ] += f"{count}{self.troops_shortcuts['offs']}"
        for player, count in self.ally_players_fakes.items():
            if count:
                ally_players_details[
                    player
                ] += f"{count}{self.troops_shortcuts['fake']}"
        for player, count in self.ally_players_nobles.items():
            if count:
                ally_players_details[
                    player
                ] += f"{count}{self.troops_shortcuts['noble']}"
        for player, count in self.ally_players_ruins.items():
            if count:
                ally_players_details[
                    player
                ] += f"{count}{self.troops_shortcuts['ruin']}"
        parse_details = ""
        for player, details in ally_players_details.items():
            parse_details += f"{player} {details}, "
        parse_details = parse_details.removesuffix(", ")
        return f"{base_line} ({parse_details})"

    @property
    def target_type(self) -> str:
        if self.target.fake:
            return "fake"
        elif self.target.ruin:
            return "ruin"
        else:
            return "real"
