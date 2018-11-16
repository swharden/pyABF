"""
Code here relates to the creation of stimulus waveforms. Usually this is
accomplished by synthesizing a waveform by reading the epoch table. This
includes the synthesis of digital output channel waveforms.

Some ABFs use a custom stimulus waveform. Code here also allows for the reading
of these waveforms from ABF and ATF files.

The Stimulus class is instantitated (once per channel) in the ABF class, and
users are encouraged to interact with those objects direclty.
"""

import numpy as np
import copy
import os
import sys
import pyabf
import logging
logging.basicConfig(level=logging.WARNING)
log = logging.getLogger(__name__)


def sweepD(abf, digitalOutputNumber=0):
    """
    Return a sweep waveform (similar to abf.sweepC) of a digital output channel.
    Digital outputs start at 0 and are usually 0-7. Returned waveform will be
    scaled from 0 to 1, although in reality they are 0V and 5V.
    """
    if abf.abfVersion["major"] == 1:
        log.debug("ABF1 don't support digital outputs.")
        return False
    states = digitalWaveformEpochs(abf)[digitalOutputNumber]
    sweepD = np.full(abf.sweepPointCount, 0)
    pts = epochPoints(abf)
    for epoch in range(len(states)):
        sweepD[pts[epoch]:pts[epoch+1]] = states[epoch]
    return sweepD


def epochPoints(abf):
    """Return a list of time points where each epoch starts and ends."""
    if abf.abfVersion["major"] == 1:
        return []
    position = int(abf.sweepPointCount/64)
    epochPoints = [position]
    for epochNumber, epochType in enumerate(abf._epochPerDacSection.nEpochType):
        pointCount = abf._epochPerDacSection.lEpochInitDuration[epochNumber]
        epochPoints.append(position + pointCount)
        position += pointCount
    return epochPoints


def epochValues(abf):
    """Return a list of epoch values by sweep by epoch."""
    if abf.abfVersion["major"] == 1:
        return [[]]
    epochList = range(len(abf._epochPerDacSection.nEpochType))
    vals = np.empty((abf.sweepCount, len(epochList)))
    for epoch in epochList:
        for sweep in abf.sweepList:
            dacHere = abf._epochPerDacSection.fEpochInitLevel[epoch]
            dacDelta = abf._epochPerDacSection.fEpochLevelInc[epoch] * sweep
            vals[sweep, epoch] = dacHere+dacDelta
    return vals


def digitalWaveformEpochs(abf):
    """
    Return a 2d array indicating the high/low state (1 or 0) of each digital
    output (rows) for each epoch (columns).
    """
    if abf.abfVersion["major"] == 1:
        return None
    numOutputs = abf._protocolSection.nDigitizerTotalDigitalOuts
    byteStatesByEpoch = abf._epochSection.nEpochDigitalOutput
    numEpochs = len(byteStatesByEpoch)
    statesAll = np.full((numOutputs, numEpochs), 0)
    for epochNumber in range(numEpochs):
        byteState = bin(byteStatesByEpoch[epochNumber])[2:]
        byteState = "0"*(numOutputs-len(byteState))+byteState
        byteState = [int(x) for x in list(byteState)]
        statesAll[:, epochNumber] = byteState[::-1]
    return statesAll


class Stimulus:
    def __init__(self, abf, channel):
        """
        handles epoch values for a single sweep/channel
        """

        self.abf = abf
        self.channel = channel

        self._initEpochVars()

        if abf.abfVersion["major"] == 1:
            self._fillEpochsFromABFv1()
        elif abf.abfVersion["major"] == 2:
            self._fillEpochsFromABFv2()
        else:
            raise NotImplemented("unsupported ABF file format")

        self._updateEpochDetails()

    def __len__(self):
        return len(self.epochList)

    def __str__(self):
        msg = f"Channel {self.channel} epochs ({self.epochCount}): "
        msg += ", ".join(self.label)
        return msg

    def __repr__(self):
        return "ChannelEpochs(ABF, %s)" % (self.channel)

    def _initEpochVars(self):
        """
        Create empty lists for every field of the waveform editor
        """
        self.label = []
        self.type = []
        self.level = []
        self.levelDelta = []
        self.duration = []
        self.durationDelta = []
        self.pulsePeriod = []
        self.pulseWidth = []
        self.digitalOutputs = []  # TODO: this never gets filled

    def _fillEpochsFromABFv1(self):
        """
        Do our best to create an epoch from what we know about the ABFv1.
        Currently this makes it look like a single step epoch over the
        entire sweep.
        """
        self.type.append(1)
        self.level.append(self.abf.holdingCommand[self.channel])
        self.levelDelta.append(0)
        self.duration.append(0)
        self.durationDelta.append(0)
        self.pulsePeriod.append(0)
        self.pulseWidth.append(0)
        self.digitalOutputs.append(0)

    def _fillEpochsFromABFv2(self):
        """
        Read the ABF header and append to the epoch lists
        """

        # load epoch values relevant to this channel
        for i, dacNum in enumerate(self.abf._epochPerDacSection.nDACNum):
            if dacNum != self.channel:
                continue
            epPerDac = self.abf._epochPerDacSection
            self.type.append(epPerDac.nEpochType[i])
            self.level.append(epPerDac.fEpochInitLevel[i])
            self.levelDelta.append(epPerDac.fEpochLevelInc[i])
            self.duration.append(epPerDac.lEpochInitDuration[i])
            self.durationDelta.append(epPerDac.lEpochDurationInc[i])
            self.pulsePeriod.append(epPerDac.lEpochPulsePeriod[i])
            self.pulseWidth.append(epPerDac.lEpochPulseWidth[i])

    def _updateEpochDetails(self):
        """
        After all epochs have been loaded, do some housekeeping
        """

        self.label = [chr(x+65) for x in range(len(self.type))]
        self.epochCount = len(self.type)
        self.epochList = range(self.epochCount)
        self.dacUnits = self.abf.dacUnits[self.channel]

    def _txtFmt(self, label, values):
        """
        Format a label and its values for text-block printing.
        """
        label = copy.copy(label)
        values = copy.copy(values)

        if label == "Type":
            for i, value in enumerate(values):
                if value == 0:
                    values[i] = "Off"
                elif value == 1:
                    values[i] = "Step"
                elif value == 2:
                    values[i] = "Ramp"
                elif value == 3:
                    values[i] = "Pulse"
                elif value == 4:
                    values[i] = "Tri"
                elif value == 5:
                    values[i] = "Cos"
                elif value == 7:
                    values[i] = "BiPhsc"
                else:
                    values[i] = "%d?" % value

        line = label.rjust(25, ' ')
        for val in values:
            if not isinstance(val, str):
                val = "%d" % val
            line += val.rjust(7, ' ')
        return line+"\n"

    @property
    def text(self):
        """
        Return all epoch levels as a text block, similar to how ClampFit does
        this when poking through the file properties dialog
        """

        if self.abf.abfVersion["major"] == 1:
            return "DAC data from ABF1 files is not available."
        elif self.abf.abfVersion["major"] == 2:
            nWaveformEnable = self.abf._dacSection.nWaveformEnable[self.channel]
            nWaveformSource = self.abf._dacSection.nWaveformSource[self.channel]

        if nWaveformEnable == 0:
            return "DAC waveform is not enabled."

        if nWaveformSource == 0:
            return "DAC waveform is not enabled."
        elif nWaveformSource == 1:
            out = "DAC waveform is controlled by epoch table:\n"
            out += self._txtFmt("Ch%d EPOCH" % self.channel, self.label)
            out += self._txtFmt("Type", self.type)
            out += self._txtFmt(f"First Level ({self.dacUnits})", self.level)
            out += self._txtFmt(f"Delta Level ({self.dacUnits})",
                                self.levelDelta)
            out += self._txtFmt("First Duration (samples)", self.duration)
            out += self._txtFmt("Delta Duration (samples)", self.durationDelta)
            out += self._txtFmt("Train Period (samples)", self.pulsePeriod)
            out += self._txtFmt("Pulse Width (samples)", self.pulseWidth)
            out += "\n"
            return out
        elif nWaveformSource == 2:
            out = "DAC waveform is controlled by custom file:\n"
            out += self.abf._stringsIndexed.lDACFilePath[self.channel]
            return out
        else:
            log.warn("unknown nWaveformSource: %s" % nWaveformSource)

    def stimulusWaveformFromFile(self):
        """
        Attempt to find the file associated with this ABF channel stimulus
        waveform, read that waveform (whether ABF or ATF), and return its
        waveform. If the file can't be found, return False.
        """

        # try to find the stimulus file in the obvious places
        stimFname = self.abf._stringsIndexed.lDACFilePath[self.channel]
        stimBN = os.path.basename(stimFname)
        abfFolder = os.path.dirname(self.abf.abfFilePath)
        if os.path.exists(stimFname):
            log.debug("stimulus file found where expected")
            stimFname = os.path.abspath(stimFname)
        elif os.path.exists(os.path.join(abfFolder, stimBN)):
            log.debug("stimulus file found next to ABF")
            stimFname = os.path.join(abfFolder, stimBN)
        else:
            log.debug("stimulus file never found: %s"%stimBN)
            return False

        # read the ABF or ATF stimulus file
        if stimFname.upper().endswith(".ABF"):
            log.debug("stimulus file is an ABF")
            abf = pyabf.ABF(stimFname)
            #TODO: data requires custom stimulus scaling!
            return abf.sweepY
        elif stimFname.upper().endswith(".ATF"):
            log.debug("stimulus file is an ATF")
            atf = pyabf.ATF(stimFname)
            #TODO: data requires custom stimulus scaling!
            return atf.sweepY


    def stimulusWaveform(self, sweepNumber=0):
        """
        Return a signal (the same size as a sweep) representing the command
        waveform of the DAC for the given channel. Since command waveforms
        can change sweep to sweep due to deltas, an optional sweep number can
        be given as an argument.
        """


        # no synthesis if ABF1 file
        if self.abf.abfVersion["major"] == 1:
            log.debug("DAC data from ABF1 files is not available")
            return np.full(self.abf.sweepPointCount, np.nan)
        elif self.abf.abfVersion["major"] == 2:
            nWaveformEnable = self.abf._dacSection.nWaveformEnable[self.channel]
            nWaveformSource = self.abf._dacSection.nWaveformSource[self.channel]

        # no synthesis if waveform is not enabled
        if nWaveformEnable == 0 or nWaveformSource == 0:
            log.debug("DAC waveform is not enabled")
            return np.full(self.abf.sweepPointCount, np.nan)

        if nWaveformSource == 0:
            return np.full(self.abf.sweepPointCount, np.nan)
        elif nWaveformSource == 1:
            return self.stimulusWaveformFromEpochTable(sweepNumber)
        elif nWaveformSource == 2:
            log.debug("DAC waveform is controlled by custom file")
            stimulusFromFile = self.stimulusWaveformFromFile()
            if stimulusFromFile is False:
                return np.full(self.abf.sweepPointCount, np.nan)
            else:
                return stimulusFromFile

        else:
            log.warn("unknown nWaveformSource: %s" % nWaveformSource)

    def stimulusWaveformFromEpochTable(self, sweepNumber):
        """
        Return sweepC (same size as sweepY) of the command signal synthesized
        from the epoch table.
        """

        # start by creating the command signal filled with the holding command
        sweepC = np.full(self.abf.sweepPointCount,
                         self.abf.holdingCommand[self.channel])

        # determine if we return to holding between epochs
        if self.abf.abfVersion["major"] == 1:
            returnToHolding = False
        elif self.abf.abfVersion["major"] == 2:
            if self.abf._dacSection.nInterEpisodeLevel[self.channel]:
                returnToHolding = True
            else:
                returnToHolding = False
        else:
            raise NotImplementedError("ABF format unsupported")

        # then step through epoch by epoch filling it with its contents
        position = int(self.abf.sweepPointCount/64)
        for epochNumber in self.epochList:

            # skip past disabled epochs
            if self.type[epochNumber] == 0:
                continue

            # determine the sweep-dependent level
            sweepLevel = self.level[epochNumber] + \
                self.levelDelta[epochNumber]*sweepNumber

            # determine the command of this epoch from the previous sweep
            sweepLevelLast = self.level[epochNumber] + \
                self.levelDelta[epochNumber]*(sweepNumber-1)

            # determine the sweep level of the previous epoch
            if epochNumber == 0:
                levelPreviousEpoch = self.abf.holdingCommand[self.channel]
            else:
                levelPreviousEpoch = self.level[epochNumber-1] + \
                    self.levelDelta[epochNumber-1]*sweepNumber

            # if not return to hold between sweeps, start where last ended
            if returnToHolding:
                sweepC.fill(sweepLevelLast)
                # TODO: this is slow, and may be buggy for stimuli with delta-time mixed in with deta-level

            # determine the sweep-dependent duration
            epochPoints = self.duration[epochNumber]
            epochPoints += self.durationDelta[epochNumber]*sweepNumber

            # update index points and slide position forward for next epoch
            i1 = position
            i2 = i1 + epochPoints
            position = position + epochPoints

            # create values useful if we analyze pulses
            pulsePeriod = self.pulsePeriod[epochNumber]
            pulseWidth = self.pulseWidth[epochNumber]
            if pulsePeriod > 0:
                pulseCount = int(int(i2-i1)/pulsePeriod)
            else:
                pulseCount = 0
            levelOff = levelPreviousEpoch
            levelOn = sweepLevel
            levelDelta = levelOn - levelOff

            # create a numpy array to hold the waveform for only this epoch
            chunk = np.empty(int(i2-i1))

            # fill epoch: step
            if self.type[epochNumber] == 1:
                chunk.fill(sweepLevel)

            # fill epoch: ramp
            elif self.type[epochNumber] == 2:
                chunk = np.arange(epochPoints)/epochPoints
                rampStart = sweepC[i1-1]
                rampDiff = sweepLevel-rampStart
                chunk *= rampDiff
                chunk += rampStart

            # fill epoch: pulse train
            elif self.type[epochNumber] == 3:
                chunk.fill(levelOff)
                for pulse in range(pulseCount):
                    p1 = int(pulsePeriod*pulse)
                    p2 = int(p1 + pulseWidth)
                    chunk[p1:p2] = levelOn

            # fill epoch: triangle train
            elif self.type[epochNumber] == 4:
                chunk.fill(levelOff)
                for pulse in range(pulseCount):
                    p1 = int(pulsePeriod*pulse)
                    p2 = int(p1 + pulseWidth)
                    p3 = int(p1+pulsePeriod)
                    chunk[p1:p2] = np.linspace(levelOff, levelOn, int(p2-p1))
                    chunk[p2:p3] = np.linspace(levelOn, levelOff, int(p3-p2))

            # fill epoch: cosine train
            elif self.type[epochNumber] == 5:
                vals = np.linspace(0, 2*pulseCount*np.pi, len(chunk))
                vals += np.pi
                cos = np.cos(vals) * levelDelta/2
                chunk.fill(levelOff)
                chunk += cos + levelDelta/2

            # fill epoch: biphasic train
            elif self.type[epochNumber] == 7:
                chunk.fill(levelOff)
                for pulse in range(pulseCount):
                    p1 = int(pulsePeriod*pulse)
                    p3 = int(p1 + pulseWidth)
                    p2 = int((p1+p3)/2)
                    chunk[p1:p2] = levelOff + levelDelta
                    chunk[p2:p3] = levelOff - levelDelta

            else:
                # unsupported epoch
                msg = f"unknown sweep type: {self.type[epochNumber]}"
                msg += " (treating as a step)"
                log.warn(msg)
                chunk.fill(sweepLevel)

            # modify this chunk based on the type of waveform
            sweepC[i1:i2] = chunk

        # code for when epochs dont return to holding between sweeps
        if returnToHolding:

            # sustain the final step through the end of the sweep
            sweepC[i2:] = sweepC[i2-1]

            # each sweep command starts where the last left off (not at hold)
            #sweepC += sweepLevelLast

        return sweepC

def _epochThings(abf):
    """
    return [epoch points, values, and digital outputs] for the current sweep and
    channel.
    """
    assert isinstance(abf, pyabf.ABF)
    if abf.abfVersion["major"]==1:
        return [[],[]]
    else:
        points = pyabf.stimulus.epochPoints(abf)
        values = list(pyabf.stimulus.epochValues(abf)[abf.sweepNumber])

        # add an extra point for the beginning of the sweep
        points = [0]+points
        values = [abf.sweepC[0]]+values

        # add extra points for the end of the sweep
        points.append(abf.sweepPointCount)
        while (len(values)<len(points)):
            values.append(abf.sweepC[-1])

        return [points, values]

@property
def epochPoints2(abf):
    """Return just the index points for the given sweep/channel epochs."""
    assert isinstance(abf, pyabf.ABF)
    if abf.abfVersion["major"]==1:
        return []
    points = epochPoints(abf)
    points = [0] + points + [abf.sweepPointCount]
    return points

@property
def epochValues2(abf):
    """Return just the values for the given sweep/channel epoch."""
    assert isinstance(abf, pyabf.ABF)
    if abf.abfVersion["major"]==1:
        return []
    values = list(epochValues(abf)[abf.sweepNumber])
    #TODO: determine if the pre-epoch value is a holdover from the last sweep
    preEpochValue = abf.holdingCommand[abf.sweepChannel]
    #TODO: determine if the post-epoch value returns to holding or is sustained
    postEpochValue = abf.holdingCommand[abf.sweepChannel]
    values = [preEpochValue] + [preEpochValue] + values + [postEpochValue]
    return values
