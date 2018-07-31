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


class ABF(ABFcore):
    def __init__(self, abf, preLoadData=True):

        # execute core tasks (read header and data)
        self._preLoadData = preLoadData
        self._loadEverything(abf)

        # perform ABF class init tasks
        self.baseline()

        # pre-load the first sweep
        self.setSweep(0)

    def __repr__(self):
        return 'ABF(abf="%s", preLoadData=%s)' % (self.abfFilePath, self._preLoadData)

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
        """

        # basic error checking
        if not sweepNumber in self.sweepList:
            msg = "Sweep %d not available (must be 0 - %d)" % (
                sweepNumber, self.sweepCount-1)
            raise ValueError(msg)
        if not channel in self.channelList:
            msg = "Channel %d not available (must be 0 - %d)" % (
                channel, self.channelCount-1)
            raise ValueError(msg)


        if not "data" in (dir(self)):
            print("ABF data not preloaded. Loading now...")
            self._fileOpen()
            self._loadAndScaleData()
            self._fileClose()

        # TODO: prevent re-loading of the same sweep.

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

        # update epoch time points
        self._updateTimePoints()

        # baseline subtraction
        if self.baselinePoints:
            baseline = np.average(
                self.sweepY[int(self.baselinePoints[0]):int(self.baselinePoints[1])])
            self.sweepY = self.sweepY-baseline
            self.sweepLabelY = "Δ " + self.sweepLabelY

        # make sure sweepPointCount is always accurate
        assert (self.sweepPointCount == len(self.sweepY))

    @property
    def sweepC(self):
        """
        Generate the sweep command waveform only when requested.
        """
        #return self._stimulusWaveform(sweepNumber=self.sweepNumber,channel=self.sweepChannel)
        sweepEpochs = self.epochsByChannel[self.sweepChannel]
        return sweepEpochs.stimulusWaveform(self.sweepNumber)

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
    warnings.warn("DO NOT RUN THIS FILE DIRECTLY!!!!")

    PATH_HERE = os.path.dirname(__file__)
    PATH_DATA = os.path.abspath(PATH_HERE + "/../../data/abfs/")
    for fname in sorted(glob.glob(PATH_DATA+"/*.abf")):
        if not "model_vc_ramp" in fname:
            continue
        abf = ABF(fname)
        for channel in abf.channelList:
            print(abf.epochsByChannel[channel].text)
            #epochs = abf.epochsByChannel[channel]
            #print(f"{abf.abfID} Ch{channel} {epochs}")


    print("DONE")
