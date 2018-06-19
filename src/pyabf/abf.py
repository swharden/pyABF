"""
Code in this file provides high-level ABF interactivity.
Things the user will interact with directly are in this file.
"""

import glob
import datetime
import numpy as np
import matplotlib.pyplot as plt

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

    def setSweep(self, sweepNumber, channel=0):

        # ensure the sweep number is valid
        assert sweepNumber>=0
        assert sweepNumber<self.sweepCount

        # ensure channel number is valid
        assert channel>=0
        assert channel<self.dataChannelCount

        # determine data bounds for that sweep
        pointStart = self.sweepPointCount*sweepNumber
        pointEnd = pointStart + self.sweepPointCount

        self.sweep = Sweep()
        self.sweep.units = self.adcUnits[channel]
        self.sweep.unitsClamp = self.dacUnits[channel]
        self.sweep.number = sweepNumber
        self.sweep.channel = channel
        self.sweep.y = self.data[channel, pointStart:pointEnd]
        self.sweep.x = np.arange(len(self.sweep.y))*self.dataSecPerPoint
