def mean(lst):
    try:
        return sum(lst)/float(len(lst))
    except ZeroDivisionError:
        return float('NaN')

def stdDev(lst):
    mn = mean(lst)
    listSum = 0.0

    for num in lst:
        listSum += (num - mn)**2

    return (listSum/len(lst))**0.5

def coeVar(lst):
    mn = mean(lst)
    stdev = stdDev(lst)

    return round((stdev / mn), 3)

# Test excecution
data =  [10, 4, 12, 15, 20, 5]
print 'STDEV: ', stdDev(data)
print 'COE: ', coeVar(data)
