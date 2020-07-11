import pickle
from . import basic_classes as basic
from base import models
from .timing import timing


@timing
def make_outline(outline: models.New_Outline):
    graph = Graph_Initial_Outline(outline=outline)
    graph.outline_make_first_time()
    return graph

def get_outline(outline: models.New_Outline):
    graph = Graph_Initial_Outline(outline=outline)
    graph.get_existing_outline()
    return graph

class Graph_Initial_Outline:
    def __init__(self, outline: models.New_Outline):
        self.outline = outline
        self.context_with_target_vertices = []
        self.context_with_village_vertices = []
        self.banned = set()
        self.data = {}


    def get_targets_from_outline(self):
        list_with_targets = self.outline.initial_period_outline_targets
        list_with_targets = basic.Wiele_wiosek(list_with_targets).lista_z_wioskami
        return list_with_targets

    # @timing
    def add_target_vertices_to_graph(self):
        for wioska in self.get_targets_from_outline():
            self.context_with_target_vertices.append(
                Vertex_Represent_Target_Village(
                    wioska.kordy,
                    self.outline.swiat,
                    float(self.outline.max_distance_initial_outline),
                )
            )
    def get_target_vertex(self, coord):
        for target in self.context_with_target_vertices:
            if target.wioska.kordy == coord:
                return target
    # @timing
    def add_vertices_army_to_graph(self):
        parent_army = basic.Parent_Army_Defence_World_Evidence(self.outline.swiat)
        for i in self.outline.zbiorka_wojsko.split("\r\n"):
            instance = Vertex_Army(
                    i,
                    parent_army,
                    self.outline.swiat,
                    float(self.outline.max_distance_initial_outline),)
            self.data[instance.get_village().kordy]=instance

            self.context_with_village_vertices.append(instance)
            

    @timing
    def add_weight_to_vertices(self):
        for vertex in self.context_with_village_vertices:
            for target in self.context_with_target_vertices:
                weight = vertex.add_connected_vertex_target(target.wioska.kordy)
                target.add_connected_vertex_army(weight)

    # @timing
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

            obj_list.append(target.get_target_vertex(self.outline))
        models.Target_Vertex.objects.all().filter(outline=self.outline).delete()
        models.Target_Vertex.objects.bulk_create(obj_list)

    def get_existing_outline(self):
        self.make()
        for target in self.context_with_target_vertices:

            obj = models.Target_Vertex.objects.get(outline=self.outline, target=target.wioska.kordy)
            dict_target = obj.__dict__
            del dict_target["_state"]
            del dict_target["target"]
            del dict_target["id"]
            del dict_target["outline_id"]
            #moze przestawiac?
            for start in dict_target.values():
                if start is not None:
                    target.result_lst.append(Weight(start, target.wioska.kordy, self.outline.swiat,self.data[start], self.outline.max_distance_initial_outline))
                    

    @timing
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
        world: int,
        army: basic.Army,
        max_distance: float,
        dictionary={},
    ):
        self.dictionary = dictionary
        self.start = basic.Wioska(start)
        self.target = basic.Wioska(target)
        self.world = world
        self.army = army
        self.max_distance = max_distance
        self.distance = self.distance_()
        self.off = self.off_()
        self.info = self.print_info()
        self.player = self.set_player()
        self.snob = self.army.get_szlachcic()

    def print_info(self):
        return (
            "Kordy: "+str(self.start.kordy)
            + "<br />"
            + "Wojsko: "+str(self.off)
            + "<br />"
            + "Odległość: "+str(round(self.distance, 1))
        )

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
        dist1 = self.distance_()
        dist2 = other.distance_()
        if dist1 > self.max_distance and dist2 < self.max_distance:
            return False

        elif dist1 > self.max_distance and dist2 > self.max_distance:
            return self.off_() < other.off_()

        elif dist1 < self.max_distance and dist2 > self.max_distance:
            return True

        elif dist1 < self.max_distance and dist2 < self.max_distance:
            return self.off_() < other.off_()

        else:
            raise ValueError

    def __eq__(self, other):
        return self.distance == other.distance and self.off == other.off


class Vertex_Army(basic.Army):
    def __init__(self, text_army, parent_army_object, world: int, max_distance: float):
        super().__init__(text_army=text_army, parent_army_object=parent_army_object)
        self.connected_to_target_vertex = []
        self.world = world
        self.max_distance = max_distance

    def add_connected_vertex_target(self, target: str):
        if self.get_village().distance(basic.Wioska(target)) <= self.max_distance:
            weight = Weight(
                self.coords_string, target, self.world, self, self.max_distance
            )
            self.connected_to_target_vertex.append(weight)
            return weight
        return None


class Vertex_Represent_Target_Village:
    def __init__(self, wioska: str, world: int, max_distance: float):
        self.wioska = basic.Wioska(wioska)
        self.slug = f"{self.wioska.x}-{self.wioska.y}"
        self.world = world
        self.connected_to_vertex_army: list = []
        self.max_distance = max_distance
        self.info = self.get_info()
        self.attacks = {}
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
            if weight.army.have_szlachcic() and weight.distance <= self.max_distance and weight.start.kordy not in banned_dict:
                result["attack{}".format(length+1)] = weight.start.kordy
                result_lst.append(weight)
        if len(result) < 4:
            return []
        else:
            self.attacks = result
            self.result_lst = result_lst

        return result.values()

    def get_player(self):
        return self.wioska.get_player(self.world)

    def get_target_vertex(self, outline):
        model_info = {}

        model_info["target"] = self.wioska.kordy
        model_info["outline"] = outline
        for i in self.attacks:
            model_info[i] = self.attacks[i]
        
        return models.Target_Vertex(
            **model_info
        )

    def get_info(self):
        return str(self.get_player())+"<br />"+ str(self.wioska.kordy)


class Vertex_Army_Employed_Village(Vertex_Army):
    pass


class Vertex_Army_Not_Used_Village(Vertex_Army):
    pass

