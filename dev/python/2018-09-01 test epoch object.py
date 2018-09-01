"""
test interaction with the abf epoch object
"""

import os
import sys
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_DATA = os.path.abspath(PATH_HERE+"../../../data/abfs/")
PATH_SRC = os.path.abspath(PATH_HERE+"../../../src/")
sys.path.insert(0, PATH_SRC)
import pyabf
import glob
import numpy as np
import matplotlib.pyplot as plt


if __name__ == "__main__":
    for fname in glob.glob(PATH_DATA+"/*.abf"):
        abf = pyabf.ABF(fname)
        if abf.abfVersion["major"] == 1:
            continue
        for sweep in abf.sweepList:
            abf.setSweep(sweep)
            plt.figure()
            plt.title(abf.abfID)
            plt.step(abf.epochPoints, abf.epochValues)
            break
    plt.show()
