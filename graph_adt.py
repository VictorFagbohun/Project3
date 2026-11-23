import heapq
import math

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

    def _reconstruct_paths(self, source, distances, parents):
        paths = {}
        for target in self.adj_list:
            if math.isinf(distances[target]):
                paths[target] = []
                continue

            route = []
            current = target
            while current is not None:
                route.append(current)
                if current == source:
                    break
                current = parents[current]

            paths[target] = list(reversed(route)) if route and route[-1] == source else []
        return paths

    def dijkstra(self, source):
        if source not in self.adj_list:
            raise ValueError(f"Unknown source building: {source}")

        distances = {b: math.inf for b in self.adj_list}
        parents = {b: None for b in self.adj_list}
        distances[source] = 0

        pq = [(0, source)]
        visited = set()

        while pq:
            current_dist, u = heapq.heappop(pq)
            if u in visited:
                continue
            visited.add(u)

            for v, weight in self.get_neighbors(u):
                if weight < 0:
                    raise ValueError(
                        f"Dijkstra requires non-negative weights; found {weight} on {u} -> {v}"
                    )
                new_dist = current_dist + weight
                if new_dist < distances[v]:
                    distances[v] = new_dist
                    parents[v] = u
                    heapq.heappush(pq, (new_dist, v))

        paths = self._reconstruct_paths(source, distances, parents)
        return distances, paths

    def bellman_ford(self, source):
        if source not in self.adj_list:
            raise ValueError(f"Unknown source building: {source}")

        buildings = self.get_buildings()
        edges = self.get_edges()

        distances = {b: math.inf for b in buildings}
        parents = {b: None for b in buildings}
        distances[source] = 0

        for _ in range(len(buildings) - 1):
            updated = False
            for (u, v), weight in edges:
                if not math.isinf(distances[u]) and distances[u] + weight < distances[v]:
                    distances[v] = distances[u] + weight
                    parents[v] = u
                    updated = True
            if not updated:
                break

        has_negative_cycle = False
        for (u, v), weight in edges:
            if not math.isinf(distances[u]) and distances[u] + weight < distances[v]:
                has_negative_cycle = True
                break

        paths = {} if has_negative_cycle else self._reconstruct_paths(source, distances, parents)
        return distances, paths, has_negative_cycle    def get_weighted_neighbors(self, u):
        # Returns [(neighbor, weight), ...]
        return list(self.weighted_adj.get(u, {}).items())

    def get_edges(self):
        # Returns [((u, v), weight), ...] for Bellman-Ford
        edges = []
        for u, nbrs in self.weighted_adj.items():
            for v, w in nbrs.items():
                edges.append(((u, v), w))
        return edges

    def dijkstra(self, source):
        if source not in self.weighted_adj:
            raise ValueError(f"Unknown source node: {source}")

        dist = {node: math.inf for node in self.weighted_adj}
        parent = {node: None for node in self.weighted_adj}
        dist[source] = 0

        pq = [(0, source)]
        visited = set()

        while pq:
            current_dist, u = heapq.heappop(pq)
            if u in visited:
                continue
            visited.add(u)

            for v, weight in self.get_weighted_neighbors(u):
                if weight < 0:
                    raise ValueError("Dijkstra does not support negative edge weights.")
                new_dist = current_dist + weight
                if new_dist < dist[v]:
                    dist[v] = new_dist
                    parent[v] = u
                    heapq.heappush(pq, (new_dist, v))

        paths = self._reconstruct_all_paths(source, dist, parent)
        return dist, paths

    def bellman_ford(self, source):
        if source not in self.weighted_adj:
            raise ValueError(f"Unknown source node: {source}")

        nodes = self.get_nodes()
        edges = self.get_edges()
        dist = {node: math.inf for node in nodes}
        parent = {node: None for node in nodes}
        dist[source] = 0

        for _ in range(len(nodes) - 1):
            updated = False
            for (u, v), weight in edges:
                if dist[u] != math.inf and dist[u] + weight < dist[v]:
                    dist[v] = dist[u] + weight
                    parent[v] = u
                    updated = True
            if not updated:
                break

        has_negative_cycle = False
        for (u, v), weight in edges:
            if dist[u] != math.inf and dist[u] + weight < dist[v]:
                has_negative_cycle = True
                break

        paths = {} if has_negative_cycle else self._reconstruct_all_paths(source, dist, parent)
        return dist, paths, has_negative_cycle

    def _reconstruct_all_paths(self, source, dist, parent):
        paths = {}
        for target in self.weighted_adj:
            if math.isinf(dist[target]):
                paths[target] = []
                continue
            path = []
            curr = target
            while curr is not None:
                path.append(curr)
                if curr == source:
                    break
                curr = parent[curr]
            paths[target] = list(reversed(path)) if path and path[-1] == source else []
        return paths
