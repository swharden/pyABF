"""
Code here provides direct access to the header and signal data of ABF files.
Efforts are invested to ensure ABF1 and ABF2 files are supported identically.

Design goals:
    Keep the ABF class tight.
    Source-out code for analysis.
    Put as much ABF header code in the structures module as possible.
"""

import os
import glob
import time
import datetime
import numpy as np
import logging
logging.basicConfig(level=logging.WARNING)
log = logging.getLogger(__name__)

import pyabf.abfHeader
from pyabf.abfHeader import HeaderV1
from pyabf.abfHeader import HeaderV2
from pyabf.abfHeader import SectionMap
from pyabf.abfHeader import ProtocolSection
from pyabf.abfHeader import ADCSection
from pyabf.abfHeader import DACSection
from pyabf.abfHeader import EpochPerDACSection
from pyabf.abfHeader import EpochSection
from pyabf.abfHeader import TagSection
from pyabf.abfHeader import StringsSection
from pyabf.abfHeader import StringsIndexed
from pyabf.abfHeader import BLOCKSIZE
from pyabf.epochs import Epochs

class ABF:
    """
    The ABF class provides direct access to the header and signal data of ABF
    files. It can load ABF1 and ABF2 files identically.

    The default action is to read all the ABF data from disk when the class is
    instantiated. When disabled (with an argument) to save speed, one can 
    quickly iterate through many ABF files to access header contents. The
    same thing is true with the loadStimulus argument and the stimulus waveform 
    file.

    Although you can access all data with abf.data, you can also call
    abf.setSweep() then access abf.sweepX and abf.sweepY and similar values.
    """

    def __init__(self, abf, loadData=True, loadStimulus=False):

        # assign arguments to the class
        self._preLoadData = loadData
        self._preloadStimulus = loadStimulus

        # clean-up file paths and filenames, then open the file
        self.abfFilePath = os.path.abspath(abf)
        if not os.path.exists(self.abfFilePath):
            raise ValueError("ABF file does not exist: %s" % self.abfFilePath)
        self.abfID = os.path.splitext(os.path.basename(self.abfFilePath))[0]
        log.debug(self.__repr__())
        self._fileOpen()

        # get a preliminary ABF version from the ABF file itself
        self.abfVersion = {}
        self.abfVersion["major"] = pyabf.abfHeader.abfFileFormat(self._fb)
        if not self.abfVersion["major"] in [1, 2]:
            raise NotImplementedError("Invalid ABF file format")

        # read the ABF header and bring its contents to the local namespace
        if self.abfVersion["major"] == 1:
            self._readHeadersV1()
        elif self.abfVersion["major"] == 2:
            self._readHeadersV2()

        # create more local variables based on the header data
        self._makeAdditionalVariables()

        # optionally load data from disk
        if self._preLoadData:
            self._loadAndScaleData()
            self.setSweep(0)

        # we are done with the ABF file, so close it
        self._fileClose()

        # populate self.sweepC with data loaded from stimulus file?
        if self._preloadStimulus:
            raise NotImplementedError()

    def __str__(self):
        txt = f"ABF file ({self.abfID}.abf)"
        txt += f" with {self.channelCount} channel"
        if self.channelCount > 1:
            txt += "s"
        txt += f", {self.sweepCount} sweep"
        if self.sweepCount > 1:
            txt += "s"
        abfLengthMin = self.sweepLengthSec*self.sweepCount/60.0
        txt += f", and a total length of %.02f min." % (abfLengthMin)
        return txt

    def __repr__(self):
        return 'ABFcore(abf="%s", loadData=%s, loadStimulus=%s)' % \
            (self.abfFilePath, self._preLoadData, self._preloadStimulus)

    def _fileOpen(self):
        """Open the ABF file in rb mode."""
        log.debug("opening ABF file")
        self._fileSize = os.path.getsize(self.abfFilePath)
        self._fb = open(self.abfFilePath, 'rb')
        self._fileOpenTime = time.perf_counter()

    def _fileClose(self):
        """Close and release the ABF file."""
        log.debug("closing ABF file")
        self._fileCloseTime = time.perf_counter()
        self._fb.close()
        self._dataLoadTimeMs = (self._fileCloseTime-self._fileOpenTime)*1000

    def _readHeadersV1(self):
        """Populate class variables from the ABF1 header."""
        assert self.abfVersion["major"] == 1

        # read the headers out of the file
        self._headerV1 = HeaderV1(self._fb)

        # create useful variables at the class level
        self.abfVersion = self._headerV1.abfVersionDict
        self.abfVersionString = self._headerV1.abfVersionString
        self.fileGUID = None
        self.creatorVersion = self._headerV1.creatorVersionDict
        self.abfDateTime = self._headerV1.abfDateTime
        self.holdingCommand = self._headerV1.fEpochInitLevel
        self.protocolPath = self._headerV1.sProtocolPath
        self.abfFileComment = ""
        self.tagComments = []
        self.tagTimesSec = []

        # data info
        self._nDataFormat = self._headerV1.nDataFormat
        self.dataByteStart = self._headerV1.lDataSectionPtr*BLOCKSIZE
        self.dataByteStart += self._headerV1.nNumPointsIgnored
        self.dataPointCount = self._headerV1.lActualAcqLength
        self.dataPointByteSize = 2  # ABF 1 files always have int16 points?
        self.channelCount = self._headerV1.nADCNumChannels
        self.dataRate = int(1e6 / self._headerV1.fADCSampleInterval)
        self.dataSecPerPoint = 1 / self.dataRate
        self.sweepCount = self._headerV1.lActualEpisodes

        # channel names
        self.adcUnits = self._headerV1.sADCUnits[:self.channelCount]
        self.adcNames = self._headerV1.sADCChannelName[:self.channelCount]
        self.dacUnits = ["?" for x in self.adcUnits]
        self.dacNames = ["?" for x in self.adcUnits]

        # data scaling
        self._dataGain = [1]*self.channelCount
        self._dataOffset = [0]*self.channelCount
        for i in range(self.channelCount):
            self._dataGain[i] /= self._headerV1.fInstrumentScaleFactor[i]
            self._dataGain[i] /= self._headerV1.fSignalGain[i]
            self._dataGain[i] /= self._headerV1.fADCProgrammableGain[i]
            if self._headerV1.nTelegraphEnable[i] == 1:
                self._dataGain[i] /= self._headerV1.fTelegraphAdditGain[i]
            self._dataGain[i] *= self._headerV1.fADCRange
            self._dataGain[i] /= self._headerV1.lADCResolution
            self._dataOffset[i] += self._headerV1.fInstrumentOffset[i]
            self._dataOffset[i] -= self._headerV1.fSignalOffset[i]

    def _readHeadersV2(self):
        """Populate class variables from the ABF2 header."""

        assert self.abfVersion["major"] == 2

        # read the headers out of the file
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

        # create useful variables at the class level
        self.abfVersion = self._headerV2.abfVersionDict
        self.abfVersionString = self._headerV2.abfVersionString
        self.fileGUID = self._headerV2.sFileGUID
        self.creatorVersion = self._headerV2.creatorVersionDict
        self.abfDateTime = self._headerV2.abfDateTime
        self.holdingCommand = self._dacSection.fDACHoldingLevel
        self.protocolPath = self._stringsIndexed.uProtocolPath
        self.abfFileComment = self._stringsIndexed.lFileComment
        self.tagComments = self._tagSection.sComment
        _tagMult = self._protocolSection.fSynchTimeUnit/1e6
        self.tagTimesSec = self._tagSection.lTagTime
        self.tagTimesSec = [_tagMult*x for x in self.tagTimesSec]

        # data info
        self._nDataFormat = self._headerV2.nDataFormat
        self.dataByteStart = self._sectionMap.DataSection[0]*BLOCKSIZE
        self.dataPointCount = self._sectionMap.DataSection[2]
        self.dataPointByteSize = self._sectionMap.DataSection[1]
        self.channelCount = self._sectionMap.ADCSection[2]
        self.dataRate = self._protocolSection.fADCSequenceInterval
        self.dataRate = int(1e6 / self.dataRate)
        self.dataSecPerPoint = 1 / self.dataRate
        self.sweepCount = self._headerV2.lActualEpisodes

        # channel names
        self.adcUnits = self._stringsIndexed.lADCUnits[:self.channelCount]
        self.adcNames = self._stringsIndexed.lADCChannelName[:self.channelCount]
        self.dacUnits = self._stringsIndexed.lDACChannelUnits[:self.channelCount]
        self.dacNames = self._stringsIndexed.lDACChannelName[:self.channelCount]

        # data scaling
        self._dataGain = [1]*self.channelCount
        self._dataOffset = [0]*self.channelCount
        for i in range(self.channelCount):
            self._dataGain[i] /= self._adcSection.fInstrumentScaleFactor[i]
            self._dataGain[i] /= self._adcSection.fSignalGain[i]
            self._dataGain[i] /= self._adcSection.fADCProgrammableGain[i]
            if self._adcSection.nTelegraphEnable[i] == 1:
                self._dataGain[i] /= self._adcSection.fTelegraphAdditGain[i]
            self._dataGain[i] *= self._protocolSection.fADCRange
            self._dataGain[i] /= self._protocolSection.lADCResolution
            self._dataOffset[i] += self._adcSection.fInstrumentOffset[i]
            self._dataOffset[i] -= self._adcSection.fSignalOffset[i]

    def _makeAdditionalVariables(self):
        """create or touch-up version-nonspecific variables."""

        if self.sweepCount == 0:  # gap free
            self.sweepCount = 1
        self.sweepPointCount = int(
            self.dataPointCount / self.sweepCount / self.channelCount)
        self.sweepLengthSec = self.sweepPointCount / self.dataRate

        self.protocol = os.path.basename(self.protocolPath)
        self.protocol = self.protocol.replace(".pro", "")
        if len(self.protocol) == 0 or ord(self.protocol[0]) == 127:
            self.protocol = "None"

        self.tagTimesMin = [x/60 for x in self.tagTimesSec]
        self.tagSweeps = [x/self.sweepLengthSec for x in self.tagTimesSec]
        self.channelList = list(range(self.channelCount))
        self.sweepList = list(range(self.sweepCount))

        self.epochsByChannel = []
        for channel in self.channelList:
            self.epochsByChannel.append(Epochs(self, channel))

        if self._nDataFormat == 0:
            self._dtype = np.int16
        elif self._nDataFormat == 1:
            self._dtype = np.float32
        else:
            raise NotImplementedError("unknown data format")

    def _loadAndScaleData(self):
        """Load data from the ABF file and scale it by its scaleFactor."""

        # read the data from the ABF file
        self._fb.seek(self.dataByteStart)
        raw = np.fromfile(self._fb, dtype=self._dtype,
                          count=self.dataPointCount)
        nRows = self.channelCount
        nCols = int(self.dataPointCount/self.channelCount)
        raw = np.reshape(raw, (nCols, nRows))
        raw = np.rot90(raw)
        raw = raw[::-1]

        # if data is int, scale it to float32 so we can scale it
        self.data = raw.astype(np.float32)

        # if the data was originally an int, it must be scaled
        if self._dtype == np.int16:
            for i in range(self.channelCount):
                self.data[i] = np.multiply(self.data[i], self._dataGain[i])
                self.data[i] = np.add(self.data[i], self._dataOffset[i])

    # These additional tools are useful add-ons to the ABF class:
    from pyabf.text import abfInfoPage as getInfoPage
    from pyabf.epochs import sweepD
    from pyabf.sweep import setSweep
    from pyabf.sweep import sweepC
    from pyabf.sweep import sweepBaseline
    from pyabf.sweep import sweepMeasureAverage as sweepAvg
    from pyabf.sweep import sweepMeasureArea as sweepArea
    from pyabf.sweep import sweepMeasureStdev as sweepStdev
    from pyabf.sweep import sweepMeasureMax as sweepMax
    from pyabf.sweep import sweepMeasureMin as sweepMin
