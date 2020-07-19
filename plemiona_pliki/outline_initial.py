import pickle
from . import basic_classes as basic
from base import models
from .timing import timing


def make_outline(outline: models.New_Outline):
    graph = Graph_Initial_Outline(outline=outline)
    graph.outline_make_first_time()
    return graph


def get_outline(outline: models.New_Outline):
    graph = Graph_Initial_Outline(outline=outline)
    graph.get_existing_outline()
    return graph


def get_branch_graph(outline: models.New_Outline, target_model: models.Target_Vertex):
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

    def get_targets_from_outline(self) -> list:
        """ getting target coords from outline, return list with strings-coords """
        list_with_targets = self.outline.initial_period_outline_targets
        list_with_targets = basic.Wiele_wiosek(list_with_targets).lista_z_wioskami
        return list_with_targets

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

    def add_vertices_army_to_graph(self):
        """ Adds all villages to graph"""
        parent_army = basic.Parent_Army_Defence_World_Evidence(self.outline.swiat)
        for i in self.outline.zbiorka_wojsko.split("\r\n"):
            instance = Vertex_Army(
                i,
                parent_army,
                self.outline.swiat,
                float(self.outline.max_distance_initial_outline),
            )
            # self.data
            # filled with key:coord - value:Vertex_Army
            self.data[instance.get_village().kordy] = instance

            self.context_with_village_vertices.append(instance)

    def add_weight_to_vertices(self):
        for vertex in self.context_with_village_vertices:
            for target in self.context_with_target_vertices:
                weight = vertex.add_connected_vertex_target(target.wioska.kordy)
                target.add_connected_vertex_army(weight)

    def add_weight_to_single_target_vertex_without_banned(self, target_model):
        """ after get_branch_graph method only """
        target_vertex = self.get_target_vertex(target_model.target)
        for vertex in self.context_with_village_vertices:
            if vertex.get_village().kordy not in self.banned:
                weight = vertex.add_connected_vertex_target(target_vertex.wioska.kordy)
                target_vertex.add_connected_vertex_army(weight)

    def sort_weight_targets(self):
        for target in self.context_with_target_vertices:
            target.connected_to_vertex_army = sorted(
                target.connected_to_vertex_army, reverse=True
            )

    def outline_make_first_time(self):
        self.make()
        obj_list = []
        for target in self.context_with_target_vertices:
            new_banned = target.get_four_best_vertices(self.banned)
            for i in new_banned:
                self.banned.add(i)

            obj_list.append(target.return_db_instance(self.outline))

        models.Target_Vertex.objects.all().filter(outline=self.outline).delete()
        # target vertices
        models.Target_Vertex.objects.bulk_create(obj_list)

        obj_list = models.Target_Vertex.objects.all().filter(outline=self.outline).order_by('target')
        target_list = sorted(self.context_with_target_vertices, key=lambda value: value.wioska.kordy)

        for target_vertex, target_model in zip(target_list, obj_list):
            #iter, weight
            result_lst = enumerate(target_vertex.result_lst)

            models.Weight.objects.bulk_create(
                [ 
                    i[1].return_db_instance(target=target_model, order=i[0]) for i in result_lst
                ]
            )

    def get_existing_outline(self):
        """ 
        fast getting graph from database Target_Vertex, used in new_outline_initial_period2.html
        """

        for target in models.Target_Vertex.objects.all().filter(outline=self.outline):
            target_vertex = self.add_single_target_vertex_to_graph(target.target)

            for weight_model in (
                    models.Weight.objects.all().filter(target=target).order_by("order")
                ):

                target_vertex.result_lst.append(
                    Weight.from_model_weight(
                        start=weight_model.start,
                        target=weight_model.target.target,
                        snob=weight_model.snob,
                        distance=weight_model.distance,
                        off=weight_model.off,
                        player=weight_model.player
                    )
                )

    def get_branch_graph(self, target_model):
        self.add_vertices_army_to_graph()

        for target in models.Target_Vertex.objects.all().filter(outline=self.outline):
            if not target == target_model:
                for weight_model in models.Weight.objects.all().filter(target=target):
                    self.banned.add(weight_model.start)

        target_vertex = self.add_single_target_vertex_to_graph(
                    target_model.target
                )
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

    def make(self):
        self.add_target_vertices_to_graph()
        self.add_vertices_army_to_graph()
        self.add_weight_to_vertices()
        self.sort_weight_targets()


class Weight:
    def __init__(
        self,
        start: str,
        target: str,
        world=None,
        max_distance=None,
        dictionary={},
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
        obj = cls(start=start, target=target,)
        obj.off = off
        obj.snob = snob
        obj.distance_rounded = distance
        obj.player = player
        return obj

    def set_player(self):
        try:
            return self.dictionary[self.start.kordy]
        except KeyError:
            player = self.start.get_player(self.world).name
            self.dictionary[self.start.kordy] = player
            return player

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

    def return_db_instance(self, target: models.Target_Vertex, order: int):
        return models.Weight(
            target=target,
            start=self.start.kordy,
            off=self.off,
            distance=self.distance_rounded,
            snob=self.snob,
            order=order,
            player=self.player
        )


class Vertex_Army(basic.Army):
    def __init__(self, text_army, parent_army_object, world: int, max_distance: float):
        super().__init__(text_army=text_army, parent_army_object=parent_army_object)
        self.connected_to_target_vertex = []
        self.world = world
        self.max_distance = max_distance

    def add_connected_vertex_target(self, target: str):
        if self.get_village().distance(basic.Wioska(target)) <= self.max_distance:
            weight = Weight(
                start=self.coords_string,
                target=target,
                world=self.world,
                max_distance=self.max_distance,
                army=self,
            )
            self.connected_to_target_vertex.append(weight)
            return weight
        return None


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
        result = {}
        result_lst = []
        for weight in self.connected_to_vertex_army:
            length = len(result)
            if length == 4:
                break
            if (
                weight.army.have_szlachcic()
                and weight.distance <= self.max_distance
                and weight.start.kordy not in banned_dict
            ):
                result["attack{}".format(length + 1)] = weight.start.kordy
                result_lst.append(weight)
        if len(result_lst) < 4:
            return []

        self.result_lst = result_lst
        return result.values()

    def get_player(self):
        return self.wioska.get_player(self.world)

    def return_db_instance(self, outline: models.New_Outline):
        return models.Target_Vertex(outline=outline, target=self.wioska.kordy, player=self.player, slug=self.slug)

    def renew(self, target_model):

        result_lst = enumerate(self.result_lst)
        models.Weight.objects.all().filter(target=target_model).delete()
        models.Weight.objects.bulk_create(
            [ 
                i[1].return_db_instance(target=target_model, order=i[0]) for i in result_lst
            ]
        )

    def delete_element(self, coord):
        for i, weight in enumerate(self.result_lst):
            if weight.start.kordy == coord:
                del self.result_lst[i]
                return

    def swap_up(self, coord):
        for i, weight in enumerate(self.result_lst):
            if weight.start.kordy == coord:
                if not i == 0:
                    start = self.result_lst[i]
                    end = self.result_lst[i - 1]
                    self.result_lst[i] = end
                    self.result_lst[i - 1] = start
                    return

    def swap_down(self, coord):
        for i, weight in enumerate(self.result_lst):
            if weight.start.kordy == coord:
                if not i == len(self.result_lst) - 1:
                    start = self.result_lst[i]
                    end = self.result_lst[i + 1]
                    self.result_lst[i] = end
                    self.result_lst[i + 1] = start
                    return

    def add_last(self, coord):
        for weight in self.connected_to_vertex_army:
            if weight.start.kordy == coord:
                self.result_lst.append(weight)
                return

    def add_first(self, coord):
        for weight in self.connected_to_vertex_army:
            if weight.start.kordy == coord:
                self.result_lst.insert(0, weight)
                return

