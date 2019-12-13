"""
ABFs can be created when signals are applied using the DAC. If these "stimulus
waveforms" are used, they either come from an epoch table or from a DAC file.
Code in this file determines where the stimulus comes from and returns it for
a given sweep and channel.

If the stimulus waveform comes from a file, code here also assists in caching
the data from that file so the file only needs to be read from disk once.
"""

import numpy as np
import copy
import os
import sys
import warnings
import pyabf
import pyabf.waveform

# cache stimulus files in this dictionary
# keys are stimulus filenames, values are ABF and ATF objects
cachedStimuli = {}


class Stimulus:
    """
    The Stimulus class used to be where all waveform generation happened.
    Waveform generation from the epoch table now occurs in waveform.py.
    This class is kept so old code doesn't break, but is getting dismantled.
    """

    def __init__(self, abf, channel):
        assert isinstance(abf, pyabf.ABF)
        self.abf = abf
        self.channel = channel
        self.text = ""  # this is displayed on the markdown info page

    def __str__(self):
        return "Stimulus(abf, %d)" % self.channel

    def __repr__(self):
        return "Stimulus(abf, %d)" % self.channel

    def stimulusWaveform(self, stimulusSweep=0):
        """
        Return a signal (the same size as a sweep) representing the command
        waveform of the DAC for the given channel.
        """

        if self.abf.abfVersion["major"] == 1:
            nWaveformEnable = self.abf._headerV1.nWaveformEnable[self.channel]
            nWaveformSource = self.abf._headerV1.nWaveformSource[self.channel]
        elif self.abf.abfVersion["major"] == 2:
            nWaveformEnable = self.abf._dacSection.nWaveformEnable[self.channel]
            nWaveformSource = self.abf._dacSection.nWaveformSource[self.channel]

        if nWaveformEnable == 0 or nWaveformSource == 0:
            self.text = "DAC waveform is not enabled"
            return np.full(self.abf.sweepPointCount,
                           self.abf.holdingCommand[self.channel])

        elif nWaveformSource == 1:
            epochTable = pyabf.waveform.EpochTable(self.abf, self.channel)
            self.text = str(epochTable)
            sweepWaveform = epochTable.epochWaveformsBySweep[stimulusSweep]
            sweepC = sweepWaveform.getWaveform()
            return sweepC

        elif nWaveformSource == 2:
            self.text = "DAC waveform is controlled by custom file"
            return stimulusWaveformFromFile(self.abf)

        else:
            self.text = "unknown nWaveformSource (%d)" % nWaveformSource
            return np.full(self.abf.sweepPointCount, np.nan)


def findStimulusWaveformFile(abf, channel=0):
    """
    Look for the stimulus waveform file in several places. Return the path
    where it can be found. Return None if it cannot be found.

    The original path is a windows filename stored in the ABF header
    """

    pathsTried = []

    pathInHeader = abf._stringsIndexed.lDACFilePath[channel]
    pathInHeader = os.path.abspath(pathInHeader)
    if os.path.exists(pathInHeader):
        return pathInHeader
    else:
        pathsTried.append(pathInHeader)

    linuxSafePath = pathInHeader.replace("\\", "/")
    stimBasename = os.path.basename(linuxSafePath)

    pathUserDefined = os.path.join(str(abf.stimulusFileFolder), stimBasename)
    pathUserDefined = os.path.abspath(pathUserDefined)
    if os.path.exists(pathUserDefined):
        return pathUserDefined
    else:
        pathsTried.append(pathUserDefined)

    abfFolder = os.path.dirname(abf.abfFilePath)
    pathSameFolder = os.path.join(abfFolder, stimBasename)
    pathSameFolder = os.path.abspath(pathSameFolder)
    if os.path.exists(pathSameFolder):
        return pathSameFolder
    else:
        pathsTried.append(pathSameFolder)

    pathsTried = ", ".join(pathsTried)
    warnings.warn("Could not locate stimulus file. Paths tried:\n"+pathsTried)
    return None


def stimulusWaveformFromFile(abf, channel=0):
    """
    Attempt to find the stimulus file used to record an ABF, read the stimulus
    file (ABF or ATF), and return the stimulus waveform (as a numpy array).
    """

    assert isinstance(abf, pyabf.ABF)
    assert channel in abf.channelList

    stimPath = findStimulusWaveformFile(abf, channel)

    if not stimPath:
        return np.full(abf.sweepPointCount, np.nan)

    if abf._cacheStimulusFiles:
        if not stimPath in cachedStimuli.keys():
            if stimPath.upper().endswith(".ABF"):
                cachedStimuli[stimPath] = pyabf.ABF(stimPath)
            elif stimPath.upper().endswith(".ATF"):
                cachedStimuli[stimPath] = pyabf.ATF(stimPath)
        return cachedStimuli[stimPath].sweepY
    else:
        if stimPath.upper().endswith(".ABF"):
            return pyabf.ABF(stimPath)
        elif stimPath.upper().endswith(".ATF"):
            return pyabf.ATF(stimPath)
