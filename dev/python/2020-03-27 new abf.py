"""
Test loading 2015_09_10_0001.abf which reportedly crashes...
"""

import glob
import os
import sys

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
    abf = pyabf.ABF(DATA_FOLDER + "/2015_09_10_0001.abf")
    for sweepNumber in abf.sweepList:
        abf.setSweep(sweepNumber)
        print("Sweep:", abf.sweepY)
        print("Command:", abf.sweepC)
