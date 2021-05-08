from typing import Dict, List
from base.models import Outline, TargetVertex as Target
import tribal_wars.basic as basic


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
        self.target_text: List[str] = []
        self.village_dict: Dict[str, str] = {}

    def _fill_target_text(self) -> None:
        if self.target_mode.is_fake:
            text: str = self.outline.initial_outline_fakes
        elif self.target_mode.is_real:
            text: str = self.outline.initial_outline_targets
        else:
            text: str = self.outline.initial_outline_ruins
        self.target_text = text.split("\r\n")

    def _player(self, coord: str) -> str:
        """Return player name"""
        return self.village_dict[coord]

    def __call__(self) -> None:
        Target.objects.filter(
            outline=self.outline,
            fake=self.target_mode.is_fake,
            ruin=self.target_mode.is_ruin,
        ).delete()

        self._fill_target_text()
        if self.target_text == [""]:
            return None

        self._fill_village_dict()
        targets: List[Target] = []

        line: str
        for line in self.target_text:
            line_list: List[str] = line.split(":")

            if line_list[1].isnumeric():
                required_off: str = line_list[1]
                exact_off: List[str] = list()
            else:
                required_off: str = "0"
                exact_off: List[str] = line_list[1].split("|")

            if line_list[2].isnumeric():
                required_noble: str = line_list[2]
                exact_noble: List[str] = list()
            else:
                required_noble: str = "0"
                exact_noble: List[str] = line_list[2].split("|")

            targets.append(
                self._target(
                    coord=line_list[0],
                    off=required_off,
                    noble=required_noble,
                    exact_off=exact_off,
                    exact_noble=exact_noble,
                )
            )
        Target.objects.bulk_create(targets, batch_size=500)

    def _target(
        self,
        coord: str,
        off: str,
        noble: str,
        exact_off: List[str],
        exact_noble: List[str],
    ) -> Target:

        target: Target = Target(
            outline=self.outline,
            target=coord,
            fake=self.target_mode.is_fake,
            ruin=self.target_mode.is_ruin,
            player=self._player(coord),
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
        """Create a dictionary with player names"""

        coords: List[str] = [line.split(":")[0] for line in self.target_text]
        village_long_str: str = " ".join(coords)

        self.village_dict = basic.coord_to_player_from_string(
            village_coord_list=village_long_str, world=self.outline.world
        )
