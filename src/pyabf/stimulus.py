"""
ABFs can be created when signals are applied using the DAC. If these "stimulus 
waveforms" are used, they either come from an epoch table or from a DAC file.
Code in this file determines where the stimulus comes from and returns it for
a given sweep and channel.
"""

import numpy as np
import copy
import os
import sys

import pyabf
import pyabf.waveform

import logging
logging.basicConfig(level=logging.WARNING)
log = logging.getLogger(__name__)


class Stimulus:
    """
    The Stimulus class USED to be where all waveform generation happened.

    It's kept here so old code doesn't break, but is getting dismantled.

    Waveform generation from the epoch table now occurs in waveform.py.
    """

    # keys are stimulus filenames (ABF or ATF), values are the first sweepY
    stimulusWaveformCache = {}

    def __init__(self, abf, channel):
        assert isinstance(abf, pyabf.ABF)
        self.abf = abf
        self.channel = channel
        self.text = "NOT INIT"

    def __str__(self):
        return "Stimulus(abf, %d)" % self.channel

    def __repr__(self):
        return "Stimulus(abf, %d)" % self.channel

    def stimulusWaveform(self, sweepNumber=0):
        """
        Return a signal (the same size as a sweep) representing the command
        waveform of the DAC for the given channel. Since command waveforms
        can change sweep to sweep due to deltas, an optional sweep number can
        be given as an argument.
        """

        if self.abf.abfVersion["major"] == 1:
            nWaveformEnable = self.abf._headerV1.nWaveformEnable[self.channel]
            nWaveformSource = self.abf._headerV1.nWaveformSource[self.channel]
        elif self.abf.abfVersion["major"] == 2:
            nWaveformEnable = self.abf._dacSection.nWaveformEnable[self.channel]
            nWaveformSource = self.abf._dacSection.nWaveformSource[self.channel]

        if nWaveformEnable == 0 or nWaveformSource == 0:
            log.debug("DAC waveform is not enabled")
            self.text = "DAC waveform is not enabled"
            return np.full(self.abf.sweepPointCount,
                           self.abf.holdingCommand[self.channel])

        elif nWaveformSource == 1:
            log.debug("DAC waveform is created from epoch table")
            epochTable = pyabf.waveform.EpochTable(self.abf, self.channel)
            self.text = str(epochTable)
            sweepWaveform = epochTable.epochWaveformsBySweep[sweepNumber]
            sweepC = sweepWaveform.getWaveform()
            return sweepC

        elif nWaveformSource == 2:
            log.debug("DAC waveform is controlled by custom file")
            self.text = "DAC waveform is controlled by custom file"
            stimulusFromFile = stimulusWaveformFromFile(self.abf)
            if stimulusFromFile is False:
                return np.full(self.abf.sweepPointCount, np.nan)
            else:
                return stimulusFromFile

        else:
            log.debug("unknown nWaveformSource (%d)" % nWaveformSource)
            self.text = "unknown nWaveformSource"
            return np.full(self.abf.sweepPointCount, np.nan)

    @property
    def protocolStorageDir(self):
        print(
            "WARNING: access abf.stimulusFileFolder instead of Stimulus.protocolStorageDir")
        return self.abf.stimulusFileFolder

    @protocolStorageDir.setter
    def protocolStorageDir(self, val=None):
        print("WARNING: set abf.stimulusFileFolder instead of Stimulus.protocolStorageDir")
        self.abf.stimulusFileFolder = val


def stimulusWaveformFromFile(abf, channel=0):
    """
    Attempt to find the stimulus file used to record an ABF, read the stimulus
    file (ABF or ATF), and return the stimulus waveform (as a numpy array).

    Now: If the file can't be found, returns False
    Soon: If the file can't be found, returns an array of nans.
    """

    assert isinstance(abf, pyabf.ABF)

    # try to find the stimulus file in these obvious places
    stimFname = abf._stringsIndexed.lDACFilePath[channel]
    stimBN = os.path.basename(stimFname)
    abfFolder = os.path.dirname(abf.abfFilePath)
    altPath = os.path.join(abf.stimulusFileFolder, stimBN)

    # try to find the stimulus file
    if os.path.exists(stimFname):
        log.debug("stimulus file found where expected")
        stimFname = os.path.abspath(stimFname)
    elif os.path.exists(os.path.join(abfFolder, stimBN)):
        log.debug("stimulus file found next to ABF")
        stimFname = os.path.join(abfFolder, stimBN)
    elif altPath and os.path.exists(altPath):
        log.debug("stimulus file found in alternate location (altPath)")
        stimFname = altPath
    else:
        log.debug("stimulus file never found: %s" % stimBN)
        log.debug("not even: %s" % stimBN)
        return False

    # get the real path so that not two cache keys point to the same object
    stimFname = os.path.realpath(stimFname)

    if abf._cacheStimulusFiles and Stimulus.stimulusWaveformCache.get(stimFname):
        log.debug("stimulus file is already cached")
    else:
        # read the ABF or ATF stimulus file
        if stimFname.upper().endswith(".ABF"):
            log.debug("stimulus file is an ABF")
            # TODO: data requires custom stimulus scaling!
            Stimulus.stimulusWaveformCache[stimFname] = pyabf.ABF(stimFname)
        elif stimFname.upper().endswith(".ATF"):
            log.debug("stimulus file is an ATF")
            # TODO: data requires custom stimulus scaling!
            Stimulus.stimulusWaveformCache[stimFname] = pyabf.ATF(stimFname)

    return Stimulus.stimulusWaveformCache[stimFname].sweepY
