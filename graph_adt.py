
class Graph:
    """Graph ADT adapted from the Project 2 Graph template for Project 3 campus routing."""

    def __init__(self, directed=False):
        self.directed = directed
        self.adj_list = {}        # {building: {neighbor_building: weight}}
        self.building_names = {}  # {building: full_name_or_notes}

    def add_building(self, code, name=""):
        if code not in self.adj_list:
            self.adj_list[code] = {}
            self.building_names[code] = name if name else code

    def add_path(self, u, v, weight, bidirectional=None):
        if u not in self.adj_list:
            self.add_building(u)
        if v not in self.adj_list:
            self.add_building(v)

        self.adj_list[u][v] = weight

        is_bidir = (not self.directed) if bidirectional is None else bidirectional
        if is_bidir:
            self.adj_list[v][u] = weight

    def get_neighbors(self, building):
        if building not in self.adj_list:
            raise ValueError(f"Unknown building: {building}")
        return list(self.adj_list[building].items())

    def get_buildings(self):
        return [building for building in self.adj_list]

    def get_edges(self):
        edges = []
        for u, nbrs in self.adj_list.items():
            for v, weight in nbrs.items():
                edges.append(((u, v), weight))
        return edges
