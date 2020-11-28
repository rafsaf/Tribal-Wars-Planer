import tribal_wars.basic as basic
import tribal_wars.get_deff as get_deff
import base.models as models

class DefensiveTroops:
    def __init__(self, outline: models.Outline):
        self.outline = outline
        self.evidence = basic.world_evidence(world_number=outline.world)
        self.deffensive_tropps = self.outline.deff_troops.split('\r\n')

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

    yields extended Army instance. """

    def __init__(self, outline: models.Outline):
        self.outline = outline
        self.evidence = basic.world_evidence(world_number=outline.world)
        self.village_dictionary = basic.coord_to_player(outline=outline)
        self.off_troops = self.outline.off_troops.split('\r\n')
        self.beyond_first_line = self.legal_coords()

    def legal_coords(self):
        query_class = basic.AllyEnemyVillagesQueries(self.outline)
        ally_villages = query_class.ally_villages()
        enemy_villages = query_class.enemy_villages()
        legal_coords_set = get_deff.get_legal_coords(
            ally_villages=ally_villages,
            enemy_villages=enemy_villages,
            radius=int(self.outline.initial_outline_front_dist),
            p=0.05,
        )
        coord_set = set()
        for coord_tuple in legal_coords_set:
            coord_set.add(f'{coord_tuple[0]}|{coord_tuple[1]}')
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
                if army.coord in self.beyond_first_line:
                    army.first_line = False
                else:
                    army.first_line = True
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
