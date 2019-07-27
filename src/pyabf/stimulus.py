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
        self.text = "" # this is displayed on the markdown info page

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

    @property
    def protocolStorageDir(self):
        warnings.warn("set abf.stimulusFileFolder (not protocolStorageDir)")
        return self.abf.stimulusFileFolder

    @protocolStorageDir.setter
    def protocolStorageDir(self, val=None):
        warnings.warn("set abf.stimulusFileFolder (not protocolStorageDir)")
        self.abf.stimulusFileFolder = val

def stimulusWaveformFromFile(abf, channel=0):
    """
    Attempt to find the stimulus file used to record an ABF, read the stimulus
    file (ABF or ATF), and return the stimulus waveform (as a numpy array).
    """

    assert isinstance(abf, pyabf.ABF)
    assert channel in abf.channelList

    # prepare potential file paths where the stimulus file may exist
    stimFname = abf._stringsIndexed.lDACFilePath[channel]
    stimBN = os.path.basename(stimFname.replace("\\", "/"))
    abfFolder = os.path.dirname(abf.abfFilePath)
    pathSameFolder = os.path.join(abfFolder, stimBN)
    pathAlt = os.path.join(str(abf.stimulusFileFolder), stimBN)

    # try to find the stimulus file
    if os.path.exists(stimFname):
        stimFname = os.path.abspath(stimFname)
    elif os.path.exists(pathSameFolder):
        stimFname = pathSameFolder
    elif pathAlt and os.path.exists(pathAlt):
        stimFname = pathAlt
    else:
        warnings.warn("could not locate stimulus file "+stimBN)
        return np.full(abf.sweepPointCount, np.nan)

    # the stimulus waveform file was found, consider caching
    if abf._cacheStimulusFiles:
        stimFname = os.path.realpath(stimFname)
        if not stimFname in cachedStimuli.keys():
            if stimFname.upper().endswith(".ABF"):
                cachedStimuli[stimFname] = pyabf.ABF(stimFname)
            elif stimFname.upper().endswith(".ATF"):
                cachedStimuli[stimFname] = pyabf.ATF(stimFname)
        return cachedStimuli[stimFname].sweepY
    else:
        if stimFname.upper().endswith(".ABF"):
            return pyabf.ABF(stimFname)
        elif stimFname.upper().endswith(".ATF"):
            return pyabf.ATF(stimFname)