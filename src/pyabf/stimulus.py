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
    It is now being kept just so old code (which manually sets a string to
    Stimulus.protocolStorageDir) does not break.

    Waveform generation from the epoch table occurs in waveform.py.
    DAC file waveform loading (and caching) is done in this file.
    """

    # protocolStorageDir is a file path to the on-disc location where custom
    # waveforms for the stimset reconstruction are to be searched. It must be
    # manually assigned to after instantiation of a Stimulus object.
    protocolStorageDir = None

    waveformCache = {}

    def __init__(self, abf, channel):
        assert isinstance(abf, pyabf.ABF)
        self.abf = abf
        self.channel = channel
        self.text = "NOT INIT"

    def __str__(self):
        return "Stimulus(abf, %d)"%self.channel

    def __repr__(self):
        return "Stimulus(abf, %d)"%self.channel

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
            stimulusFromFile = self.stimulusWaveformFromFile()
            if stimulusFromFile is False:
                return np.full(self.abf.sweepPointCount, np.nan)
            else:
                return stimulusFromFile
                
        else:
            log.debug("unknown nWaveformSource (%d)" % nWaveformSource)
            self.text = "unknown nWaveformSource"
            return np.full(self.abf.sweepPointCount, np.nan)

    def stimulusWaveformFromFile(self):
        """
        Attempt to find the file associated with this ABF channel stimulus
        waveform, read that waveform (whether ABF or ATF), and return its
        waveform. If the file can't be found, return False.
        """

        # try to find the stimulus file in these obvious places
        stimFname = self.abf._stringsIndexed.lDACFilePath[self.channel]
        stimBN = os.path.basename(stimFname)
        abfFolder = os.path.dirname(self.abf.abfFilePath)

        # prepare an alternate path protocolStorageDir
        if self.protocolStorageDir:
            altStimPath = os.path.join(self.protocolStorageDir, stimBN)
        else:
            altStimPath = None

        # try to find the stimulus file
        if os.path.exists(stimFname):
            log.debug("stimulus file found where expected")
            stimFname = os.path.abspath(stimFname)
        elif os.path.exists(os.path.join(abfFolder, stimBN)):
            log.debug("stimulus file found next to ABF")
            stimFname = os.path.join(abfFolder, stimBN)
        elif altStimPath and os.path.exists(altStimPath):
            log.debug("stimulus file found in protocolStorageDir")
            stimFname = altStimPath
        else:
            log.debug("stimulus file never found: %s" % stimBN)
            log.debug("not even: %s" % stimBN)
            return False

        # get the real path so that not two cache keys point to the same object
        stimFname = os.path.realpath(stimFname)

        if Stimulus.waveformCache.get(stimFname):
            log.debug("stimulus file is already cached")
        else:
            # read the ABF or ATF stimulus file
            if stimFname.upper().endswith(".ABF"):
                log.debug("stimulus file is an ABF")
                # TODO: data requires custom stimulus scaling!
                Stimulus.waveformCache[stimFname] = pyabf.ABF(stimFname)
            elif stimFname.upper().endswith(".ATF"):
                log.debug("stimulus file is an ATF")
                # TODO: data requires custom stimulus scaling!
                Stimulus.waveformCache[stimFname] = pyabf.ATF(stimFname)

        return Stimulus.waveformCache[stimFname].sweepY