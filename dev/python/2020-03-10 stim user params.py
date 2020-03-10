"""
Invent a better (truly unique) GUID system
"""

import glob
import os
import sys
import matplotlib.pyplot as plt
import uuid
import datetime
import time
import hashlib

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
    abf = pyabf.ABF(PATH_DATA+"/2020_03_02_0000.abf")

    # show clamp level for epoch B of every sweep
    levelsBySweep = []
    epochIndex = 2
    for sweepNumber in abf.sweepList:
        abf.setSweep(sweepNumber)
    print(levelsBySweep)

    # create a figure
    plt.figure(figsize=(8,8))
    for sweepNumber in abf.sweepList:
        plt.subplot(311)
        abf.setSweep(sweepNumber, channel=0)
        plt.plot(abf.sweepX, abf.sweepY, color='b', lw=.5)
        plt.subplot(313)
        plt.plot(abf.sweepX, abf.sweepC, color='r', lw=.5)
        plt.subplot(312)
        abf.setSweep(sweepNumber, channel=1)
        plt.plot(abf.sweepX, abf.sweepY, color='k', lw=.5)
    plt.tight_layout()
    plt.savefig(__file__+".png")