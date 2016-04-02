import random, pylab

# You are given this function
def getMeanAndStd(X):
    mean = sum(X)/float(len(X))
    tot = 0.0
    for x in X:
        tot += (x - mean)**2
    std = (tot/len(X))**0.5
    return mean, std

# You are given this class
class Die(object):
    def __init__(self, valList):
        """ valList is not empty """
        self.possibleVals = valList[:]
    def roll(self):
        return random.choice(self.possibleVals)

# Implement this -- Coding Part 1 of 2
def makeHistogram(values, numBins, xLabel, yLabel, title=None):
    """
      - values, a sequence of numbers
      - numBins, a positive int
      - xLabel, yLabel, title, are strings
      - Produces a histogram of values with numBins bins and the indicated labels
        for the x and y axis
      - If title is provided by caller, puts that title on the figure and otherwise
        does not title the figure
    """
    pylab.hist(values, numBins)
    pylab.xlabel(xLabel)
    pylab.ylabel(yLabel)

    if title is not None:
        pylab.title(title)

    pylab.show()

# Implement this -- Coding Part 2 of 2
def rollDie(die, numRolls):

    # Roll dies and log results to rolls[]
    rolls = []
    for x in xrange(numRolls):
        rolls.append(die.roll())

    # print rolls

    # Iterate and get longest run
    count = 1
    longestRun = 1

    # Only if we have rolls to iterate over
    if len(rolls) > 1:
        for i, roll in enumerate(rolls):
            # If we are not past the max index for i + 1 and we have
            # a succesfull match then count it (+1)
            if (i <  (len(rolls) - 1)) and (rolls[i + 1] == rolls[i]):
                count += 1
                if count > longestRun:
                    longestRun = count
            else:
                count = 1

    return longestRun


def getAverage(die, numRolls, numTrials):
    """
      - die, a Die
      - numRolls, numTrials, are positive ints
      - Calculates the expected mean value of the longest run of a number
        over numTrials runs of numRolls rolls.
      - Calls makeHistogram to produce a histogram of the longest runs for all
        the trials. There should be 10 bins in the histogram
      - Choose appropriate labels for the x and y axes.
      - Returns the mean calculated
    """

    trials = []

    for i in xrange(numTrials):
        trials.append(rollDie(die, numRolls))

    makeHistogram(trials, 10, 'Longest Run', 'Frequency of Occurance', 'Distribution of consecutive dice rolls')

    return getMeanAndStd(trials)[0]

# My Tests
# getAverage(Die([1,2,3,4,5,6]), 10, 10)

# Exam Tests
# print getAverage(Die([1]), 10, 1000)
# print getAverage(Die([1,1]), 10, 1000)
# print getAverage(Die([1,2,3,4,5,6]), 50, 1000) # GOOD
# print getAverage(Die([1,2,3,4,5,6,6,6,7]), 50, 1000)
# print getAverage(Die([1,2,3,4,5,6,6,6,7]), 1, 1000) # GOOD


# Included in Test
print getAverage(Die([1,2,3,4,5,6,6,6,7]), 500, 10000)
