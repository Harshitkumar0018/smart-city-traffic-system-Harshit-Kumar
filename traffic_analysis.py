import networkx as nx


def analyze_traffic(graph, source, destination, road_u, road_v, extra_cost):
    original_graph = graph.copy()
    updated_graph = graph.copy()

    try:
        original_path = nx.bellman_ford_path(
            original_graph, source, destination, weight="weight"
        )
        original_cost = nx.bellman_ford_path_length(
            original_graph, source, destination, weight="weight"
        )

        if updated_graph.has_edge(road_u, road_v):
            updated_graph[road_u][road_v]["weight"] += extra_cost

        updated_path = nx.bellman_ford_path(
            updated_graph, source, destination, weight="weight"
        )
        updated_cost = nx.bellman_ford_path_length(
            updated_graph, source, destination, weight="weight"
        )

        return original_path, original_cost, updated_path, updated_cost

    except (nx.NetworkXNoPath, nx.NodeNotFound):
        return None, float("inf"), None, float("inf")