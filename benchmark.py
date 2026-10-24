import time
import networkx as nx
import pandas as pd


def benchmark_algorithms(sizes=(10, 25, 50, 100)):
    results = []

    for size in sizes:
        graph = nx.gnm_random_graph(
            size, min(size * 3, size * (size - 1) // 2),
            seed=42
        )

        for u, v in graph.edges():
            graph[u][v]["weight"] = 1 + (u + v) % 20

        source = 0
        destination = size - 1

        algorithms = {
            "BFS": lambda: list(nx.bfs_tree(graph, source)),
            "DFS": lambda: list(nx.dfs_tree(graph, source)),
            "Dijkstra": lambda: nx.single_source_dijkstra(
                graph, source, target=destination, weight="weight"
            ),
            "Bellman-Ford": lambda: nx.single_source_bellman_ford(
                graph, source, target=destination, weight="weight"
            ),
            "Prim": lambda: nx.minimum_spanning_tree(
                graph, algorithm="prim", weight="weight"
            ),
            "Kruskal": lambda: nx.minimum_spanning_tree(
                graph, algorithm="kruskal", weight="weight"
            )
        }

        for name, algorithm in algorithms.items():
            start = time.perf_counter()
            algorithm()
            elapsed = time.perf_counter() - start

            results.append({
                "Intersections": size,
                "Roads": graph.number_of_edges(),
                "Algorithm": name,
                "Execution Time (ms)": round(elapsed * 1000, 4)
            })

    return pd.DataFrame(results)