import networkx as nx

def check_connectivity(graph):
    return nx.is_connected(graph)

def get_bfs_traversal(graph, source):
    return list(nx.bfs_tree(graph, source).nodes())

def get_dfs_traversal(graph, source):
    return list(nx.dfs_tree(graph, source).nodes())

def get_connected_components(graph):
    return list(nx.connected_components(graph))