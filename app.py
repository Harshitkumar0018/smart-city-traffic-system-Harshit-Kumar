import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

from route_planner import find_shortest_route
from traffic_analysis import analyze_traffic
from benchmark import benchmark_algorithms
from connectivity_module import (
    check_connectivity,
    get_bfs_traversal,
    get_dfs_traversal,
    get_connected_components,
)
from mst_planner import find_mst


# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="Smart City Traffic Management",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------- CUSTOM STYLE --------------------
st.markdown(
    """
    <style>
    .main {background-color: #f7f9fc;}
    [data-testid="stMetric"] {
        background: white;
        border: 1px solid #e8edf5;
        padding: 16px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(20, 40, 80, 0.04);
    }
    .block-container {padding-top: 1.6rem; padding-bottom: 2rem;}
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        min-height: 2.5rem;
    }
    .section-note {
        color: #64748b;
        font-size: 0.92rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# -------------------- CITY NETWORK --------------------
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
        ("A", "F", 15),
    ]
    graph.add_weighted_edges_from(roads, weight="weight")
    return graph


if "city" not in st.session_state:
    st.session_state.city = create_city()

G = st.session_state.city


# -------------------- GRAPH VISUALIZATION --------------------
def show_graph(graph, highlighted_edges=None, title=None):
    if graph.number_of_nodes() == 0:
        st.info("The road network is empty. Add intersections to get started.")
        return

    highlighted_edges = highlighted_edges or []
    pos = nx.spring_layout(graph, seed=42)

    fig, ax = plt.subplots(figsize=(10, 5.5))
    nx.draw_networkx_nodes(
        graph, pos, node_color="#bfdbfe", edgecolors="#2563eb",
        node_size=1050, linewidths=1.5, ax=ax
    )
    nx.draw_networkx_labels(
        graph, pos, font_size=11, font_weight="bold", ax=ax
    )

    normal_edges = [
        edge for edge in graph.edges()
        if edge not in highlighted_edges
        and (edge[1], edge[0]) not in highlighted_edges
    ]
    nx.draw_networkx_edges(
        graph, pos, edgelist=normal_edges, edge_color="#94a3b8",
        width=2, ax=ax
    )
    if highlighted_edges:
        nx.draw_networkx_edges(
            graph, pos, edgelist=highlighted_edges,
            edge_color="#ef4444", width=4, ax=ax
        )

    labels = nx.get_edge_attributes(graph, "weight")
    nx.draw_networkx_edge_labels(
        graph, pos, edge_labels=labels, font_size=9, ax=ax
    )
    ax.set_title(title or "City Road Network", fontsize=14, fontweight="bold")
    ax.axis("off")
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


def safe_connected(graph):
    return graph.number_of_nodes() > 0 and nx.is_connected(graph)


def format_path(path):
    return " → ".join(map(str, path))


# -------------------- SIDEBAR --------------------
st.sidebar.title("🚦 Smart City")
st.sidebar.caption("Traffic and Road Network Control")
page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Dashboard",
        "Road Network",
        "Route Planning",
        "Traffic Management",
        "Network Connectivity",
        "Infrastructure Planning",
        "Performance Analysis",
    ],
)
st.sidebar.divider()
st.sidebar.metric("Intersections", G.number_of_nodes())
st.sidebar.metric("Roads", G.number_of_edges())
if st.sidebar.button("Reset City Network", use_container_width=True):
    st.session_state.city = create_city()
    st.rerun()


# -------------------- DASHBOARD --------------------
if page == "Dashboard":
    st.title("🚦 Smart City Traffic Management System")
    st.markdown(
        '<p class="section-note">An interactive graph-based system for route '
        'optimization, traffic simulation and infrastructure planning.</p>',
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Intersections", G.number_of_nodes())
    c2.metric("Roads", G.number_of_edges())
    c3.metric("Network Status", "Connected" if safe_connected(G) else "Disconnected")
    c4.metric("Connected Components", len(get_connected_components(G)) if G else 0)

    st.subheader("City Road Network")
    show_graph(G)

    left, right = st.columns(2)
    with left:
        st.info(
            "**Route Planning**\n\nFind the minimum-cost path between two "
            "intersections using Dijkstra's algorithm."
        )
        st.info(
            "**Traffic Management**\n\nSimulate congestion or a road closure "
            "and compare the route before and after the change."
        )
    with right:
        st.info(
            "**Network Connectivity**\n\nExplore BFS, DFS and connected "
            "components in the city network."
        )
        st.info(
            "**Infrastructure Planning**\n\nUse Prim's or Kruskal's algorithm "
            "to find a minimum spanning tree."
        )


# -------------------- ROAD NETWORK --------------------
elif page == "Road Network":
    st.title("🛣️ Road Network Management")
    st.caption("Add intersections and roads to customize the city graph.")

    with st.form("node_form", clear_on_submit=True):
        new_node = st.text_input("Intersection name", placeholder="Example: G")
        add_node = st.form_submit_button("＋ Add Intersection")

    if add_node:
        new_node = new_node.strip()
        if not new_node:
            st.warning("Please enter an intersection name.")
        elif new_node in G:
            st.warning("This intersection already exists.")
        else:
            G.add_node(new_node)
            st.success(f"Intersection {new_node} added.")
            st.rerun()

    nodes = sorted(G.nodes(), key=str)
    st.subheader("Connect two intersections")
    if len(nodes) >= 2:
        with st.form("road_form", clear_on_submit=True):
            col1, col2, col3 = st.columns(3)
            with col1:
                source = st.selectbox("Starting intersection", nodes)
            with col2:
                destination = st.selectbox("Ending intersection", nodes, index=1)
            with col3:
                weight = st.number_input("Road cost / distance", min_value=0.1, value=1.0, step=0.5)
            add_road = st.form_submit_button("＋ Add / Update Road")

        if add_road:
            if source == destination:
                st.warning("Select two different intersections.")
            else:
                G.add_edge(source, destination, weight=float(weight))
                st.success(f"Road {source} — {destination} saved.")
                st.rerun()
    else:
        st.info("Add at least two intersections before connecting roads.")

    st.subheader("Current Road Network")
    show_graph(G)

    if G.number_of_edges():
        road_rows = [
            {"Starting Point": u, "Ending Point": v, "Cost": data.get("weight", 1)}
            for u, v, data in G.edges(data=True)
        ]
        st.dataframe(pd.DataFrame(road_rows), use_container_width=True, hide_index=True)

        with st.expander("Remove a road"):
            road_options = list(G.edges())
            selected_road = st.selectbox(
                "Choose road",
                road_options,
                format_func=lambda edge: f"{edge[0]} — {edge[1]}",
            )
            if st.button("Remove Selected Road"):
                G.remove_edge(*selected_road)
                st.success("Road removed.")
                st.rerun()

    with st.expander("Network Data: Adjacency List and Matrix"):
        st.write("**Adjacency List**")
        st.json({
            str(node): {
                str(neighbor): data.get("weight", 1)
                for neighbor, data in G[node].items()
            }
            for node in G.nodes()
        })
        st.write("**Adjacency Matrix**")
        st.dataframe(nx.to_pandas_adjacency(G, weight="weight"), use_container_width=True)


# -------------------- ROUTE PLANNING --------------------
elif page == "Route Planning":
    st.title("📍 Shortest Route Planning")
    st.caption("Dijkstra's algorithm finds the minimum-cost route between two intersections.")

    nodes = sorted(G.nodes(), key=str)
    if len(nodes) < 2:
        st.warning("Add at least two intersections in Road Network.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            source = st.selectbox("Journey starts at", nodes, key="route_source")
        with col2:
            destination = st.selectbox("Journey ends at", nodes, key="route_destination")

        if st.button("Find Shortest Route", type="primary"):
            if source == destination:
                st.warning("Starting point and destination must be different.")
            else:
                route, distance = find_shortest_route(G, source, destination)
                if route is not None:
                    m1, m2 = st.columns(2)
                    m1.metric("Minimum Travel Cost", f"{distance:g}")
                    m2.metric("Roads in Route", max(0, len(route) - 1))
                    st.success(format_path(route))
                    show_graph(
                        G,
                        highlighted_edges=list(zip(route, route[1:])),
                        title="Shortest Route Highlighted",
                    )
                    st.write("**Route steps**")
                    for index, location in enumerate(route, start=1):
                        st.write(f"{index}. {location}")
                else:
                    st.error("No route exists between these intersections.")


# -------------------- TRAFFIC MANAGEMENT --------------------
elif page == "Traffic Management":
    st.title("🚧 Traffic Management and Road Disruption")
    st.caption("Compare the original route with a route after congestion or road closure.")

    nodes = sorted(G.nodes(), key=str)
    edges = list(G.edges(data=True))

    if len(nodes) < 2 or not edges:
        st.warning("The network needs at least two intersections and one road.")
    else:
        mode = st.radio(
            "Choose traffic scenario",
            ["Congestion on a road", "Road closure"],
            horizontal=True,
        )
        road_index = st.selectbox(
            "Select affected road",
            range(len(edges)),
            format_func=lambda i: (
                f"{edges[i][0]} — {edges[i][1]} "
                f"(current cost: {edges[i][2].get('weight', 1)})"
            ),
        )
        source_col, destination_col = st.columns(2)
        with source_col:
            source = st.selectbox("Journey source", nodes, key="traffic_source")
        with destination_col:
            destination = st.selectbox("Journey destination", nodes, key="traffic_destination")

        extra_cost = 0.0
        if mode == "Congestion on a road":
            extra_cost = st.number_input(
                "Additional congestion cost",
                min_value=0.0,
                value=5.0,
                step=1.0,
            )

        if st.button("Simulate Traffic Change", type="primary"):
            if source == destination:
                st.warning("Choose different starting and ending intersections.")
            else:
                u, v, data = edges[road_index]
                original_path, original_cost = find_shortest_route(G, source, destination)

                changed_graph = G.copy()
                if mode == "Congestion on a road":
                    changed_graph[u][v]["weight"] += extra_cost
                else:
                    changed_graph.remove_edge(u, v)

                if original_path is None:
                    st.error("No original route exists for this journey.")
                else:
                    if nx.has_path(changed_graph, source, destination):
                        changed_path = nx.dijkstra_path(
                            changed_graph, source, destination, weight="weight"
                        )
                        changed_cost = nx.dijkstra_path_length(
                            changed_graph, source, destination, weight="weight"
                        )
                        a, b = st.columns(2)
                        a.metric("Original Route Cost", f"{original_cost:g}")
                        b.metric("Updated Route Cost", f"{changed_cost:g}", delta=f"{changed_cost-original_cost:+g}")
                        st.write("**Original route:**", format_path(original_path))
                        st.write("**Updated route:**", format_path(changed_path))
                        st.success(
                            "An alternate route is available."
                            if changed_path != original_path
                            else "The same route remains the best available option."
                        )
                        show_graph(
                            changed_graph,
                            highlighted_edges=list(zip(changed_path, changed_path[1:])),
                            title=f"Network After {mode}",
                        )
                    else:
                        st.error("No alternate route is available after this change.")
                        st.write("Original route:", format_path(original_path))
                        show_graph(changed_graph, title="Network After Road Disruption")


# -------------------- CONNECTIVITY --------------------
elif page == "Network Connectivity":
    st.title("🔗 Network Connectivity")
    st.caption("Explore graph traversal and connectivity using BFS and DFS.")

    nodes = sorted(G.nodes(), key=str)
    connected = safe_connected(G)
    c1, c2, c3 = st.columns(3)
    c1.metric("Network Connected", "Yes" if connected else "No")
    c2.metric("Connected Components", len(get_connected_components(G)) if G else 0)
    c3.metric("Total Intersections", G.number_of_nodes())

    if nodes:
        start = st.selectbox("Traversal starting intersection", nodes)
        bfs_col, dfs_col = st.columns(2)
        with bfs_col:
            if st.button("Run BFS", use_container_width=True):
                order = get_bfs_traversal(G, start)
                st.subheader("BFS Traversal")
                st.success(format_path(order))
                st.write(f"Intersections reached: {len(order)}")
        with dfs_col:
            if st.button("Run DFS", use_container_width=True):
                order = get_dfs_traversal(G, start)
                st.subheader("DFS Traversal")
                st.success(format_path(order))
                st.write(f"Intersections reached: {len(order)}")

    st.subheader("Connected Components")
    components = get_connected_components(G)
    for index, component in enumerate(components, start=1):
        st.write(f"**Component {index}:** {', '.join(map(str, sorted(component, key=str)))}")
    show_graph(G)


# -------------------- INFRASTRUCTURE PLANNING --------------------
elif page == "Infrastructure Planning":
    st.title("🏗️ Infrastructure Planning")
    st.caption("Find a Minimum Spanning Tree using Prim's or Kruskal's algorithm.")

    if G.number_of_nodes() == 0:
        st.info("Add intersections to begin infrastructure planning.")
    else:
        algorithm = st.selectbox("Select algorithm", ["Prim", "Kruskal"])
        mst, total_cost = find_mst(G, algorithm.lower())

        if not safe_connected(G):
            st.warning(
                "The network is disconnected. The result is a minimum spanning "
                "forest for the available connected components."
            )

        st.metric("Total Infrastructure Cost", f"{total_cost:g}")
        st.subheader("Selected Roads")
        mst_rows = [
            {"Road": f"{u} — {v}", "Cost": data.get("weight", 1)}
            for u, v, data in mst.edges(data=True)
        ]
        if mst_rows:
            st.dataframe(pd.DataFrame(mst_rows), use_container_width=True, hide_index=True)
        else:
            st.info("No roads are available for the spanning tree.")
        show_graph(mst, title=f"{algorithm} Minimum Spanning Tree")


# -------------------- PERFORMANCE ANALYSIS --------------------
elif page == "Performance Analysis":
    st.title("📊 Algorithm Performance Analysis")
    st.caption("Compare execution time for BFS, DFS, Dijkstra, Bellman-Ford, Prim and Kruskal.")

    st.write(
        "The benchmark tests networks with different numbers of intersections. "
        "Execution time can vary between runs and depends on the computer."
    )

    if st.button("Run Benchmark", type="primary"):
        with st.spinner("Running algorithm benchmarks..."):
            results = benchmark_algorithms()
        st.session_state.benchmark_results = results

    if "benchmark_results" in st.session_state:
        results = st.session_state.benchmark_results
        st.success("Benchmark completed.")
        st.dataframe(results, use_container_width=True, hide_index=True)

        st.subheader("Execution Time Comparison")
        chart_data = results.pivot(
            index="Intersections",
            columns="Algorithm",
            values="Execution Time (ms)",
        )
        st.line_chart(chart_data, use_container_width=True)

        st.subheader("Compare algorithms for one network size")
        sizes = sorted(results["Intersections"].unique())
        selected_size = st.selectbox("Number of intersections", sizes)
        size_data = results[results["Intersections"] == selected_size].set_index("Algorithm")
        st.bar_chart(size_data["Execution Time (ms)"], use_container_width=True)

        st.download_button(
            "⬇️ Download Benchmark CSV",
            data=results.to_csv(index=False).encode("utf-8"),
            file_name="smart_city_benchmark_results.csv",
            mime="text/csv",
        )
    else:
        st.info("Click **Run Benchmark** to generate the performance results.")
