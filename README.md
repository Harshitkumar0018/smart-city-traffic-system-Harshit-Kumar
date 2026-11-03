# 🚦 Smart City Traffic Management System

### A Graph-Based Approach to Smart Routing and Traffic Optimization

A Python-based project that demonstrates how graph algorithms can be used to model city road networks, find efficient routes, analyze traffic conditions, and plan connected infrastructure.

The project provides an interactive **Streamlit web application** where users can manage intersections and roads, calculate shortest paths, simulate traffic congestion, analyze network connectivity, and compare algorithm performance.

---

## 📌 Project Overview

In a city, finding an efficient route between two locations can become difficult due to road networks, traffic congestion, and road closures.

This project models a city's road network as a **weighted graph**, where:

* **Vertices (Nodes):** Represent city intersections.
* **Edges:** Represent roads connecting intersections.
* **Weights:** Represent travel time or road cost.

Different graph algorithms are implemented to solve routing, connectivity, and infrastructure planning problems.

## 🎯 Objectives

* Model a city road network using graph structures.
* Find the shortest and minimum-cost route between intersections.
* Simulate traffic congestion and road closures.
* Analyze network connectivity using BFS and DFS.
* Find Minimum Spanning Trees using Prim's and Kruskal's algorithms.
* Compare the performance of different algorithms.
* Display results through an interactive web interface.

## ✨ Key Features

### 1. Road Network Management

* Add and manage city intersections.
* Add, update, and remove roads.
* View the road network graph.
* Display adjacency lists and adjacency matrices.

### 2. Shortest Route Planning

* Calculate the shortest route between two intersections.
* Use Dijkstra's algorithm.
* Display the selected route and total travel cost.

### 3. Traffic Management

* Simulate traffic congestion by increasing road costs.
* Simulate road closures.
* Compare routes before and after traffic changes.
* Display the updated route and travel cost.

### 4. Network Connectivity

* Perform Breadth First Search (BFS).
* Perform Depth First Search (DFS).
* Identify reachable intersections.
* Analyze network connectivity.

### 5. Infrastructure Planning

* Generate a Minimum Spanning Tree (MST).
* Implement Prim's algorithm.
* Implement Kruskal's algorithm.
* Compare infrastructure costs.

### 6. Performance Analysis

* Compare multiple graph algorithms.
* Measure execution time.
* Analyze performance across different graph sizes.
* Display comparison charts.
* Export benchmark results as CSV.

## 🧠 Algorithms Implemented

| Algorithm           | Purpose                          | Time Complexity  |
| ------------------- | -------------------------------- | ---------------- |
| Dijkstra            | Shortest route calculation       | O((V + E) log V) |
| Bellman-Ford        | Shortest-path calculation        | O(V × E)         |
| BFS                 | Graph traversal and reachability | O(V + E)         |
| DFS                 | Graph traversal and connectivity | O(V + E)         |
| Prim's Algorithm    | Minimum Spanning Tree            | O(E log V)       |
| Kruskal's Algorithm | Minimum Spanning Tree            | O(E log E)       |

**Where:**

* V = Number of vertices
* E = Number of edges

*Complexities depend on the implementation and underlying data structures.*

## 🛠️ Technologies Used

| Technology       | Purpose                               |
| ---------------- | ------------------------------------- |
| Python           | Core programming language             |
| Streamlit        | Interactive web application           |
| NetworkX         | Graph representation and operations   |
| Pandas           | Data handling and analysis            |
| NumPy            | Numerical operations                  |
| Matplotlib       | Graphs and visualizations             |
| Jupyter Notebook | Algorithm demonstrations and analysis |
| Git & GitHub     | Version control and project hosting   |

## 📂 Project Structure

```text
Smart-City-Traffic-Management-System/
│
├── app.py
├── benchmark.py
├── connectivity_module.py
├── mst_planner.py
├── route_planner.py
├── traffic_analysis.py
│
├── project_notebook.ipynb
├── requirements.txt
│
├── Screenshots1/
│   └── Screenshots/
│       ├── 01_Dashboard_Full.png
│       ├── 02_Road_Network_Full.png
│       ├── 03_Shortest_Route_Dijkstra_Full.png
│       ├── 04_Traffic_Road_Congestion_Full.png
│       ├── 05_Traffic_Road_Closure_Full.png
│       ├── 06_Network_Connectivity_BFS_Full.png
│       ├── 07_Network_Connectivity_DFS_Full.png
│       ├── 08_Prims_MST_FULL.png
│       ├── 09_Kruskal_MST_Full.png
│       ├── 10_Benchmark_Results_Full.png
│       ├── 11_Execution_Time_Comparison_Full.png
│       ├── 12_Algorithm_Comparison_Chart_Full.png
│       └── 13_Adjacency_Matrix_Full.png
│
└── README.md
```

## ⚙️ Installation and Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/Harshitkumar0018/smart-city-traffic-system-Harshit-Kumar.git
```

### Step 2: Open the Project Folder

```bash
cd smart-city-traffic-system-Harshit-Kumar
```

### Step 3: Create a Virtual Environment

```bash
python -m venv venv
```

### Step 4: Activate the Virtual Environment

**Windows:**

```bash
venv\Scripts\activate
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 6: Run the Application

```bash
streamlit run app.py
```

The application will open in your browser, usually at:

**http://localhost:8501**

## 📊 Performance Analysis

The project includes a benchmarking module to compare the execution performance of different graph algorithms.

The performance analysis focuses on:

* Execution time comparison.
* Algorithm performance on different graph sizes.
* Comparison of graph traversal algorithms.
* Comparison of shortest-path algorithms.
* Visualization of benchmark results.

Benchmark results can also be exported in CSV format for further analysis.

## 📸 Application Screenshots

The `Screenshots1/Screenshots/` directory contains screenshots captured during application testing.

These screenshots demonstrate:

1. Main Dashboard
2. Road Network Management
3. Dijkstra Shortest Route
4. Traffic Congestion Simulation
5. Road Closure and Route Updating
6. BFS Network Traversal
7. DFS Network Traversal
8. Prim's Minimum Spanning Tree
9. Kruskal's Minimum Spanning Tree
10. Benchmark Results
11. Execution Time Comparison
12. Algorithm Comparison Chart
13. Adjacency Matrix

## 🔮 Future Enhancements

* Integration with real-time traffic data.
* GPS-based route tracking.
* Live traffic congestion detection.
* Interactive geographical maps.
* Machine Learning-based traffic prediction.
* Dynamic route recommendations.

## 🎓 Academic Information

| Detail        | Information                                     |
| ------------- | ----------------------------------------------- |
| Project Title | Smart City Traffic Management System            |
| Course        | Design and Analysis of Algorithms Lab (ENCA351) |
| Program       | BCA (Artificial Intelligence & Data Science)    |
| Semester      | V                                               |
| University    | K.R. Mangalam University                        |

## 👨‍💻 Author

**Harshit Kumar**

BCA (Artificial Intelligence & Data Science)
K.R. Mangalam University

## 📚 References

* Python Documentation
* Streamlit Documentation
* NetworkX Documentation
* Pandas Documentation
* NumPy Documentation
* Matplotlib Documentation
