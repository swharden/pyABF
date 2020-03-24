"""
big file test (64-bit numpy required)
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
    abf = pyabf.ABF(DATA_FOLDER + "/vc_drug_memtest.abf")
    for sweepNumber in abf.sweepList:
        abf.setSweep(sweepNumber)
        print(abf.sweepY)
