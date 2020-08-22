from trbial_wars import basic
from base import models


class TargetsGeneral:
    """ Iterable class with methods on user input targets """

    def __init__(self, outline_targets: str, world: int):
        self.coords = []
        self.target_list = outline_targets.split("\r\n")

        self.targets_dict = self.targets_dict()
        self.village_dict = self.target_village_dictionary(world=world)

    def player(self, coord):
        """ Return player name  """
        return self.village_dict[coord]

    def single(self, coord):
        """ Return SingleTarget instance """
        return self.targets_dict[coord]

    def targets_dict(self):
        """ Parse coord:off:noble of use input """
        result_dict = {}

        for line in self.target_list:
            line_lst = line.split(":")
            self.coords.append(line_lst[0])
            target_line = SingleTarget(line=line_lst)

            result_dict[line_lst[0]] = target_line

        return result_dict

    def target_village_dictionary(self, world):
        """ Create a dictionary with player names """
        village_long_str = " ".join(self.coords)

        result_dict = basic.coord_to_player_from_string(
            village_coord_list=village_long_str, world=world
        )
        return result_dict

    def __iter__(self):
        return iter(self.coords)


class SingleTarget:
    """ Represent single target line coord:off:noble """
    def __init__(self, line: list):
        self.off_index = 0
        self.index = 1000
        self.coord = line[0]
        self.target_required_offs = int(line[1])
        self.target_required_nobles = int(line[2])
        self.offs_to_write_out = self.target_required_offs
        self.nobles_to_write_out = self.target_required_nobles

    def add_off(self, times=1):
        """ Decrease current number of offs """
        self.offs_to_write_out -= times

    def are_offs_to_write_out(self):
        """ Bool if target needs more offs"""
        return self.offs_to_write_out > 0

    def add_noble(self, times=1):
        """ Decrease current number of nobles """
        self.nobles_to_write_out -= times

    def are_nobles_to_write_out(self):
        """ Bool if target needs more nobles """
        return self.nobles_to_write_out > 0

    def are_nobles_not_required(self):
        """ Check if no more nobles need to be written out to outline """
        return self.nobles_to_write_out == 0

    def parse_nearest(self, weight_max, target):
        """
        For given WeightMax and Target instances return list

        with Weigths with nobles that need to be created.

        Also updates weight_max instance.

        """
        result_weight_lst = []

        times = min(self.nobles_to_write_out, weight_max.nobleman_left)

        army = weight_max.off_max // times
        first_army = army + weight_max.off_max - times * army

        for i in range(times):
            if i == 0:
                army = first_army

            result_weight_lst.append(
                models.WeightModel(
                    target=target,
                    player=weight_max.player,
                    start=weight_max.start,
                    state=weight_max,
                    off=army,
                    distance=basic.dist(weight_max.start, target.target),
                    nobleman=1,
                    order=self.index,
                    first_line=weight_max.first_line,
                )
            )
            self.index += 1
            self.nobles_to_write_out -= 1

        weight_max.nobleman_left = weight_max.nobleman_max - times
        weight_max.nobleman_state = times
        weight_max.off_state = weight_max.off_max
        weight_max.off_left = 0

        return result_weight_lst

    def parse_off(self, weight_max, target):
        """
        For given WeightMax and Target instances return list

        with Weigths with NO nobles, only off that need to be created.

        Also updates weight_max instance.

        """
        weight = models.WeightModel(
            target=target,
            player=weight_max.player,
            start=weight_max.start,
            state=weight_max,
            off=weight_max.off_max,
            distance=basic.dist(weight_max.start, target.target),
            nobleman=0,
            order=self.off_index,
            first_line=weight_max.first_line,
        )
        self.off_index += 1
        self.offs_to_write_out -= 1

        weight_max.off_state = weight_max.off_max
        weight_max.off_left = 0

        return weight
