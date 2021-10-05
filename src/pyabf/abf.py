"""
Code here provides direct access to the header and signal data of ABF files.
Efforts are invested to ensure ABF1 and ABF2 files are supported identically.

This file is LIMITED TO THE MANAGEMENT OF HEADER AND DATA information.
Analysis routines are not written in the ABF class itself. If useful, they
are to be written in another file and imported as necessary.
"""

from io import BufferedReader
import pathlib
from pyabf.abf2.dataSection import DataSection
import pyabf.abfWriter
import pyabf.stimulus

from pyabf.abf2.stringsSection import StringsSection
from pyabf.abf2.tagSection import TagSection
from pyabf.abf2.epochSection import EpochSection
from pyabf.abf2.epochPerDacSection import EpochPerDACSection
from pyabf.abf2.dacSection import DACSection
from pyabf.abf2.adcSection import ADCSection
from pyabf.abf2.protocolSection import ProtocolSection
from pyabf.abf2.synchArraySection import SynchArraySection
from pyabf.abf2.userListSection import UserListSection
from pyabf.abf2.headerV2 import HeaderV2
from pyabf.abf1.headerV1 import HeaderV1

from pyabf.tools.abfHeaderDisplay import abfInfoPage

import os
import time
import numpy as np
from pathlib import PureWindowsPath
import hashlib
from typing import Union, List, Tuple


class ABF:
    """
    The ABF class provides direct access to the header and signal data of ABF
    files. It can load ABF1 and ABF2 files identically.

    The default action is to read all the ABF data from disk when the class is
    instantiated. When disabled (with an argument) to save speed, one can
    quickly iterate through many ABF files to access header contents.

    Although you can access all data with abf.data, you can also call
    abf.setSweep() then access abf.sweepX and abf.sweepY and similar values.
    """

    def __init__(self,
                 abfFilePath: Union[str, pathlib.Path],
                 loadData: bool = True,
                 cacheStimulusFiles: bool = True,
                 stimulusFileFolder: bool = None):
        """
        Load header and sweep data from an ABF file.

        ### Parameters

        1. abfFilePath -- path to the ABF file

        2. loadData -- whether or not to load sweep data values from the file immediately on instantiation.
        Set this to False if you intent to iterate many ABF files rapidly and only inspect their headers.

        3. cacheStimulusFiles -- Some ABF files use a source ABF as a stimulus file to control its DAC.
        This module automatically loads the stimulus waveform from disk if it is available.
        This parameter controls whether stimulus files should be stored in memory at the module level.
        Set to False to prevent memory issues if you intend to iterate very large numbers of ABFs with
        unique stimulus waveforms.

        4. stimulusFileFolder -- Some ABF files use a source ABF as a stimulus file to control its DAC.
        This module automatically loads the stimulus waveform from disk if it is available.
        The ABF header contains an absolute file path to the stimulus file used to control the DAC.
        If supplied, this path is used as an alternate search path to look for stimulus files with the same filename
        in the case the original path does not exist on the machine loading the ABF.
        """

        if (isinstance(abfFilePath, pathlib.Path)):
            abfFilePath = str(abfFilePath)

        if abfFilePath.lower().endswith(".atf"):
            raise Exception("use pyabf.ATF (not pyabf.ABF) for ATF files")

        if (os.path.isdir(abfFilePath)):
            raise Exception("path must be a path to a FILE not a FOLDER.")

        self._preLoadData = loadData
        self._cacheStimulusFiles = cacheStimulusFiles

        self.abfFilePath = os.path.abspath(abfFilePath)
        self.abfFolderPath = os.path.dirname(self.abfFilePath)

        if stimulusFileFolder:
            self.stimulusFileFolder = stimulusFileFolder
        else:
            self.stimulusFileFolder = self.abfFolderPath

        if not os.path.exists(self.abfFilePath):
            raise ValueError("ABF file does not exist: %s" % self.abfFilePath)
        self.abfID = os.path.splitext(os.path.basename(self.abfFilePath))[0]

        with open(self.abfFilePath, 'rb') as fb:

            # The first 4 bytes of the ABF indicates what type of file it is
            self.abfVersion = {}
            fb.seek(0)
            fileSignature = fb.read(4).decode("ascii", errors='ignore')
            if fileSignature == "ABF ":
                self.abfVersion["major"] = 1
                self._readHeadersV1(fb)
            elif fileSignature == "ABF2":
                self.abfVersion["major"] = 2
                self._readHeadersV2(fb)
            else:
                raise NotImplementedError("Invalid ABF file format")

            # create more local variables based on the header data
            self._makeAdditionalVariables()

            # note the file size
            fb.seek(0, os.SEEK_END)
            self._fileSize = fb.tell()

            # optionally load data from disk
            if self._preLoadData:
                self._loadAndScaleData(fb)
                self.setSweep(0)

    def __str__(self):
        """
        Return a string describing basic properties of the loaded ABF.
        """

        txt = """
        ABF (vVERSN)
        with CHNM channels (CHUNITS),
        sampled at RATEKHZ kHz,
        containing SWCNT sweeps,
        having no tags,
        with a total length of LENMIN minutes,
        recorded without a protocol file.
        """.strip().replace("\n", " ")
        while "  " in txt:
            txt = txt.replace("  ", " ")

        # ABF version
        # NOTE: self.versionString is improperly implemented but left to maintain back compatibility
        realVersion = self.abfVersionString.replace(".", "")
        realVersion = list(realVersion)
        realVersion.insert(1, ".")
        realVersion = "".join(realVersion)
        if (realVersion[-1] == "0"):
            realVersion = realVersion[:-1]
        if (realVersion[-1] == "0"):
            realVersion = realVersion[:-1]
        txt = txt.replace("VERSN", realVersion)

        # channels
        txt = txt.replace("CHNM", str(self.channelCount))
        txt = txt.replace("CHUNITS", ", ".join(self.adcUnits))
        if self.channelCount == 1:
            txt = txt.replace(" channels ", " channel ")

        # data dimensions
        txt = txt.replace("RATEKHZ", str(self.dataRate/1e3))
        txt = txt.replace("SWCNT", str(self.sweepCount))
        txt = txt.replace("LENMIN", "%.02f" % (self.dataLengthMin))
        if self.sweepCount == 1:
            txt = txt.replace("sweeps", "sweep")

        # protocol
        if self.protocol and self.protocol != "None":
            protoMsg = 'with protocol "%s"' % self.protocol
            txt = txt.replace('without a protocol file', protoMsg)

        # tags
        if len(self.tagComments) > 0:
            tagmsg = ", ".join(self.tagComments)
            tagmsg = "%d tags (%s)" % (len(self.tagComments), tagmsg)
            tagmsg = tagmsg.replace("no tags", tagmsg)
            if len(self.tagComments) == 1:
                tagmsg = tagmsg.replace(" tags ", " tag ")
            txt = txt.replace("no tags", tagmsg)

        return txt

    def __repr__(self):
        return self.__str__() + f" path={self.abfFilePath}"

    def _readHeadersV1(self, fb: BufferedReader):
        """Populate class variables from the ABF1 header."""
        assert self.abfVersion["major"] == 1

        # read the headers out of the file
        self._headerV1 = HeaderV1(fb)

        # create useful variables at the class level
        self.abfVersion = self._headerV1.abfVersionDict
        self.abfVersionString = self._headerV1.abfVersionString
        self._fileGUID = self._headerV1.sFileGUID
        self.creator = self._headerV1.sCreatorInfo + \
            " " + self._headerV1.creatorVersionString
        self.creatorVersion = self._headerV1.creatorVersionDict
        self.creatorVersionString = self._headerV1.creatorVersionString
        self.abfDateTime = self._headerV1.abfDateTime
        self.abfDateTimeString = self._headerV1.abfDateTimeString
        self.holdingCommand = self._headerV1.fEpochInitLevel
        self.protocolPath = self._headerV1.sProtocolPath
        if self._headerV1.sFileCommentNew:
            self.abfFileComment = self._headerV1.sFileCommentNew
        else:
            self.abfFileComment = self._headerV1.sFileCommentOld
        self.nOperationMode = self._headerV1.nOperationMode
        try:
            self.userList = [float(x)
                             for x in self._headerV1.sULParamValueList if x]
        except:
            self.userList = self._headerV1.sULParamValueList
        self.userListEnable = self._headerV1.nULEnable
        self.userListParamToVary = self._headerV1.nULParamToVary
        self.userListParamToVaryName = [pyabf.names.getUserListParameterName(x)
                                        for x in self.userListParamToVary]
        self.userListRepeat = self._headerV1.nULRepeat
        _tagMult = self._headerV1.fADCSampleInterval / 1e6
        _tagMult = _tagMult / self._headerV1.nADCNumChannels
        self.tagComments = self._headerV1.sTagComment
        self.tagTimesSec = self._headerV1.lTagTime
        self.tagTimesSec = [_tagMult*x for x in self.tagTimesSec]

        # data info
        self._nDataFormat = self._headerV1.nDataFormat
        self.dataByteStart = self._headerV1.lDataSectionPtr*512
        self.dataByteStart += self._headerV1.nNumPointsIgnored
        self.dataPointCount = self._headerV1.lActualAcqLength

        if self._nDataFormat == 0:
            self.dataPointByteSize = 2
        elif self._nDataFormat == 1:
            raise ValueError("Support for float data is not implemented")
        else:
            raise ValueError(
                "_nDataFormat={} is invalid".format(self._nDataFormat))

        self.channelCount = self._headerV1.nADCNumChannels
        self.dataRate = 1e6 / self._headerV1.fADCSampleInterval
        self.dataRate = int(self.dataRate / self.channelCount)
        self.dataSecPerPoint = 1.0 / self.dataRate
        self.dataPointsPerMs = int(self.dataRate/1000)
        self.sweepCount = self._headerV1.lActualEpisodes

        self.adcUnits = [""] * self.channelCount
        self.adcNames = [""] * self.channelCount
        self.channelList = [-1] * self.channelCount

        # channel names
        for i in range(self.channelCount):
            physicalChannel = self._headerV1.nADCSamplingSeq[i]
            logicalChannel = self._headerV1.nADCPtoLChannelMap[physicalChannel]
            self.adcUnits[i] = self._headerV1.sADCUnits[physicalChannel]
            self.adcNames[i] = self._headerV1.sADCChannelName[physicalChannel]
            self.channelList[i] = i

        # TODO not sure if these lists needs to be reduced
        self.dacUnits = self._headerV1.sDACChannelUnit
        self.dacNames = self._headerV1.sDACChannelName

        # data scaling
        self._dataGain = [1]*self.channelCount
        self._dataOffset = [0]*self.channelCount

        for index, channel in enumerate(self.channelList):
            adcIndex = self._headerV1.nADCSamplingSeq[channel]
            self._dataGain[index] /= self._headerV1.fInstrumentScaleFactor[adcIndex]
            self._dataGain[index] /= self._headerV1.fSignalGain[adcIndex]
            self._dataGain[index] /= self._headerV1.fADCProgrammableGain[adcIndex]
            if self._headerV1.nTelegraphEnable[adcIndex] == 1:
                self._dataGain[index] /= self._headerV1.fTelegraphAdditGain[adcIndex]
            self._dataGain[index] *= self._headerV1.fADCRange
            self._dataGain[index] /= self._headerV1.lADCResolution
            self._dataOffset[index] += self._headerV1.fInstrumentOffset[adcIndex]
            self._dataOffset[index] -= self._headerV1.fSignalOffset[adcIndex]

    def _readHeadersV2(self, fb: BufferedReader):
        """Populate class variables from the ABF2 header."""

        assert self.abfVersion["major"] == 2

        # read the headers out of the file
        self._headerV2 = HeaderV2(fb)
        self._protocolSection = ProtocolSection(fb)
        self._dataSection = DataSection(fb)
        self._adcSection = ADCSection(fb)
        self._dacSection = DACSection(fb)
        self._epochPerDacSection = EpochPerDACSection(fb)
        self._epochSection = EpochSection(fb)
        self._tagSection = TagSection(fb)
        self._stringsSection = StringsSection(fb)
        self._synchArraySection = SynchArraySection(fb)
        self._userListSection = UserListSection(fb)

        # create useful variables at the class level
        self.abfVersion = self._headerV2.abfVersionDict
        self.abfVersionString = self._headerV2.abfVersionString
        self._fileGUID = self._headerV2.sFileGUID
        self.creator = \
            self._stringsSection._indexedStrings[self._headerV2.uCreatorNameIndex] + " " + \
            self._headerV2.creatorVersionString
        self.creatorVersion = self._headerV2.creatorVersionDict
        self.creatorVersionString = self._headerV2.creatorVersionString
        self.abfDateTime = self._headerV2.abfDateTime
        self.abfDateTimeString = self._headerV2.abfDateTimeString
        self.holdingCommand = self._dacSection.fDACHoldingLevel
        self.protocolPath = self._stringsSection._indexedStrings[self._headerV2.uProtocolPathIndex]
        self.abfFileComment = self._stringsSection._indexedStrings[
            self._protocolSection.lFileCommentIndex]
        self.nOperationMode = self._protocolSection.nOperationMode

        # populate the user list
        self.userList = None
        self.userListEnable = self._userListSection.nULEnable
        self.userListParamToVary = self._userListSection.nULParamToVary
        self.userListParamToVaryName = [pyabf.names.getUserListParameterName(x)
                                        for x in self.userListParamToVary]
        self.userListRepeat = self._userListSection.nULRepeat

        try:
            # This is the correct way, but it doesn't seem to work for every ABF.
            # I think this is because there is a bug in the string indexer.
            #self.userList = self._stringsIndexed.indexedStrings[self._userListSection.nStringIndex[0]]
            #self.userList = [float(x) for x in self.userList.split(",")]

            # This is weird but it's been in the code for a while and seems to work.
            firstBlockStrings = self._stringsSection._stringsRaw[0].split(
                b'\x00')
            self.userList = firstBlockStrings[-2].decode("utf-8").split(",")
            self.userList = [float(x) for x in self.userList if x]
        except:
            self.userList = None

        # data info
        self._nDataFormat = self._headerV2.nDataFormat
        self.dataByteStart = self._dataSection._byteStart
        self.dataPointCount = self._dataSection._entryCount
        self.dataPointByteSize = self._dataSection._entrySize
        self.channelCount = self._adcSection._entryCount
        self.dataRate = self._protocolSection.fADCSequenceInterval
        self.dataRate = int(1e6 / self.dataRate)
        self.dataSecPerPoint = 1.0 / self.dataRate
        self.dataPointsPerMs = int(self.dataRate/1000)
        self.sweepCount = self._headerV2.lActualEpisodes
        self.channelList = list(range(self.channelCount))

        # tags
        self.tagComments = self._tagSection.sComment
        self.tagTimesSec = self._tagSection.lTagTime
        for i in range(len(self.tagTimesSec)):
            if self._protocolSection.fSynchTimeUnit == 0:
                _tagMult = 1.0/self.dataRate/self.channelCount
            else:
                _tagMult = self._protocolSection.fSynchTimeUnit/1e6
            self.tagTimesSec[i] = self.tagTimesSec[i] * _tagMult
            self.tagTimesSec[i] = round(self.tagTimesSec[i], 5)

        # channel names
        self.adcNames = [self._stringsSection._indexedStrings[x]
                         for x in self._adcSection.lADCChannelNameIndex[:self.channelCount]]
        self.adcUnits = [self._stringsSection._indexedStrings[x]
                         for x in self._adcSection.lADCUnitsIndex[:self.channelCount]]
        self.dacNames = [self._stringsSection._indexedStrings[x]
                         for x in self._dacSection.lDACChannelNameIndex[:self.channelCount]]
        self.dacUnits = [self._stringsSection._indexedStrings[x]
                         for x in self._dacSection.lDACChannelUnitsIndex[:self.channelCount]]

        # data scaling
        self._dataGain = [1]*self.channelCount
        self._dataOffset = [0]*self.channelCount
        for i in range(self.channelCount):
            #adcIndex = self._adcSection.nADCSamplingSeq[i]
            # NOTE: ADC sequence is handled inside the ADC section so it doesn't need to be handled here
            adcIndex = i
            self._dataGain[i] /= self._adcSection.fInstrumentScaleFactor[adcIndex]
            self._dataGain[i] /= self._adcSection.fSignalGain[adcIndex]
            self._dataGain[i] /= self._adcSection.fADCProgrammableGain[adcIndex]
            if self._adcSection.nTelegraphEnable[adcIndex] == 1:
                self._dataGain[i] /= self._adcSection.fTelegraphAdditGain[adcIndex]
            self._dataGain[i] *= self._protocolSection.fADCRange
            self._dataGain[i] /= self._protocolSection.lADCResolution
            self._dataOffset[i] += self._adcSection.fInstrumentOffset[adcIndex]
            self._dataOffset[i] -= self._adcSection.fSignalOffset[adcIndex]

    def _makeAdditionalVariables(self):
        """create or touch-up version-nonspecific variables."""

        # correct for files crazy large or small holding levels (usually the
        # result of non-filled binary data getting interpreted as a float)
        for i, level in enumerate(self.holdingCommand):
            if abs(level) > 1e6:
                self.holdingCommand[i] = np.nan
            if abs(level) > 0 and abs(level) < 1e-6:
                self.holdingCommand[i] = 0

        # ensure gap-free files have a single sweep
        if self.abfVersion["major"] == 1:
            if self._headerV1.nOperationMode == 3:
                self.sweepCount = 1
        if self.abfVersion["major"] == 2:
            if self._protocolSection.nOperationMode == 3:
                self.sweepCount = 1

        # sweep information
        if self.sweepCount == 0:
            self.sweepCount = 1
        self.sweepPointCount = int(
            self.dataPointCount / self.sweepCount / self.channelCount)
        self.sweepLengthSec = float(self.sweepPointCount) / self.dataRate
        self.sweepList = list(range(self.sweepCount))

        # set sweepIntervalSec (can be different than sweepLengthSec)
        if self.abfVersion["major"] == 1:
            self.sweepIntervalSec = self.sweepLengthSec
        if self.abfVersion["major"] == 2:
            self.sweepIntervalSec = self._protocolSection.fEpisodeStartToStart
            if self.sweepIntervalSec == 0:
                self.sweepIntervalSec = self.sweepLengthSec

        # determine total ABF recording length
        self.dataLengthSec = self.sweepIntervalSec*self.sweepCount
        if self.sweepCount > 1:
            self.dataLengthSec += self.sweepLengthSec
        self.dataLengthMin = self.dataLengthSec / 60.0

        # protocol file
        if self.protocolPath.endswith(".pro"):
            self.protocol = PureWindowsPath(self.protocolPath).stem
        else:
            self.protocolPath = "None"
            self.protocol = "None"

        # tag details
        self.tagTimesMin = [x/60 for x in self.tagTimesSec]
        self.tagSweeps = [x/self.sweepLengthSec for x in self.tagTimesSec]

        # fix empty channel units and names
        for i, val in enumerate(self.adcUnits):
            if val == "" or val == None:
                self.adcUnits[i] = "?"
        for i, val in enumerate(self.adcNames):
            if val == "" or val == None:
                self.adcNames[i] = "?"

        # create objects for each channel stimulus
        self.stimulusByChannel = []
        for channel in self.channelList:
            self.stimulusByChannel.append(
                pyabf.stimulus.Stimulus(self, channel))

        # note if data is float or int
        if self._nDataFormat == 0:
            self._dtype = np.int16
        elif self._nDataFormat == 1:
            self._dtype = np.float32
        else:
            raise NotImplementedError("unknown data format")

    def _loadAndScaleData(self, fb: BufferedReader):
        """Load data from the ABF file and scale it by its scaleFactor."""

        # read the data from the ABF file
        fb.seek(self.dataByteStart)
        raw = np.fromfile(fb, dtype=self._dtype, count=self.dataPointCount)
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

    def _ide_helper(self):
        """
        Add things here to help auto-complete IDEs aware of things added by
        external modules. This function should never actually get called.
        """
        self.sweepNumber = -1
        self.sweepChannel = -1
        self.sweepUnitsX = ""
        self.sweepUnitsY = ""
        self.sweepUnitsC = ""
        self.sweepLabelX = ""
        self.sweepLabelY = ""
        self.sweepLabelC = ""
        self.sweepX = np.array([])
        self.sweepY = np.array([])
        self.sweepEpochs = pyabf.waveform.EpochSweepWaveform()

    @property
    def headerText(self):
        """Return all header information as a text-formatted string."""
        return abfInfoPage(self).getText()

    @property
    def headerMarkdown(self):
        """Return all header information as a markdown-formatted string."""
        return abfInfoPage(self).generateMarkdown()

    @property
    def headerHTML(self):
        """Return all header information as a text-formatted string."""
        return abfInfoPage(self).generateHTML()

    def headerLaunch(self):
        """Display ABF header information in the web browser."""
        html = abfInfoPage(self).generateHTML()

        # open a temp file, save HTML, launch it, then delete it
        import tempfile

        namedTempFile = tempfile.NamedTemporaryFile(delete=False)
        tmpFilePath = namedTempFile.name+'.html'

        try:
            with open(tmpFilePath, 'w') as f:
                f.write(html)
            os.system(tmpFilePath)
        finally:
            time.sleep(3)  # give it time to display before deleting the file
            os.remove(tmpFilePath)

    def saveABF1(self, filePath: Union[str, pathlib.Path]):
        """
        Save this ABF file as an ABF1 file compatible with ClampFit and MiniAnalysis.
        Not all header values are saved, but the minimum necessary are to read sweep data.

        ### Parameters
        1. filePath -- path of the ABF1 file to create
        """
        if (self.nOperationMode == 1):
            raise Exception(
                "saving ABFs with variable-length sweeps is not supported")

        if isinstance(filePath, pathlib.Path):
            filePath = str(filePath)

        filePath = os.path.abspath(filePath)
        sweepData = np.empty((self.sweepCount, self.sweepPointCount))
        for sweep in self.sweepList:
            self.setSweep(sweep)
            sweepData[sweep] = self.sweepY
        pyabf.abfWriter.writeABF1(sweepData, filePath, self.dataRate)

    def launchInClampFit(self):
        """
        Launch the ABF in the default ABF viewing program (usually ClampFit) as
        if it were double-clicked in the windows explorer. 

        This assumes ClampFit is installed on your system and the default application
        for opening ABF files.

        This will fail is ClampFit is already open.
        """
        cmd = 'explorer.exe "%s"' % (self.abfFilePath)
        print("Launching %s.abf in ClampFit..." % (self.abfID))
        print(cmd)
        os.system(cmd)

    def setSweep(self,
                 sweepNumber: int,
                 channel: int = 0,
                 absoluteTime: bool = False,
                 baseline: List[float] = [None, None]):
        """
        Args:

        ### Parameters
        1. sweepNumber -- sweep number to load (starting at 0)
        2. channel -- ABF channel (starting at 0)
        3. absoluteTime -- Whether sweepX should represent time in sweep or time in file.
            If False, the first value of sweepX will always be 0.
            If True, sweepX of successive sweeps will start at larger and larger values.
        4. baseline -- If two times are provided (in seconds), the entire sweep will be subtracted
            to the mean of the sweep between those two times (baseline subtraction).
            Use [None, None] to disable automatic baseline subtraction.
        """

        # basic error checking
        if not sweepNumber in self.sweepList:
            msg = "Sweep %d not available (must be 0 - %d)" % (
                sweepNumber, self.sweepCount-1)
            raise ValueError(msg)
        if not channel in self.channelList:
            msg = "Channel %d not available (must be 0 - %d)" % (
                channel, self.channelCount-1)
            raise ValueError(msg)

        if not "data" in (dir(self)):
            with open(self.abfFilePath, 'rb') as fb:
                self._loadAndScaleData(fb)

        adcName, adcUnits = self._getAdcNameAndUnits(channel)
        dacName, dacUnits = self._getDacNameAndUnits(channel)

        # sweep information
        self.sweepNumber = sweepNumber
        self.sweepChannel = channel
        self.sweepUnitsY = adcUnits
        self.sweepUnitsC = dacUnits
        self.sweepUnitsX = "sec"

        # standard labels
        self.sweepLabelY = f"{adcName} ({adcUnits})"
        self.sweepLabelC = f"{dacName} ({dacUnits})"
        self.sweepLabelX = "Time (seconds)"
        self.sweepLabelD = "Digital Output (V)"

        # use fancy labels for known units
        if self.sweepUnitsY == "pA":
            self.sweepLabelY = "Clamp Current (pA)"
            self.sweepLabelC = "Membrane Potential (mV)"
        elif self.sweepUnitsY == "mV":
            self.sweepLabelY = "Membrane Potential (mV)"
            self.sweepLabelC = "Applied Current (pA)"

        # determine if this ABF uses variable-length sweeps
        hasMultipleSweeps = self.sweepCount > 1
        if hasMultipleSweeps and hasattr(self, "_synchArraySection"):
            uniqueSweepLengths = set(self._synchArraySection.lLength)
            isFixedLengthSweeps = len(uniqueSweepLengths) == 1
        else:
            isFixedLengthSweeps = True

        # determine data bounds for this sweep
        if (isFixedLengthSweeps):
            pointStart = self.sweepPointCount*sweepNumber
            pointCount = self.sweepPointCount
        else:
            pointStart = 0
            for i in range(1, sweepNumber):
                pointStart += self._synchArraySection.lLength[i-1]
            pointCount = self._synchArraySection.lLength[sweepNumber]
        pointEnd = pointStart + pointCount

        # load the actual sweep data
        self.sweepY = self.data[channel, pointStart:pointEnd]
        self.sweepX = np.arange(len(self.sweepY))*self.dataSecPerPoint
        if absoluteTime:
            if isFixedLengthSweeps:
                self.sweepX += sweepNumber * self.sweepIntervalSec
            else:
                sweepOffsetPoints = self._synchArraySection.lStart[sweepNumber]
                sweepOffsetSec = sweepOffsetPoints / self.dataRate
                self.sweepX += sweepOffsetSec

        # default case is disabled
        if not hasattr(self, '_sweepBaselinePoints'):
            self._sweepBaselinePoints = False

        # if baseline subtraction is used, apply it
        assert isinstance(baseline, list) and len(baseline) == 2
        if not None in baseline:
            pt1, pt2 = [int(x*self.dataRate) for x in baseline]
            blVal = np.average(self.sweepY[pt1:pt2])
            self.sweepY = self.sweepY-blVal

        # make sure sweepPointCount is always accurate
        if isFixedLengthSweeps:
            assert (self.sweepPointCount == len(self.sweepY))

        # prepare the stimulus waveform table for this sweep/channel
        if (channel < len(self.holdingCommand)):
            epochTable = pyabf.waveform.EpochTable(self, channel)
            self.sweepEpochs = epochTable.epochWaveformsBySweep[sweepNumber]
        else:
            epochTable = None
            self.sweepEpochs = None

    def _getAdcNameAndUnits(self, adcIndex: int) -> Tuple[str, str]:
        if (adcIndex < len(self.adcNames)):
            return [self.adcNames[adcIndex], self.adcUnits[adcIndex]]
        else:
            return [None, None]

    def _getDacNameAndUnits(self, dacIndex: int) -> Tuple[str, str]:
        if (dacIndex < len(self.dacNames)):
            return [self.dacNames[dacIndex], self.dacUnits[dacIndex]]
        else:
            return [None, None]

    @property
    def sweepC(self):
        """Generate the sweep command waveform."""
        if hasattr(self, "_sweepC") and isinstance(self._sweepC, np.ndarray):
            # someone set a custom waveform, so always return it
            return self._sweepC
        else:
            # auto-generate (or auto-load) the waveform using the stimulus module
            if not hasattr(self, 'sweepChannel'):
                # call setsweep if it hasn't been called before
                self.setSweep(0)
            stimulus = self.stimulusByChannel[self.sweepChannel]
            stimulusWaveform = stimulus.stimulusWaveform(self.sweepNumber)
            if len(stimulusWaveform) > len(self.sweepX):
                stimulusWaveform = stimulusWaveform[:len(self.sweepX)]
            return stimulusWaveform

    @sweepC.setter
    def sweepC(self, sweepData=None):
        """
        Manually define sweepC so the given sweepData will always be returned as
        sweepC and the stimulus waveform will no longer be automatically generated
        or loaded from file. Undo this by deleting "abf._sweepC".
        """
        if sweepData is None:
            del self._sweepC
            return
        if not len(sweepData):
            raise ValueError("an array must be given when setting sweepC")
        sweepData = np.array(sweepData)
        if not sweepData.shape == self.sweepY.shape:
            raise ValueError("sweepC.shape must match sweepY.shape")
        self._sweepC = sweepData

    def sweepD(self, digOutNumber=0):
        """Generate a waveform for the given digital output."""
        assert isinstance(self, pyabf.ABF)
        if (self.sweepChannel >= len(self.holdingCommand)):
            return None
        epochTable = pyabf.waveform.EpochTable(self, self.sweepChannel)
        sweepWaveform = epochTable.epochWaveformsBySweep[self.sweepNumber]
        sweepD = sweepWaveform.getDigitalWaveform(digOutNumber)
        return sweepD

    @property
    def sweepTimesSec(self):
        """Numpy array of sweep start times (in seconds)"""
        return np.arange(self.sweepCount)*self.sweepIntervalSec

    @property
    def sweepTimesMin(self):
        """Numpy array of sweep start times (in minutes)"""
        return self.sweepTimesSec/60

    @property
    def sweepDerivative(self):
        """First derivative of sweepY (delta units / second)"""
        ddt = np.diff(self.sweepY)
        ddt = np.append(ddt, [ddt[-1]])
        ddt *= self.dataRate
        return ddt

    @property
    def fileGUID(self):
        return self._fileGUID

    @property
    def md5(self):
        """MD5 hash string of the whole ABF file."""
        if not hasattr(self, "_md5"):
            with open(self.abfFilePath, 'rb') as f:
                hasher = hashlib.md5(f.read())
                self._md5 = hasher.hexdigest().upper()
        return self._md5

    @property
    def fileUUID(self):
        """Create a unique ABF file ID using the MD5 of the whole file."""
        uuid = list(self.md5)
        for index in [8, 13, 18, 23]:
            uuid.insert(index, "-")
        return "".join(uuid)

    @property
    def sampleRate(self):
        """Sample rate (Hz) for each channel"""
        return self.dataRate

    def getAllYs(self, channelIndex: int = 0) -> np.ndarray:
        """Return data from all sweeps for the specified channel."""
        return self.data[channelIndex]

    def getAllXs(self, channelIndex: int = 0) -> np.ndarray:
        """Return times from all sweeps for the specified channel."""
        return np.arange(len(self.data[channelIndex]))/self.sampleRate
