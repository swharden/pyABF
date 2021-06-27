"""
Code here relates to the creation of stimulus waveforms from epoch tables.

In the waveform editor of ClampEx, you can edit the stimulus waveform table
for each channel (DAC). Each waveform table is made of epochs, which appear
as a single column of values in the waveform editor.

The overall strategy here is that data for each epoch (column) is stored in
an Epoch object. A single channel (DAC) has a list of Epoch objects, and can
be considered an epoch table. These epoch tables (Epoch lists) can be passed
around to be displayed or used to generate signal waveforms.

The epoch table must be built and stepped through (sweep by sweep) before an
epoch waveform can be created for a single sweep. This is because levels for
one sweep can depend on the last level of the previous sweep.

The minimum amount of information actually needed to create a waveform for a
sweep is: level, levelDelta, duration, durationDelta, pulsePeriod, pulseWidth,
and epochType. The EpochSweepWaveform holds this minimum amount of information
for every sweep, and contains the code necessary to generate waveforms from it.
"""

import glob
import warnings
import time
import numpy as np
import pyabf
import os
import sys
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_DATA = os.path.abspath(PATH_HERE+"../../../data/abfs/")
PATH_SRC = os.path.abspath(PATH_HERE+"../../../src/")
sys.path.insert(0, PATH_SRC)

_DIGITAL_OUTPUT_COUNT = 8


class Epoch:
    """
    The Epoch class represents data contained in a single epoch column
    of the stimulus waveform editor. It's just an easy way to hold and convert
    all the data values for a single epoch.
    """

    # settable values
    epochNumber = -1
    epochType = -1
    level = -1
    levelDelta = -1
    duration = -1
    durationDelta = -1
    digitalPattern = [0]*_DIGITAL_OUTPUT_COUNT
    pulsePeriod = -1
    pulseWidth = -1
    dacNum = -1

    @property
    def epochLetter(self):
        if self.epochNumber < 0:
            return "?"
        epochLetter = ""
        num = self.epochNumber
        while num >= 0:
            epochLetter += chr(num % 26 + 65)
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
        digStr = [str(x) for x in self.digitalPattern]
        txt += "DigOuts: %s" % ("".join(digStr))
        return txt


class EpochSweepWaveform:

    def __init__(self):
        """
        This object holds the minimal amount of information needed to create
        and retrieve information about a sweep's epoch waveform. This object
        can only be populated after the full waveform table is created and
        stepped through sweep-by-sweep (because levels in a sweep can depend
        on levels of the previous sweep).

        Waveform synthesis happens in this class.
        """

        self.p1s = []
        self.p2s = []
        self.levels = []
        self.types = []
        self.pulseWidths = []
        self.pulsePeriods = []
        self.digitalStates = []

    def addEpoch(self, pt1, pt2, level, epochType, pulseWidth, pulsePeriod,
                 digitalState):

        assert isinstance(pt1, int)
        self.p1s.append(pt1)

        assert isinstance(pt2, int)
        self.p2s.append(pt2)

        assert isinstance(level, int) or isinstance(level, float)
        self.levels.append(level)

        assert isinstance(epochType, str)
        self.types.append(epochType)

        assert isinstance(pulseWidth, int)
        self.pulseWidths.append(pulseWidth)

        assert isinstance(pulsePeriod, int)
        self.pulsePeriods.append(pulsePeriod)

        assert isinstance(digitalState, list)
        numberOfDigitalStates = len(digitalState)
        if (numberOfDigitalStates != _DIGITAL_OUTPUT_COUNT):
            warnings.warn("Number of digital states (%d) is different than expected (%d)" % (
                numberOfDigitalStates, _DIGITAL_OUTPUT_COUNT))
        self.digitalStates.append(digitalState)

    def getDigitalWaveform(self, digitalChannel):
        """Return a waveform reflecting a certain digital output channel."""
        sweepD = np.full(self.p2s[-1], 5)
        for i in range(len(self.levels)):
            digitalState = self.digitalStates[i]
            digitalStateForChannel = digitalState[digitalChannel]
            sweepD[self.p1s[i]:self.p2s[i]] = digitalStateForChannel
        return sweepD

    def getWaveform(self):
        sweepC = np.full(self.p2s[-1], np.nan)
        for i in range(len(self.levels)):

            # get easier access to epoch values
            epochType = self.types[i]
            chunkSize = self.p2s[i] - self.p1s[i]
            pulsePeriod = self.pulsePeriods[i]
            pulseWidth = self.pulseWidths[i]
            level = self.levels[i]
            if i == 0:
                levelBefore = level
            else:
                levelBefore = self.levels[i-1]
            levelDelta = level - levelBefore

            # determine how many pulses there are
            if self.pulsePeriods[i] > 0:
                pulseCount = int(chunkSize/self.pulsePeriods[i])
            else:
                pulseCount = 0

            # now create a "chunk" (np array) for this epoch waveform

            if epochType == "Step":
                # epoch type 1: step
                chunk = np.full(chunkSize, level)

            elif epochType == "Ramp":
                # epoch type 2: smooth ramp
                chunk = np.linspace(levelBefore, level, chunkSize)

            elif epochType == "Pulse":
                # epoch type 3: pulse train
                chunk = np.full(chunkSize, levelBefore)
                for pulse in range(pulseCount):
                    p1 = int(pulsePeriod*pulse)
                    p2 = int(p1 + pulseWidth)
                    chunk[p1:p2] = level

            elif epochType == "Tri":
                # epoch type 4: triangle train
                chunk = np.full(chunkSize, np.nan)
                for pulse in range(pulseCount):
                    p1 = int(pulsePeriod*pulse)
                    p2 = int(p1 + pulseWidth)
                    p3 = int(p1+pulsePeriod)
                    chunk[p1:p2] = np.linspace(levelBefore, level, int(p2-p1))
                    chunk[p2:p3] = np.linspace(level, levelBefore, int(p3-p2))

            elif epochType == "Cos":
                # epoch type 5: cosine train
                chunk = np.full(chunkSize, levelBefore)
                vals = np.linspace(0, 2*pulseCount*np.pi, len(chunk))
                vals += np.pi
                cos = np.cos(vals) * levelDelta/2
                chunk += cos + levelDelta/2

            elif epochType == "BiPhsc":
                # epoch type 7: biphasic train
                chunk = np.full(chunkSize, levelBefore)
                for pulse in range(pulseCount):
                    p1 = int(pulsePeriod*pulse)
                    p3 = int(p1 + pulseWidth)
                    p2 = int((p1+p3)/2)
                    chunk[p1:p2] = levelBefore + levelDelta
                    chunk[p2:p3] = levelBefore - levelDelta

            else:
                # unsupported epoch type
                msg = "Epoch type (%s) unsupported" % epochType
                warnings.warn(msg)
                chunk = np.full(chunkSize, np.nan)

            # add the newly-made chunk to the sweepC
            sweepC[self.p1s[i]:self.p2s[i]] = chunk

        return sweepC

    def __str__(self):
        txt = "Sweep epoch waveform: "
        for i in range(len(self.levels)):
            txt += "%s %.02f [%d:%d], " % (self.types[i], self.levels[i],
                                           self.p1s[i], self.p2s[i])
        return txt[:-2]


class EpochTable:

    def __init__(self, abf, channel):
        """
        An epoch table represents all epochs for a single DAC.
        Upon instantiation, epoch waveform objects are created for every sweep.
        """

        # populate useful values from the common ABF header
        assert isinstance(abf, pyabf.ABF)
        self.sampleRateHz = abf.dataRate
        self.holdingLevel = abf.holdingCommand[channel]
        self.sweepPointCount = abf.sweepPointCount
        self.channel = channel

        # populate epochs and other details based on ABF version
        if abf.abfVersion["major"] == 1:
            if channel > 1:
                channel = 0  # use channel 0's stimulus when channel is too high
            self.epochs = self._initABF1(abf, channel)
            nInterEpisodeLevel = abf._headerV1.nInterEpisodeLevel[channel]
        elif abf.abfVersion["major"] == 2:
            self.epochs = self._initABF2(abf, channel)
            nInterEpisodeLevel = abf._dacSection.nInterEpisodeLevel[channel]
        else:
            raise ValueError("ABF version not supported")

        # nInterEpisodeLevel determines what level will be used when epochs end
        if nInterEpisodeLevel:
            self.returnToHold = True
        else:
            self.returnToHold = False

        # delete "Off" epochs
        self.epochs = [x for x in self.epochs if x.epochType != 0]

        # create a list of waveform objects (one per sweep)
        self.epochWaveformsBySweep = self.getEpochWaveformsBySweep(abf)

    def _initABF1(self, abf, channel):
        """Populate epoch values from the ABF1 header."""

        epochs = []

        # ABF1 files have a fixed 20 slots in memory for epoch info.
        assert len(abf._headerV1.nEpochType) == 20
        for i in range(20):
            epoch = Epoch()
            epoch.epochNumber = i % 10
            epoch.epochType = abf._headerV1.nEpochType[i]
            epoch.level = abf._headerV1.fEpochInitLevel[i]
            epoch.levelDelta = abf._headerV1.fEpochLevelInc[i]
            epoch.duration = abf._headerV1.lEpochInitDuration[i]
            epoch.durationDelta = abf._headerV1.lEpochDurationInc[i]
            epoch.pulsePeriod = 0  # not supported in ABF1
            epoch.pulseWidth = 0  # not supported in ABF1
            epochs.append(epoch)

        # ABF1 files store 10 epochs eac for just two DAC channels.
        if channel == 0:
            epochs = epochs[0:10]
        elif channel == 1:
            epochs = epochs[10:20]
        else:
            warnings.debug("ABF1 does not support stimulus waveforms >2 DACs")
            epochs = []

        return epochs

    def _initABF2(self, abf, channel):
        """Populate epoch values from the ABF2 header."""

        epochs = []

        # the epoch table is stored in _epochPerDacSection
        for i, epochDacNum in enumerate(abf._epochPerDacSection.nDACNum):
            if epochDacNum != channel:
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

            if epochDacNum == abf._protocolSection.nActiveDACChannel:
                iCh = len(epochs)
                digitalOutValue = abf._epochSection.nEpochDigitalOutput[iCh]
                epoch.digitalPattern = self._valToBitList(digitalOutValue)
            else:
                epoch.digitalPattern = self._valToBitList(0)
            epochs.append(epoch)

        # digital output values are in _epochSection.
        # digital outputs are only used for the nActiveDACChannel channel.

        #digitalOutValue = abf._epochSection.nEpochDigitalOutput[i]
        #epoch.digitalPattern = self._valToBitList(digitalOutValue)

        return epochs

    def _valToBitList(self, value, bitCount=_DIGITAL_OUTPUT_COUNT):
        """
        Given an integer, return a list of 0s and 1s representing the state of
        each of the bit.
        """
        value = int(value)
        binString = bin(value)[2:].zfill(bitCount)
        bits = list(binString)
        bits = [int(x) for x in bits]
        bits.reverse()
        return bits

    def __str__(self):
        return self.text

    @property
    def text(self):
        """
        Given a list of epochs, return a text string formatted to look like the
        epoch table displayed as plain text in pCLAMP and ClampFit.
        """

        # create a copy of the epochs list we can modify
        epochList = self.epochs

        # remove empty epochs
        epochList = [x for x in epochList if x.duration > 0]

        # prepare lists to hold values for each epoch
        epochCount = len(epochList)
        epochLetters = [''] * epochCount
        epochTypes = [''] * epochCount
        epochLevels = [''] * epochCount
        epochLevelsDelta = [''] * epochCount
        durations = [''] * epochCount
        durationsDelta = [''] * epochCount
        durationsMs = [''] * epochCount
        durationsDeltaMs = [''] * epochCount
        digitalPatternLs = [''] * epochCount
        digitalPatternHs = [''] * epochCount
        trainPeriods = [''] * epochCount
        pulseWidths = [''] * epochCount

        # populate values for each epoch
        pointsPerMsec = self.sampleRateHz*1000
        for i, epoch in enumerate(epochList):
            assert isinstance(epoch, Epoch)
            if epoch.epochTypeStr == "Off":
                continue
            epochLetters[i] = epoch.epochLetter
            epochTypes[i] = epoch.epochTypeStr
            epochLevels[i] = "%.02f" % epoch.level
            epochLevelsDelta[i] = "%.02f" % epoch.levelDelta
            durations[i] = "%d" % epoch.duration
            durationsDelta[i] = "%d" % epoch.durationDelta
            durationsMs[i] = "%.02f" % (epoch.duration/pointsPerMsec)
            durationsDeltaMs[i] = "%.02f" % (epoch.durationDelta/pointsPerMsec)
            digStr = "".join(str(int(x)) for x in epoch.digitalPattern)
            digitalPatternLs[i] = digStr[:4]
            digitalPatternHs[i] = digStr[4:]
            trainPeriods[i] = "%d" % epoch.pulsePeriod
            pulseWidths[i] = "%d" % epoch.pulseWidth

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
        txt += "First Duration (points)".rjust(padLabel)
        txt += "".join([x.rjust(pad) for x in durations])+"\n"
        txt += "Delta Duration (points)".rjust(padLabel)
        txt += "".join([x.rjust(pad) for x in durationsDelta])+"\n"
        txt += "Digital Pattern #3-0".rjust(padLabel)
        txt += "".join([x.rjust(pad) for x in digitalPatternLs])+"\n"
        txt += "Digital Pattern #7-4".rjust(padLabel)
        txt += "".join([x.rjust(pad) for x in digitalPatternHs])+"\n"
        txt += "Train Period (points)".rjust(padLabel)
        txt += "".join([x.rjust(pad) for x in trainPeriods])+"\n"
        txt += "Pulse Width (points)".rjust(padLabel)
        txt += "".join([x.rjust(pad) for x in pulseWidths])+"\n"
        return txt.strip('\n')

    def getEpochWaveformsBySweep(self, abf):
        """Return a list of EpochSweepWaveform objects (one per sweep)."""

        epochWaveformsBySweep = []

        lastSweepLastLevel = self.holdingLevel
        for sweep in abf.sweepList:
            ep = EpochSweepWaveform()

            # add the pre-epoch values
            preEpochEndPoint = int(self.sweepPointCount/64)
            pt2 = preEpochEndPoint
            ep.addEpoch(0, preEpochEndPoint, lastSweepLastLevel, "Step",
                        0, 0, [0]*_DIGITAL_OUTPUT_COUNT)

            # step through each epoch
            position = preEpochEndPoint
            level = self.holdingLevel
            for epoch in self.epochs:
                duration = epoch.duration + epoch.durationDelta * sweep
                pt1, pt2 = position, position + duration
                level = epoch.level + epoch.levelDelta*sweep
                ep.addEpoch(pt1, pt2, level, epoch.epochTypeStr,
                            epoch.pulseWidth, epoch.pulsePeriod,
                            epoch.digitalPattern)
                position = pt2

            # add the post-epoch values
            if self.returnToHold:
                lastSweepLastLevel = level
            else:
                lastSweepLastLevel = self.holdingLevel
            ep.addEpoch(pt2, self.sweepPointCount, lastSweepLastLevel, "Step",
                        0, 0, [0]*_DIGITAL_OUTPUT_COUNT)

            # add this sweep waveform to the list
            epochWaveformsBySweep.append(ep)

        return epochWaveformsBySweep


def _demo_create_graphs():
    """Plot sweepC of ABFs containing waveforms of all types."""
    import matplotlib.pyplot as plt
    for fname in glob.glob(PATH_DATA+"/18702001-*.abf"):
        abf = pyabf.ABF(fname)
        plt.figure()
        eptbl = EpochTable(abf, 1)
        for epwv in eptbl.epochWaveformsBySweep:
            sweepC = epwv.getWaveform()
            plt.plot(sweepC)
        plt.title(abf.abfID)
    plt.show()


def _demo_epoch_table():
    """Demonstrate the text epoch table feature."""
    import matplotlib.pyplot as plt
    abfFiles = glob.glob(PATH_DATA+"/18702001-*.abf")
    for fname in abfFiles:
        abf = pyabf.ABF(fname)
        print("\n\n", "#"*20, abf.abfID, "(CH 1)", "#"*20)

        # show the epoch table as a big text block
        epochTable = EpochTable(abf, 1)
        print(epochTable)


def _demo_epoch_access():
    """Demonstrate how to access epoch levels and point indexes."""
    import matplotlib.pyplot as plt
    for fname in glob.glob(PATH_DATA+"/18702001-*.abf"):
        abf = pyabf.ABF(fname)
        print("\n\n", "#"*20, abf.abfID, "(CH 1)", "#"*20)

        # show waveform info for each sweep
        epochTable = EpochTable(abf, 1)
        for sweep in abf.sweepList:
            sweepWaveform = epochTable.epochWaveformsBySweep[sweep]
            print("\n", "#"*5, "Sweep", sweep, "#"*5)
            print(sweepWaveform)
            print("levels:", sweepWaveform.levels)
            print("types:", sweepWaveform.types)
            print("p1s:", sweepWaveform.p1s)
            print("p2s:", sweepWaveform.p2s)
            print("pulsePeriods:", sweepWaveform.pulsePeriods)
            print("pulseWidths:", sweepWaveform.pulseWidths)


def _demo_sweepC():
    """Demonstrate how to generate the sweepC waveform."""
    import matplotlib.pyplot as plt
    for fname in glob.glob(PATH_DATA+"/18702001-*.abf"):
        abf = pyabf.ABF(fname)
        print("\n%s (CH 1)" % abf.abfID)
        epochTable = EpochTable(abf, 1)
        for sweep in abf.sweepList:
            sweepWaveform = epochTable.epochWaveformsBySweep[sweep]
            sweepC = sweepWaveform.getWaveform()
            print("SweepC", sweep, "=", sweepC)


def _demo_digOut_by_channel():
    """Demonstrate that only a single channel commands digital outputs."""
    import matplotlib.pyplot as plt
    abf = pyabf.ABF(PATH_DATA+"/2018_12_15_0000.abf")
    for channel in abf.channelList:
        epochTable = EpochTable(abf, channel)
        print("\n\n", "#"*20, abf.abfID, "(CH %d)" % channel, "#"*20)
        print(epochTable)


def _demo_sweepD():
    """Demonstrate how to access digital outputs."""
    import matplotlib.pyplot as plt
    abf = pyabf.ABF(PATH_DATA+"/17o05026_vc_stim.abf")
    epochTable = EpochTable(abf, 0)  # channel 0
    sweepWaveform = epochTable.epochWaveformsBySweep[0]  # sweep 0
    sweepD = sweepWaveform.getDigitalWaveform(4)  # digital output 4
    print("SweepD", sweepD)
    plt.plot(sweepD)
    plt.show()


def _demo_deltaT():
    """Demonstrate delta duration."""
    import matplotlib.pyplot as plt
    abf = pyabf.ABF(PATH_DATA+"/2018_04_13_0016a_original.abf")
    epochTable = EpochTable(abf, 0)

    fig = plt.figure(figsize=(8, 5))
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212, sharex=ax1)
    for sweep in abf.sweepList[:20]:
        abf.setSweep(sweep)
        sweepWaveform = epochTable.epochWaveformsBySweep[sweep]
        sweepC = sweepWaveform.getWaveform()
        ax1.plot(abf.sweepX, abf.sweepY, color='b', lw=.5)
        ax2.plot(abf.sweepX, sweepC, color='r', lw=.5)
    plt.show()
