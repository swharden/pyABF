"""
Code here relates to reading epoch information from ABF files and synthesizing
analog and digital waveforms to represent command signals.
"""

import warnings
import numpy as np
import copy


class Epochs:
    def __init__(self, abf, channel):
        """
        handles epoch values for a single sweep/channel
        """

        self.abf = abf
        self.channel = channel

        self._initEpochVars()

        if abf.abfFileFormat == 1:
            self._fillEpochsFromABFv1()
        elif abf.abfFileFormat == 2:
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

    def _is_custom_waveform(self):
        """
        Return True if the epoch is defined by a custom waveform in different
        file, False for regular epochs.
        """

        return self.abf._dacSection.nWaveformSource[self.channel] == 2

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

        if self.abf.abfFileFormat == 1:
            return "Epoch data from ABF1 files is not available"
        elif self._is_custom_waveform():
            out = "Epochs ignored. DAC controlled by custom waveform:\n"
            out += self.abf._stringsIndexed.lDACFilePath[self.channel]
            return out

        out = "\n"
        out += self._txtFmt("Ch%d EPOCH" % self.channel, self.label)
        out += self._txtFmt("Type", self.type)
        out += self._txtFmt(f"First Level ({self.dacUnits})", self.level)
        out += self._txtFmt(f"Delta Level ({self.dacUnits})", self.levelDelta)
        out += self._txtFmt("First Duration (samples)", self.duration)
        out += self._txtFmt("Delta Duration (samples)", self.durationDelta)
        out += self._txtFmt("Train Period (samples)", self.pulsePeriod)
        out += self._txtFmt("Pulse Width (samples)", self.pulseWidth)
        out += "\n"
        return out

    def stimulusWaveform(self, sweepNumber=0):
        """
        Return a signal (the same size as a sweep) representing the command
        waveform of the DAC for the given channel. Since command waveforms
        can change sweep to sweep due to deltas, an optional sweep number can
        be given as an argument.
        """

        # return an empty waveform for ABFv1 files
        if self.abf.abfFileFormat == 1:
            sweepC = np.full(self.abf.sweepPointCount, np.nan)
            return sweepC
        elif self._is_custom_waveform():
            warnings.warn("Custom waveforms are unsupported, using NaNs instead " +
                          "for channel {} of sweep {}".format(self.channel,
                          sweepNumber))
            sweepC = np.full(self.abf.sweepPointCount, np.nan)
            return sweepC

        # start by creating the command signal filled with the holding command
        sweepC = np.full(self.abf.sweepPointCount,
                         self.abf.holdingCommand[self.channel])

        # determine if we return to holding between epochs
        if self.abf.abfFileFormat == 1:
            returnToHolding = False
        elif self.abf.abfFileFormat == 2:
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
                warnings.warn(msg)
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
