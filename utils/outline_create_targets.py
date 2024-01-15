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

from base.models import Outline, Player, TargetVertex
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
        self.village_dict: dict[str, Player] = {}

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

        self._fill_village_dict()
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
        TargetVertex.objects.bulk_create(targets, batch_size=500)

    def _target(
        self,
        coord: str,
        off: str,
        noble: str,
        exact_off: list[str],
        exact_noble: list[str],
    ) -> TargetVertex:
        player = self.village_dict[coord]
        target = TargetVertex(
            outline=self.outline,
            target=coord,
            fake=self.target_mode.is_fake,
            ruin=self.target_mode.is_ruin,
            player=player.name if player else "",
            points=player.points if player else 0,
            player_created_at=player.created_at if player else now(),
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

    def _fill_village_dict(self) -> None:
        """Create a dictionary with player models"""

        coords: list[str] = [line.split(":")[0] for line in self.target_text]
        village_long_str: str = " ".join(coords)

        self.village_dict = basic.coord_to_player_model_from_string(
            village_coord_list=village_long_str, world=self.outline.world
        )
