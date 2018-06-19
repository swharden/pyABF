"""
Code in this file provides high-level ABF interactivity.
Things the user will interact with directly are in this file.
"""

import glob
import datetime
import numpy as np
import matplotlib.pyplot as plt

from pyabf.core import ABFcore
import pyabf.text


class ABF(ABFcore):
    def __init__(self, abf, preLoadData=True):
        self._loadEverything(abf, preLoadData)
        self.setSweep(0)

    def setSweep(self, sweepNumber, channel=0):

        # ensure the sweep number is valid
        while sweepNumber < 0:
            sweepNumber = self.sweepCount - sweepNumber
        if sweepNumber >= self.sweepCount:
            sweepNumber = self.sweepCount - 1

        # determine data bounds for that sweep
        pointStart = self.sweepPointCount*sweepNumber
        pointEnd = pointStart + self.sweepPointCount
        self.sweepY = self.data[channel, pointStart:pointEnd]

    def getInfoPage(self):
        """
        Return an object to let the user inspect methods and variables 
        of this ABF class as well as the full contents of the ABF header
        """
        page = pyabf.text.InfoPage(self.abfID+".abf")

        # add info about this ABF instance

        page.addSection("ABF Class Methods")
        for thingName in sorted(dir(self)):
            if thingName.startswith("_"):
                continue
            thing = getattr(self, thingName)
            if "method" in str(type(thing)):
                page.addThing("abf.%s()" % (thingName))
                
        page.addSection("ABF Class Variables")
        for thingName in sorted(dir(self)):
            if thingName.startswith("_"):
                continue
            thing = getattr(self, thingName)
            if isinstance(thing, (int, list, float, datetime.datetime, str, np.ndarray)):
                page.addThing(thingName, thing)

        # add all ABF header information (different in ABF1 vs ABF2)

        headerParts = []
        if self.abfFileFormat==1:
            headerParts.append(["ABF1 Header", self._headerV1])
        elif self.abfFileFormat==2:
            headerParts.append(["ABF2 Header", self._headerV2])
            headerParts.append(["SectionMap", self._sectionMap])
            headerParts.append(["ProtocolSection", self._protocolSection])
            headerParts.append(["ADCSection", self._adcSection])
            headerParts.append(["DACSection", self._dacSection])
            headerParts.append(["EpochPerDACSection", self._epochPerDacSection])
            headerParts.append(["EpochSection", self._epochSection])
            headerParts.append(["TagSection", self._tagSection])
            headerParts.append(["StringsSection", self._stringsSection])
            headerParts.append(["StringsIndexed", self._stringsIndexed])
        for headerItem in headerParts:
            thingTitle, thingItself = headerItem
            page.addSection(thingTitle)
            page.addDocs(thingItself.__doc__)
            for subItemName in sorted(dir(thingItself)):
                if subItemName.startswith("_"):
                    continue
                page.addThing(subItemName, getattr(thingItself, subItemName))

        return page
