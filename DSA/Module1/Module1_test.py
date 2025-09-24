import numpy as np
from Module1.Graph import DSAGraph, GraphErrorHandle
from Module1.Linked_list import DSALinkedList
from Module1.GraphVertex import Edge

def testModule():
    testGraph = DSAGraph()

    nodes = DSALinkedList()
    edges = DSALinkedList()

    # Node population
    nodes.insertLast('A')
    nodes.insertLast('B')
    nodes.insertLast('C')
    nodes.insertLast('D')
    nodes.insertLast('E')
    nodes.insertLast('F')
    nodes.insertLast('G')
    nodes.insertLast('H')

    # populate edges as edge objects
    edges.insertLast(Edge('A', 'B', 5))
    edges.insertLast(Edge('A', 'C', 3))
    edges.insertLast(Edge('B', 'D', 4))
    edges.insertLast(Edge('B', 'E', 6))
    edges.insertLast(Edge('C', 'F', 2))
    edges.insertLast(Edge('C', 'G', 7))
    edges.insertLast(Edge('D', 'E', 3))
    edges.insertLast(Edge('E', 'F', 4))
    edges.insertLast(Edge('F', 'G', 5))
    edges.insertLast(Edge('D', 'F', 2))
    edges.insertLast(Edge('B', 'G', 8))

    # add nodes and edges to the graph
    try:
        current = nodes.head
        while current:
            testGraph.addVertex(current.getValue())
            current = current.getNext()

        current = edges.head
        while current:
            edge = current.getValue()
            testGraph.addEdge(edge.getSource(), edge.getDest(), edge.getWeight())
            current = current.getNext()
    except GraphErrorHandle as e:
        print(f"Error setting up the test graph {e}")
        return

    # display graph
    print("CityDrop logistics network")
    print("===============================")
    testGraph.displayAsList()

    #BFS: reachable zones from node A
    print("\n1) reachable delivery zones from warehouse A")
    print("==============================================")
    try:
        bfsResult = testGraph.BFS('A')
        print("Hub\tLevel (Number of hops)")
        print("-----------------------")
        reachable = np.empty(testGraph.getVertexCount(), dtype=object)
        idx = 0
        current = bfsResult.head
        while current:
            pair = current.getValue()
            reachable[idx] = pair.getLabel()
            print(f"{pair.getLabel()}\t{pair.getLevel()}")
            current = current.getNext()
            idx += 1
        reachable = reachable[:idx]

        allHubs = np.empty(testGraph.getVertexCount(), dtype=object)
        idx = 0
        current = testGraph.vertices.head
        while current:
            allHubs[idx] = current.getValue().getLabel()
            current = current.getNext()
            idx += 1

        unreachable = np.empty(allHubs.size, dtype=object)
        unreach_count = 0

        for i in range(allHubs.size):
            hub = allHubs[i]
            is_reachable = False

            j = 0
            while j < reachable.size and not is_reachable:
                if hub == reachable[j]:
                    is_reachable = True
                j += 1

            if not is_reachable:
                unreachable[unreach_count] = hub
                unreach_count += 1

        unreachable = unreachable[:unreach_count]

        if unreachable.size > 0:
            print("\nUnreachable hubs:", ", ".join(unreachable))
    except GraphErrorHandle as e:
        print(f"BFS error: {e}")

    # DFS: cycle detection
    print("\n2) Cycle detection in the delivery network")
    print("==============================================")
    try:
        hasCycle, cycleNodes = testGraph.DFS_cycle_detection()
        if hasCycle:
            print("Inefficient loops have been found in the delivery network")
            cycleArray = np.empty(cycleNodes.get_count(), dtype=object)
            idx = 0
            current = cycleNodes.head
            while current:
                cycleArray[idx] = str(current.getValue())
                current = current.getNext()
                idx += 1
            print(f"Cycle involves hubs: {' -> '.join(cycleArray)}")
        else:
            print("No cycles were detected within the network")
    except GraphErrorHandle as e:
        print(f"DFS error: {e}")

    # shortest paths from A
    print("\n3) Shortest delivery routes from warehouse A")
    print("=================================================")
    try:
        shortestPath = testGraph.dijkstra('A')
        print("Hub\tTravel time\tRoute")
        print("-----------------------------")
        current = shortestPath.head
        while current:
            hubInfo = current.getValue()
            hub = hubInfo.getLabel()
            distance = hubInfo.getDistance()
            pathList = hubInfo.getPath()
            pathArray = np.empty(pathList.get_count(), dtype=object)
            idx = 0
            pathCurrent = pathList.head
            while pathCurrent:
                pathArray[idx] = str(pathCurrent.getValue())
                pathCurrent = pathCurrent.getNext()
                idx += 1
            route = " -> ".join(pathArray) if pathArray.size > 0 else "NA"
            time_str = f"{distance} mins" if distance != float('inf') else "Unreachable"
            print(f"{hub}\t{time_str}\t{route}")
            current = current.getNext()
    except GraphErrorHandle as e:
        print(f"Shortest path error {e}")


if __name__ == "__main__":
    testModule()

