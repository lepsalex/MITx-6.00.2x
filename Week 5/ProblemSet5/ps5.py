# 6.00.2x Problem Set 5
# Graph optimization
# Finding shortest paths through MIT buildings
#

import string
# This imports everything from `graph.py` as if it was defined in this file!
from graph import *

#
# Problem 2: Building up the Campus Map
#
# Step One: Init a new WeightedDigraph
#
# Step Two: The campus map text file will read in line by line using Python's
# build in input readlines() method. For each line, we will temporarily save
# each value (space separated) into list and then add each of the nodes
# (first two values) and then connect them via a new WeightedEdge using the
# final two values.
#

def load_map(mapFilename):
    """
    Parses the map file and constructs a directed graph

    Parameters:
        mapFilename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a directed graph representing the map
    """

    print "Loading map from file..."

    # Init new WeightedDigraph
    weightedDigraph = WeightedDigraph()

    # Open file
    f = open(mapFilename, 'r')

    # For each line in the file ...
    for line in f:
        line = line.rstrip('\n')
        data = line.split(' ')
        try:
            weightedDigraph.addNode(Node(data[0]))
        except ValueError:
            pass
        try:
            weightedDigraph.addNode(Node(data[1]))
        except ValueError:
            pass
        try:
            weightedDigraph.addEdge(WeightedEdge(Node(data[0]), Node(data[1]), float(data[2]), float(data[3])))
        except ValueError:
            pass

    return weightedDigraph


# Problem 2 Test
# mitMap = load_map('mit_map.txt')
# print isinstance(mitMap, Digraph)
# print isinstance(mitMap, WeightedDigraph)
# print mitMap.nodes
# print mitMap.edges


#
# Problem 3: Finding the Shortest Path using Brute Force Search
#
def getAllPaths(digraph, start, end, path=[]):
    # If start is end, return empty path
    path = path + [start.getName()]
    if start == end:
        return [path]

    # Store all possible paths
    allPaths = []
    # Slight mod to lecture code to return ALL possible paths
    for node in digraph.childrenOf(start):
        if node.getName() not in path:
            newPaths = getAllPaths(digraph, node, end, path)
            for newPath in newPaths:
                allPaths.append(newPath)
    # Returns as list of all possilbe paths from start to end
    return allPaths

def evalDistance(digraph, path):
    # Sums up distances in a given path
    totalDistance = 0.0
    totalOutdoorDistance = 0.0

    # For each node in path up to second-last one
    for x in xrange(len(path) - 1):
        destinations = digraph.edges[Node(path[x])]
        for dest in destinations:
            if dest[0] == Node(path[x + 1]):
                totalDistance += float(dest[1][0])
                totalOutdoorDistance += float(dest[1][1])
                break
    # Return tuple with totals
    return (totalDistance, totalOutdoorDistance)

def bruteForceSearch(digraph, start, end, maxTotalDist, maxDistOutdoors):
    """
    Finds the shortest path from start to end using brute-force approach.
    The total distance travelled on the path must not exceed maxTotalDist, and
    the distance spent outdoor on this path must not exceed maxDistOutdoors.

    Parameters:
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """

    # Start with shortest distance as max distance
    shortestTotalDistance = maxTotalDist
    # Will store shortest path
    shortestPath = []

    # Get all paths possible given start and end node in digraph
    allPaths = getAllPaths(digraph, Node(start), Node(end))

    for path in allPaths:
        distances = evalDistance(digraph, path)
        # If within contrainsts
        if distances[0] <= maxTotalDist and distances[1] <= maxDistOutdoors:
            if distances[0] <= shortestTotalDistance:
                shortestTotalDistance = distances[0]
                shortestPath = path

    if shortestPath == []:
        raise ValueError('Could not find path with given contrainsts')

    return shortestPath

# Test Output
# mitMap = load_map('mit_map.txt')
# print bruteForceSearch(mitMap, Node(32), Node(56), 200, 100)

# Testing Grader Problems
# map1 = load_map('map1.txt')
# print map1
# print bruteForceSearch(map1, "1", "3", 100, 100)

#
# Problem 4: Finding the Shorest Path using Optimized Search Method
#
def directedDFS(digraph, start, end, maxTotalDist, maxDistOutdoors):
    """
    Finds the shortest path from start to end using directed depth-first.
    search approach. The total distance travelled on the path must not
    exceed maxTotalDist, and the distance spent outdoor on this path must
	not exceed maxDistOutdoors.

    Parameters:
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """
    #TODO
    pass


# Uncomment below when ready to test
#### NOTE! These tests may take a few minutes to run!! ####
if __name__ == '__main__':
    # Test cases
    mitMap = load_map("mit_map.txt")
    print isinstance(mitMap, Digraph)
    print isinstance(mitMap, WeightedDigraph)
    print 'nodes', mitMap.nodes
    print 'edges', mitMap.edges


    LARGE_DIST = 1000000

    # # Test case 1
    # print "---------------"
    # print "Test case 1:"
    # print "Find the shortest-path from Building 32 to 56"
    # expectedPath1 = ['32', '56']
    # brutePath1 = bruteForceSearch(mitMap, '32', '56', LARGE_DIST, LARGE_DIST)
    # # dfsPath1 = directedDFS(mitMap, '32', '56', LARGE_DIST, LARGE_DIST)
    # print "Expected: ", expectedPath1
    # print "Brute-force: ", brutePath1
    # # print "DFS: ", dfsPath1
    # # print "Correct? BFS: {0}; DFS: {1}".format(expectedPath1 == brutePath1, expectedPath1 == dfsPath1)

    # Test case 2
    print "---------------"
    print "Test case 2:"
    print "Find the shortest-path from Building 32 to 56 without going outdoors"
    expectedPath2 = ['32', '36', '26', '16', '56']
    brutePath2 = bruteForceSearch(mitMap, '32', '56', LARGE_DIST, 0)
    # dfsPath2 = directedDFS(mitMap, '32', '56', LARGE_DIST, 0)
    print "Expected: ", expectedPath2
    print "Brute-force: ", brutePath2
    # print "DFS: ", dfsPath2
    # print "Correct? BFS: {0}; DFS: {1}".format(expectedPath2 == brutePath2, expectedPath2 == dfsPath2)

#     Test case 3
#     print "---------------"
#     print "Test case 3:"
#     print "Find the shortest-path from Building 2 to 9"
#     expectedPath3 = ['2', '3', '7', '9']
#     brutePath3 = bruteForceSearch(mitMap, '2', '9', LARGE_DIST, LARGE_DIST)
#     dfsPath3 = directedDFS(mitMap, '2', '9', LARGE_DIST, LARGE_DIST)
#     print "Expected: ", expectedPath3
#     print "Brute-force: ", brutePath3
#     print "DFS: ", dfsPath3
#     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath3 == brutePath3, expectedPath3 == dfsPath3)

#     Test case 4
#     print "---------------"
#     print "Test case 4:"
#     print "Find the shortest-path from Building 2 to 9 without going outdoors"
#     expectedPath4 = ['2', '4', '10', '13', '9']
#     brutePath4 = bruteForceSearch(mitMap, '2', '9', LARGE_DIST, 0)
#     dfsPath4 = directedDFS(mitMap, '2', '9', LARGE_DIST, 0)
#     print "Expected: ", expectedPath4
#     print "Brute-force: ", brutePath4
#     print "DFS: ", dfsPath4
#     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath4 == brutePath4, expectedPath4 == dfsPath4)

#     Test case 5
#     print "---------------"
#     print "Test case 5:"
#     print "Find the shortest-path from Building 1 to 32"
#     expectedPath5 = ['1', '4', '12', '32']
#     brutePath5 = bruteForceSearch(mitMap, '1', '32', LARGE_DIST, LARGE_DIST)
#     dfsPath5 = directedDFS(mitMap, '1', '32', LARGE_DIST, LARGE_DIST)
#     print "Expected: ", expectedPath5
#     print "Brute-force: ", brutePath5
#     print "DFS: ", dfsPath5
#     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath5 == brutePath5, expectedPath5 == dfsPath5)

#     Test case 6
#     print "---------------"
#     print "Test case 6:"
#     print "Find the shortest-path from Building 1 to 32 without going outdoors"
#     expectedPath6 = ['1', '3', '10', '4', '12', '24', '34', '36', '32']
#     brutePath6 = bruteForceSearch(mitMap, '1', '32', LARGE_DIST, 0)
#     dfsPath6 = directedDFS(mitMap, '1', '32', LARGE_DIST, 0)
#     print "Expected: ", expectedPath6
#     print "Brute-force: ", brutePath6
#     print "DFS: ", dfsPath6
#     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath6 == brutePath6, expectedPath6 == dfsPath6)

#     Test case 7
#     print "---------------"
#     print "Test case 7:"
#     print "Find the shortest-path from Building 8 to 50 without going outdoors"
#     bruteRaisedErr = 'No'
#     dfsRaisedErr = 'No'
#     try:
#         bruteForceSearch(mitMap, '8', '50', LARGE_DIST, 0)
#     except ValueError:
#         bruteRaisedErr = 'Yes'

#     try:
#         directedDFS(mitMap, '8', '50', LARGE_DIST, 0)
#     except ValueError:
#         dfsRaisedErr = 'Yes'

#     print "Expected: No such path! Should throw a value error."
#     print "Did brute force search raise an error?", bruteRaisedErr
#     print "Did DFS search raise an error?", dfsRaisedErr

#     Test case 8
#     print "---------------"
#     print "Test case 8:"
#     print "Find the shortest-path from Building 10 to 32 without walking"
#     print "more than 100 meters in total"
#     bruteRaisedErr = 'No'
#     dfsRaisedErr = 'No'
#     try:
#         bruteForceSearch(mitMap, '10', '32', 100, LARGE_DIST)
#     except ValueError:
#         bruteRaisedErr = 'Yes'

#     try:
#         directedDFS(mitMap, '10', '32', 100, LARGE_DIST)
#     except ValueError:
#         dfsRaisedErr = 'Yes'

#     print "Expected: No such path! Should throw a value error."
#     print "Did brute force search raise an error?", bruteRaisedErr
#     print "Did DFS search raise an error?", dfsRaisedErr
