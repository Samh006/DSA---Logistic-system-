Graph based route planning

This module implements a graph based route planner to optimize
delivery routes. This network is modeled as a weighted,
undirected graph with nodes, hubs and edges as roads with
travel times.

FILES:
- Graph.py: Implements the Graph system with adjacency list and
  algorithms (BFS, DFS, Dijkstra’s)

- Linked_list.py: provides a data structure for adjacency lists

- GraphVertex.py: Defines the graph nodes and also the edge class

- Queue: Implements a shuffle queue for BFS

- Module1_test.py: Tests the graph with hard coded data

SAMPLE GRAPH:
8 nodes, A-H. 11 edges, H is disconnected, includes a cycle

HOW TO TEST:
linux environment: from desktop change directory to the root
folder, then type python3 -m Module1.Module1_test

Pycharm: Set the main directory to the source root, run the
test file.