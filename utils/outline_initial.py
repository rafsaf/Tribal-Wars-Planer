from typing import Dict, List, Tuple
from base import models
from utils.basic import Army
from base.models import Outline, WeightMaximum

import utils.basic as basic
import base.models as models


class MakeOutline:
    """
    The first and basic step in every oultine

    ASSUMES THAT DATA ARE UP-TO-DATE!

    Iterates over army troops for given outline,
    calculates offs, nobles etc. for every line, then create WeightMaximum object

    Finally bulk_create given list with WeightMaximums
    """

    def __init__(self, outline: models.Outline) -> None:
        self.outline: Outline = outline
        self.evidence: Tuple[int, int, int] = basic.world_evidence(world=outline.world)
        self.village_dictionary: Dict[str, str] = basic.coord_to_player(outline=outline)
        self.off_troops: List[str] = self.outline.off_troops.split("\r\n")
        self.weight_max_create_list: List[WeightMaximum] = []

    def __call__(self) -> None:
        WeightMaximum.objects.filter(outline=self.outline).delete()
        line: str
        for line in self.off_troops:
            army: Army = Army(line, self.evidence)
            player_name: str = self.village_dictionary[army.coord]
            self._add_weight_max(army=army, player=player_name)
        WeightMaximum.objects.bulk_create(self.weight_max_create_list)

    def _add_weight_max(self, army: Army, player: str) -> None:
        self.weight_max_create_list.append(
            WeightMaximum(
                outline=self.outline,
                player=player,
                start=army.coord,
                x_coord=int(army.coord[0:3]),
                y_coord=int(army.coord[4:7]),
                off_max=army.off,
                off_left=army.off,
                catapult_max=army.catapult,
                catapult_left=army.catapult,
                nobleman_max=army.nobleman,
                nobleman_left=army.nobleman,
                first_line=False,
                fake_limit=self.outline.initial_outline_fake_limit,
            )
        )
