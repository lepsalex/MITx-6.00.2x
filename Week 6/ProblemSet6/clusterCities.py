#Code shared across examples
import pylab, string

def stdDev(X):
    mean = sum(X)/float(len(X))
    tot = 0.0
    for x in X:
        tot += (x - mean)**2
    return (tot/len(X))**0.5

def scaleFeatures(vals):
    """Assumes vals is a sequence of numbers"""
    result = pylab.array(vals)
    mean = sum(result)/float(len(result))
    result = result - mean
    sd = stdDev(result)
    result = result/sd
    return result

class Point(object):
    def __init__(self, name, originalAttrs):
        """originalAttrs is an array"""
        self.name = name
        self.attrs = originalAttrs
    def dimensionality(self):
        return len(self.attrs)
    def getAttrs(self):
        return self.attrs
    def distance(self, other):
        #Euclidean distance metric
        result = 0.0
        for i in range(self.dimensionality()):
            result += (self.attrs[i] - other.attrs[i])**2
        return result**0.5
    def getName(self):
        return self.name
    def toStr(self):
        return self.name + str(self.attrs)
    def __str__(self):
        return self.name

class Cluster(object):
    """ A Cluster is defines as a set of elements, all having
    a particular type """
    def __init__(self, points, pointType):
        """ Elements of a cluster are saved in self.points
        and the pointType is also saved """
        self.points = points
        self.pointType = pointType
    def singleLinkageDist(self, other):
        """ Returns the float distance between the points that
        are closest to each other, where one point is from
        self and the other point is from other. Uses the
        Euclidean dist between 2 points, defined in Point."""
        dist = self.points[0].distance(other.points[0])
        for p1 in self.points:
            for p2 in other.points:
                if p1.distance(p2) < dist:
                    dist = float(p1.distance(p2))
        return dist
    def maxLinkageDist(self, other):
        """ Returns the float distance between the points that
        are farthest from each other, where one point is from
        self and the other point is from other. Uses the
        Euclidean dist between 2 points, defined in Point."""
        dist = self.points[0].distance(other.points[0])
        for p1 in self.points:
            for p2 in other.points:
                if p1.distance(p2) > dist:
                    dist = float(p1.distance(p2))
        return dist
    def averageLinkageDist(self, other):
        """ Returns the float average (mean) distance between all
        pairs of points, where one point is from self and the
        other point is from other. Uses the Euclidean dist
        between 2 points, defined in Point."""
        dist = 0.0
        for p1 in self.points:
            for p2 in other.points:
                dist += p1.distance(p2)
        return float(dist/(len(self.points)*len(other.points)))
    def members(self):
        for p in self.points:
            yield p
    def isIn(self, name):
        """ Returns True is the element named name is in the cluster
        and False otherwise """
        for p in self.points:
            if p.getName() == name:
                return True
        return False
    def toStr(self):
        result = ''
        for p in self.points:
            result = result + p.toStr() + ', '
        return result[:-2]
    def getNames(self):
        """ For consistency, returns a sorted list of all
        elements in the cluster """
        names = []
        for p in self.points:
            names.append(p.getName())
        return sorted(names)
    def __str__(self):
        names = self.getNames()
        result = ''
        for p in names:
            result = result + p + ', '
        return result[:-2]

class ClusterSet(object):
    """ A ClusterSet is defined as a list of clusters """
    def __init__(self, pointType):
        """ Initialize an empty set, without any clusters """
        self.members = []
    def add(self, c):
        """ Append a cluster to the end of the cluster list
        only if it doesn't already exist. If it is already in the
        cluster set, raise a ValueError """
        if c in self.members:
            raise ValueError
        self.members.append(c)
    def getClusters(self):
        return self.members[:]
    def mergeClusters(self, c1, c2):
        """ Assumes clusters c1 and c2 are in self
        Adds to self a cluster containing the union of c1 and c2
        and removes c1 and c2 from self """
        newPoints = []
        for point in c1.members():
            newPoints.append(point)
        for point in c2.members():
            newPoints.append(point)
        newCluster = Cluster(newPoints, type(point))
        self.members.remove(c1)
        self.members.remove(c2)
        self.add(newCluster)
        return c1, c2
    def findClosest(self, linkage):
        """ Returns a tuple containing the two most similar
        clusters in self
        Closest defined using the metric linkage """
        mergeTarget = (self.members[0], self.members[1])
        dist = linkage(self.members[0], self.members[1])
        for clusterOne in self.members:
            for clusterTwo in self.members:
                if clusterOne == clusterTwo:
                    continue
                if linkage(clusterOne, clusterTwo) < dist:
                    dist = linkage(clusterOne, clusterTwo)
                    mergeTarget = (clusterOne, clusterTwo)
        return mergeTarget
    def mergeOne(self, linkage):
        """ Merges the two most simililar clusters in self
        Similar defined using the metric linkage
        Returns the clusters that were merged """
        if len(self.members) == 1:
            return None
        elif len(self.members) == 2:
            return self.mergeClusters(self.members[0], self.members[1])
        mergeTarget = self.findClosest(linkage)
        self.mergeClusters(mergeTarget[0], mergeTarget[1])
        return mergeTarget
    def numClusters(self):
        return len(self.members)
    def toStr(self):
        cNames = []
        for c in self.members:
            cNames.append(c.getNames())
        cNames.sort()
        result = ''
        for i in range(len(cNames)):
            names = ''
            for n in cNames[i]:
                names += n + ', '
            names = names[:-2]
            result += '  C' + str(i) + ':' + names + '\n'
        return result

#City climate example
class City(Point):
    pass

def readCityData(fName, scale = False):
    """Assumes scale is a Boolean.  If True, features are scaled"""
    dataFile = open(fName, 'r')
    numFeatures = 0
    #Process lines at top of file
    for line in dataFile: #Find number of features
        if line[0:4] == '#end': #indicates end of features
            break
        numFeatures += 1
    numFeatures -= 1
    featureVals = []

    #Produce featureVals, cityNames
    featureVals, cityNames = [], []
    for i in range(numFeatures):
        featureVals.append([])

    #Continue processing lines in file, starting after comments
    for line in dataFile:
        dataLine = string.split(line[:-1], ',') #remove newline; then split
        cityNames.append(dataLine[0])
        for i in range(numFeatures):
            featureVals[i].append(float(dataLine[i+1]))

    #Use featureVals to build list containing the feature vectors
    #For each city scale features, if needed
    if scale:
        for i in range(numFeatures):
            featureVals[i] = scaleFeatures(featureVals[i])
    featureVectorList = []
    for city in range(len(cityNames)):
        featureVector = []
        for feature in range(numFeatures):
            featureVector.append(featureVals[feature][city])
        featureVectorList.append(featureVector)
    return cityNames, featureVectorList

def buildCityPoints(fName, scaling):
    cityNames, featureList = readCityData(fName, scaling)
    points = []
    for i in range(len(cityNames)):
        point = City(cityNames[i], pylab.array(featureList[i]))
        points.append(point)
    return points

#Use hierarchical clustering for cities
def hCluster(points, linkage, numClusters, printHistory):
    cS = ClusterSet(City)
    for p in points:
        cS.add(Cluster([p], City))
    history = []
    while cS.numClusters() > numClusters:
        merged = cS.mergeOne(linkage)
        history.append(merged)
    if printHistory:
        print ''
        for i in range(len(history)):
            names1 = []
            for p in history[i][0].members():
                names1.append(p.getName())
            names2 = []
            for p in history[i][1].members():
                names2.append(p.getName())
            print 'Step', i, 'Merged', names1, 'with', names2
            print ''
    print 'Final set of clusters:'
    print cS.toStr()
    return cS

def test():
    # Build Data (no scaling)
    points = buildCityPoints('cityTemps.txt', False)

    print '\n\n'
    print 'Problem 3-1:\n'
    hCluster(points, Cluster.maxLinkageDist, 10, False)
    print '\n\n'

    print 'Problem 3-2 (non-scaled):\n'
    hCluster(points, Cluster.singleLinkageDist, 5, False)
    print '\n\n'

    # Build Data (scaled)
    points = buildCityPoints('cityTemps.txt', True)

    print 'Problem 3-2 (scaled):\n'
    hCluster(points, Cluster.singleLinkageDist, 5, False)
    print '\n\n'

    # hCluster(points, Cluster.maxLinkageDist, 10, False)
    # print '\n\n'
    # hCluster(points, Cluster.averageLinkageDist, 10, False)
    # print '\n\n'
    # hCluster(points, Cluster.singleLinkageDist, 10, False)

test()
