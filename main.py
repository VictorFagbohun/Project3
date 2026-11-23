from bellmanFord import bellmanFord
from dijkstra import dijkstra
from graph_adt import Graph


def build_campus_graph():
    graph = Graph()

    buildings = [
        "College Square", "Lewis Science Center", "Computer Science", "Burdick",
        "Speech Language Hearing", "Prince Center", "Torreyson Library", "Old Main",
        "Police Dept.", "Fine Art", "McAlister Hall", "Maintenance College",
        "Student Center", "Wingo", "Student Health Center", "New Business Building",
        "Oak Tree Apt.", "Brewer-Hegeman", "Bear village Apt."
    ]

    for building in buildings:
        graph.add_building(building)

    paths = [
        ("College Square", "Lewis Science Center", 200),
        ("College Square", "Prince Center", 300),
        ("Lewis Science Center", "Computer Science", 150),
        ("Lewis Science Center", "Speech Language Hearing", 250),
        ("Computer Science", "Burdick", 30),
        ("Computer Science", "Prince Center", 80),
        ("Computer Science", "Torreyson Library", 40),
        ("Burdick", "Speech Language Hearing", 100),
        ("Burdick", "Torreyson Library", 80),
        ("Burdick", "McAlister Hall", 200),
        ("Burdick", "Maintenance College", 300),
        ("Speech Language Hearing", "Maintenance College", 120),
        ("Prince Center", "Torreyson Library", 30),
        ("Prince Center", "Police Dept.", 100),
        ("Torreyson Library", "Old Main", 30),
        ("Old Main", "Police Dept.", 200),
        ("Old Main", "Fine Art", 90),
        ("Old Main", "McAlister Hall", 100),
        ("Police Dept.", "Fine Art", 50),
        ("Police Dept.", "Student Health Center", 100),
        ("Fine Art", "McAlister Hall", 180),
        ("Fine Art", "Student Center", 80),
        ("McAlister Hall", "Student Center", 100),
        ("McAlister Hall", "Wingo", 50),
        ("McAlister Hall", "Maintenance College", 150),
        ("Maintenance College", "Wingo", 100),
        ("Maintenance College", "New Business Building", 150),
        ("Maintenance College", "Oak Tree Apt.", 160),
        ("Student Center", "Student Health Center", 50),
        ("Student Center", "Wingo", 100),
        ("Student Center", "New Business Building", 110),
        ("Wingo", "New Business Building", 50),
        ("New Business Building", "Oak Tree Apt.", 30),
        ("New Business Building", "Brewer-Hegeman", 20),
        ("Oak Tree Apt.", "Brewer-Hegeman", 40),
        ("Student Health Center", "Brewer-Hegeman", 200),
        ("Brewer-Hegeman", "Bear village Apt.", 350)
    ]

    for start, end, weight in paths:
        graph.add_path(start, end, weight)

    return graph


def display_results(buildings, distances, paths):
    for building in buildings:
        distance = distances[building]
        distance_text = "Unreachable" if distance == float("inf") else str(distance)
        route = " -> ".join(paths[building]) if paths[building] else "No path"
        print(f"{building}: {distance_text} | {route}")


def main():
    graph = build_campus_graph()
    source = "Computer Science"
    buildings = graph.get_buildings()

    print(f"Campus graph: {len(buildings)} buildings, {len(graph.get_edges()) // 2} bidirectional paths")
    print(f"Source: {source}")

    d_distances, d_paths, d_negative_cycle = dijkstra(graph, source)

    if d_negative_cycle:
        raise ValueError("Dijkstra returned an unexpected negative cycle")

    b_distances, b_paths, b_negative_cycle = bellmanFord(graph, source)

    if b_negative_cycle:
        raise ValueError("Bellman-Ford detected a negative cycle")

    print("\nDIJKSTRA SHORTEST ROUTES:")
    display_results(buildings, d_distances, d_paths)

    print("\nBELLMAN-FORD SHORTEST ROUTES:")
    display_results(buildings, b_distances, b_paths)

    distances_match = d_distances == b_distances

    print("\nALGORITHM COMPARISON:")
    print("Dijkstra and Bellman-Ford distances match:", "Yes" if distances_match else "No")

    if not distances_match:
        for building in buildings:
            if d_distances[building] != b_distances[building]:
                print(f"{building}: Dijkstra={d_distances[building]}, Bellman-Ford={b_distances[building]}")

    return distances_match


if __name__ == "__main__":
    main()