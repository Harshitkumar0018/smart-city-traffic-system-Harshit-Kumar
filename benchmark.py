import time
import tracemalloc

import networkx as nx
import pandas as pd


def benchmark_algorithms(sizes=(10, 25, 50, 100)):
    """Measure execution time and peak Python memory for six graph algorithms."""
    results = []

    for size in sizes:
        graph = nx.gnm_random_graph(
            size,
            min(size * 3, size * (size - 1) // 2),
            seed=42,
        )

        for u, v in graph.edges():
            graph[u][v]["weight"] = 1 + (u + v) % 20

        source = 0
        destination = size - 1

        # Ensure shortest-path algorithms have a valid source-destination path.
        if not nx.has_path(graph, source, destination):
            graph.add_edge(source, destination, weight=20)

        algorithms = {
            "BFS": lambda: list(nx.bfs_tree(graph, source)),
            "DFS": lambda: list(nx.dfs_tree(graph, source)),
            "Dijkstra": lambda: nx.dijkstra_path(
                graph, source, destination, weight="weight"
            ),
            "Bellman-Ford": lambda: nx.bellman_ford_path(
                graph, source, destination, weight="weight"
            ),
            "Prim": lambda: nx.minimum_spanning_tree(
                graph, algorithm="prim", weight="weight"
            ),
            "Kruskal": lambda: nx.minimum_spanning_tree(
                graph, algorithm="kruskal", weight="weight"
            ),
        }

        for name, algorithm in algorithms.items():
            tracemalloc.start()
            start = time.perf_counter()
            algorithm()
            elapsed = time.perf_counter() - start
            _, peak_memory = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            results.append(
                {
                    "Intersections": size,
                    "Roads": graph.number_of_edges(),
                    "Algorithm": name,
                    "Execution Time (ms)": round(elapsed * 1000, 4),
                    "Peak Memory (KB)": round(peak_memory / 1024, 2),
                }
            )

    return pd.DataFrame(results)
