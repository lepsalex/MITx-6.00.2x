#!/usr/bin/env python
"""This script extracts temparature data from the julyTemps.txt file in the same
directory. If then uses pylab to build a nice chart to show the range in high/low
over the course of the month of July :)"""

# import pylab
import pylab
import numpy as np

def loadFile():
    # Read in July Temps file
    inFile = open('julyTemps.txt')

    # Initialize high/low lists
    highTemps = []
    lowTemps = []

    # Iterate over each line in the file
    for line in inFile:
        fields = line.split()
        if len(fields) != 3 or 'Boston' == fields[0] or 'Day' == fields[0]:
            continue
        else:
            highTemps.append(int(fields[1]))
            lowTemps.append(int(fields[2]))
    return (lowTemps, highTemps)

def producePlot(lowTemps, highTemps):
    # Get temperature differences
    diffTemps = list(np.array(highTemps) - np.array(lowTemps))
    pylab.plot(range(1,32), diffTemps)
    pylab.title('Day by Day Ranges in Temperature in Boston in July 2012')
    pylab.xlabel('Days')
    pylab.ylabel('Temperature Ranges')
    pylab.show()

(low, high) = loadFile()
producePlot(low, high)
