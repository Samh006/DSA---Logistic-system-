import numpy as np
from Module1.Linked_list import DSALinkedList
from Module1.Queue import DSASqueue
from Module1.GraphVertex import DSAGraphVertex, VertexLevelPair, DijkstraResult

class GraphErrorHandle(Exception):
    pass

"""Graph class using adjacency list for route planning."""
class DSAGraph:
    def __init__(self):
        self.vertices = DSALinkedList()  # Create a linked list to store vertices

    def hasVertex(self, label):        # Check if a vertex exists in the graph
        current = self.vertices.head   # Start at the head of the vertices list
        while current:
            if current.getValue().getLabel() == label:  # Check if current vertex label matches
                return True                             # Return True if vertex is found
            current = current.getNext()                 # Move to the next node
        return False

    def getVertex(self, label):               # Retrieve a vertex by its label
        current = self.vertices.head          # Start at the head of the vertices list
        while current:                        # Iterate through the linked list
            vertex = current.getValue()       # Get the vertex object from the current node
            if vertex.getLabel() == label:    # Check if the vertex label matches
                return vertex                 # Return the vertex object
            current = current.getNext()       # Move to the next node
        raise GraphErrorHandle(f"Vertex '{label}' not found")

    def addVertex(self, label):             # Add a new vertex to the graph
        if self.hasVertex(label):           # Check if vertex already exists
            raise GraphErrorHandle(f"Vertex '{label}' already exists")
        self.vertices.insertLast(DSAGraphVertex(label))  # Create and insert new vertex at t
        return True                                      # Return True to indicate success

    def addEdge(self, label1, label2, weight=1):  # Add an undirected edge between two vertices
        if not self.hasVertex(label1) or not self.hasVertex(label2):  # Check if both vertices exist
            raise GraphErrorHandle("One or both vertices not found")
        if label1 == label2:                                          # Check if the edge is a self-loop
            raise GraphErrorHandle("Cannot create edge to self")
        if self.isAdjacent(label1, label2):                           # Check if edge already exists
            raise GraphErrorHandle("Edge already exists")
        vertex1 = self.getVertex(label1)  # Get the first vertex object
        vertex2 = self.getVertex(label2)  # Get the second vertex object
        vertex1.addEdge(vertex2, weight)  # Add edge from vertex1 to vertex2
        vertex2.addEdge(vertex1, weight)  # Add edge from vertex2 to vertex1 (undirected)
        return True

    def isAdjacent(self, label1, label2):                             # Check if two vertices are adjacent
        if not self.hasVertex(label1) or not self.hasVertex(label2):  # Check if both vertices exist
            return False                                              # Return False if either vertex is missing
        vertex1 = self.getVertex(label1)                              # Get the first vertex object
        adj = vertex1.getAdjacent()                                   # Get the adjacency list of vertex1
        current = adj.head                                            # Start at the head of the adjacency list
        while current:                                                # Iterate through the adjacency list
            if current.getValue().getVertex().getLabel() == label2:   # Check if neighbor is vertex2
                return True
            current = current.getNext()
        return False

    def getVertexCount(self):                   # Get the total number of vertices in the graph
        count = 0                               # Initialize vertex counter
        current = self.vertices.head            # Start at the head of the vertices list
        while current:                          # Iterate through the linked list
            count += 1
            current = current.getNext()     # Move to the next node
        return count                        # Return the total count

    def displayAsList(self):                    # Display the graph as an adjacency list
        if self.getVertexCount() == 0:
            print("Graph is empty")
            return

        print("\nAdjacency List:")
        current = self.vertices.head          # Start at the head of the vertices list
        while current:                        # Iterate through all vertices
            vertex = current.getValue()       # Get the current vertex
            print(f"{vertex.getLabel()}: ", end="")  # Print the vertex label
            adj = vertex.getAdjacent()               # Get the adjacency list of the vertex
            adj_node = adj.head                      # Start at the head of the adjacency list
            while adj_node:                          # Iterate through neighbors
                edge = adj_node.getValue()           # Get the edge object
                print(f"{edge.getVertex().getLabel()}({edge.getWeight()}) ", end="")  # Print neighbor and weight
                adj_node = adj_node.getNext()                                         # Move to the next neighbor
            print()
            current = current.getNext()                                               # Move to the next vertex

    """Perform Breadth-First Search to find reachable nodes and their levels."""
    def BFS(self, source_label):               # Perform Breadth-First Search from a source vertex
        if not self.hasVertex(source_label):   # Check if source vertex exists
            raise GraphErrorHandle(f"Source vertex '{source_label}' not found")

        vertex_count = self.getVertexCount()                  # Get the total number of vertices
        vertex_labels = np.empty(vertex_count, dtype=object)  # Create array for vertex labels
        vertex_levels = np.full(vertex_count, -1, dtype=int)  # Create array for vertex levels, init to -1

        current = self.vertices.head  # Start at the head of the vertices list
        idx = 0                       # Initialize index for vertex_labels array
        while current:                # Iterate through vertices
            vertex_labels[idx] = current.getValue().getLabel()  # Store vertex label in array
            current.getValue().clearVisited()                   # Clear visited flag for the vertex
            current = current.getNext()                         # Move to the next vertex
            idx += 1

        def find_index(labels, target):   # Helper function to find index of a label
            for i in range(len(labels)):  # Iterate through labels array
                if labels[i] == target:   # Check if label matches
                    return i              # Return index if found
            return -1

        queue = DSASqueue()                    # Create a queue for BFS
        source = self.getVertex(source_label)  # Get the source vertex object
        source_idx = find_index(vertex_labels, source_label)  # Find index of source vertex
        source.setVisited()                                   # Mark source as visited
        vertex_levels[source_idx] = 0                         # Set source level to 0
        queue.enqueue(source)                                 # Enqueue the source vertex

        while not queue.is_empty():        # Continue until queue is empty
            vertex = queue.dequeue()       # Dequeue the next vertex
            v_label = vertex.getLabel()    # Get the vertex label
            v_idx = find_index(vertex_labels, v_label)  # Find index of current vertex
            v_level = vertex_levels[v_idx]              # Get the level of the current vertex

            adj = vertex.getAdjacent()          # Get adjacency list of current vertex
            adj_node = adj.head                 # Start at head of adjacency list
            while adj_node:                     # Iterate through neighbors
                neighbor = adj_node.getValue().getVertex()  # Get neighbor vertex
                n_label = neighbor.getLabel()               # Get neighbor label
                n_idx = find_index(vertex_labels, n_label)  # Find index of neighbor
                if not neighbor.getVisited():               # Check if neighbor is unvisited
                    neighbor.setVisited()                   # Mark neighbor as visited
                    vertex_levels[n_idx] = v_level + 1      # Set neighbor level
                    queue.enqueue(neighbor)                 # Enqueue neighbor
                adj_node = adj_node.getNext()               # Move to next neighbor

        result = DSALinkedList()         # Create linked list for results
        for i in range(vertex_count):    # Iterate through all vertices
            if vertex_levels[i] != -1:   # Check if vertex is reachable
                result.insertLast(VertexLevelPair(vertex_labels[i], vertex_levels[i]))  # Add vertex and level
        return result

    """Detect cycles in the graph using Depth-First Search."""
    def DFS_cycle_detection(self):          # Detect cycles in the graph using DFS
        cycle_vertices = DSALinkedList()    # Create list to store vertices in a cycle
        cycle_found = [False]               # Use list to allow modification in nested function

        vertex_count = self.getVertexCount()                  # Get the total number of vertices
        vertex_labels = np.empty(vertex_count, dtype=object)  # Create array for vertex labels

        current = self.vertices.head  # Start at head of vertices list
        idx = 0                       # Initialize index for vertex_labels
        while current:                # Iterate through vertices
            vertex_labels[idx] = current.getValue().getLabel()  # Store vertex label
            current = current.getNext()                         # Move to next vertex
            idx += 1

        vertex_states = np.zeros(vertex_count, dtype=int)       # Create array for vertex states (0=unvisited, 1=visiting, 2=visited)
        parent_indices = np.full(vertex_count, -1, dtype=int)   # Create array for parent indices, init to -1

        def getLabelIndex(label):              # Helper function to find index of a label
            for i in range(vertex_count):      # Iterate through labels
                if vertex_labels[i] == label:  # Check if label matches
                    return i                   # Return index if found
            return -1

        def DFSVisit(vertex_idx, parent_idx):  # Recursive DFS function for cycle detection
            if cycle_found[0]:                 # Check if cycle has already been found
                return                         # Exit if cycle found

            vertex_states[vertex_idx] = 1             # Mark vertex as visiting
            vertex_label = vertex_labels[vertex_idx]  # Get vertex label

            vertex = self.getVertex(vertex_label)  # Get vertex object
            adj = vertex.getAdjacent()             # Get adjacency list
            adj_node = adj.head                    # Start at head of adjacency list

            while adj_node and not cycle_found[0]:            # Iterate through neighbors
                edge = adj_node.getValue()  # Get edge object
                neighbor_label = edge.getVertex().getLabel()  # Get neighbor label
                neighbor_idx = getLabelIndex(neighbor_label)  # Find neighbor index

                if parent_idx != -1 and neighbor_idx == parent_idx:  # Skip edge back to parent
                    adj_node = adj_node.getNext()                    # Move to next neighbor
                    continue

                if vertex_states[neighbor_idx] == 0:           # If neighbor is unvisited
                    parent_indices[neighbor_idx] = vertex_idx  # Set parent of neighbor
                    DFSVisit(neighbor_idx, vertex_idx)         # Recursively visit neighbor
                elif vertex_states[neighbor_idx] == 1:         # If neighbor is visiting (back edge)
                    cycle_found[0] = True                      # Mark cycle as found
                    cycle_vertices.insertLast(neighbor_label)  # Add neighbor to cycle
                    current_idx = vertex_idx                   # Start tracing back from current vertex

                    while current_idx != -1 and current_idx != neighbor_idx:   # Trace parent chain
                        cycle_vertices.insertLast(vertex_labels[current_idx])  # Add vertex to cycle
                        current_idx = parent_indices[current_idx]              # Move to parent
                    cycle_vertices.insertLast(neighbor_label)                  # Close the cycle
                    return
                adj_node = adj_node.getNext()                                  # Move to next neighbor

            vertex_states[vertex_idx] = 2  # Mark vertex as visited

        for i in range(vertex_count):                         # Iterate through all vertices
            if vertex_states[i] == 0 and not cycle_found[0]:  # If vertex is unvisited
                DFSVisit(i, -1)                               # Start DFS from this vertex

        return (cycle_found[0], cycle_vertices)  # Return cycle status and vertices

    """
    Dijkstra's algorithm for shortest paths.
    https://www.geeksforgeeks.org/dijkstras-shortest-path-algorithm-greedy-algo-7/
    """
    def dijkstra(self, source_label):         # Implement Dijkstra's algorithm for shortest paths
        if not self.hasVertex(source_label):
            raise GraphErrorHandle(f"Source vertex '{source_label}' not found")

        vertex_count = self.getVertexCount()                  # Get total number of vertices
        vertex_labels = np.empty(vertex_count, dtype=object)  # Create array for vertex labels
        distances = np.full(vertex_count, float('inf'))       # Initialize distances to infinity
        predecessors = np.empty(vertex_count, dtype=object)   # Create array for predecessors
        visited = np.zeros(vertex_count, dtype=bool)          # Initialize visited flags

        current = self.vertices.head      # Start at head of vertices list
        idx = 0                           # Initialize index for vertex_labels
        while current:                    # Iterate through vertices
            vertex = current.getValue()   # Get vertex object
            vertex_labels[idx] = vertex.getLabel()  # Store vertex label
            current = current.getNext()             # Move to next vertex
            idx += 1

        def find_index(labels, target):    # Helper function to find index of a label
            for i in range(len(labels)):   # Iterate through labels
                if labels[i] == target:    # Check if label matches
                    return i               # Return index if found
            return -1

        source_idx = find_index(vertex_labels, source_label)  # Find index of source vertex
        distances[source_idx] = 0                             # Set source distance to 0

        for _ in range(vertex_count):       # Iterate through all vertices
            min_dist = float('inf')         # Initialize minimum distance
            min_idx = -1                    # Initialize index of minimum distance vertex
            for i in range(vertex_count):   # Find unvisited vertex with minimum distance
                if not visited[i] and distances[i] < min_dist:  # Check if unvisited and smaller distance
                    min_dist = distances[i]                     # Update minimum distance
                    min_idx = i                                 # Update index
            if min_idx == -1:                                   # If no unvisited vertex found
                continue                                        # Skip to next iteration

            visited[min_idx] = True                          # Mark vertex as visited
            vertex = self.getVertex(vertex_labels[min_idx])  # Get vertex object
            adj = vertex.getAdjacent()                       # Get adjacency list
            adj_node = adj.head                              # Start at head of adjacency list
            while adj_node:                                  # Iterate through neighbors
                edge = adj_node.getValue()                   # Get edge object
                neighbor = edge.getVertex()                  # Get neighbor vertex
                n_label = neighbor.getLabel()                # Get neighbor label
                n_idx = find_index(vertex_labels, n_label)   # Find neighbor index
                if not visited[n_idx]:                       # If neighbor is unvisited
                    weight = edge.getWeight()                # Get edge weight
                    new_dist = distances[min_idx] + weight   # Calculate new distance
                    if new_dist < distances[n_idx]:          # If new distance is shorter
                        distances[n_idx] = new_dist          # Update distance
                        predecessors[n_idx] = vertex_labels[min_idx]  # Update predecessor
                adj_node = adj_node.getNext()                         # Move to next neighbor

        result = DSALinkedList()         # Create linked list for results
        for i in range(vertex_count):    # Iterate through all vertices
            label = vertex_labels[i]     # Get vertex label
            distance = distances[i]      # Get distance to vertex
            path_list = DSALinkedList()  # Create list for path
            if distance != float('inf'):  # If vertex is reachable
                current_label = label     # Start with current vertex
                while current_label:      # Trace back predecessors
                    path_list.insertFirst(current_label)                    # Add vertex to path
                    current_idx = find_index(vertex_labels, current_label)  # Find index
                    current_label = predecessors[current_idx]               # Move to predecessor
            result.insertLast(DijkstraResult(label, distance, path_list))   # Add result
        return result                                                       # Return list of shortest paths