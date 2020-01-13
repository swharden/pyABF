"""
Test ABFs with invalid date codes
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

    ### for ABF1 files
    #lFileStartDate = is a 4-byte integer at byte 20
    #lFileStartTime = is a 4-byte integer at byte 24
    abf1 = pyabf.ABF(DATA_FOLDER+"/invalidDate-abf1.abf")
    print(abf1.abfDateTime)

    ### for ABF2 files
    #lFileStartDate = is a 4-byte integer at byte 16
    #lFileStartTime = is a 4-byte integer at byte 20
    abf2 = pyabf.ABF(DATA_FOLDER+"/invalidDate-abf2.abf")
    print(abf2.abfDateTime)