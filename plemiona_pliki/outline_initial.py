""" File with outline making and getting stuff """
from math import floor
from base import models
from . import basic_classes as basic
from .timing import timing

import itertools
def make_outline(outline: models.New_Outline):
    """ For a given outline builds graph with outline instance, save a lot of objects in database while working """
    graph = Graph_Initial_Outline(outline=outline)
    graph.outline_make_first_time()
    return graph

def get_branch_graph(outline: models.New_Outline, target_model: models.Target_Vertex):
    """ To get existing graph outline from database for specific Target_Vertex """
    graph = Graph_Initial_Outline(outline=outline)
    graph.get_branch_graph(target_model=target_model)
    return graph


class Graph_Initial_Outline:
    def __init__(self, outline: models.New_Outline):
        self.outline = outline
        self.context_with_target_vertices = []
        self.context_with_village_vertices = []

        # banned set: all coords USED in targets
        self.banned = set()

        # filled with key:coord - value:Vertex_Army
        self.data = {}

    def get_player_dictionary(self):
        # average < 200ms
        my_tribe = self.outline.moje_plemie_skrot.split(", ")
        my_tribe_id = [
            tribe.tribe_id
            for tribe in models.Tribe.objects.all().filter(
                world=self.outline.swiat, tag__in=my_tribe
            )
        ]

        players = models.Player.objects.all().filter(tribe_id__in=my_tribe_id)
        # id : name
        player_dictionary = {}
        # village : name
        village_dictionary = {}
        for player in players:
            player_dictionary[player.player_id] = player.name
        villages = models.Village.objects.all().filter(player_id__in=player_dictionary)
        for v in villages:
            village_dictionary[str(v.x) + "|" + str(v.y)] = player_dictionary[
                v.player_id
            ]
        return village_dictionary

    def get_targets_from_outline(self) -> list:
        """ getting target coords from outline, return list with strings-coords """
        list_with_targets = self.outline.initial_period_outline_targets
        list_with_targets = basic.Wiele_wiosek(list_with_targets).lista_z_wioskami
        return list_with_targets

    @timing
    def add_target_vertices_to_graph(self):
        """ Adds all targets to graph """
        for wioska in self.get_targets_from_outline():
            self.context_with_target_vertices.append(
                Vertex_Represent_Target_Village(
                    wioska.kordy,
                    self.outline.swiat,
                    float(self.outline.max_distance_initial_outline),
                )
            )

    def add_single_target_vertex_to_graph(self, coord):
        instance = Vertex_Represent_Target_Village(
            coord, self.outline.swiat, float(self.outline.max_distance_initial_outline)
        )
        self.context_with_target_vertices.append(instance)
        return instance

    def get_target_vertex(self, coord):
        """ Return target from graph(add_target_vertices method first) """
        for target in self.context_with_target_vertices:
            if target.wioska.kordy == coord:
                return target

    @timing
    def add_vertices_army_to_graph(self, dictionary):
        """ Adds all villages to graph"""
        parent_army = basic.Parent_Army_Defence_World_Evidence(self.outline.swiat)
        for i in self.outline.zbiorka_wojsko.split("\r\n"):
            instance = Vertex_Army(
                i,
                parent_army,
                self.outline.swiat,
                float(self.outline.max_distance_initial_outline),
                dictionary=dictionary,
            )
            # self.data
            # filled with key:coord - value:Vertex_Army
            self.data[instance.get_village().kordy] = instance

            self.context_with_village_vertices.append(instance)

    @timing
    def add_weight_to_vertices(self):
        for vertex in self.context_with_village_vertices:
            for target in self.context_with_target_vertices:
                weight = vertex.add_connected_vertex_target(target.wioska.kordy)
                target.add_connected_vertex_army(weight)

    def add_weight_to_single_target_vertex_without_banned(self, target_model):
        """ after get_branch_graph method only """
        target_vertex = self.get_target_vertex(target_model.target)
        for weight_model_max in (
            models.Weight_Maximum.objects.all()
            .filter(outline=self.outline)
            .exclude(start__in=self.banned)
        ):
            target_vertex.add_connected_vertex_army(
                Weight.from_model_weight_maximum(
                    start=weight_model_max.start,
                    target=target_model.target,
                    snob=weight_model_max.snob_max - weight_model_max.snob_state,
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
        models.Weight_Maximum.objects.all().delete()
        models.Weight_Maximum.objects.bulk_create(
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

        models.Target_Vertex.objects.all().filter(outline=self.outline).delete()
        # target vertices
        models.Target_Vertex.objects.bulk_create(obj_list)

        obj_list = (
            models.Target_Vertex.objects.all()
            .filter(outline=self.outline)
            .order_by("target")
        )
        target_list = sorted(
            self.context_with_target_vertices, key=lambda value: value.wioska.kordy
        )

        for target_vertex, target_model in zip(target_list, obj_list):
            # iter, weight
            result_lst = enumerate(target_vertex.result_lst)

            models.Weight.objects.bulk_create(
                [
                    i[1].return_db_instance(
                        outline=target_model.outline, target=target_model, order=i[0]
                    )
                    for i in result_lst
                ]
            )
            for weight in models.Weight.objects.all().filter(target=target_model):
                weight.state.off_state = weight.off
                weight.state.snob_state = weight.snob
                weight.state.save()

    def get_branch_graph(self, target_model):

        for target in models.Target_Vertex.objects.all().filter(outline=self.outline):
            for weight_model in models.Weight.objects.all().filter(target=target):
                if (
                    weight_model.state.off_state == weight_model.state.off_max
                    and weight_model.state.snob_state == weight_model.state.snob_max
                ):
                    self.banned.add(weight_model.start)

        target_vertex = self.add_single_target_vertex_to_graph(target_model.target)
        for weight_model in models.Weight.objects.all().filter(target=target_model):
            target_vertex.result_lst.append(
                Weight.from_model_weight(
                    start=weight_model.start,
                    target=weight_model.target.target,
                    snob=weight_model.snob,
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
        self.start = basic.Wioska(start)
        self.target = basic.Wioska(target)
        if world is not None and max_distance is not None and army is not None:
            self.dictionary = dictionary
            self.world = world
            self.army = army
            self.max_distance = max_distance
            self.distance = self.distance_()
            self.distance_rounded = round(self.distance, 1)
            self.off = self.off_()
            self.player = self.set_player()
            self.snob = self.army.get_szlachcic()

    @classmethod
    def from_model_weight(
        cls, start: str, target: str, snob: int, distance: float, off: int, player: str,
    ):
        weight = cls(start=start, target=target)
        weight.off = off
        weight.snob = snob
        weight.distance_rounded = distance
        weight.player = player
        return weight

    @classmethod
    def from_model_weight_maximum(
        cls, start: str, target: str, snob: int, off: int, player: str,
    ):
        weight = cls(start=start, target=target)
        weight.off = off
        weight.snob = snob
        weight.distance = weight.distance_()
        weight.distance_rounded = round(weight.distance, 1)
        weight.player = player
        return weight

    def set_player(self):
        return self.dictionary[self.start.kordy]

    def distance_(self):
        return self.start.distance(self.target)

    def off_(self):
        return self.army.get_off_units()

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

    def return_db_instance(self, outline, target: models.Target_Vertex, order: int):
        weight_max = models.Weight_Maximum.objects.get(
            outline=target.outline, start=self.start.kordy
        )
        return models.Weight(
            target=target,
            state=weight_max,
            start=self.start.kordy,
            off=self.off,
            distance=self.distance_rounded,
            snob=self.snob,
            order=order,
            player=self.player,
        )


class Vertex_Army(basic.Army):
    def __init__(
        self,
        text_army,
        parent_army_object,
        world: int,
        max_distance: float,
        dictionary=None,
    ):
        super().__init__(text_army=text_army, parent_army_object=parent_army_object)
        self.connected_to_target_vertex = []
        self.world = world
        self.max_distance = max_distance
        self.dictionary = dictionary
        self.player = self.set_player()

    def set_player(self):
        return self.dictionary[self.coords_string]

    def add_connected_vertex_target(self, target: str):
        if self.get_village().distance(basic.Wioska(target)) <= self.max_distance:
            weight = Weight(
                start=self.coords_string,
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
        return models.Weight_Maximum(
            player=self.player,
            outline=outline,
            start=self.coords_string,
            off_max=self.get_off_units(),
            snob_max=self.get_szlachcic(),
        )


class Vertex_Represent_Target_Village:
    def __init__(self, wioska: str, world: int, max_distance: float):
        self.wioska = basic.Wioska(wioska)
        self.slug = f"{self.wioska.x}{self.wioska.y}"
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
        #        and weight.start.kordy not in banned_dict
        #    ):
        #        result["attack{}".format(length + 1)] = weight.start.kordy
        #        result_lst.append(weight)
        # if len(result_lst) < 4:
        #    return []
        #
        # self.result_lst = result_lst
        # return result.values()

    def get_player(self):
        return self.wioska.get_player(self.world)

    def return_db_instance(self, outline: models.New_Outline):
        return models.Target_Vertex(
            outline=outline,
            target=self.wioska.kordy,
            player=self.player,
            slug=self.slug,
        )

    def renew(self, target_model):

        result_lst = enumerate(self.result_lst)
        models.Weight.objects.all().filter(target=target_model).delete()
        models.Weight.objects.bulk_create(
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
        state = models.Weight_Maximum.objects.get(
            outline=target_model.outline, start=coord
        )
        state.off_state -= weight.off
        state.snob_state -= weight.snob
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
            if weight.start.kordy == coord:
                self.result_lst.append(weight)
                state = models.Weight_Maximum.objects.get(
                    outline=target_model.outline, start=coord
                )

                state.off_state += weight.off
                state.snob_state += weight.snob
                state.save()
                return

    def add_first(self, target_model, coord):
        for weight in self.connected_to_vertex_army:
            if weight.start.kordy == coord:
                self.result_lst.insert(0, weight)
                state = models.Weight_Maximum.objects.get(
                    outline=target_model.outline, start=coord
                )
                state.off_state += weight.off
                state.snob_state += weight.snob
                state.save()
                return

    def duplicate(self, order, fraction=1 / 2):
        weight = self.result_lst[order]
        index = order
        new_off = floor(weight.off * fraction)
        if weight.snob > 1:
            new_snob = 1
            old_snob = weight.snob - new_snob
        else:
            new_snob = 0
            old_snob = weight.snob - new_snob
        old_off = weight.off - new_off

        weight.off = old_off
        weight.snob = old_snob

        new_weight = Weight.from_model_weight(
            start=weight.start.kordy,
            target=weight.target.kordy,
            snob=new_snob,
            distance=weight.distance_rounded,
            off=new_off,
            player=weight.player,
        )
        self.result_lst.insert(index + 1, new_weight)

        return