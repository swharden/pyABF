"""
Test ABF with variable length sweeps.
"""

import glob
import os
import sys
import matplotlib.pyplot as plt
import numpy as np

try:
    PATH_HERE = os.path.abspath(os.path.dirname(__file__))
    PATH_DATA = os.path.abspath(PATH_HERE+"../../../data/abfs/")
    PATH_SRC = os.path.abspath(PATH_HERE+"../../../src/")
    DATA_FOLDER = os.path.join(PATH_SRC, "../data/abfs/")
    sys.path.insert(0, PATH_SRC)
    import pyabf
except:
    raise EnvironmentError()

if __name__ == "__main__":

    ### THIS EXAMPLE ASSUMES A SINGLE CHANNEL ###

    filePath = DATA_FOLDER + "/2020_06_16_0000.abf"
    abf = pyabf.ABF(filePath)

    sweepYs = []
    sweepXs = []
    with open(filePath, 'rb') as fb:
        fb.seek(abf.dataByteStart)
        for sweepIndex in abf.sweepList:
            firstPoint = abf._synchArraySection.lStart[sweepIndex]
            pointCount = abf._synchArraySection.lLength[sweepIndex]
            sweepY = np.fromfile(fb, dtype=abf._dtype, count=pointCount)
            sweepY = np.multiply(sweepY, abf._dataGain)
            sweepY = np.add(sweepY, abf._dataOffset)
            sweepYs.append(sweepY)
            offsetSec = firstPoint / abf.dataRate
            sweepX = np.arange(len(sweepY)) / abf.dataRate + offsetSec
            sweepXs.append(sweepX)

    plt.figure()
    for i in abf.sweepList:
        plt.plot(sweepXs[i], sweepYs[i])
    plt.show()
