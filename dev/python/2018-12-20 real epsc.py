"""
Determine what paramaters create real-looking EPSCs.
What I concluded was that 30pA and 180ms tau looks good.
"""

import os
import sys
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_DATA = os.path.abspath(PATH_HERE+"../../../data/abfs/")
PATH_SRC = os.path.abspath(PATH_HERE+"../../../src/")
sys.path.insert(0, PATH_SRC)
import pyabf
import pyabf.tools.generate
import glob
import matplotlib.pyplot as plt
import numpy as np


def plotRealEPSC():

    # load a trae with a real life EPSC
    abfPath = R"X:\Data\SD\Piriform Oxytocin\core ephys 2018\Sagittal Pilot\2018_12_11_ts_0020.abf"
    abf = pyabf.ABF(abfPath)
    abf.setSweep(12, baseline=[2.6, 2.68])

    # blank-out data we don't want to see
    t1, t2 = [2.68, 2.75]
    abf.sweepY[:int(t1*abf.dataRate)] = np.nan
    abf.sweepY[int(t2*abf.dataRate):] = np.nan

    # plot it
    plt.figure()
    plt.plot(abf.sweepX, abf.sweepY, alpha=.5, label="real")
    return


def plotFakeEPSC():

    # simulate a trace
    dataRate = 20000
    synth = pyabf.tools.generate.SynthSweep(dataRate, 10)

    # blank-out data we don't want to see
    t1, t2 = [2.68, 2.75]
    synth.sweepY[:int(t1*dataRate)] = np.nan
    synth.sweepY[int(t2*dataRate):] = np.nan

    # add an EPSC for comparison
    tauMs = 180
    synth.addEvent(2.7, -35, tauMs, False)

    # plot it
    plt.plot(synth.sweepX, synth.sweepY, lw=3, alpha=.5, label="simulated")


if __name__ == "__main__":
    plotRealEPSC()
    plotFakeEPSC()

    plt.grid(alpha=.2)
    plt.margins(0, .1)
    plt.title("Real vs. Simulated EPSC")
    plt.ylabel("current (pA)")
    plt.xlabel("time (sec)")
    plt.legend()
    plt.savefig(__file__+".png")
    print("DONE")