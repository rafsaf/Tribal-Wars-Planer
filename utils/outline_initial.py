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


import utils.basic as basic
from base import models
from base.models import Outline, WeightMaximum
from utils.basic import Army


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
        self.evidence = basic.world_evidence(world=outline.world)
        self.village_dictionary: dict[str, str] = basic.coord_to_player(outline=outline)
        self.village_points_dictionary = basic.coord_to_player_points(outline=outline)
        self.off_troops: list[str] = self.outline.off_troops.split("\r\n")
        self.weight_max_create_list: list[WeightMaximum] = []

    def __call__(self) -> None:
        WeightMaximum.objects.filter(outline=self.outline).delete()
        line: str
        for line in self.off_troops:
            army: Army = Army(line, self.evidence)
            player_name: str = self.village_dictionary[army.coord]
            points: int = self.village_points_dictionary[army.coord]
            self._add_weight_max(army=army, player=player_name, points=points)
        WeightMaximum.objects.bulk_create(self.weight_max_create_list)
        self.outline.avaiable_offs = []
        self.outline.avaiable_offs_near = []
        self.outline.avaiable_nobles = []
        self.outline.avaiable_nobles_near = []
        self.outline.avaiable_ruins = None
        self.outline.off_troops_weightmodels_hash = (
            self.outline.get_or_set_off_troops_hash()
        )
        self.outline.save()

    def _add_weight_max(self, army: Army, player: str, points: int) -> None:
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
                points=points,
            )
        )
