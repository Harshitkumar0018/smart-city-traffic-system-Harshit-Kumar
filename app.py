import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

from route_planner import find_shortest_route
from traffic_analysis import analyze_traffic
from benchmark import benchmark_algorithms
from connectivity_module import (
    check_connectivity,
    get_bfs_traversal,
    get_dfs_traversal,
    get_connected_components
)
from mst_planner import find_mst


st.set_page_config(
    page_title="Smart City Traffic Management",
    page_icon="🚦",
    layout="wide"
)


def create_city():
    graph = nx.Graph()
    roads = [
        ("A", "B", 4),
        ("A", "C", 2),
        ("B", "C", 1),
        ("B", "D", 5),
        ("C", "D", 8),
        ("C", "E", 10),
        ("D", "E", 2),
        ("D", "F", 6),
        ("E", "F", 3),
        ("A", "F", 15)
    ]
    graph.add_weighted_edges_from(roads)
    return graph


if "city" not in st.session_state:
    st.session_state.city = create_city()

G = st.session_state.city


def show_graph(graph, highlighted_edges=None):
    pos = nx.spring_layout(graph, seed=42)
    fig, ax = plt.subplots(figsize=(9, 5))

    nx.draw_networkx_nodes(
        graph, pos,
        node_color="lightblue",
        node_size=900,
        ax=ax
    )

    nx.draw_networkx_labels(graph, pos, ax=ax)

    nx.draw_networkx_edges(
        graph, pos,
        edge_color="gray",
        width=2,
        ax=ax
    )

    if highlighted_edges:
        nx.draw_networkx_edges(
            graph, pos,
            edgelist=highlighted_edges,
            edge_color="red",
            width=4,
            ax=ax
        )

    labels = nx.get_edge_attributes(graph, "weight")

    nx.draw_networkx_edge_labels(
        graph, pos,
        edge_labels=labels,
        ax=ax
    )

    ax.set_axis_off()
    st.pyplot(fig)
    plt.close(fig)


st.title("🚦 Smart City Traffic Management System")
st.caption("Graph Algorithms for Intelligent Traffic Optimization")

page = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "Road Network",
        "Route Planning",
        "Traffic Analysis",
        "Network Connectivity",
        "Infrastructure Planning",
        "Performance Comparison"
    ]
)


# HOME
if page == "Home":
    st.header("City Traffic Dashboard")

    col1, col2, col3 = st.columns(3)
    col1.metric("Intersections", G.number_of_nodes())
    col2.metric("Roads", G.number_of_edges())
    col3.metric(
        "Network Status",
        "Connected" if check_connectivity(G) else "Disconnected"
    )

    st.info("Manage roads and optimize routes across the city.")
    show_graph(G)


# ROAD NETWORK
elif page == "Road Network":
    st.header("Road Network Modeling")

    with st.form("node_form"):
        new_node = st.text_input("New intersection name")
        add_node = st.form_submit_button("Add Intersection")

    if add_node:
        new_node = new_node.strip()

        if not new_node:
            st.warning("Enter an intersection name.")
        elif new_node in G:
            st.warning("Intersection already exists.")
        else:
            G.add_node(new_node)
            st.success("Intersection added.")
            st.rerun()

    nodes = sorted(G.nodes(), key=str)

    with st.form("road_form"):
        source = st.selectbox("Starting intersection", nodes)
        destination = st.selectbox("Ending intersection", nodes)
        weight = st.number_input("Road cost", min_value=0.1, value=1.0)
        add_road = st.form_submit_button("Add Road")

    if add_road:
        if source == destination:
            st.warning("Choose different intersections.")
        else:
            G.add_edge(source, destination, weight=weight)
            st.success("Road added.")
            st.rerun()

    show_graph(G)

    st.subheader("Adjacency List")
    st.json({
        str(node): {
            str(neighbor): data["weight"]
            for neighbor, data in G[node].items()
        }
        for node in G.nodes()
    })

    st.subheader("Adjacency Matrix")
    st.dataframe(nx.to_pandas_adjacency(G, weight="weight"))


# DIJKSTRA
elif page == "Route Planning":
    st.header("Route Planning - Dijkstra Algorithm")
    nodes = sorted(G.nodes(), key=str)

    if len(nodes) < 2:
        st.warning("Add at least two intersections.")
    else:
        source = st.selectbox("Source", nodes, key="route_source")
        destination = st.selectbox(
            "Destination", nodes, key="route_destination"
        )

        if st.button("Find Shortest Route"):
            if source == destination:
                st.warning("Choose different locations.")
            else:
                route, distance = find_shortest_route(
                    G, source, destination
                )

                if route is not None:
                    st.success("Shortest route found!")
                    st.write("Route:", " -> ".join(route))
                    st.metric("Total Travel Cost", f"{distance:g}")

                    show_graph(
                        G,
                        list(zip(route, route[1:]))
                    )
                else:
                    st.error("No route found.")


# BELLMAN-FORD
elif page == "Traffic Analysis":
    st.header("Traffic Analysis - Bellman-Ford")

    edges = list(G.edges(data=True))
    nodes = sorted(G.nodes(), key=str)

    if not edges:
        st.warning("No roads available.")
    elif len(nodes) < 2:
        st.warning("Add at least two intersections.")
    else:
        selected = st.selectbox(
            "Select road for congestion",
            range(len(edges)),
            format_func=lambda i: (
                f"{edges[i][0]} - {edges[i][1]} "
                f"(cost {edges[i][2]['weight']})"
            )
        )

        extra_cost = st.number_input(
            "Additional congestion cost",
            min_value=0.0,
            value=5.0
        )

        source = st.selectbox(
            "Journey source", nodes, key="traffic_source"
        )
        destination = st.selectbox(
            "Journey destination", nodes, key="traffic_destination"
        )

        if st.button("Analyze Traffic"):
            if source == destination:
                st.warning("Choose different locations.")
            else:
                u, v, data = edges[selected]

                old_path, old_cost, new_path, new_cost = analyze_traffic(
                    G, source, destination,
                    u, v, extra_cost
                )

                if old_path is not None and new_path is not None:
                    st.subheader("Original Route")
                    st.write(" -> ".join(old_path))
                    st.metric("Original Cost", f"{old_cost:g}")

                    st.subheader("Route After Congestion")
                    st.write(" -> ".join(new_path))
                    st.metric("Updated Cost", f"{new_cost:g}")

                    st.metric(
                        "Change in Cost",
                        f"{new_cost - old_cost:g}"
                    )

                    updated_graph = G.copy()
                    updated_graph[u][v]["weight"] += extra_cost

                    show_graph(
                        updated_graph,
                        list(zip(new_path, new_path[1:]))
                    )
                else:
                    st.error("No route found.")


# BFS AND DFS
elif page == "Network Connectivity":
    st.header("Network Connectivity - BFS and DFS")

    nodes = sorted(G.nodes(), key=str)

    st.write(
        "Network Connected:",
        "Yes" if check_connectivity(G) else "No"
    )

    st.metric("Total Intersections", G.number_of_nodes())
    st.metric("Connected Components", len(
        get_connected_components(G)
    ))

    if nodes:
        start = st.selectbox(
            "Starting intersection", nodes, key="connectivity_start"
        )

        col1, col2 = st.columns(2)

        if col1.button("Run BFS"):
            order = get_bfs_traversal(G, start)
            st.subheader("BFS Traversal")
            st.write(" -> ".join(order))
            st.write("Reachable intersections:", len(order))

        if col2.button("Run DFS"):
            order = get_dfs_traversal(G, start)
            st.subheader("DFS Traversal")
            st.write(" -> ".join(order))
            st.write("Reachable intersections:", len(order))

        show_graph(G)


# PRIM AND KRUSKAL
elif page == "Infrastructure Planning":
    st.header("Infrastructure Planning - Minimum Spanning Tree")

    algorithm = st.selectbox(
        "Select Algorithm", ["Prim", "Kruskal"]
    )

    mst, total_cost = find_mst(G, algorithm.lower())

    st.metric("Total Infrastructure Cost", f"{total_cost:g}")

    st.subheader("Selected Roads")

    st.dataframe([
        {
            "Road": f"{u} - {v}",
            "Cost": data["weight"]
        }
        for u, v, data in mst.edges(data=True)
    ])

    show_graph(mst)


# PERFORMANCE COMPARISON
elif page == "Performance Comparison":
    st.header("Algorithm Performance Comparison")

    st.write(
        "Compare BFS, DFS, Dijkstra, Bellman-Ford, Prim and Kruskal "
        "on networks of different sizes."
    )

    if st.button("Run Benchmark"):
        with st.spinner("Running experiments..."):
            results = benchmark_algorithms()

        st.success("Benchmark completed!")
        st.subheader("Execution Time Results")
        st.dataframe(results, width="stretch")

        st.subheader("Algorithm Execution Time")

        chart_data = results.pivot(
            index="Intersections",
            columns="Algorithm",
            values="Execution Time (ms)"
        )

        st.line_chart(chart_data)

        st.download_button(
            "Download Results CSV",
            results.to_csv(index=False),
            file_name="benchmark_results.csv",
            mime="text/csv"
        )