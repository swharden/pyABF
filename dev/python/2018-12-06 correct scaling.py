"""
A few ABFs were recorded with incorrect scaling factors.
This script can fix them.
"""

import os
import sys
import glob
import time
import numpy as np
import matplotlib.pyplot as plt

PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_DATA = os.path.abspath(PATH_HERE+"../../../data/abfs/")
PATH_SRC = os.path.abspath(PATH_HERE+"../../../src/")
sys.path.insert(0, PATH_SRC)
import pyabf

if __name__=="__main__":

    ### Example good ABF
    abfGood = R"X:\Data\F344\Aging BLA\halo\data\20180514_ts_0023.abf"
    # fInstrumentScaleFactor = 0.009999999776482582
    
    ### Example bad ABF
    abfBroken = R"X:\Data\F344\Aging BLA\halo\data\20180514_ts_0008.abf"
    # fInstrumentScaleFactor = 0.0005000000237487257

    ### Broken ABFs have a scaling factor too large by 20x.
    # fix the scaling factor, load the data with the new scaling, and save as ABF1
    abf=pyabf.ABF(abfBroken)
    abf._dataGain[0] = abf._dataGain[0]/20
    with open(abfBroken, 'rb') as fb:
        abf._loadAndScaleData(fb)
    abf.saveABF1(abf.abfFilePath.replace(".abf","_fixed.abf"))