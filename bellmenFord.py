def bellmenFord(graph, source):
    nodes = graph.get_buildings()
    edges = graph.get_edges()

    if source not in nodes:
        raise ValueError(f"Unknown source building: {source}")

    path_lengths = {}
    paths = {}

    for v in nodes:
        path_lengths[v] = float('inf')
        paths[v] = []

    path_lengths[source] = 0
    paths[source] = [source]

    for _ in range(len(nodes) - 1):
        for (u, v), w_uv in edges:
            if path_lengths[u] != float('inf') and path_lengths[u] + w_uv < path_lengths[v]:
                path_lengths[v] = path_lengths[u] + w_uv
                paths[v] = paths[u] + [v]

    # Check for negative cycles
    has_negative_cycle = False

    for (u, v), w_uv in edges:
        if path_lengths[u] != float('inf') and path_lengths[u] + w_uv < path_lengths[v]:
            has_negative_cycle = True
            break

    if has_negative_cycle:
        paths = {}

    return path_lengths, paths, has_negative_cycle
