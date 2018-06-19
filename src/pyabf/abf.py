"""
Code in this file provides high-level ABF interactivity.
Things the user will interact with directly are in this file.
"""
import sys
import glob
import datetime
import numpy as np
import warnings

if __name__ == "__main__":
    warnings.warn("DO NOT RUN THIS FILE DIRECTLY! It is for testing only.")
    sys.path.append(".")

from pyabf.core import ABFcore


class Sweep:
    def __init__(self):
        self.x = None
        self.y = None
        self.c = None
        self.number = None
        self.channel = None
        self.units = None
        self.unitsX = "seconds"
        self.unitsClamp = None


class ABF(ABFcore):
    def __init__(self, abf, preLoadData=True):
        self._loadEverything(abf, preLoadData)
        self.setSweep(0)

    def setSweep(self, sweepNumber, channel=0, absoluteTime=False):

        # sweep number error checking
        while sweepNumber < 0:
            sweepNumber = self.sweepCount - sweepNumber
        if sweepNumber >= self.sweepCount:
            warnings.warn(
                "Requested sweep is out of bounds. Using last sweep.")
            sweepNumber = self.sweepCount

        # channel error checking
        if channel < 0 or channel >= self.channelCount:
            warnings.warn(
                "Requested channel is out of bounds. Using first channel.")

        # determine data bounds for that sweep
        pointStart = self.sweepPointCount*sweepNumber
        pointEnd = pointStart + self.sweepPointCount

        # start updating class-level variables

        # sweep information
        self.sweepNumber = sweepNumber
        self.sweepChannel = channel
        self.sweepUnitsY = self.adcUnits[channel]
        self.sweepUnitsC = self.dacUnits[channel]
        self.sweepUnitsX = "sec"

        # standard labels
        self.sweepLabelY = "{} ({})".format(
            self.adcNames[channel], self.adcUnits[channel])
        self.sweepLabelC = "{} ({})".format(
            self.dacNames[channel], self.dacUnits[channel])
        self.sweepLabelX = "time (seconds)"

        # use fancy labels for known units
        if self.sweepUnitsY == "pA":
            self.sweepLabelY = "Clamp Current (pA)"
            self.sweepLabelC = "Membrane Potential (mV)"
        elif self.sweepUnitsY == "mV":
            self.sweepLabelY = "Membrane Potential (mV)"
            self.sweepLabelC = "Applied Current (pA)"

        # load the actual sweep data
        self.sweepY = self.data[channel, pointStart:pointEnd]
        self.sweepX = np.arange(len(self.sweepY))*self.dataSecPerPoint
        if absoluteTime:
            self.sweepX += sweepNumber * self.sweepLengthSec
        self._updateStimulusWaveform(sweepNumber, channel)




# developer sandbox
if __name__ == "__main__":
    import matplotlib.pyplot as plt

    for fname in sorted(glob.glob("../data/*.abf")):
        abf = ABF(fname)
        print(abf.abfID, abf._commandContainsDeltas())

    # abf = ABF("../data/171116sh_0018.abf")

    # fig = plt.figure()
    # ax1 = fig.add_subplot(211)
    # ax2 = fig.add_subplot(212, sharex=ax1)
    # for sweep in abf.sweepList:
    #     abf.setSweep(sweep, absoluteTime=True)
    #     ax1.plot(abf.sweepX, abf.sweepY, color='b')
    #     ax2.plot(abf.sweepX, abf.sweepC, color='r')
    # plt.show()

    print("DONE")
