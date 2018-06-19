import os
import glob
import time
import datetime
import numpy as np

from structures import HeaderV1
from structures import HeaderV2
from structures import SectionMap
from structures import ProtocolSection
from structures import ADCSection
from structures import DACSection
from structures import EpochPerDACSection
from structures import EpochSection
from structures import TagSection
from structures import StringsSection
from structures import StringsIndexed


def showThings(theThing):
    """
    Display all the child methods of an object
    """
    print()
    things = dir(theThing)
    for thingName in sorted(things):
        if thingName.startswith("__"):
            continue
        val = getattr(theThing, thingName)
        if "__main__" in str(type(val)):
            continue
        if "__main__" in str(val):
            continue
        print(thingName, "=", val)


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
        assert os.path.exists(self.abfFilePath)
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
        if preLoadData:
            self._loadAndScaleData()
        self._fileClose()

    def _fileOpen(self):
        """Open the ABF file in rb mode."""
        self.fb = open(self.abfFilePath, 'rb')
        self._fileOpenTime = time.perf_counter()

    def _determineAbfFormat(self):
        """
        The first few characters of an ABF file tell you its format.
        "ABF " is for ABF1 files, and "ABF2" is for ABF2 files.
        Anything else is probably a file that's not actually an ABF.
        """
        self.fb.seek(0)
        code = self.fb.read(4)
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
        self.fb.close()
        self._dataLoadTimeMs = (self._fileCloseTime-self._fileOpenTime)*1000

    def _readHeaders(self):
        """
        Read all headers into memory. 
        Store them in variables that can be accessed at any time.
        """
        if self.abfFileFormat == 1:
            self.headerV1 = HeaderV1(self.fb)
        elif self.abfFileFormat == 2:
            self.headerV2 = HeaderV2(self.fb)
            self.sectionMap = SectionMap(self.fb)
            self.protocolSection = ProtocolSection(self.fb, self.sectionMap)
            self.adcSection = ADCSection(self.fb, self.sectionMap)
            self.dacSection = DACSection(self.fb, self.sectionMap)
            self.epochPerDacSection = EpochPerDACSection(
                self.fb, self.sectionMap)
            self.epochSection = EpochSection(self.fb, self.sectionMap)
            self.tagSection = TagSection(self.fb, self.sectionMap)
            self.stringsSection = StringsSection(self.fb, self.sectionMap)
            self.stringsIndexed = StringsIndexed(
                self.headerV2, self.protocolSection, self.adcSection,
                self.dacSection, self.stringsSection)
        else:
            raise NotImplementedError("Invalid ABF file format")

    def _formatVersion(self):
        """
        The ABF Version differs in format from ABF1 and ABF2.
        This function formats the version as x.x.x.x for all ABF files.
        """
        if self.abfFileFormat == 1:
            self.abfVersion = "%.03f" % self.headerV1.fFileVersionNumber
            self.abfVersion = list(self.abfVersion.replace(".", ""))
            self.abfVersion = ".".join(self.abfVersion)
        elif self.abfFileFormat == 2:
            self.abfVersion = self.headerV2.fFileVersionNumber[::-1]
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
            startDate = str(self.headerV2.uFileStartDate)
            startTime = round(self.headerV2.uFileStartTimeMS/1000)
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
        if self.abfFileFormat == 1:
            self.dataByteStart = self.headerV1.lDataSectionPtr*512
            self.dataByteStart += self.headerV1.nNumPointsIgnored
            self.dataPointCount = self.headerV1.lActualAcqLength
            self.dataChannels = self.headerV1.nADCNumChannels
            self.dataRate = int(1e6 / self.headerV1.fADCSampleInterval)
            self.dataSecPerPoint = 1/self.dataRate
            self.sweepCount = self.headerV1.lActualEpisodes
            if self.sweepCount == 0:  # gap free file
                self.sweepCount = 1
            self.sweepPointCount = int(self.dataPointCount / self.sweepCount)
            self.sweepLengthSec = self.sweepPointCount / self.dataRate
        elif self.abfFileFormat == 2:
            self.dataByteStart = self.sectionMap.DataSection[0]*512
            self.dataPointCount = self.sectionMap.DataSection[2]
            self.dataChannels = self.sectionMap.ADCSection[2]
            self.dataRate = int(
                1e6 / self.protocolSection.fADCSequenceInterval)
            self.dataSecPerPoint = 1/self.dataRate
            self.sweepCount = self.headerV2.lActualEpisodes
            if self.sweepCount == 0:  # gap free file
                self.sweepCount = 1
            self.sweepPointCount = int(self.dataPointCount / self.sweepCount)
            self.sweepLengthSec = self.sweepPointCount / self.dataRate
        else:
            raise NotImplementedError("Invalid ABF file format")

    def _determineDataUnits(self):
        """
        Channel units and names are stored in the strings section as indexed
        strings where the indexes are scattered around the header. This function
        organizes channel units and names into simple lists of strings.
        """
        if self.abfFileFormat == 1:
            self.adcUnits = self.headerV1.sADCUnits[:self.dataChannels]
            self.adcNames = self.headerV1.sADCChannelName[:self.dataChannels]
            self.dacUnits = ["?" for x in self.adcUnits]
            self.dacNames = ["?" for x in self.adcUnits]
        elif self.abfFileFormat == 2:
            self.adcUnits = self.stringsIndexed.lADCUnits[:self.dataChannels]
            self.adcNames = self.stringsIndexed.lADCChannelName[:self.dataChannels]
            self.dacUnits = self.stringsIndexed.lDACChannelUnits[:self.dataChannels]
            self.dacNames = self.stringsIndexed.lDACChannelName[:self.dataChannels]
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
            self.scaleFactors = [1]*self.dataChannels
            for i in range(self.dataChannels):
                self.scaleFactors[i] = self.headerV1.lADCResolution/1e6
        elif self.abfFileFormat == 2:
            self.scaleFactors = [1]*self.dataChannels
            for i in range(self.dataChannels):
                self.scaleFactors[i] /= self.adcSection.fInstrumentScaleFactor[i]
                self.scaleFactors[i] /= self.adcSection.fSignalGain[i]
                self.scaleFactors[i] /= self.adcSection.fADCProgrammableGain[i]
                if self.adcSection.nTelegraphEnable:
                    self.scaleFactors[i] /= self.adcSection.fTelegraphAdditGain[i]
                self.scaleFactors[i] *= self.protocolSection.fADCRange
                self.scaleFactors[i] /= self.protocolSection.lADCResolution
                self.scaleFactors[i] += self.adcSection.fInstrumentOffset[i]
                self.scaleFactors[i] -= self.adcSection.fSignalOffset[i]
        else:
            raise NotImplementedError("Invalid ABF file format")

    def _determineHoldingValues(self):
        """
        When an ABF isn't being driven by an epoch (protocol), its command
        values are clamped at a certain holding value. This section looks-up
        those values.
        """
        if self.abfFileFormat == 1:
            self.holdingCommand = self.headerV1.fEpochInitLevel
        elif self.abfFileFormat == 2:
            self.holdingCommand = self.dacSection.fDACHoldingLevel
        else:
            raise NotImplementedError("Invalid ABF file format")

    def _determineProtocolPath(self):
        """
        If the ABF was recorded from a saved protocol, that path is stored in
        the ABF header.
        """
        if self.abfFileFormat == 1:
            self.protocolPath = self.headerV1.sProtocolPath
            self.protocol = os.path.basename(self.protocolPath)
            self.protocol = os.path.splitext(self.protocol)[0]
        elif self.abfFileFormat == 2:
            self.protocolPath = self.stringsIndexed.uProtocolPath
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
            self.abfFileComment = self.stringsIndexed.lFileComment
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
            self.tagComments = self.tagSection.sComment
            self.tagTimesSec = self.tagSection.lTagTime
            mult = self.protocolSection.fSynchTimeUnit/1e6
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

        self.fb.seek(self.dataByteStart)
        raw = np.fromfile(self.fb, dtype=np.int16, count=self.dataPointCount)
        raw = np.reshape(
            raw, (int(len(raw)/self.dataChannels), self.dataChannels))
        raw = np.rot90(raw)
        self.data = np.empty(raw.shape, dtype='float32')
        for i in range(self.dataChannels):
            self.data[i] = np.multiply(
                raw[i], self.scaleFactors[i], dtype='float32')


if __name__ == "__main__":
    dataFolder = R"C:\Users\scott\Documents\GitHub\pyABF\data"
    for fname in glob.glob(dataFolder+"/*.abf"):
        abf = ABFcore(fname)
        print(abf.abfID, "loaded in %.02f ms" % (abf._dataLoadTimeMs))
    print("DONE")
