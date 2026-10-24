import networkx as nx

def find_shortest_route(graph, source, destination):
    try:
        route = nx.dijkstra_path(graph, source, destination, weight="weight")
        distance = nx.dijkstra_path_length(graph, source, destination, weight="weight")
        return route, distance
    except (nx.NetworkXNoPath, nx.NodeNotFound):
        return None, float("inf")