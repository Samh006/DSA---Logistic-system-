from Module1.Linked_list import DSALinkedList

class GraphErrorHandle(Exception):
    pass

class Edge:
    def __init__(self, source, dest, weight):
        self.source = source
        self.dest = dest
        self.weight = weight

    def getSource(self):
        return self.source

    def getDest(self):
        return self.dest

    def getWeight(self):
        return self.weight

class DSAEdge:
    def __init__(self, vertex, weight):
        self.vertex = vertex
        self.weight = weight

    def getVertex(self):
        return self.vertex

    def getWeight(self):
        return self.weight

# used in BFS
class VertexLevelPair:
    def __init__(self, label, level):
        self.label = label
        self.level = level

    def getLabel(self):
        return self.label

    def getLevel(self):
        return self.level

class VertexParentPair:
    def __init__(self, label, parent):
        self.label = label
        self.parent = parent

    def getLabel(self):
        return self.label

    def getParent(self):
        return self.parent

class DijkstraResult:
    def __init__(self, label, dist, pathList):
        self.label = label
        self.dist = dist
        self.pathList = pathList

    def getLabel(self):
        return self.label

    def getDistance(self):
        return self.dist

    def getPath(self):
        return self.pathList

class DSAGraphVertex:
    def __init__(self, label):
        self.label = label
        self.adjacent = DSALinkedList()
        self.visited = False
        self.distance = float('inf')
        self.predecessor = None

    def getLabel(self):
        return self.label

    def getAdjacent(self):
        return self.adjacent

    def addEdge(self, vertex, weight):
        if weight <= 0:
            raise GraphErrorHandle("Edge weight must be positive")
        self.adjacent.insertLast(DSAEdge(vertex, weight))

    def removeEdge(self, vertex_label):
        prev = None
        current = self.adjacent.head
        while current:
            if current.getValue().getVertex().getLabel() == vertex_label:
                if prev is None:
                    self.adjacent.head = current.getNext()
                else:
                    prev.setNext(current.getNext())
                if current.getNext() is None:
                    self.adjacent.tail = prev
                return True
            prev = current
            current = current.getNext()
        return False

    def setVisited(self):
        self.visited = True

    def clearVisited(self):
        self.visited = False

    def getVisited(self):
        return self.visited

    def setDistance(self, distance):
        self.distance = distance

    def getDistance(self):
        return self.distance

    def setPredecessor(self, vertex):
        self.predecessor = vertex

    def getPredecessor(self):
        return self.predecessor