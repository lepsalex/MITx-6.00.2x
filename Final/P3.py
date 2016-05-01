import random
import pylab

# Global Variables
MAXRABBITPOP = 1000
CURRENTRABBITPOP = 500
CURRENTFOXPOP = 30

# debug variable
debug = False

def rabbitGrowth():
    """
    rabbitGrowth is called once at the beginning of each time step.

    It makes use of the global variables: CURRENTRABBITPOP and MAXRABBITPOP.

    The global variable CURRENTRABBITPOP is modified by this procedure.

    For each rabbit, based on the probabilities in the problem set write-up,
      a new rabbit may be born.
    Nothing is returned.
    """
    # you need this line for modifying global variables
    global CURRENTRABBITPOP

    # If current pop less than max pop ...
    if (CURRENTRABBITPOP < MAXRABBITPOP):

        # Calculate growth probability
        threshold = 1.0 - (CURRENTRABBITPOP / float(MAXRABBITPOP))

        # Get random value
        prob = random.random()

        # If random > threshold reproduce + 1 rabbit
        if (prob > threshold):
            CURRENTRABBITPOP += 1

    if (debug == True):
        print CURRENTRABBITPOP


def foxGrowth():
    """
    foxGrowth is called once at the end of each time step.

    It makes use of the global variables: CURRENTFOXPOP and CURRENTRABBITPOP,
        and both may be modified by this procedure.

    Each fox, based on the probabilities in the problem statement, may eat
      one rabbit (but only if there are more than 10 rabbits).

    If it eats a rabbit, then with a 1/3 prob it gives birth to a new fox.

    If it does not eat a rabbit, then with a 1/10 prob it dies.

    Nothing is returned.
    """
    # you need these lines for modifying global variables
    global CURRENTRABBITPOP
    global CURRENTFOXPOP

    # Fox reproduction and death thresholds
    repThresh = (1 / float(3))
    dieThresh = (1 / float(10))

    # for each fox in the current fox pop
    for fox in range(CURRENTFOXPOP):
        # First determine if a fox eats rabbit
        if (CURRENTRABBITPOP >= 10):
            eatThresh = (CURRENTRABBITPOP / float(MAXRABBITPOP))
            eatProb = random.random()
            if ((eatProb < eatThresh) and (CURRENTRABBITPOP > 10)):
                # Eat Rabbit
                CURRENTRABBITPOP -= 1
                # Attempt to Reproduce
                repProb = random.random()
                if (repProb < repThresh):
                    CURRENTFOXPOP += 1
            # Else if fox doesn't eat it may die ...
            elif ((random.random() < dieThresh) and (CURRENTFOXPOP > 10)):
                    CURRENTFOXPOP -= 1

    if (debug == True):
        print 'Rabbits: ' + str(CURRENTRABBITPOP) + ' - Foxes: ' + str(CURRENTFOXPOP)


def runSimulation(numSteps):
    """
    Runs the simulation for `numSteps` time steps.

    Returns a tuple of two lists: (rabbit_populations, fox_populations)
      where rabbit_populations is a record of the rabbit population at the
      END of each time step, and fox_populations is a record of the fox population
      at the END of each time step.

    Both lists should be `numSteps` items long.
    """

    # Lists of Populations to return
    rabbit_populations = []
    fox_populations = []

    for x in range(numSteps):
        # Run each function
        rabbitGrowth()
        foxGrowth()
        # Append populations at end of timestep
        rabbit_populations.append(CURRENTRABBITPOP)
        fox_populations.append(CURRENTFOXPOP)

    return (rabbit_populations, fox_populations)

print runSimulation(200)
