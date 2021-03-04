import tribal_wars.basic as basic
import base.models as models


class ExtendedArmy(basic.Army):
    def __init__(self, text_army: str, evidence):
        super().__init__(text_army, evidence)
        self.player: str = "player_name"

    def set_player(self, player: str) -> None:
        self.player = player


class OffTroops:
    """
    Helps iterating over user's off_troops from script

    yields extended Army instance."""

    def __init__(self, outline: models.Outline):
        self.outline = outline
        self.evidence = basic.world_evidence(world=outline.world)
        self.village_dictionary = basic.coord_to_player(outline=outline)
        self.off_troops = self.outline.off_troops.split("\r\n")

    def __iter__(self):
        for line in self.off_troops:
            army = ExtendedArmy(line, self.evidence)
            player = self.village_dictionary[army.coord]
            army.set_player(player=player)
            yield army
