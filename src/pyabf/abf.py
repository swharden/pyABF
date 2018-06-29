"""
Code in this file provides high-level ABF interactivity.
Things the user will interact with directly are in this file.
"""
import os
import sys
import glob
import datetime
import numpy as np
import warnings

if __name__ == "__main__":
    warnings.warn("DO NOT RUN THIS FILE DIRECTLY!")
    sys.path.append(os.path.dirname(__file__)+"/../")

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

        # execute core tasks (read header and data)
        self._loadEverything(abf, preLoadData)

        # perform ABF class init tasks
        self.baseline()

        # pre-load the first sweep
        self.setSweep(0)

    def baseline(self, timeSec1=None, timeSec2=None):
        """
        Call this to define a baseline region (in seconds). All subsequent
        data obtained from setSweep will be automatically baseline-subtracted
        to this region. This also affects downstream methods for data analysis.
        Call this without arguments to reset baseline.
        """
        if timeSec1 or timeSec2:
            if not timeSec1:
                timeSec1 = 0
            if not timeSec2:
                timeSec2 = abf.sweepLengthSec
            blPoint1 = timeSec1*self.dataRate
            blPoint2 = timeSec2*self.dataRate
            if blPoint1 < 0:
                blPoint1 = 0
            if blPoint2 >= len(self.sweepY):
                blPoint2 = len(self.sweepY)
            self.baselineTimes = [timeSec1, timeSec2]
            self.baselinePoints = [blPoint1, blPoint2]
        else:
            self.baselineTimes = False
            self.baselinePoints = False

    def setSweep(self, sweepNumber, channel=0, absoluteTime=False):
        """
        Args:
            sweepNumber: sweep number to load (starting at 0)
            channel: ABF channel (starting at 0)
            absoluteTime: if False, sweepX always starts at 0.
            baselineTimes: times (in seconds) to baseline subtract to
        """

        # TODO: prevent re-loading of the same sweep.

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

        # update stimulus waveform
        self._stimulusWaveform(sweepNumber, channel)

        # baseline subtraction
        if self.baselinePoints:
            baseline = np.average(
                self.sweepY[int(self.baselinePoints[0]):int(self.baselinePoints[1])])
            self.sweepY = self.sweepY-baseline
            
    @property
    def sweepC(self):
        """
        Generate the sweep command waveform only when requested.
        """
        return self._stimulusWaveform(sweepNumber=self.sweepNumber,
                                      channel=self.sweepChannel)

    def sweepAverage(self, timeSec1, timeSec2):
        """
        Return the average value between two times of the current sweep.
        """
        point1 = int(timeSec1*self.dataRate)
        point2 = int(timeSec2*self.dataRate)
        return np.average(self.sweepY[point1:point2])

    def sweepError(self, timeSec1, timeSec2, stdErr=True):
        """
        Return the standard error or standard deviation of the current sweep
        between the given times.
        """
        point1 = int(timeSec1*self.dataRate)
        point2 = int(timeSec2*self.dataRate)
        er = np.std(self.sweepY[point1:point2])
        if stdErr:
            er = er / np.sqrt(point2-point1)
        return er


# developer sandbox
if __name__ == "__main__":
    import matplotlib.pyplot as plt

    for fname in sorted(glob.glob("../data/*.abf")):
        abf = ABF(fname)
        print(abf.abfID, abf._commandContainsDeltas())

    print("DONE")
