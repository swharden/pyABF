"""
I got an email that this ABF1 is messing up.
This script investigates the issue.
"""

import os
import sys
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_DATA = os.path.abspath(PATH_HERE+"../../../data/abfs/")
PATH_SRC = os.path.abspath(PATH_HERE+"../../../src/")
sys.path.insert(0, PATH_SRC)

import matplotlib.pyplot as plt
import numpy as np
import glob

import pyabf

def listMultichannelABF1Files():
    for fname in glob.glob(PATH_DATA+"/*.abf"):
        abf = pyabf.ABF(fname)
        if abf.abfVersion["major"] > 1:
            continue
        if abf.channelCount == 1:
            continue
        print(abf.abfFilePath, abf.sweepX[-1], abf.sweepPointCount)

def plotAdriansFile():
    abf = pyabf.ABF(PATH_DATA+"/190619B_0003.abf")

    print(abf)
    # OUTPUT:
    #   ABF (version 1.8.3.0) with 2 channels (mV, pA),
    #   sampled at 20.0 kHz, containing 10 sweeps,
    #   having no tags, with a total length of 0.28 minutes,
    #   recorded with protocol "IV_FI_IN0_saray".

    plt.figure(figsize=(10, 4))
    plt.grid(alpha=.2, ls='--')
    for sweepNumber in abf.sweepList:
        abf.setSweep(sweepNumber)
        plt.plot(abf.sweepX, abf.sweepY, label=f"sweep {sweepNumber+1}")
    plt.margins(0, .1)
    plt.legend(fontsize=8)
    plt.title(abf.abfID+".abf")
    plt.ylabel(abf.sweepLabelY)
    plt.xlabel(abf.sweepLabelX)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    #listMultichannelABF1Files()
    plotAdriansFile()