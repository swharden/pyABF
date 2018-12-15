"""
Code here relates to the creation of stimulus waveforms from epoch tables.
"""

import os
import sys
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_DATA = os.path.abspath(PATH_HERE+"../../../data/abfs/")
PATH_SRC = os.path.abspath(PATH_HERE+"../../../src/")
sys.path.insert(0, PATH_SRC)
import pyabf
import numpy as np

class Epoch:

    # ABF settings
    _nDigitalOutputs = 8

    # settable values
    epochNumber = -1
    epochType = -1
    level = -1
    levelDelta = -1
    duration = -1
    durationDelta = -1
    digitalPattern = [3]*_nDigitalOutputs
    pulsePeriod = -1
    pulseWidth = -1
    dacNum = -1

    @property
    def epochLetter(self):
        if self.epochNumber<0:
            return "?"
        epochLetter = ""
        num = self.epochNumber
        while num>=0:
            epochLetter+=chr(num % 26 + 65)
            num -= 26
        return epochLetter

    @property
    def epochTypeStr(self):
        if self.epochType == 0:
            return "Off"
        elif self.epochType == 1:
            return "Step"
        elif self.epochType == 2:
            return "Ramp"
        elif self.epochType == 3:
            return "Pulse"
        elif self.epochType == 4:
            return "Tri"
        elif self.epochType == 5:
            return "Cos"
        elif self.epochType == 7:
            return "BiPhsc"
        else:
            return "Unknown"

    def __str__(self):
        txt = "Epoch: %s; " % (self.epochLetter)
        txt += "Type: %s (%d); " % (self.epochTypeStr, self.epochType)
        txt += "Level: %.02f (delta %.02f); " % (self.level,
                                                 self.levelDelta)
        txt += "Duration: %.02f (delta %.02f); " % (self.duration,
                                                    self.durationDelta)
        return txt


def epochTableText(epochList):
    """
    Given a list of epochs, return a text string formatted to look like the
    epoch table seen in pCLAMP and ClampFit.

    EPOCH                    A      B      C      D      E      F      G     
    Type                     Step   Step   Step   Step   Step   Train  Off   
    First level (nA)         0      -0.05  0      0      0      2.5    0     
    Delta level (nA)         0      0      0      0      0      0      0     
    First duration (samples) 2344   6250   7500   25     4975   5000   0     
    Delta duration (samples) 0      0      0      0      0      0      0     
    First duration (ms)      93.8   250.0  300.0  1.0    199.0  200.0  0.0   
    Delta duration (ms)      0.0    0.0    0.0    0.0    0.0    0.0    0.0   
    Digital pattern #3-0     0000   0000   0000   0001   0000   0000   0000  
    Digital pattern #7-4     0000   0000   0000   0000   0000   0000   0000  
    Train Period (samples)   0      500    0      0      500    250    0     
    Pulse Width (samples)    0      50     0      0      50     50     0     
    Train Rate (Hz)          0.00   50.00  0.00   0.00   50.00  100.00 0.00  
    Pulse Width (ms)         0.0    2.0    0.0    0.0    2.0    2.0    0.0   
    Intersweep holding: same as for signal ME1.

    """

    # remove empty epochs
    epochList = [x for x in epochList if x.duration>0]

    # prepare lists to hold values for each epoch
    epochCount = len(epochList)
    epochLetters = [''] * epochCount
    epochTypes = [''] * epochCount
    epochLevels = [''] * epochCount
    epochLevelsDelta = [''] * epochCount
    durations = [''] * epochCount
    durationsDelta = [''] * epochCount
    digitalPatternLs = [''] * epochCount
    digitalPatternHs = [''] * epochCount
    trainPeriods = [''] * epochCount
    pulseWidths = [''] * epochCount

    # populate values for each epoch
    for i, epoch in enumerate(epochList):
        assert isinstance(epoch, Epoch)
        if epoch.epochTypeStr=="Off":
            continue
        epochLetters[i] = epoch.epochLetter
        epochTypes[i] = epoch.epochTypeStr
        epochLevels[i] = "%.02f"%epoch.level
        epochLevelsDelta[i] = "%.02f"%epoch.levelDelta
        durations[i] = "%.02f"%epoch.duration
        durationsDelta[i] = "%.02f"%epoch.durationDelta
        digStr = "".join(str(int(x)) for x in epoch.digitalPattern)
        digitalPatternLs[i] = digStr[:4]
        digitalPatternHs[i] = digStr[4:]
        trainPeriods[i] = "%d"%epoch.pulsePeriod
        pulseWidths[i] = "%d"%epoch.pulseWidth

    # convert list of epoch values to a formatted string
    padLabel = 25
    pad = 10
    txt = ""
    txt += "EPOCH".rjust(padLabel)
    txt += "".join([x.rjust(pad) for x in epochLetters])+"\n"
    txt += "Type".rjust(padLabel)
    txt += "".join([x.rjust(pad) for x in epochTypes])+"\n"
    txt += "First Level".rjust(padLabel)
    txt += "".join([x.rjust(pad) for x in epochLevels])+"\n"
    txt += "Delta Level".rjust(padLabel)
    txt += "".join([x.rjust(pad) for x in epochLevelsDelta])+"\n"
    txt += "First Duration (ms)".rjust(padLabel)
    txt += "".join([x.rjust(pad) for x in durations])+"\n"
    txt += "Delta Duration (ms)".rjust(padLabel)
    txt += "".join([x.rjust(pad) for x in durationsDelta])+"\n"
    txt += "Digital Pattern #3-0".rjust(padLabel)
    txt += "".join([x.rjust(pad) for x in digitalPatternLs])+"\n"
    txt += "Digital Pattern #7-4".rjust(padLabel)
    txt += "".join([x.rjust(pad) for x in digitalPatternHs])+"\n"
    txt += "Train Period (samples)".rjust(padLabel)
    txt += "".join([x.rjust(pad) for x in trainPeriods])+"\n"
    txt += "Pulse Width (samples)".rjust(padLabel)
    txt += "".join([x.rjust(pad) for x in pulseWidths])+"\n"
    return txt.strip('\n')

def getEpochs(abf, dacNum=0):
    assert isinstance(abf, pyabf.ABF)

    if abf.abfVersion["major"] == 1:
        # the epoch table of AB2 files is stored in the ABF1 header
        epochCount = len(abf._headerV1.nEpochType)
        epochs = [None] * epochCount
        for i in range(epochCount):
            epoch = Epoch()
            epoch.epochNumber = i
            epoch.epochType = abf._headerV1.nEpochType[i]
            epoch.level = abf._headerV1.fEpochInitLevel[i]
            epoch.levelDelta = abf._headerV1.fEpochLevelInc[i]
            epoch.duration = abf._headerV1.lEpochInitDuration[i]
            epoch.durationDelta = abf._headerV1.lEpochDurationInc[i]
            epoch.pulsePeriod = 0 # not supported in ABF1
            epoch.pulseWidth = 0 # not supported in ABF1
            epochs[i] = epoch
    elif abf.abfVersion["major"] == 2:
        # the epoch table of AB2 files is stored in _epochPerDacSection
        # with digital output values in _epochSection
        epochs = []
        for i, epochDacNum in enumerate(abf._epochPerDacSection.nDACNum):
            if epochDacNum != dacNum:
                continue
            epoch = Epoch()
            epoch.epochNumber = abf._epochPerDacSection.nEpochNum[i]
            epoch.epochType = abf._epochPerDacSection.nEpochType[i]
            epoch.level = abf._epochPerDacSection.fEpochInitLevel[i]
            epoch.levelDelta = abf._epochPerDacSection.fEpochLevelInc[i]
            epoch.durationDelta = abf._epochPerDacSection.lEpochDurationInc[i]
            epoch.duration = abf._epochPerDacSection.lEpochInitDuration[i]
            epoch.pulsePeriod = abf._epochPerDacSection.lEpochPulsePeriod[i]
            epoch.pulseWidth = abf._epochPerDacSection.lEpochPulseWidth[i]
            epochs.append(epoch)
    else:
        raise ValueError("ABF version unsupported for epoch synthesis")
    
    return epochs

def showEpochTable(abfFileName, dacNum=0):
    abf = pyabf.ABF(abfFileName)
    print("\n" + abf.abfID)
    epochs = getEpochs(abf, dacNum)
    print(epochTableText(epochs))

if __name__ == "__main__":
    #showEpochTable(PATH_DATA+"/18711001.abf")
    #showEpochTable(PATH_DATA+"/05210017_vc_abf1.abf")
    showEpochTable(PATH_DATA+"/pclamp11_4ch.abf", 0)
    showEpochTable(PATH_DATA+"/pclamp11_4ch.abf", 1)