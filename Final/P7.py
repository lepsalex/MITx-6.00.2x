class Node(object):
    def __init__(self, name):
        self.name = str(name)
    def getName(self):
        return self.name
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name
    def __eq__(self, other):
        return self.name == other.name
    def __ne__(self, other):
        return not self.__eq__(other)
    def __hash__(self):
        # Override the default hash method
        # Think: Why would we want to do this?
        return self.name.__hash__()

class Edge(object):
    def __init__(self, src, dest):
        self.src = src
        self.dest = dest
    def getSource(self):
        return self.src
    def getDestination(self):
        return self.dest
    def __str__(self):
        return '{0}->{1}'.format(self.src, self.dest)

class siteGraph(object):
    """
    A directed graph
    """
    def __init__(self):
        # A Python Set is basically a list that doesn't allow duplicates.
        # Entries into a set must be hashable (where have we seen this before?)
        # Because it is backed by a hashtable, lookups are O(1) as opposed to the O(n) of a list (nifty!)
        # See http://docs.python.org/2/library/stdtypes.html#set-types-set-frozenset
        self.nodes = set([])
        self.edges = {}
    def addNode(self, node):
        if node in self.nodes:
            # Even though self.nodes is a Set, we want to do this to make sure we
            # don't add a duplicate entry for the same node in the self.edges list.
            raise ValueError('Duplicate node')
        else:
            self.nodes.add(node)
            self.edges[node] = []
    def addEdge(self, edge):
        src = edge.getSource()
        dest = edge.getDestination()
        if not(src in self.nodes and dest in self.nodes):
            raise ValueError('Node not in graph')
        self.edges[src].append(dest)
    def childrenOf(self, node):
        return self.edges[node]
    def hasNode(self, node):
        return node in self.nodes
    def __str__(self):
        res = ''
        for k in self.edges:
            for d in self.edges[k]:
                res = '{0}{1}->{2}\n'.format(res, k, d)
        return res[:-1]

# 7-4
# def initializeGraph(n): # n is an integer, the number of nodes in the graph
#     G = siteGraph() # Initializes an empty graph, with G.graphNodes set to []
#     for i in range(n):
#         G.addNode(Node(i))
#     for i in range(n):
#     	x = Node(i)
#         y = Node((i+1) % n)
#     	G.addEdge(Edge(x, y))
#         G.addEdge(Edge(y, x))
#     return G
#
# # print initializeGraph(100)

# 7-5
class siteGraph75(object):
    """
    A directed graph
    """
    def __init__(self):
        # A Python Set is basically a list that doesn't allow duplicates.
        # Entries into a set must be hashable (where have we seen this before?)
        # Because it is backed by a hashtable, lookups are O(1) as opposed to the O(n) of a list (nifty!)
        # See http://docs.python.org/2/library/stdtypes.html#set-types-set-frozenset
        self.nodes = set([])
        self.edges = {}
    def addNode(self, node):
        if node in self.nodes:
            # Even though self.nodes is a Set, we want to do this to make sure we
            # don't add a duplicate entry for the same node in the self.edges list.
            raise ValueError('Duplicate node')
        else:
            self.nodes.add(node)
            self.edges[node] = []
    def addEdge(self, edge):
        src = edge.getSource()
        dest = edge.getDestination()
        if not(src in self.nodes and dest in self.nodes):
            raise ValueError('Node not in graph')
        self.edges[src].append(dest)
    def addEdges(self, n):
        for i in range(n):
            x = Node(i % 100)
            y = Node((i+1) % 100)
            # print str(x) + ' - ' + str(y)
            self.addEdge(Edge(x, y))
            self.addEdge(Edge(y, x))
    def childrenOf(self, node):
        return self.edges[node]
    def hasNode(self, node):
        return node in self.nodes
    def __str__(self):
        res = ''
        for k in self.edges:
            for d in self.edges[k]:
                res = '{0}{1}->{2}\n'.format(res, k, d)
        return res[:-1]

def initializeGraph(n): # n is an integer, the number of nodes in the graph
    G = siteGraph75() # Initializes an empty graph, with G.graphNodes set to []
    for i in range(n):
        G.addNode(Node(i))
    return G

n = 100
maxDegrees, meanDegrees, meanDegreeVariances, meanShortestPaths = [],[],[],[]
graph = initializeGraph(n)
for nEdges in range(n, n*n, n*n/10 ):
    print nEdges
    graph.addEdges(nEdges)
   # maxDegrees.append(graph.maxDegree())
   # meanDegrees.append(graph.meanDegree())
   # meanDegreeVariances.append(graph.meanDegreeVariances())
   # meanShortestPaths.append(graph.meanShortestPath())
