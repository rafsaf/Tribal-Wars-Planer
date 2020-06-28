from . import basic_classes as basic
from base import models


class Graph:
    def __init__(self):
        self.vert_list = {}

    def add_vertex(self, key):
        new_vertex = Vertex(key[0], key[1])
        self.vert_list[key] = new_vertex

    def get_vertex(self, key):
        vertex: Vertex = self.vert_list[key]
        return vertex

    def add_edge(self, f, t, weight=(1, 1, 0)):
        if f not in self.vert_list:
            self.add_vertex(f)
        if t not in self.vert_list:
            self.add_vertex(t)
        self.vert_list[f].add_neighbor(self.vert_list[t], weight)
    
    def get_best_four_village(self, key):
        target = self.get_vertex(key)
        sorted_list = target.sort_connected_to()[:4]
        return sorted_list

    def __iter__(self):
        return iter(self.vert_list.values())


class Vertex:
    def __init__(self, key_x: int, key_y: int):
        self.id = (key_x, key_y)
        self.connected_to = {}
    
    def get_id(self):
        return self.id

    def get_village(self):
        return basic.Wioska(str(self.id[0]) + "|" + str(self.id[1]))

    def add_neighbor(self, nbr, weight=(1, 1, 0)):
        self.connected_to[nbr] = weight

    def sort_connected_to(self):
        sorted_list = sorted(
            self.connected_to.items(),
            key=lambda tuple_dist_units: tuple_dist_units[1][1],
            reverse=True,
        )
        return [(vertex,tup) for (vertex, tup) in sorted_list if tup[2]>0]

    def get_neighbors(self):
        return self.__str__() + str(
            [(str(i), self.connected_to[i]) for i in self.connected_to]
        )

    def __str__(self):
        return str(self.get_village())


g = Graph()
g.add_edge((500, 400), (500, 401), (2, 4000, 0))
g.add_edge((500, 400), (500, 402), (3, 5020, 1))
g.add_edge((500, 400), (500, 392), (5, 5000, 1))
g.add_edge((500, 400), (500, 397), (2, 10000, 1))
g.add_edge((500, 400), (500, 395), (7, 1500, 1))
print(g.get_best_four_village((500,400)))


def make_initial_outline(outline: models.New_Outline):
    text_wojsko = outline.zbiorka_wojsko.split("\r\n")

    priority_players = outline.initial_period_outline_players.split("\r\n")
    targets = basic.Wiele_wiosek(
        outline.initial_period_outline_targets
    ).lista_z_wioskami
    parent_army_world_evidence = basic.Parent_Army_Defence_World_Evidence(
        int(outline.swiat)
    )

    outsiders = []  # villages out of range-12 of any target
    graph = Graph()

    for line in text_wojsko:

        line_army = basic.Army(
            text_army=line, parent_army_object=parent_army_world_evidence
        )
        actual_village = line_army.get_village()

        # fill graph
        outsider = True  # check if out of range of any target
        for target in targets:
            if target.distance(actual_village) <= 8:
                outsider = False
                g.add_edge(
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



