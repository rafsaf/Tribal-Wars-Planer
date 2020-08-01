""" File with outline making and getting stuff """
from math import floor
from base import models
from . import basic
from .basic import timing


def make_outline(outline: models.Outline):
    """ For a given outline builds graph with outline instance, save a lot of objects in database while working """
    graph = Graph_Initial_Outline(outline=outline)
    graph.outline_make_first_time()
    return graph

def get_branch_graph(outline: models.Outline, target_model: models.TargetVertex):
    """ To get existing graph outline from database for specific TargetVertex """
    graph = Graph_Initial_Outline(outline=outline)
    graph.get_branch_graph(target_model=target_model)
    return graph


class Graph_Initial_Outline:
    def __init__(self, outline: models.Outline):
        self.outline = outline
        self.context_with_target_vertices = []
        self.context_with_village_vertices = []

        # banned set: all coords USED in targets
        self.banned = set()

        # filled with key:coord - value:Vertex_Army
        self.data = {}

    def get_player_dictionary(self):
        # average < 200ms
        my_tribe = self.outline.ally_tribe_tag.split(", ")
        my_tribe_id = [
            tribe.tribe_id
            for tribe in models.Tribe.objects.all().filter(
                world=self.outline.world, tag__in=my_tribe
            )
        ]

        players = models.Player.objects.all().filter(tribe_id__in=my_tribe_id)
        # id : name
        player_dictionary = {}
        # village : name
        village_dictionary = {}
        for player in players:
            player_dictionary[player.player_id] = player.name
        villages = models.VillageModel.objects.all().filter(player_id__in=player_dictionary)
        for v in villages:
            village_dictionary[str(v.x_coord) + "|" + str(v.y_coord)] = player_dictionary[
                v.player_id
            ]
        return village_dictionary

    def get_targets_from_outline(self) -> list:
        """ getting target coords from outline, return list with strings-coords """
        list_with_targets = self.outline.initial_outline_targets
        list_with_targets = basic.many_villages(list_with_targets).village_list
        return list_with_targets

    @timing
    def add_target_vertices_to_graph(self):
        """ Adds all targets to graph """
        for wioska in self.get_targets_from_outline():
            self.context_with_target_vertices.append(
                Vertex_Represent_Target_Village(
                    wioska.coord,
                    self.outline.world,
                    float(self.outline.initial_outline_max_distance),
                )
            )

    def add_single_target_vertex_to_graph(self, coord):
        instance = Vertex_Represent_Target_Village(
            coord, self.outline.world, float(self.outline.initial_outline_max_distance)
        )
        self.context_with_target_vertices.append(instance)
        return instance

    def get_target_vertex(self, coord):
        """ Return target from graph(add_target_vertices method first) """
        for target in self.context_with_target_vertices:
            if target.wioska.coord == coord:
                return target

    @timing
    def add_vertices_army_to_graph(self, dictionary):
        """ Adds all villages to graph"""
        parent_army = basic.world_evidence(self.outline.world)
        for i in self.outline.off_troops.split("\r\n"):
            instance = Vertex_Army(
                i,
                parent_army,
                self.outline.world,
                float(self.outline.initial_outline_max_distance),
                dictionary=dictionary,
            )
            # self.data
            # filled with key:coord - value:Vertex_Army
            self.data[instance.coord] = instance

            self.context_with_village_vertices.append(instance)

    @timing
    def add_weight_to_vertices(self):
        for vertex in self.context_with_village_vertices:
            for target in self.context_with_target_vertices:
                weight = vertex.add_connected_vertex_target(target.wioska.coord)
                target.add_connected_vertex_army(weight)

    def add_weight_to_single_target_vertex_without_banned(self, target_model):
        """ after get_branch_graph method only """
        target_vertex = self.get_target_vertex(target_model.target)
        for weight_model_max in (
            models.WeightMaximum.objects.all()
            .filter(outline=self.outline)
            .exclude(start__in=self.banned)
        ):
            target_vertex.add_connected_vertex_army(
                Weight.from_model_weight_maximum(
                    start=weight_model_max.start,
                    target=target_model.target,
                    nobleman=weight_model_max.snob_max - weight_model_max.snob_state,
                    off=weight_model_max.off_max - weight_model_max.off_state,
                    player=weight_model_max.player,
                )
            )

    def sort_weight_targets(self):
        for target in self.context_with_target_vertices:
            target.connected_to_vertex_army = sorted(
                target.connected_to_vertex_army, reverse=True
            )

    @timing
    def outline_make_first_time(self):

        dictionary = self.get_player_dictionary()

        self.add_target_vertices_to_graph()
        self.add_vertices_army_to_graph(dictionary)
        self.add_weight_to_vertices()

        # dodaje do db maximum
        models.WeightMaximum.objects.all().delete()
        models.WeightMaximum.objects.bulk_create(
            [
                village.return_db_instance(self.outline)
                for village in self.context_with_village_vertices
            ]
        )

        obj_list = []
        for target in self.context_with_target_vertices:
            new_banned = target.get_four_best_vertices(self.banned)
            for i in new_banned:
                self.banned.add(i)

            obj_list.append(target.return_db_instance(self.outline))

        models.TargetVertex.objects.all().filter(outline=self.outline).delete()
        # target vertices
        models.TargetVertex.objects.bulk_create(obj_list)

        obj_list = (
            models.TargetVertex.objects.all()
            .filter(outline=self.outline)
            .order_by("target")
        )
        target_list = sorted(
            self.context_with_target_vertices, key=lambda value: value.wioska.coord
        )

        for target_vertex, target_model in zip(target_list, obj_list):
            # iter, weight
            result_lst = enumerate(target_vertex.result_lst)

            models.WeightModel.objects.bulk_create(
                [
                    i[1].return_db_instance(
                        outline=target_model.outline, target=target_model, order=i[0]
                    )
                    for i in result_lst
                ]
            )
            for weight in models.WeightModel.objects.all().filter(target=target_model):
                weight.state.off_state = weight.off
                weight.state.snob_state = weight.nobleman
                weight.state.save()

    def get_branch_graph(self, target_model):

        for target in models.TargetVertex.objects.all().filter(outline=self.outline):
            for weight_model in models.WeightModel.objects.all().filter(target=target):
                if (
                    weight_model.state.off_state == weight_model.state.off_max
                    and weight_model.state.snob_state == weight_model.state.snob_max
                ):
                    self.banned.add(weight_model.start)

        target_vertex = self.add_single_target_vertex_to_graph(target_model.target)
        for weight_model in models.WeightModel.objects.all().filter(target=target_model):
            target_vertex.result_lst.append(
                Weight.from_model_weight(
                    start=weight_model.start,
                    target=weight_model.target.target,
                    nobleman=weight_model.nobleman,
                    distance=weight_model.distance,
                    off=weight_model.off,
                    player=weight_model.player,
                )
            )
        self.add_weight_to_single_target_vertex_without_banned(target_model)


class Weight:
    def __init__(
        self,
        start: str,
        target: str,
        world=None,
        max_distance=None,
        dictionary=None,
        army: basic.Army = None,
    ):
        self.start = basic.Village(start)
        self.target = basic.Village(target)
        if world is not None and max_distance is not None and army is not None:
            self.dictionary = dictionary
            self.world = world
            self.army = army
            self.max_distance = max_distance
            self.distance = self.distance_()
            self.distance_rounded = round(self.distance, 1)
            self.off = self.off_()
            self.player = self.set_player()
            self.nobleman = self.army.get_szlachcic()

    @classmethod
    def from_model_weight(
        cls, start: str, target: str, nobleman: int, distance: float, off: int, player: str,
    ):
        weight = cls(start=start, target=target)
        weight.off = off
        weight.nobleman = nobleman
        weight.distance_rounded = distance
        weight.player = player
        return weight

    @classmethod
    def from_model_weight_maximum(
        cls, start: str, target: str, nobleman: int, off: int, player: str,
    ):
        weight = cls(start=start, target=target)
        weight.off = off
        weight.nobleman = nobleman
        weight.distance = weight.distance_()
        weight.distance_rounded = round(weight.distance, 1)
        weight.player = player
        return weight

    def set_player(self):
        return self.dictionary[self.start.coord]

    def distance_(self):
        return self.start.distance(self.target)

    def off_(self):
        return self.army.off

    def __lt__(self, other):
        dist1 = self.distance_rounded
        dist2 = other.distance_rounded
        if dist1 > self.max_distance and dist2 < self.max_distance:
            return False

        elif dist1 > self.max_distance and dist2 > self.max_distance:
            return self.off < other.off

        elif dist1 < self.max_distance and dist2 > self.max_distance:
            return True

        elif dist1 < self.max_distance and dist2 < self.max_distance:
            return self.off < other.off

        else:
            raise ValueError

    def __eq__(self, other):
        return self.distance_rounded == other.distance_rounded and self.off == other.off

    def return_db_instance(self, outline, target: models.TargetVertex, order: int):
        weight_max = models.WeightMaximum.objects.get(
            outline=target.outline, start=self.start.coord
        )
        return models.WeightModel(
            target=target,
            state=weight_max,
            start=self.start.coord,
            off=self.off,
            distance=self.distance_rounded,
            nobleman=self.nobleman,
            order=order,
            player=self.player,
        )


class Vertex_Army(basic.Army):
    def __init__(
        self,
        text_army,
        evidence,
        world: int,
        max_distance: float,
        dictionary=None,
    ):
        super().__init__(text_army=text_army, evidence=evidence)
        self.connected_to_target_vertex = []
        self.world = world
        self.max_distance = max_distance
        self.dictionary = dictionary
        self.player = self.set_player()

    def set_player(self):
        return self.dictionary[self.coord]

    def add_connected_vertex_target(self, target: str):
        if self.village.distance(basic.Village(target)) <= self.max_distance:
            weight = Weight(
                start=self.coord,
                target=target,
                world=self.world,
                max_distance=self.max_distance,
                army=self,
                dictionary=self.dictionary,
            )
            self.connected_to_target_vertex.append(weight)
            return weight
        return None

    def return_db_instance(self, outline):
        return models.WeightMaximum(
            player=self.player,
            outline=outline,
            start=self.coord,
            off_max=self.off,
            snob_max=self.nobleman,
        )


class Vertex_Represent_Target_Village:
    def __init__(self, wioska: str, world: int, max_distance: float):
        self.wioska = basic.Village(wioska)
        self.slug = f"{self.wioska.x_coord}{self.wioska.y_coord}"
        self.world = world
        self.connected_to_vertex_army: list = []
        self.max_distance = max_distance
        self.result_lst = []
        self.player = str(self.get_player())

    def add_connected_vertex_army(self, weight):
        if weight is not None:
            self.connected_to_vertex_army.append(weight)

    def get_four_best_vertices(self, banned_dict: dict):
        return []
        # result = {}
        # result_lst = []
        # for weight in self.connected_to_vertex_army:
        #    length = len(result)
        #    if length == 4:
        #        break
        #    if (
        #        weight.army.have_szlachcic()
        #        and weight.distance <= self.max_distance
        #        and weight.start.coord not in banned_dict
        #    ):
        #        result["attack{}".format(length + 1)] = weight.start.coord
        #        result_lst.append(weight)
        # if len(result_lst) < 4:
        #    return []
        #
        # self.result_lst = result_lst
        # return result.values()

    def get_player(self):
        return "none"

    def return_db_instance(self, outline: models.Outline):
        return models.TargetVertex(
            outline=outline,
            target=self.wioska.coord,
            player=self.player,
            slug=self.slug,
        )

    def renew(self, target_model):

        result_lst = enumerate(self.result_lst)
        models.WeightModel.objects.all().filter(target=target_model).delete()
        models.WeightModel.objects.bulk_create(
            [
                i[1].return_db_instance(
                    outline=target_model.outline, target=target_model, order=i[0]
                )
                for i in result_lst
            ]
        )

    def delete_element(self, target_model, coord, order):
        weight = self.result_lst[order]
        del self.result_lst[order]
        state = models.WeightMaximum.objects.get(
            outline=target_model.outline, start=coord
        )
        state.off_state -= weight.off
        state.snob_state -= weight.nobleman
        state.save()
        return

    def swap_up(self, order):
        i = order
        if not i == 0:
            start = self.result_lst[i]
            end = self.result_lst[i - 1]
            self.result_lst[i] = end
            self.result_lst[i - 1] = start
            return

    def swap_down(self, order):
        i = order
        if not i == len(self.result_lst) - 1:
            start = self.result_lst[i]
            end = self.result_lst[i + 1]
            self.result_lst[i] = end
            self.result_lst[i + 1] = start
            return
        return

    def add_last(self, target_model, coord):
        for weight in self.connected_to_vertex_army:
            if weight.start.coord == coord:
                self.result_lst.append(weight)
                state = models.WeightMaximum.objects.get(
                    outline=target_model.outline, start=coord
                )

                state.off_state += weight.off
                state.snob_state += weight.nobleman
                state.save()
                return

    def add_first(self, target_model, coord):
        for weight in self.connected_to_vertex_army:
            if weight.start.coord == coord:
                self.result_lst.insert(0, weight)
                state = models.WeightMaximum.objects.get(
                    outline=target_model.outline, start=coord
                )
                state.off_state += weight.off
                state.snob_state += weight.nobleman
                state.save()
                return

    def duplicate(self, order, fraction=1 / 2):
        weight = self.result_lst[order]
        index = order
        new_off = floor(weight.off * fraction)
        if weight.nobleman > 1:
            new_snob = 1
            old_snob = weight.nobleman - new_snob
        else:
            new_snob = 0
            old_snob = weight.nobleman - new_snob
        old_off = weight.off - new_off

        weight.off = old_off
        weight.nobleman = old_snob

        new_weight = Weight.from_model_weight(
            start=weight.start.coord,
            target=weight.target.coord,
            nobleman=new_snob,
            distance=weight.distance_rounded,
            off=new_off,
            player=weight.player,
        )
        self.result_lst.insert(index + 1, new_weight)

        return