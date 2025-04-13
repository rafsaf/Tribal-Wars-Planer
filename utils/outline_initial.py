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


from base import models
from base.models import Outline, WeightMaximum
from base.models.village_model import VillageModel
from utils import basic
from utils.basic import Army, Defence


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

        self.villages_map: dict[str, VillageModel] = {}
        self.weight_max_create_list: list[WeightMaximum] = []

        self._fill_villages_map()

    def __call__(self) -> None:
        WeightMaximum.objects.filter(outline=self.outline).delete()
        if self.outline.input_data_type == models.Outline.ARMY_COLLECTION:
            for line in self.outline.off_troops.split("\r\n"):
                army = Army(line, self.evidence)
                self._add_weight_max(army=army, village=self.villages_map[army.coord])
            self.outline.off_troops_weightmodels_hash = (
                self.outline.get_or_set_off_troops_hash()
            )
        else:
            current_coord = ""
            for line in self.outline.deff_troops.split("\r\n"):
                army = Defence(line, self.evidence)
                if army.coord == current_coord:
                    # we dont want to create weight max from enroute troops
                    self.outline.deff_collection_text_enroute = (
                        army.deff_collection_text
                    )
                    continue
                else:
                    current_coord = army.coord
                    self.outline.deff_collection_text_in_village = (
                        army.deff_collection_text
                    )

                self._add_weight_max(army=army, village=self.villages_map[army.coord])
            self.outline.deff_troops_weightmodels_hash = (
                self.outline.get_or_set_deff_troops_hash()
            )
        WeightMaximum.objects.bulk_create(self.weight_max_create_list)
        self.outline.avaiable_offs = []
        self.outline.avaiable_offs_near = []
        self.outline.avaiable_nobles = []
        self.outline.avaiable_nobles_near = []
        self.outline.available_catapults = []
        self.outline.avaiable_ruins = None
        self.outline.save(
            update_fields=[
                "avaiable_nobles_near",
                "avaiable_offs_near",
                "avaiable_nobles",
                "avaiable_offs",
                "available_catapults",
                "avaiable_ruins",
                "off_troops_weightmodels_hash",
                "deff_troops_weightmodels_hash",
                "deff_collection_text_in_village",
                "deff_collection_text_enroute",
            ]
        )

    def _add_weight_max(self, army: Army | Defence, village: VillageModel) -> None:
        if village.player is None:
            raise RuntimeError(
                "unexpected None player in outline %s village %s for %s",
                self.outline,
                village,
                army.coord,
            )

        self.weight_max_create_list.append(
            WeightMaximum(
                outline=self.outline,
                player=village.player.name,
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
                points=village.player.points,
                player_id=village.player.player_id,
                village_id=village.village_id,
            )
        )

    def _fill_villages_map(self) -> None:
        villages = (
            VillageModel.objects.select_related("player")
            .filter(
                player__tribe__tag__in=self.outline.ally_tribe_tag,
                world=self.outline.world,
            )
            .only(
                "coord",
                "village_id",
                "player__name",
                "player__points",
                "player__player_id",
            )
        )

        self.villages_map = {village.coord: village for village in villages}
