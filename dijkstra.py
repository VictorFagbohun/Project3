import heapq
from itertools import count


def dijkstra(graph, source):
    buildings = graph.get_buildings()

    if source not in buildings:
        raise ValueError(f"Unknown source building: {source}")

    # Dijkstra's algorithm requires nonnegative edge weights.
    for (u, v), weight in graph.get_edges():
        if weight < 0:
            raise ValueError(
                f"Dijkstra's algorithm cannot use a negative edge: {u} -> {v}"
            )

    distances = {building: float("inf") for building in buildings}
    paths = {building: [] for building in buildings}

    distances[source] = 0
    paths[source] = [source]

    # The counter breaks ties without requiring building codes to be comparable.
    order = count()
    priority_queue = [(0, next(order), source)]

    while priority_queue:
        current_distance, _, current = heapq.heappop(priority_queue)

        # Ignore an older queue entry if a shorter route was found afterward.
        if current_distance > distances[current]:
            continue

        for neighbor, weight in graph.get_neighbors(current):
            new_distance = current_distance + weight

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                paths[neighbor] = paths[current] + [neighbor]
                heapq.heappush(
                    priority_queue,
                    (new_distance, next(order), neighbor)
                )

    return distances, paths, False