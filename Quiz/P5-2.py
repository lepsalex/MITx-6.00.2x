import random

def drawTrial():
    bucket = ['red', 'red', 'red', 'red', 'green', 'green', 'green', 'green']
    draws = []

    for i in xrange(3):
        # Draw a ball at rnadom
        draw = random.choice(bucket)
        # Removew draw from bucket
        bucket.remove(draw)
        # Add draw to draws
        draws.append(draw)

    return len(set(draws)) <= 1

def noReplacementSimulation(numTrials):
    '''
    Runs numTrials trials of a Monte Carlo simulation
    of drawing 3 balls out of a bucket containing
    4 red and 4 green balls. Balls are not replaced once
    drawn. Returns the a decimal - the fraction of times 3
    balls of the same color were drawn.
    '''

    trials = []

    for i in xrange(numTrials):
        trials.append(drawTrial())

    return float(trials.count(True)) / len(trials)

# Test Output
print noReplacementSimulation(10000000)
