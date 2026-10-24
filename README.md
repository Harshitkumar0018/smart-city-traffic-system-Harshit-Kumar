# Smart City Traffic Management System

## Project Overview
The Smart City Traffic Management System models a city's road network as a weighted graph. It uses graph algorithms to find shortest routes, analyze traffic changes, check network connectivity, and plan cost-effective road infrastructure.

## Technologies Used
- Python
- Streamlit
- NetworkX
- Pandas
- NumPy
- Matplotlib
- Jupyter Notebook

## Algorithms Implemented
1. Dijkstra's Algorithm – Finds the shortest route.
2. Bellman-Ford Algorithm – Analyzes route changes after traffic costs increase.
3. BFS – Traverses the road network.
4. DFS – Explores the road network.
5. Prim's Algorithm – Finds a minimum spanning tree.
6. Kruskal's Algorithm – Finds a minimum spanning tree.
7. Performance Benchmarking – Compares execution time for different graph sizes.

## Project Structure
- `app.py` – Streamlit application.
- `route_planner.py` – Shortest route planning.
- `traffic_analysis.py` – Traffic analysis.
- `benchmark.py` – Algorithm performance benchmarking.
- `project_notebook.ipynb` – Algorithm demonstrations and analysis.
- `requirements.txt` – Python dependencies.
- `screenshots/` – Application screenshots.

## Installation
1. Clone or download this repository.
2. Create and activate a Python virtual environment.
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Run the Application

```bash
streamlit run app.py
```

## Performance Analysis
The project compares BFS, DFS, Dijkstra, Bellman-Ford, Prim, and Kruskal using graphs with 10, 25, 50, and 100 intersections.

Execution times can vary depending on the system and runtime conditions.

## Author
Harshit Kumar 
2401201057
BCA (AI & Data Science)-B 