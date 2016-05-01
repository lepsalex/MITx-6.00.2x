import numpy

lists = [
    [0,1,2,3,4,5,6,7,8],
    [5,10,10,10,15],
    [0,1,2,4,6,8],
    [6,7,11,12,13,15],
    [9,0,0,3,3,3,6,6]
]

# P2-2
def meanVar(lists):
    for list in lists:
        mean = numpy.mean(list)
        var = numpy.var(list)
        print 'Mean: ' + str(mean) + ' - Var: ' + str(var)

# P2-3
def possible_mean(L):
    return sum(L)/len(L)

def possible_variance(L):
    mu = possible_mean(L)
    temp = 0
    for e in L:
        temp += (e-mu)**2
    return temp / len(L)

def p23(lists):
    for list in lists:
        pMean = possible_mean(list)
        pVar = possible_variance(list)
        print 'Mean: ' + str(pMean) + ' - Var: ' + str(pVar)

p23(lists)
