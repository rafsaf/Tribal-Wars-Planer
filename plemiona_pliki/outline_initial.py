from ast import literal_eval as make_tuple

from . import basic_classes as basic
from base import models


class Graph:
    def __init__(self, outline):
        self.outline = outline
        self.vert_list = {}
        self.target_vertex = []
        self.used_vertex = []

    def add_to_used_vertex(self, key):
        self.used_vertex.append(key)

    def add_vertex(self, key):
        new_vertex = Vertex(key[0], key[1])
        self.vert_list[key] = new_vertex

    def get_vertex(self, key):
        vertex: Vertex = self.vert_list[key]
        return vertex

    def add_edge(self, f, t, weight=(1, 1, 0)):
        if f not in self.vert_list:
            self.add_vertex(f)
            self.target_vertex.append(f)
        if t not in self.vert_list:
            self.add_vertex(t)
        self.vert_list[f].add_neighbor(self.vert_list[t], weight)
    
    def get_best_four_village(self, key):
        target = self.get_vertex(key)
        sorted_list = target.sort_connected_to(self.used_vertex)[:4]
        for vertex in sorted_list:
            self.used_vertex.append(vertex[0])
        return sorted_list
    
    def get_rest_of_four_villages(self, key, sorted_list):
        result = []
        vertex = self.get_vertex(key)
        for i in vertex.connected_to:
            if not i.id in [i[0] for i in sorted_list]:
                result.append((i.id, vertex.connected_to[i]))
        return result

    def get_result_outline(self):
        for target in self.target_vertex:
            sorted_list = self.get_best_four_village(target)

            for i in sorted_list:
                obj = models.Initial_Outline(outline=self.outline, target=str(target), village1=str(i[0]), params=str(i[1]))
                obj.save()
            for i in self.get_rest_of_four_villages(target, sorted_list):
                obj = models.Initial_Outline(outline=self.outline, target=str(target[0])+"|"+str(target[1]), village2=str(i[0]), params=(str(i[1])))
                obj.save()

    def __iter__(self):
        return iter(self.vert_list.values())


class Vertex:
    def __init__(self, key_x: int, key_y: int):
        self.id = (key_x, key_y)
        self.connected_to = {}

    def get_id(self):
        return self.id

    def get_village(self):
        return basic.Wioska.from_coords(*self.id)

    def add_neighbor(self, nbr, weight=(1, 1, 0)):
        self.connected_to[nbr] = weight

    def sort_connected_to(self, used_vertex):
        sorted_list = sorted(
            self.connected_to.items(),
            key=lambda tuple_dist_units: tuple_dist_units[1][1],
            reverse=True,
        )
        return [(vertex.id,tup) for (vertex, tup) in sorted_list if (tup[2] > 0 and vertex.id not in used_vertex)]

    def get_neighbors(self):
        return self.__str__() + str(
            [(str(i), self.connected_to[i]) for i in self.connected_to]
        )

    def __str__(self):
        return str(self.id)

class Some:
    def __init__(self, query, world):
        self.target_village = make_tuple(query.target)
        try:
            self.village1 = make_tuple(query.village1) 
        except Exception:
            self.village1 = ""
            pass

        try:
            self.village2 = make_tuple(query.village2)
        except Exception:
            self.village2 = ""
            pass

        self.owner = None
        try:
            self.params = make_tuple(query.params)
        except Exception:
            self.params = ""
            pass
        self.world = world
        self.set_attrs()
    def set_target_village(self):
        self.target_village = str(basic.Wioska(str(self.target_village[0])+"|"+str(self.target_village[1])))
    def get_village(self, coords):
        return basic.Wioska(str(coords[0])+"|"+str(coords[1]))

    def set_owner(self):
        self.owner = self.get_village(self.village1).get_player(self.world).name
    
    def set_village(self):
        if self.village1 == None:
            self.village2 = str(self.get_village(self.village2))
        else:
            self.village1 = str(self.get_village(self.village1))
    def set_params(self):
        if not self.params == "":
            self.params = f"Odległość: <br />{round(self.params[0],1)}<br /> Wojsko: <br />{self.params[1]}"
    def set_attrs(self):
        self.set_owner()
        self.set_params()
        self.set_village()
        self.set_target_village()
    def get_results(self):
        return [self.target_village, self.village1, self.village2, self.owner]

"""
g = Graph()
g.add_edge((500, 400), (500, 401), (2, 4000, 0))
g.add_edge((500, 400), (500, 402), (3, 5020, 1))
g.add_edge((500, 400), (500, 392), (5, 5000, 1))
g.add_edge((500, 400), (500, 397), (2, 10000, 1))
g.add_edge((500, 400), (500, 395), (7, 1500, 1))
g.add_edge((500, 400), (500, 398), (3, 1500, 1))
g.add_edge((501, 400), (500, 398), (7, 1500, 1))
print(g.get_result_outline())
"""

def make_initial_outline(outline: models.New_Outline):
    models.Initial_Outline.objects.all().filter(outline=outline).delete()
    text_wojsko = outline.zbiorka_wojsko.split("\r\n")

    priority_players = outline.initial_period_outline_players.split("\r\n")
    targets = basic.Wiele_wiosek(
        outline.initial_period_outline_targets
    ).lista_z_wioskami
    parent_army_world_evidence = basic.Parent_Army_Defence_World_Evidence(
        int(outline.swiat)
    )

    outsiders = []  # villages out of range-12 of any target
    graph = Graph(outline)

    for line in text_wojsko:

        line_army = basic.Army(
            text_army=line, parent_army_object=parent_army_world_evidence
        )
        actual_village = line_army.get_village()

        # fill graph
        outsider = True  # check if out of range of any target
        for target in targets:
            if target.distance(actual_village) <= 12:
                outsider = False
                graph.add_edge(
                    (target.x, target.y),
                    (actual_village.x, actual_village.y),
                    (
                        target.distance(actual_village),
                        line_army.get_off_units(),
                        line_army.get_szlachcic(),
                    ),
                )
        if outsider is True:
            outsiders.append(line_army)
        # add to db
    return graph



