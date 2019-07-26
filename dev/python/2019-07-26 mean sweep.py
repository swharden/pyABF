import os
import sys
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_DATA = os.path.abspath(PATH_HERE+"../../../data/abfs/")
PATH_SRC = os.path.abspath(PATH_HERE+"../../../src/")
sys.path.insert(0, PATH_SRC)

import pyabf
import pyabf.tools.sweep
import matplotlib.pyplot as plt

if __name__ == "__main__":

    abf = pyabf.ABF(PATH_DATA+"/17o05026_vc_stim.abf")

    stimEpochNumber = 3
    stimOn = abf.sweepEpochs.p1s[stimEpochNumber] * abf.dataSecPerPoint
    stimOff = abf.sweepEpochs.p2s[stimEpochNumber] * abf.dataSecPerPoint
    baselineStart = stimOn - .04
    baselineEnd = stimOn - .01
    baseline = [baselineStart, baselineEnd]

    plt.figure(figsize=(8, 5))
    plt.grid(alpha=.2)
    plt.axhline(0, color='k', ls='--')
    plt.ylabel(abf.sweepLabelY)
    plt.xlabel(abf.sweepLabelX)
    plt.title(f"Mean response ({abf.sweepCount} sweeps)")

    for sweepNumber in abf.sweepList:
        abf.setSweep(sweepNumber, baseline=baseline)
        plt.plot(abf.sweepX, abf.sweepY, color='.5', alpha=.5, lw=.5)

    meanSweep = pyabf.tools.sweep.getMeanSweep(abf, baseline)
    plt.plot(abf.sweepX, meanSweep, color='k', label="mean")

    plt.axis([1.10, 1.25, -125, 50])

    plt.axvspan(baselineStart, baselineEnd, color='b',
                alpha=.1, lw=0, label="baseline")

    plt.axvspan(stimOn, stimOff, color='r',
                alpha=.3, lw=0, label="stimulation")

    plt.legend()
    plt.show()
