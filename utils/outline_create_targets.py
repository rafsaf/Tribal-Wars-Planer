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


from django.utils.timezone import now

from base.models import Outline, TargetVertex
from base.models.village_model import VillageModel
from utils import basic


class OutlineCreateTargets:
    """
    WE ASSUME DATA IS ALREADY UP-TO-DATE AND SYNTAX IS VALID

    For given target type target_mode (real, fake, ruin)

    1. Firstly deletes old targets of given type

    2. Then forloop user's input from outline.initial_outline_(fakes or targets or ruin)
        For every line creates suitable Target

    3. Finally bulk_create Targets
    """

    def __init__(self, outline: Outline, target_mode: basic.TargetMode) -> None:
        self.outline: Outline = outline
        self.target_mode: basic.TargetMode = target_mode
        self.target_text: list[str] = []
        self.villages_map: dict[str, VillageModel] = {}

    def _fill_target_text(self) -> None:
        if self.target_mode.is_fake:
            text: str = self.outline.initial_outline_fakes
        elif self.target_mode.is_real:
            text = self.outline.initial_outline_targets
        else:
            text = self.outline.initial_outline_ruins
        self.target_text = text.split("\r\n")

    def __call__(self) -> None:
        TargetVertex.objects.filter(
            outline=self.outline,
            fake=self.target_mode.is_fake,
            ruin=self.target_mode.is_ruin,
        ).delete()

        self._fill_target_text()
        if self.target_text == [""]:
            return None

        self._fill_villages_map()
        targets: list[TargetVertex] = []

        line: str
        for line in self.target_text:
            line_list: list[str] = line.split(":")

            if line_list[1].isnumeric():
                required_off: str = line_list[1]
                exact_off: list[str] = []
            else:
                required_off = "0"
                exact_off = line_list[1].split("|")

            if line_list[2].isnumeric():
                required_noble: str = line_list[2]
                exact_noble: list[str] = []
            else:
                required_noble = "0"
                exact_noble = line_list[2].split("|")

            targets.append(
                self._target(
                    coord=line_list[0],
                    off=required_off,
                    noble=required_noble,
                    exact_off=exact_off,
                    exact_noble=exact_noble,
                )
            )
        TargetVertex.objects.bulk_create(targets, batch_size=2000)

    def _target(
        self,
        coord: str,
        off: str,
        noble: str,
        exact_off: list[str],
        exact_noble: list[str],
    ) -> TargetVertex:
        village = self.villages_map[coord]
        target = TargetVertex(
            outline=self.outline,
            target=coord,
            fake=self.target_mode.is_fake,
            ruin=self.target_mode.is_ruin,
            player=village.player.name if village.player else "",
            points=village.player.points if village.player else 0,
            player_created_at=village.player.created_at if village.player else now(),
            player_id=village.player.player_id if village.player else None,
            village_id=village.village_id,
            required_off=off,
            required_noble=noble,
            exact_off=exact_off,
            exact_noble=exact_noble,
            mode_off=self.outline.mode_off,
            mode_noble=self.outline.mode_noble,
            mode_division=self.outline.mode_division,
            mode_guide=self.outline.mode_guide,
            night_bonus=self.outline.night_bonus,
            enter_t1=self.outline.enter_t1,
            enter_t2=self.outline.enter_t2,
        )
        return target

    def _fill_villages_map(self) -> None:
        """Create a dictionary with player models"""

        coords: list[str] = [line.split(":")[0] for line in self.target_text]

        villages = (
            VillageModel.objects.select_related("player")
            .filter(world=self.outline.world, coord__in=coords)
            .only(
                "coord",
                "village_id",
                "player__name",
                "player__points",
                "player__created_at",
                "player__player_id",
            )
        )

        self.villages_map = {village.coord: village for village in villages}
