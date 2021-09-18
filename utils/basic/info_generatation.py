from typing import Dict, List, Tuple

from django.db.models.query import QuerySet
from django.utils.translation import gettext as _

from base import models
from utils import basic


class OutlineInfo:
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
        self.world_evidence: Tuple[int, int, int] = basic.world_evidence(
            self.outline.world
        )

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

    def add_target_info(self, line: str, target_type: str) -> None:
        if target_type == "real":
            self.target_message += line
        elif target_type == "fake":
            self.fake_message += line
        else:
            self.ruin_message += line

    def show_sum_up(self):
        return (
            self.target_message
            + "\r\n\r\n"
            + self.fake_message
            + "\r\n\r\n"
            + self.ruin_message
        )

    @staticmethod
    def parse_weight_to_army_line(
        weight_max: models.WeightMaximum,
        line_lst: List[str],
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
        evidence_dictionary: Dict[Tuple[int, int, int], int] = {
            (1, 1, 1): 16,
            (1, 1, 0): 15,
            (0, 1, 1): 15,
            (1, 0, 1): 14,
            (1, 0, 0): 13,
            (0, 0, 1): 13,
            (0, 1, 0): 14,
            (0, 0, 0): 12,
        }
        line_length: int = evidence_dictionary[self.world_evidence]

        line_lst: List[str] = ["0," for _ in range(line_length)]

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
        self, target: models.TargetVertex, weight_lst: QuerySet["models.WeightModel"]
    ) -> None:
        self.target: models.TargetVertex = target
        self.weight_lst: QuerySet["models.WeightModel"] = weight_lst

    @property
    def line(self) -> str:
        if self.target.fake:
            fakes_string: str = _("fakes")
            fake_nobles_string: str = _("fake nobles")

            fakes: int = len(
                [weight for weight in self.weight_lst if weight.nobleman == 0]
            )
            fake_nobles: int = 0
            weight: models.WeightModel
            for weight in self.weight_lst:
                fake_nobles += weight.nobleman
            return f"\r\n{self.target.target} - {fakes} {fakes_string} - {fake_nobles} {fake_nobles_string}"

        if self.target.ruin:
            offs_string: str = _("offs")
            ruins_string: str = _("ruins")

            ruins: int = len([weight for weight in self.weight_lst if weight.ruin])
            offs: int = len(self.weight_lst) - ruins
            return f"\r\n{self.target.target} - {offs} {offs_string} - {ruins} {ruins_string}"

        else:
            offs_string: str = _("offs")
            nobles_string: str = _("nobles")

            offs: int = len(
                [weight for weight in self.weight_lst if weight.nobleman == 0]
            )
            nobles: int = 0
            weight: models.WeightModel
            for weight in self.weight_lst:
                nobles += weight.nobleman

            return f"\r\n{self.target.target} - {offs} {offs_string} - {nobles} {nobles_string}"

    @property
    def target_type(self) -> str:
        if self.target.fake:
            return "fake"
        elif self.target.ruin:
            return "ruin"
        else:
            return "real"
