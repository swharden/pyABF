"""
Ensure no ABFs have empty sweepC arrays
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

if __name__=="__main__":
    # show digital outputs
    # for abfFile in sorted(glob.glob(PATH_DATA+"/*.abf")):
    #     abf=pyabf.ABF(abfFile)
    #     print(abf.abfID.rjust(35), abf.sweepC, abf.sweepD(4))

    # abf=pyabf.ABF(PATH_DATA+"/2018_04_13_0016a_original.abf")
    # for sweep in abf.sweepList:
    #     plt.plot(abf.sweepX, abf.sweepC)
    # plt.show()

    # show sweep epoch stuff
    for abfFile in sorted(glob.glob(PATH_DATA+"/*.abf")):
        abf=pyabf.ABF(abfFile)
        print(abf.sweepEpochs.levels)