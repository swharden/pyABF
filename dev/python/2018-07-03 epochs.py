# import the pyabf module from this development folder
import os
import sys
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_SRC = os.path.abspath(PATH_HERE+"/../../src/")
PATH_DATA = os.path.abspath(PATH_HERE+"/../../data/abfs/")
sys.path.insert(0, PATH_SRC)  # for importing
sys.path.append("../../src/")  # for your IDE
import pyabf
import glob

import matplotlib.pyplot as plt
import numpy as np
import warnings


# class Epoch:
#     def __init__(self):
#         self.type = 1
#         self.level = -70
#         self.levelDelta = 5


class Epochs:
    def __init__(self, abf):
        self.abf = abf
        self._readHeader()

    def _readHeader(self, channel=0):
        # create variables to hold every field of the waveform editor
        self.epochPointStart = []
        self.epochPointEnd = []
        self.epochType = []
        self.epochValue = []
        self.epochValueDelta = []
        self.epochDuration = []
        self.epochDurationDelta = []
        self.epochPulsePeriod = []
        self.epochPulseWidth = []

        # TODO: do digital outputs (from EpochSection) belong here?
        # self.epochDigitalOutputs=[]

        # calculate the pre-epoch period (1/64th the sweep length, but why?)
        pointOffset = int(abf.sweepPointCount/64)

        # pre-load a fake step epoch to serve as the pre-epoch waveform
        self.epochPointStart.append(0)
        self.epochPointEnd.append(pointOffset)
        self.epochType.append(1)
        self.epochValue.append(abf.holdingCommand[channel])
        self.epochValueDelta.append(0)
        self.epochDuration.append(pointOffset)
        self.epochDurationDelta.append(0)
        self.epochPulsePeriod.append(0)
        self.epochPulseWidth.append(0)

        # load epoch values relevant to this channel
        for i, dacNum in enumerate(abf._epochPerDacSection.nDACNum):
            if dacNum != channel:
                continue
            self.epochPointStart.append(
                self.epochPointStart[-1]+self.epochDuration[-1])
            self.epochType.append(abf._epochPerDacSection.nEpochType[i])
            self.epochValue.append(abf._epochPerDacSection.fEpochInitLevel[i])
            self.epochValueDelta.append(
                abf._epochPerDacSection.fEpochLevelInc[i])
            self.epochDuration.append(
                abf._epochPerDacSection.lEpochInitDuration[i])
            self.epochDurationDelta.append(
                abf._epochPerDacSection.lEpochDurationInc[i])
            self.epochPulsePeriod.append(
                abf._epochPerDacSection.lEpochPulsePeriod[i])
            self.epochPulseWidth.append(
                abf._epochPerDacSection.lEpochPulseWidth[i])
            self.epochPointEnd.append(
                self.epochPointStart[-1]+self.epochDuration[-1])

        # do we revert back to holding current between epochs?
        if self.abf._dacSection.nInterEpisodeLevel[channel]:
            # if not, sustain the last epoch through to the end of the sweep
            self.epochPointEnd[-1] = self.abf.sweepPointCount-1 + pointOffset
        else:
            # if so, add a fake epoch (step) back to the holding values
            self.epochPointStart.append(self.epochPointEnd[-1])  # TODO: +1?
            self.epochPointEnd.append(abf.sweepPointCount - 1 + pointOffset)
            self.epochType.append(1)
            self.epochValue.append(self.epochValue[-1])
            self.epochValueDelta.append(0)
            self.epochDuration.append(0)
            self.epochDurationDelta.append(0)
            self.epochPulsePeriod.append(0)
            self.epochPulseWidth.append(0)

    def _formatLine(self, label, values):

        if label == "Type":
            for i, value in enumerate(values):
                if value == 0:
                    values[i] = "Off"
                elif value == 1:
                    values[i] = "Step"
                elif value == 2:
                    values[i] = "Ramp"
                else:
                    values[i] = "%d?" % value

        line = label.rjust(25, ' ')
        for val in values:
            if not isinstance(val, str):
                val = "%d" % val
            line += val.rjust(7, ' ')
        return line+"\n"

    def text(self):

        # TODO: make units for each channel available as an array

        out = "\n"

        for channel in self.abf.channelList:
            self._readHeader(channel=channel)
            epochList = [chr(x+64) for x in range(len(self.epochType))]
            epochList[0] = "pre"
            if self.epochDuration[-1] == 0:
                epochList[-1] = "post"

            out += self._formatLine("Ch%d EPOCH" % channel, epochList)
            out += self._formatLine("Type", self.epochType)
            out += self._formatLine("First Level (%s)" %
                                    self.abf.dacUnits[channel], self.epochValue)
            out += self._formatLine("Delta Level (%s)" %
                                    self.abf.dacUnits[channel], self.epochValueDelta)
            out += self._formatLine("First Duration (samples)",
                                    self.epochDuration)
            out += self._formatLine("Delta Duration (samples)",
                                    self.epochDurationDelta)
            out += self._formatLine("Train Period (samples)",
                                    self.epochPulsePeriod)
            out += self._formatLine("Pulse Width (samples)",
                                    self.epochPulseWidth)
            out += self._formatLine("Epoch Start (samples)",
                                    self.epochPointStart)
            out += self._formatLine("Epoch End (samples)", self.epochPointEnd)
            out += "\n"

        return out


if __name__ == "__main__":
    # abf = pyabf.ABF(PATH_DATA+"/171116sh_0013.abf")  # ramp
    # abf = pyabf.ABF(PATH_DATA+"/2018_04_13_0016a_original.abf") # delta t
    # abf = pyabf.ABF(PATH_DATA+"/14o16001_vc_pair_step.abf")  # delta c
    abf = pyabf.ABF(PATH_DATA+"/18702001-step.abf")  # complex step

    ep = Epochs(abf)
    print(ep.text())

    print("DONE")
