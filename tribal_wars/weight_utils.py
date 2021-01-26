import tribal_wars.basic as basic
import tribal_wars.get_deff as get_deff
import base.models as models


class DefensiveTroops:
    def __init__(self, outline: models.Outline):
        self.outline = outline
        self.evidence = basic.world_evidence(world_number=outline.world)
        self.deffensive_tropps = self.outline.deff_troops.split("\r\n")

    def in_village_dict(self):
        result = {}
        for i, line in enumerate(self.deffensive_tropps):
            if i % 2 == 1:
                continue
            army = basic.Defence(line, evidence=self.evidence)
            result[army.coord] = army

        return result


class VillageOwnerDoesNotExist(Exception):
    """ Raised when outline is out of date """


class OffTroops:
    """
    Helps iterating over user's off_troops from script

    yields extended Army instance."""

    def __init__(self, outline: models.Outline):
        self.outline = outline
        self.evidence = basic.world_evidence(world=outline.world)
        self.village_dictionary = basic.coord_to_player(outline=outline)
        self.off_troops = self.outline.off_troops.split("\r\n")

    def legal_coords(self):
        ally_villages = (
            models.VillageModel.objects.select_related()
            .filter(
                player__tribe__tag__in=self.outline.ally_tribe_tag,
                world=self.outline.world,
            )
            .values("x_coord", "y_coord", "coord")
        )
        enemy_villages = (
            models.VillageModel.objects.select_related()
            .filter(
                player__tribe__tag__in=self.outline.enemy_tribe_tag,
                world=self.outline.world,
            )
            .values("x_coord", "y_coord")
        )
        legal_coords_set = get_deff.get_legal_coords(
            ally_villages=ally_villages,
            enemy_villages=enemy_villages,
            radius=int(self.outline.initial_outline_front_dist),
        )
        coord_set = set()
        for coord_tuple in legal_coords_set:
            coord_set.add(f"{coord_tuple[0]}|{coord_tuple[1]}")
        return coord_set

    def __iter__(self):
        for line in self.off_troops:
            army = ArmyLineExtended(line, self.evidence)
            try:
                player = self.village_dictionary[army.coord]
            except KeyError:
                raise VillageOwnerDoesNotExist()
            else:
                army.player = player
                army.first_line = False
                yield army


class ArmyLineExtended(basic.Army):
    """ Class extending Army class from basic """

    def is_enough_off_units(self):
        """ Check if army is enough to use it """
        if self.nobleman > 0:
            return True
        elif self.off < 500 or self.deff > 5000:
            return False
        else:
            return True
