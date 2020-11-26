from base import models
from tribal_wars import basic


class TargetsGeneralInput:
    """ class with methods on user input targets """

    def __init__(self, outline_targets: str, world: int, outline: models.Outline, fake=False):
        self.outline = outline
        self.fake = fake
        
        self.targets = []
        self.target_text = outline_targets.split("\r\n")
        if not self.target_text == ['']:
            self.village_dict = self.target_village_dictionary(world=world)

    def player(self, coord):
        """ Return player name  """
        return self.village_dict[coord]

    def generate_targets(self):
        if not self.target_text == ['']:
            for line in self.target_text:
                line = line.split(":")
                self.targets.append(
                    models.TargetVertex(
                        outline=self.outline,
                        target=line[0],
                        fake=self.fake,
                        player=self.player(line[0]),
                        required_off=line[1],
                        required_noble=line[2],
                        mode_off=self.outline.mode_off,
                        mode_noble=self.outline.mode_noble,
                        mode_division=self.outline.mode_division,
                        mode_guide=self.outline.mode_guide,
                    )
                )

    def target_village_dictionary(self, world):
        """ Create a dictionary with player names """
        coords = [line.split(":")[0] for line in self.target_text]
        village_long_str = " ".join(coords)

        result_dict = basic.coord_to_player_from_string(
            village_coord_list=village_long_str, world=world
        )
        return result_dict

