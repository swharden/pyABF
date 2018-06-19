import glob
from pyabf.core import ABFcore
import matplotlib.pyplot as plt

class ABF(ABFcore):
    def __init__(self, abf, preLoadData=True):
        self._loadEverything(abf, preLoadData)
        self.setSweep(0)

    def setSweep(self, sweepNumber, channel=0):

        # ensure the sweep number is valid
        while sweepNumber<0:
            sweepNumber = self.sweepCount - sweepNumber
        if sweepNumber>=self.sweepCount:
            sweepNumber = self.sweepCount - 1

        # determine data bounds for that sweep
        pointStart = self.sweepPointCount*sweepNumber
        pointEnd = pointStart + self.sweepPointCount
        self.sweepY = self.data[channel,pointStart:pointEnd]