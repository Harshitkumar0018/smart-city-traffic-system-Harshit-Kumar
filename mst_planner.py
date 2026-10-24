import networkx as nx

def find_mst(graph, algorithm="prim"):
    if algorithm not in ("prim", "kruskal"):
        raise ValueError("Algorithm must be 'prim' or 'kruskal'")

    mst = nx.minimum_spanning_tree(
        graph, algorithm=algorithm, weight="weight"
    )

    total_cost = mst.size(weight="weight")
    return mst, total_cost

def get_mst_edges(graph, algorithm="prim"):
    mst, total_cost = find_mst(graph, algorithm)
    return list(mst.edges(data=True)), total_cost