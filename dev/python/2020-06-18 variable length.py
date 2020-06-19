"""
Test ABF with variable length sweeps.
"""

import glob
import os
import sys
import matplotlib.pyplot as plt

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
    abf = pyabf.ABF(DATA_FOLDER + "/2020_06_16_0000.abf")

    for sweepIndex in abf.sweepList:
        sweepStart = abf._syncArraySection.lStart[sweepIndex]
        sweepStartSec = sweepStart / abf.dataRate

        sweepLength = abf._syncArraySection.lLength[sweepIndex]
        sweepPointCount = sweepLength / abf.channelCount
        sweepLengthSec = sweepPointCount / abf.dataRate
        print(f"sweep {sweepIndex + 1} " +
              f"starts at {sweepStartSec} sec " +
              f"and lasts {sweepLengthSec} sec")
