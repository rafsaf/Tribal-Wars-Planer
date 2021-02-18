import tribal_wars.basic as basic
import base.models as models


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
            army = basic.Army(line, self.evidence)
            army.player = self.village_dictionary[army.coord]
            army.first_line = False
            yield army

