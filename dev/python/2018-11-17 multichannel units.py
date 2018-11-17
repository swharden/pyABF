"""
Double-check to ensure sweepUnitsY are always the right units for multi-channel
abfs that mix voltage-clamp and current-clamp. It passed right away, so I think
whatever bug used to be here got fixed a while back
"""

import os
import sys
import glob
import time
import numpy as np

PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_DATA = os.path.abspath(PATH_HERE+"../../../data/abfs/")
PATH_SRC = os.path.abspath(PATH_HERE+"../../../src/")
sys.path.insert(0, PATH_SRC)
import pyabf

if __name__=="__main__":
    for abfFileName in glob.glob(PATH_DATA+"/*.abf"):
        abf = pyabf.ABF(abfFileName)
        if abf.channelCount>1:
            units1 = abf.adcUnits[0]
            units2 = abf.adcUnits[1]
            if units1 != units2:
                # found a multi-channel ABF with different units
                print(f"{abf.abfID} has {abf.channelCount} channels")
                abf.setSweep(sweepNumber=0, channel=0)
                assert abf.sweepUnitsY == units1
                abf.setSweep(sweepNumber=0, channel=1)
                assert abf.sweepUnitsY == units2