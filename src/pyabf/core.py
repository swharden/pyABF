"""
This file contains the core ABF handling class and supporting functions.
All code in this script should identically support ABF1 and ABF2 files.

Nothing the user will interact with directly is in this file.
"""

import os
import glob
import time
import datetime
import numpy as np
import warnings

from pyabf.structures import HeaderV1
from pyabf.structures import HeaderV2
from pyabf.structures import SectionMap
from pyabf.structures import ProtocolSection
from pyabf.structures import ADCSection
from pyabf.structures import DACSection
from pyabf.structures import EpochPerDACSection
from pyabf.structures import EpochSection
from pyabf.structures import TagSection
from pyabf.structures import StringsSection
from pyabf.structures import StringsIndexed
import pyabf.text


class ABFcore:
    """
    The ABFcore class provides direct access to contents of ABF files.
    This class provides a common framework to access header and data values
    from ABF1 and ABF2 files.

    The input ABF could be a path to an ABF file or another ABFcore class.

    If preLoadData is enabled, all data in the ABF is read from disk and
    scaled at instantiation. In practice this is almost always the fastest way
    to work with ABFs (modern computers can easily float the data in memory).
    However, it can be disabled for projects which only read ABF headers.

    Immediately after instantiating, it is expected you will call the
    _loadEverything function.
    """

    def __init__(self, abf, preLoadData=True):
        self._loadEverything(abf, preLoadData)

    def _loadEverything(self, abf, preLoadData):
        """
        This used to be the __init__ of the ABF class.
        """
        self.abfFilePath = os.path.abspath(abf)
        if not os.path.exists(self.abfFilePath):
            raise ValueError("file does not exist", self.abfFilePath)
        self.abfID = os.path.splitext(os.path.basename(self.abfFilePath))[0]
        self._fileOpen()
        self._determineAbfFormat()
        self._readHeaders()
        self._formatVersion()
        self._determineCreationDateTime()
        self._determineDataProperties()
        self._determineDataUnits()
        self._determineDataScaling()
        self._determineHoldingValues()
        self._determineProtocolPath()
        self._determineProtocolComment()
        self._makeTagTimesHumanReadable()
        self._makeUsefulObjects()
        self._digitalWaveformEpochs()
        if preLoadData:
            self._loadAndScaleData()
        self._fileClose()

    def _fileOpen(self):
        """Open the ABF file in rb mode."""
        self._fb = open(self.abfFilePath, 'rb')
        self._fileOpenTime = time.perf_counter()

    def _determineAbfFormat(self):
        """
        The first few characters of an ABF file tell you its format.
        "ABF " is for ABF1 files, and "ABF2" is for ABF2 files.
        Anything else is probably a file that's not actually an ABF.
        """
        self._fb.seek(0)
        code = self._fb.read(4)
        code = code.decode("ascii", errors='ignore')
        if code == "ABF ":
            self.abfFileFormat = 1
        elif code == "ABF2":
            self.abfFileFormat = 2
        else:
            raise NotImplementedError("Not a valid ABF1 or ABF2 file!")

    def _fileClose(self):
        """
        Close the ABF file. Releasing it allows it to be read by ClampFit. 
        Clampfit, regrettably, is a file-access-blocking data viewer.
        """
        self._fileCloseTime = time.perf_counter()
        self._fb.close()
        self._dataLoadTimeMs = (self._fileCloseTime-self._fileOpenTime)*1000

    def _readHeaders(self):
        """
        Read all headers into memory. 
        Store them in variables that can be accessed at any time.
        """
        if self.abfFileFormat == 1:
            self._headerV1 = HeaderV1(self._fb)
        elif self.abfFileFormat == 2:
            self._headerV2 = HeaderV2(self._fb)
            self._sectionMap = SectionMap(self._fb)
            self._protocolSection = ProtocolSection(self._fb, self._sectionMap)
            self._adcSection = ADCSection(self._fb, self._sectionMap)
            self._dacSection = DACSection(self._fb, self._sectionMap)
            self._epochPerDacSection = EpochPerDACSection(
                self._fb, self._sectionMap)
            self._epochSection = EpochSection(self._fb, self._sectionMap)
            self._tagSection = TagSection(self._fb, self._sectionMap)
            self._stringsSection = StringsSection(self._fb, self._sectionMap)
            self._stringsIndexed = StringsIndexed(
                self._headerV2, self._protocolSection, self._adcSection,
                self._dacSection, self._stringsSection)
        else:
            raise NotImplementedError("Invalid ABF file format")

    def _formatVersion(self):
        """
        The ABF Version differs in format from ABF1 and ABF2.
        This function formats the version as x.x.x.x for all ABF files.
        """
        if self.abfFileFormat == 1:
            self.abfVersion = "%.03f" % self._headerV1.fFileVersionNumber
            self.abfVersion = list(self.abfVersion.replace(".", ""))
            self.abfVersion = ".".join(self.abfVersion)
        elif self.abfFileFormat == 2:
            self.abfVersion = self._headerV2.fFileVersionNumber[::-1]
            self.abfVersion = [str(x) for x in self.abfVersion]
            self.abfVersion = ".".join(self.abfVersion)
        else:
            raise NotImplementedError("Invalid ABF file format")

    def _determineCreationDateTime(self):
        """
        Determine when the ABF was recorded. This is stored in the header of
        ABF2 files, but is just the system file creation date of ABF1 files.
        """
        if self.abfFileFormat == 1:
            # use the time the ABF file was created on disk
            self.abfDateTime = round(os.path.getctime(self.abfFilePath))
            self.abfDateTime = datetime.datetime.fromtimestamp(
                self.abfDateTime)
        elif self.abfFileFormat == 2:
            # use file creation time stored in ABF header
            startDate = str(self._headerV2.uFileStartDate)
            startTime = round(self._headerV2.uFileStartTimeMS/1000)
            startDate = datetime.datetime.strptime(startDate, "%Y%M%d")
            startTime = datetime.timedelta(seconds=startTime)
            self.abfDateTime = startDate+startTime
        else:
            raise NotImplementedError("Invalid ABF file format")

    def _determineDataProperties(self):
        """
        Read the header to determine information about the signal data.
        This includes things like data rate, number of channels, number
        of sweeps, etc.
        """

        # ABF file version specific lookups
        if self.abfFileFormat == 1:
            self.dataByteStart = self._headerV1.lDataSectionPtr*512
            self.dataByteStart += self._headerV1.nNumPointsIgnored
            self.dataPointCount = self._headerV1.lActualAcqLength
            self.channelCount = self._headerV1.nADCNumChannels
            self.dataRate = int(1e6 / self._headerV1.fADCSampleInterval)
            self.dataSecPerPoint = 1/self.dataRate
            self.sweepCount = self._headerV1.lActualEpisodes
        elif self.abfFileFormat == 2:
            self.dataByteStart = self._sectionMap.DataSection[0]*512
            self.dataPointCount = self._sectionMap.DataSection[2]
            self.channelCount = self._sectionMap.ADCSection[2]
            self.dataRate = int(
                1e6 / self._protocolSection.fADCSequenceInterval)
            self.dataSecPerPoint = 1/self.dataRate
            self.sweepCount = self._headerV2.lActualEpisodes
        else:
            raise NotImplementedError("Invalid ABF file format")

        # now calculate things with the values we calculated
        if self.sweepCount == 0:  # gap free
            self.sweepCount = 1
        self.sweepPointCount = int(
            self.dataPointCount / self.sweepCount / self.channelCount)
        self.sweepLengthSec = self.sweepPointCount / self.dataRate

    def _determineDataUnits(self):
        """
        Channel units and names are stored in the strings section as indexed
        strings where the indexes are scattered around the header. This function
        organizes channel units and names into simple lists of strings.
        """
        if self.abfFileFormat == 1:
            self.adcUnits = self._headerV1.sADCUnits[:self.channelCount]
            self.adcNames = self._headerV1.sADCChannelName[:self.channelCount]
            self.dacUnits = ["?" for x in self.adcUnits]
            self.dacNames = ["?" for x in self.adcUnits]
        elif self.abfFileFormat == 2:
            self.adcUnits = self._stringsIndexed.lADCUnits[:self.channelCount]
            self.adcNames = self._stringsIndexed.lADCChannelName[:self.channelCount]
            self.dacUnits = self._stringsIndexed.lDACChannelUnits[:self.channelCount]
            self.dacNames = self._stringsIndexed.lDACChannelName[:self.channelCount]
        else:
            raise NotImplementedError("Invalid ABF file format")

    def _determineDataScaling(self):
        """
        Because data is stored as int16 values in the ABF file, after it is read
        out of the file it must be scaled to floating-point values which match
        the units. Scaling data may be different by channel, and this section
        reads the header to determine how to scale each channel.
        """
        if self.abfFileFormat == 1:
            self.scaleFactors = [1]*self.channelCount
            for i in range(self.channelCount):
                self.scaleFactors[i] = self._headerV1.lADCResolution/1e6
        elif self.abfFileFormat == 2:
            self.scaleFactors = [1]*self.channelCount
            for i in range(self.channelCount):
                self.scaleFactors[i] /= self._adcSection.fInstrumentScaleFactor[i]
                self.scaleFactors[i] /= self._adcSection.fSignalGain[i]
                self.scaleFactors[i] /= self._adcSection.fADCProgrammableGain[i]
                if self._adcSection.nTelegraphEnable:
                    self.scaleFactors[i] /= self._adcSection.fTelegraphAdditGain[i]
                self.scaleFactors[i] *= self._protocolSection.fADCRange
                self.scaleFactors[i] /= self._protocolSection.lADCResolution
                self.scaleFactors[i] += self._adcSection.fInstrumentOffset[i]
                self.scaleFactors[i] -= self._adcSection.fSignalOffset[i]
        else:
            raise NotImplementedError("Invalid ABF file format")

    def _determineHoldingValues(self):
        """
        When an ABF isn't being driven by an epoch (protocol), its command
        values are clamped at a certain holding value. This section looks-up
        those values.
        """
        if self.abfFileFormat == 1:
            self.holdingCommand = self._headerV1.fEpochInitLevel
        elif self.abfFileFormat == 2:
            self.holdingCommand = self._dacSection.fDACHoldingLevel
        else:
            raise NotImplementedError("Invalid ABF file format")

    def _determineProtocolPath(self):
        """
        If the ABF was recorded from a saved protocol, that path is stored in
        the ABF header.
        """
        if self.abfFileFormat == 1:
            self.protocolPath = self._headerV1.sProtocolPath
            self.protocol = os.path.basename(self.protocolPath)
            self.protocol = os.path.splitext(self.protocol)[0]
        elif self.abfFileFormat == 2:
            self.protocolPath = self._stringsIndexed.uProtocolPath
            self.protocol = os.path.basename(self.protocolPath)
            self.protocol = os.path.splitext(self.protocol)[0]
        else:
            raise NotImplementedError("Invalid ABF file format")

    def _determineProtocolComment(self):
        """
        ABF2 files give the user the option to store a comment when in the
        waveform editor section. This is stored in the header.
        """
        if self.abfFileFormat == 1:
            self.abfFileComment = ""  # not supported in ABF1
        elif self.abfFileFormat == 2:
            self.abfFileComment = self._stringsIndexed.lFileComment
        else:
            raise NotImplementedError("Invalid ABF file format")

    def _makeTagTimesHumanReadable(self):
        """
        Tags are comments placed at specific time points in ABF files. 
        Unfortunately the time code (lTagTime) isn't in useful unit. This 
        section converts tag times into human-readable units (like seconds).
        """
        if self.abfFileFormat == 1:
            self.tagComments = []
            self.tagTimesSec = []
            self.tagTimesMin = []
            self.tagSweeps = []
        elif self.abfFileFormat == 2:
            self.tagComments = self._tagSection.sComment
            self.tagTimesSec = self._tagSection.lTagTime
            mult = self._protocolSection.fSynchTimeUnit/1e6
            self.tagTimesSec = [mult*x for x in self.tagTimesSec]
            self.tagTimesMin = [x/60 for x in self.tagTimesSec]
            self.tagSweeps = [x/self.sweepLengthSec for x in self.tagTimesSec]
        else:
            raise NotImplementedError("Invalid ABF file format")

    def _loadAndScaleData(self):
        """
        Actual electrophysiology data is stored in the DataSection of ABF files
        as 16-bit integers. This section reads those integers into a numpy
        array, reshapes them into a 2D array (each channel is a row), and
        scales them by multiplying each channel by its scaling factor.

        To access data sweep by sweep, write your own class function! 
        That's outside the scope of this core ABF class.
        """

        # usually ABF data is 16-bit integers. Every once and a while you
        # find ABFs with other data formats. Usually this happens after the
        # file is modified with ClampFIt.
        if self.abfFileFormat==1:
            dtype = np.int16
        elif self.abfFileFormat==2:
            if self._sectionMap.DataSection[1] == 2:
                dtype = np.int16
            elif self._sectionMap.DataSection[1] == 4:
                if self._headerV2.nDataFormat==1:
                    dtype = np.float32
                else:
                    dtype = np.int16
            else:
                raise NotImplementedError("strange data point size")

        self._fb.seek(self.dataByteStart)
        raw = np.fromfile(self._fb, dtype=dtype, count=self.dataPointCount)
        raw = np.reshape(
            raw, (int(len(raw)/self.channelCount), self.channelCount))
        raw = np.rot90(raw)
        raw = raw[::-1]
        self.data = np.empty(raw.shape, dtype='float32')
        for i in range(self.channelCount):
            self.data[i] = np.multiply(
                raw[i], self.scaleFactors[i], dtype='float32')

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
            if "method" in str(type(thing)):
                continue
            if isinstance(thing, (int, list, float, datetime.datetime, str, np.ndarray, range)):
                page.addThing(thingName, thing)
            elif thing is None or thing is False or thing is True:
                page.addThing(thingName, thing)
            else:
                print("Unsure how to generate info for:",
                      thingName, type(thing))

        # add all ABF header information (different in ABF1 vs ABF2)

        headerParts = []
        if self.abfFileFormat == 1:
            headerParts.append(["ABF1 Header", self._headerV1])
        elif self.abfFileFormat == 2:
            headerParts.append(["ABF2 Header", self._headerV2])
            headerParts.append(["SectionMap", self._sectionMap])
            headerParts.append(["ProtocolSection", self._protocolSection])
            headerParts.append(["ADCSection", self._adcSection])
            headerParts.append(["DACSection", self._dacSection])
            headerParts.append(
                ["EpochPerDACSection", self._epochPerDacSection])
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

    def _makeUsefulObjects(self):
        """
        Create a few extra little objects which are useful when working with
        the abf object.
        """
        self.channelList = list(range(self.channelCount))
        self.sweepList = list(range(self.sweepCount))

    def _updateStimulusWaveform(self, sweepNumber, channel):
        """
        Update self.sweepC with the stimulus waveform for a given sweep.
        Epoch information is stored in EpochPerDACSection.
        """

        # known epoch types
        epoch_disabled = 0
        epoch_step = 1
        epoch_ramp = 2

        # create the waveform and pre-fill it entirely with the holding value
        self.sweepC = np.full(self.sweepPointCount,
                              self.holdingCommand[channel])

        # this function only supports ABF2 formatted files
        if self.abfFileFormat != 2:
            return

        # it's just holding through 1/64th of the sweep length (why?!?)
        position = int(self.sweepPointCount/64)
        self.epochPoints = [position]

        # update the waveform for each epoch
        for epochNumber, epochType in enumerate(self._epochPerDacSection.nEpochType):
            pointCount = self._epochPerDacSection.lEpochInitDuration[epochNumber]
            deltaCommand = self._epochPerDacSection.fEpochLevelInc[epochNumber] * sweepNumber
            deltaCommandLast = self._epochPerDacSection.fEpochLevelInc[epochNumber] * (
                sweepNumber-1)
            thisCommand = self._epochPerDacSection.fEpochInitLevel[epochNumber]
            afterDelta = thisCommand+deltaCommand
            position2 = position + pointCount
            self.epochPoints.append(position2)

            # TODO: make updating sweepC optional

            # if nInterEpisodeLevel start from the last command
            if self._dacSection.nInterEpisodeLevel[channel]:
                self.sweepC = np.full(
                    self.sweepPointCount, thisCommand+deltaCommandLast)

            # do something different depending on what type of epoch it is
            if epochType == epoch_disabled:
                continue

            elif epochType == epoch_step:
                self.sweepC[position:position2] = afterDelta

            elif epochType == epoch_ramp:
                ramp = np.arange(pointCount)/pointCount
                rampStart = self.sweepC[position-1]
                rampEnd = afterDelta
                rampDiff = rampEnd-rampStart
                ramp *= rampDiff
                ramp += rampStart
                self.sweepC[position:position2] = ramp

            else:
                warnings.warn(
                    "treating unknown epoch type like a step", epochType)
                self.sweepC[position:position2] = afterDelta
            position += pointCount

        # if nInterEpisodeLevel sustain the last command (ignore holding)
        if self._dacSection.nInterEpisodeLevel[channel]:
            self.sweepC[position2:] = afterDelta

    def _commandContainsDeltas(self):
        """
        returns True if sweeps contain deltas.
        """
        if self.abfFileFormat == 1:
            return False
        if np.any(self._epochPerDacSection.fEpochLevelInc):
            return True
        else:
            return False

    def _digitalWaveformEpochs(self):
        """
        Create a 2d array indicating the high/low state (1 or 0) of each digital
        output (rows) for each epoch (columns).
        """
        if self.abfFileFormat != 2:
            self.digitalWaveformEpochs = None
            return
        numOutputs = self._protocolSection.nDigitizerTotalDigitalOuts
        byteStatesByEpoch = self._epochSection.nEpochDigitalOutput
        numEpochs = len(byteStatesByEpoch)
        statesAll = np.full((numOutputs, numEpochs), 0)
        for epochNumber in range(numEpochs):
            byteState = bin(byteStatesByEpoch[epochNumber])[2:]
            byteState = "0"*(numOutputs-len(byteState))+byteState
            byteState = [int(x) for x in list(byteState)]
            statesAll[:, epochNumber] = byteState[::-1]
        self.digitalWaveformEpochs = statesAll

    def sweepD(self, digitalOutputNumber=0):
        """
        Return a sweep waveform (similar to abf.sweepC) of a digital output channel.
        Digital outputs start at 0 and are usually 0-7. Returned waveform will be
        scaled from 0 to 1, although in reality they are 0V and 5V.
        """
        if self.abfFileFormat != 2:
            warnings.warn("Digital outputs of ABF1 files not supported.")
            return False
        states = self.digitalWaveformEpochs[digitalOutputNumber]
        sweepD = np.full(self.sweepPointCount, 0)
        for epoch in range(len(states)):
            sweepD[self.epochPoints[epoch]:
                   self.epochPoints[epoch+1]] = states[epoch]
        return sweepD
