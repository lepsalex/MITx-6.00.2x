# Problem Set 4: Building on problem set 3 and expirementing with different trials

import numpy
import random
import pylab


class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """


class SimpleVirus(object):

    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    def __init__(self, maxBirthProb, clearProb):
        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.
        maxBirthProb: Maximum reproduction probability (a float between 0-1)
        clearProb: Maximum clearance probability (a float between 0-1).
        """

        # Error checking input
        if maxBirthProb < 0 or maxBirthProb > 1:
            raise ValueError('maxBirthProb must be a float between 0 and 1!')
        if clearProb < 0 or clearProb > 1:
            raise ValueError('clearProb must be a float between 0 and 1!')

        # Assign init variables
        self.maxBirthProb = float(maxBirthProb)
        self.clearProb = float(clearProb)

    def getMaxBirthProb(self):
        """
        Returns the max birth probability.
        """
        return self.maxBirthProb

    def getClearProb(self):
        """
        Returns the clear probability.
        """
        return self.clearProb

    def doesClear(self):
        """ Stochastically determines whether this virus particle is cleared from the
        patient's body at a time step.
        returns: True with probability self.getClearProb and otherwise returns
        False.
        """
        doesClear = random.random()
        if doesClear <= self.getClearProb():
            return True
        else:
            return False

    def reproduce(self, popDensity):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient and
        TreatedPatient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).

        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.

        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.
        """

        reproduce = random.random()
        if reproduce <= (self.getMaxBirthProb() * (1 - float(popDensity))):
            return SimpleVirus(self.getMaxBirthProb(), self.getClearProb())
        else:
            raise NoChildException


class Patient(object):
    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: the maximum virus population for this patient (an integer)
        """

        self.viruses = viruses
        self.maxPop = maxPop

    def getViruses(self):
        """
        Returns the viruses in this Patient.
        """
        return self.viruses


    def getMaxPop(self):
        """
        Returns the max population.
        """
        return self.maxPop


    def getTotalPop(self):
        """
        Gets the size of the current total virus population.
        returns: The total virus population (an integer)
        """
        return len(self.getViruses())

    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:

        - Determine whether each virus particle survives and updates the list
        of virus particles accordingly.

        - The current population density is calculated. This population density
          value is used until the next call to update()

        - Based on this value of population density, determine whether each
          virus particle should reproduce and add offspring virus particles to
          the list of viruses in this patient.

        returns: The total virus population at the end of the update (an
        integer)
        """

        # Clear viruses that clear in list of viruses
        self.viruses = [virus for virus in self.getViruses() if not virus.doesClear()]

        """ IMPORTANT NOTE:
            You will see below that we are slicing the list with [:], this returns
            a new list ... but why? ... because we are potentially manipulating the list
            by adding additional items to the end, we don't want to traverse the newly added
            items as part of this loop. We could have assigned a new variable but this works
            just as well and is a little more compact
        """

        # For each virus that does not clear ...
        for virus in self.getViruses()[:]:
            # If virus max pop not exceeded
            if self.getTotalPop() < self.getMaxPop():
                # Calculate virus pop density
                popDensity = float(self.getTotalPop()) / float(self.getMaxPop())
                # Attempt virus reproduction
                try:
                    self.viruses.append(virus.reproduce(popDensity))
                except NoChildException:
                    pass

        return self.getTotalPop()


def runTrial(numViruses, maxPop, maxBirthProb, clearProb):
    viruses = [SimpleVirus(maxBirthProb, clearProb) for x in xrange(numViruses)]
    patient = Patient(viruses, maxPop)

    # Run update within limit
    trial = []
    for x in xrange(300):
        trial.append(patient.update())

    # Return list with each step of virus growth
    return trial

def simulationWithoutDrug(numViruses, maxPop, maxBirthProb, clearProb,
                          numTrials):
    """
    Run the simulation and plot the graph for problem 3 (no drugs are used,
    viruses do not have any drug resistance).
    For each of numTrials trial, instantiates a patient, runs a simulation
    for 300 timesteps, and plots the average virus population size as a
    function of time.

    numViruses: number of SimpleVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)
    clearProb: Maximum clearance probability (a float between 0-1)
    numTrials: number of simulation runs to execute (an integer)
    """

    trials = [runTrial(numViruses, maxPop, maxBirthProb, clearProb) for x in xrange(numTrials)]

    trialLength = len(trials[0])
    results = []
    for x in xrange(trialLength):
        total = 0
        for y in xrange(len(trials)):
            total += trials[y][x]
        results.append(total / float(len(trials)))

    # Plot Results
    pylab.plot(results)
    pylab.title('SimpleVirus simulation')
    pylab.xlabel('Time Steps')
    pylab.ylabel('Average Virus Population')
    pylab.legend()
    pylab.show()


class ResistantVirus(SimpleVirus):
    """
    Representation of a virus which can have drug resistance.
    """

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
        """
        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)

        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'srinol':False}, means that this virus
        particle is resistant to neither guttagonol nor srinol.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.
        """

        # Init from Simple Virus inheritence
        SimpleVirus.__init__(self, maxBirthProb, clearProb)

        # New properties
        self.resistances = resistances
        self.mutProb = mutProb

    def getResistances(self):
        """
        Returns the resistances for this virus.
        """
        return self.resistances

    def getMutProb(self):
        """
        Returns the mutation probability for this virus.
        """
        return self.mutProb

    def isResistantTo(self, drug):
        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in TreatedPatient to determine how many virus
        particles have resistance to a drug.

        drug: The drug (a string)

        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
        return self.resistances.get(drug, False)


    def reproduce(self, popDensity, activeDrugs):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the TreatedPatient class.

        A virus particle will only reproduce if it is resistant to ALL the drugs
        in the activeDrugs list. For example, if there are 2 drugs in the
        activeDrugs list, and the virus particle is resistant to 1 or no drugs,
        then it will NOT reproduce.

        Hence, if the virus is resistant to all drugs
        in activeDrugs, then the virus reproduces with probability:

        self.maxBirthProb * (1 - popDensity).

        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent). The offspring virus
        will have the same maxBirthProb, clearProb, and mutProb as the parent.

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.

        For example, if a virus particle is resistant to guttagonol but not
        srinol, and self.mutProb is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90%
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        srinol and a 90% chance that the offspring will not be resistant to
        srinol.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings).

        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.
        """

        # Get reproduction chance like in Simple Virus
        reproduce = random.random()
        # If all active drugs have resistances within virus and virus does then reproduce
        if all(self.isResistantTo(drugs) for drugs in activeDrugs) and reproduce <= (self.getMaxBirthProb() * (1 - float(popDensity))):

            # Dictionary comp method:
            # For each k/v pair in resistances:
            #   If random number is >= the mutProb then leave untouched
            #   Else switch V for K in pair (ie. if True now False)
            resistances = {k:v if random.random() >= self.mutProb else not v for k, v in self.resistances.items()}

            # Long form example:
            # resistances = {}
            # for k, v in self.resistances.items():
            #     if random.random() >= self.mutProb:
            #         resistances[k] = v
            #     else:
            #         resistances[k] = not v

            return ResistantVirus(self.getMaxBirthProb(), self.getClearProb(), resistances, self.getMutProb())
        else:
            raise NoChildException


class TreatedPatient(Patient):
    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).

        viruses: The list representing the virus population (a list of
        virus instances)

        maxPop: The  maximum virus population for this patient (an integer)
        """

        # Init from Patient inheritence
        Patient.__init__(self, viruses, maxPop)

        # Initialize empty active drugs list
        self.activeDrugs = []


    def addPrescription(self, newDrug):
        """
        Administer a drug to this patient. After a prescription is added, the
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: The list of drugs being administered to a patient is updated
        """
        if newDrug not in self.activeDrugs:
            self.activeDrugs.append(newDrug)

    def getPrescriptions(self):
        """
        Returns the drugs that are being administered to this patient.

        returns: The list of drug names (strings) being administered to this
        patient.
        """
        return self.activeDrugs

    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in
        drugResist.

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'srinol'])

        returns: The population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
        return len([virus for virus in self.getViruses() if all(virus.isResistantTo(drug) for drug in drugResist)])

    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:

        - Determine whether each virus particle survives and update the list of
          virus particles accordingly

        - The current population density is calculated. This population density
          value is used until the next call to update().

        - Based on this value of population density, determine whether each
          virus particle should reproduce and add offspring virus particles to
          the list of viruses in this patient.
          The list of drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces.

        returns: The total virus population at the end of the update (an
        integer)
        """

        self.viruses = [virus for virus in self.viruses if not virus.doesClear()]

        for virus in self.getViruses()[:]:
             # If virus max pop not exceeded
            if self.getTotalPop() < self.getMaxPop():
                # Calculate virus pop density
                popDensity = float(self.getTotalPop()) / float(self.getMaxPop())
                try:
                    self.viruses.append(virus.reproduce(popDensity, self.getPrescriptions()))
                except NoChildException:
                    pass

        return self.getTotalPop()

#
# PART A
#
def plotTrialsHists(trials_300, trials_150, trials_75, trials_0):
        # Plot Results
        numBins = 50
        xlabel = 'Final Virus particle count'
        ylabel = 'Occurance in trials'

        pylab.hist(trials_300, numBins)
        pylab.subplot(221)
        pylab.title("300 Steps")
        pylab.xlabel(xlabel)
        pylab.ylabel(ylabel)

        pylab.hist(trials_150, numBins)
        pylab.subplot(222)
        pylab.title("150 Steps")
        pylab.xlabel(xlabel)
        pylab.ylabel(ylabel)

        pylab.hist(trials_75, numBins)
        pylab.subplot(223)
        pylab.title("75 Steps")
        pylab.xlabel(xlabel)
        pylab.ylabel(ylabel)

        pylab.hist(trials_0, numBins)
        pylab.subplot(224)
        pylab.title("0 Steps")
        pylab.xlabel(xlabel)
        pylab.ylabel(ylabel)

        pylab.show()

def runTrialwithDelayedDrugs(numViruses, maxPop, maxBirthProb, clearProb, resistances, mutProb, initialSteps):
    viruses = [ResistantVirus(maxBirthProb, clearProb, resistances, mutProb) for x in xrange(numViruses)]
    patient = TreatedPatient(viruses, maxPop)
    prescription = 'guttagonol'

    # Run first half of steps without drugs in patient
    for x in xrange(initialSteps):
        patient.update()

    # Add drug guttagonol
    patient.addPrescription(prescription)

    # Run second half of time steps with drug in patient
    for x in xrange(150):
        patient.update()

    # Return list with each step of virus growth
    return patient.getTotalPop()

def simulationDelayedTreatment(numViruses, maxPop, maxBirthProb, clearProb, resistances, mutProb, numTrials):
    trials_300 = []
    trials_150 = []
    trials_75 = []
    trials_0 = []

    for x in xrange (numTrials):
        trials_300.append(runTrialwithDelayedDrugs(numViruses, maxPop, maxBirthProb, clearProb, resistances, mutProb, 300))
        trials_150.append(runTrialwithDelayedDrugs(numViruses, maxPop, maxBirthProb, clearProb, resistances, mutProb, 150))
        trials_75.append(runTrialwithDelayedDrugs(numViruses, maxPop, maxBirthProb, clearProb, resistances, mutProb, 75))
        trials_0.append(runTrialwithDelayedDrugs(numViruses, maxPop, maxBirthProb, clearProb, resistances, mutProb, 0))

    plotTrialsHists(trials_300, trials_150, trials_75, trials_0)


#
# PART B
#
def runTwoDrugsDelayedTreatment(numViruses, maxPop, maxBirthProb, clearProb, resistances, mutProb, steps):
    viruses = [ResistantVirus(maxBirthProb, clearProb, resistances, mutProb) for x in xrange(numViruses)]
    patient = TreatedPatient(viruses, maxPop)
    prescription = 'guttagonol'
    prescription2 = 'grimpex'

    # Run first part of steps without drugs in patient
    for x in xrange(150):
        patient.update()

    # Add first drug
    patient.addPrescription(prescription)

    # Run second part of steps without drugs in patient (variable)
    for x in xrange(steps):
        patient.update()

    # Add second drug
    patient.addPrescription(prescription2)

    # Run second half of time steps with drug in patient
    for x in xrange(150):
        patient.update()

    # Return list with each step of virus growth
    return patient.getTotalPop()

def simulationTwoDrugsDelayedTreatment(numViruses, maxPop, maxBirthProb, clearProb, resistances, mutProb, numTrials):
    trials_300 = []
    trials_150 = []
    trials_75 = []
    trials_0 = []

    for x in xrange (numTrials):
        trials_300.append(runTwoDrugsDelayedTreatment(numViruses, maxPop, maxBirthProb, clearProb, resistances, mutProb, 300))
        trials_150.append(runTwoDrugsDelayedTreatment(numViruses, maxPop, maxBirthProb, clearProb, resistances, mutProb, 150))
        trials_75.append(runTwoDrugsDelayedTreatment(numViruses, maxPop, maxBirthProb, clearProb, resistances, mutProb, 75))
        trials_0.append(runTwoDrugsDelayedTreatment(numViruses, maxPop, maxBirthProb, clearProb, resistances, mutProb, 0))

    plotTrialsHists(trials_300, trials_150, trials_75, trials_0)


# Run it!
# simulationTwoDrugsDelayedTreatment(100, 1000, 0.1, 0.05, {'guttagonol': False}, 0.005, 2)
# simulationTwoDrugsDelayedTreatment(100, 1000, 0.1, 0.05, {'guttagonol': False, 'grimpex': False}, 0.005, 100)
