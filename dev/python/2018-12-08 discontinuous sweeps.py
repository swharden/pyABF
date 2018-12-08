"""
Ensure discontinuous sweeps (sweeps whose sweep length is less than their inter-
sweep interval) are loaded properly and work with comments.

I confirmed there is a problem on 2018_11_16_sh_0006.abf: print(abf) says total 
length of 0.10 min when it should be 5 minutes.

Inter-sweep interval seems to be defined by fEpisodeStartToStart.
"""

import os
import sys
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_DATA = os.path.abspath(PATH_HERE+"../../../data/abfs/")
PATH_SRC = os.path.abspath(PATH_HERE+"../../../src/")
sys.path.insert(0, PATH_SRC)
import pyabf
import glob

if __name__ == "__main__":
    print("ABFs where sweep length != sweep interval:")
    print("interval\tlength\t\tABF")
    for abfFilePath in glob.glob(PATH_DATA+"/*.abf"):
        abf = pyabf.ABF(abfFilePath)
        if abf.sweepIntervalSec != abf.sweepLengthSec:
            print("%.02f\t\t%.02f\t\t%s" %
                  (abf.sweepIntervalSec, abf.sweepLengthSec, abf.abfFilePath))
            abf.setSweep(1, absoluteTime=True)
            assert(abf.sweepX[0])==abf.sweepIntervalSec