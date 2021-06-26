from pyabf.abfReader import readStruct
from pyabf.abfHeader import DATETIME_FORMAT
from pyabf.abfHeader import BLOCKSIZE
import datetime
import os  # TODO: replace with pathutil


class HeaderV1:
    """
    The first several bytes of an ABF1 file contain variables
    located at specific byte positions from the start of the file.
    All ABF1 header values are read in this single block.
    Arrays which reference ADC entries are shown as read, no physical <-> logical
    channel mapping and interpretation of the sampling sequence is done.
    """

    def __init__(self, fb):
        # GROUP 1 - File ID and size information. (40 bytes)
        self.lFileSignature = readStruct(fb, "i", 0)
        self.fFileVersionNumber = readStruct(fb, "f", 4)
        self.nOperationMode = readStruct(fb, "h", 8)
        self.lActualAcqLength = readStruct(fb, "i", 10)
        self.nNumPointsIgnored = readStruct(fb, "h", 14)
        self.lActualEpisodes = readStruct(fb, "i", 16)
        self.lFileStartDate = readStruct(fb, "i", 20)
        self.lFileStartTime = readStruct(fb, "i", 24)
        self.lStopwatchTime = readStruct(fb, "i", 28)
        self.fHeaderVersionNumber = readStruct(fb, "f", 32)
        self.nFileType = readStruct(fb, "h", 36)
        self.nMSBinFormat = readStruct(fb, "h", 38)

        # GROUP 2 - File Structure (78 bytes)
        self.lDataSectionPtr = readStruct(fb, "i", 40)
        self.lTagSectionPtr = readStruct(fb, "i", 44)
        self.lNumTagEntries = readStruct(fb, "i", 48)

        # missing entries

        self.lSynchArrayPtr = readStruct(fb, "i", 92)
        self.lSynchArraySize = readStruct(fb, "i", 96)
        self.nDataFormat = readStruct(fb, "h", 100)

        # missing entries

        # GROUP 3 - Trial hierarchy information (82 bytes)
        self.nADCNumChannels = readStruct(fb, "h", 120)
        self.fADCSampleInterval = readStruct(fb, "f", 122)
        # missing entries
        self.fSynchTimeUnit = readStruct(fb, "f", 130)
        # missing entries
        self.lNumSamplesPerEpisode = readStruct(fb, "i", 138)
        self.lPreTriggerSamples = readStruct(fb, "i", 142)
        self.lEpisodesPerRun = readStruct(fb, "i", 146)
        # missing entries

        # GROUP 4 - Display Parameters (44 bytes)
        # missing entries

        # GROUP 5 - Hardware information (16 bytes)
        self.fADCRange = readStruct(fb, "f", 244)
        self.fDACRange = readStruct(fb, "f", 248)
        self.lADCResolution = readStruct(fb, "i", 252)
        self.lDACResolution = readStruct(fb, "i", 256)

        # GROUP 6 - Environmental Information (118 bytes)
        self.nExperimentType = readStruct(fb, "h", 260)
        # missing entries
        self.sCreatorInfo = readStruct(fb, "16s", 294)
        self.sFileCommentOld = readStruct(fb, "56s", 310)
        self.nFileStartMillisecs = readStruct(fb, "h", 366)
        # missing entries

        # GROUP 7 - Multi-channel information (1044 bytes)
        self.nADCPtoLChannelMap = readStruct(fb, "16h", 378)
        self.nADCSamplingSeq = readStruct(fb, "16h", 410)
        self.sADCChannelName = readStruct(fb, "10s"*16, 442)
        self.sADCUnits = readStruct(fb, "8s"*16, 602)
        self.fADCProgrammableGain = readStruct(fb, "16f", 730)
        # missing entries
        self.fInstrumentScaleFactor = readStruct(fb, "16f", 922)
        self.fInstrumentOffset = readStruct(fb, "16f", 986)
        self.fSignalGain = readStruct(fb, "16f", 1050)
        self.fSignalOffset = readStruct(fb, "16f", 1114)
        self.sDACChannelName = readStruct(fb, "10s"*4, 1306)
        self.sDACChannelUnit = readStruct(fb, "8s"*4, 1346)
        # missing entries

        # GROUP 8 - Synchronous timer outputs (14 bytes)
        # missing entries
        # GROUP 9 - Epoch Waveform and Pulses (184 bytes)
        self.nDigitalEnable = readStruct(fb, "h", 1436)
        # missing entries
        self.nActiveDACChannel = readStruct(fb, "h", 1440)
        # missing entries
        self.nDigitalHolding = readStruct(fb, "h", 1584)
        self.nDigitalInterEpisode = readStruct(fb, "h", 1586)
        # missing entries
        self.nDigitalValue = readStruct(fb, "10h", 1588)

        # GROUP 10 - DAC Output File (98 bytes)
        # missing entries
        # GROUP 11 - Presweep (conditioning) pulse train (44 bytes)
        # missing entries
        # GROUP 13 - Autopeak measurement (36 bytes)
        # missing entries
        # GROUP 14 - Channel Arithmetic (52 bytes)
        # missing entries
        # GROUP 15 - On-line subtraction (34 bytes)
        # missing entries
        # GROUP 16 - Miscellaneous variables (82 bytes)
        # missing entries
        # EXTENDED GROUP 2 - File Structure (16 bytes)
        self.lDACFilePtr = readStruct(fb, "2i", 2048)
        self.lDACFileNumEpisodes = readStruct(fb, "2i", 2056)
        # EXTENDED GROUP 3 - Trial Hierarchy
        # missing entries
        # EXTENDED GROUP 7 - Multi-channel information (62 bytes)
        self.fDACCalibrationFactor = readStruct(fb, "4f", 2074)
        self.fDACCalibrationOffset = readStruct(fb, "4f", 2090)

        # GROUP 17 - Trains parameters (160 bytes)
        # missing entries
        # EXTENDED GROUP 9 - Epoch Waveform and Pulses (412 bytes)
        self.nWaveformEnable = readStruct(fb, "2h", 2296)
        self.nWaveformSource = readStruct(fb, "2h", 2300)
        self.nInterEpisodeLevel = readStruct(fb, "2h", 2304)
        self.nEpochType = readStruct(fb, "20h", 2308)
        self.fEpochInitLevel = readStruct(fb, "20f", 2348)
        self.fEpochLevelInc = readStruct(fb, "20f", 2428)
        self.lEpochInitDuration = readStruct(fb, "20i", 2508)
        self.lEpochDurationInc = readStruct(fb, "20i", 2588)
        # missing entries

        # EXTENDED GROUP 10 - DAC Output File (552 bytes)
        self.fDACFileScale = readStruct(fb, "2f", 2708)
        self.fDACFileOffset = readStruct(fb, "2f", 2716)
        self.lDACFileEpisodeNum = readStruct(fb, "2i", 2724)
        self.nDACFileADCNum = readStruct(fb, "2h", 2732)
        self.sDACFilePath = readStruct(fb, "256s"*2, 2736)
        # EXTENDED GROUP 11 - Presweep (conditioning) pulse train (100 bytes)
        # missing entries
        # EXTENDED GROUP 12 - Variable parameter user list (1096 bytes)
        if self.fFileVersionNumber > 1.6:
            self.nULEnable = readStruct(fb, "4i", 3360)
            self.nULParamToVary = readStruct(fb, "4i", 3360)
            self.sULParamValueList = readStruct(fb, "1024s", 3360)
            self.nULRepeat = readStruct(fb, "1024s", 4400)
        else:
            self.nULEnable = []
            self.nULParamToVary = []
            self.sULParamValueList = []
            self.nULRepeat = []
        # EXTENDED GROUP 15 - On-line subtraction (56 bytes)
        # missing entries
        # EXTENDED GROUP 6 Environmental Information  (898 bytes)
        self.nTelegraphEnable = readStruct(fb, "16h", 4512)
        self.nTelegraphInstrument = readStruct(fb, "16h", 4544)
        self.fTelegraphAdditGain = readStruct(fb, "16f", 4576)
        self.fTelegraphFilter = readStruct(fb, "16f", 4640)
        self.fTelegraphMembraneCap = readStruct(fb, "16f", 4704)
        self.nTelegraphMode = readStruct(fb, "16h", 4768)
        self.nTelegraphDACScaleFactorEnable = readStruct(fb, "4h", 4800)
        # missing entries
        self.sProtocolPath = readStruct(fb, "256s", 4898)
        self.sFileCommentNew = readStruct(fb, "128s", 5154)
        self.fInstrumentHoldingLevel = readStruct(fb, "4f", 5298)
        self.ulFileCRC = readStruct(fb, "I", 5314)
        # missing entries
        self.nCreatorMajorVersion = readStruct(fb, "h", 5798)
        self.nCreatorMinorVersion = readStruct(fb, "h", 5800)
        self.nCreatorBugfixVersion = readStruct(fb, "h", 5802)
        self.nCreatorBuildVersion = readStruct(fb, "h", 5804)

        # EXTENDED GROUP 13 - Statistics measurements (388 bytes)
        # missing entries
        # GROUP 18 - Application version data (16 bytes)
        self.uFileGUID = readStruct(fb, "16B", 5282)
        # missing entries
        # GROUP 19 - LTP protocol (14 bytes)
        # missing entries
        # GROUP 20 - Digidata 132x Trigger out flag. (8 bytes)
        # missing entries
        # GROUP 21 - Epoch resistance (56 bytes) // TODO old value of 40 correct??
        # missing entries
        # GROUP 22 - Alternating episodic mode (58 bytes)
        # missing entries
        # GROUP 23 - Post-processing actions (210 bytes)
        # missing entries

        # format version number
        versionParts = list(str(int(self.fFileVersionNumber*1000)))
        versionPartsInt = [int(x) for x in versionParts]
        self.abfVersionString = ".".join(versionParts)
        self.abfVersionFloat = int("".join(versionParts))/1000.0
        self.abfVersionDict = {}
        self.abfVersionDict["major"] = versionPartsInt[0]
        self.abfVersionDict["minor"] = versionPartsInt[1]
        self.abfVersionDict["bugfix"] = versionPartsInt[2]
        self.abfVersionDict["build"] = versionPartsInt[3]

        # format creator version
        self.creatorVersionDict = {}
        self.creatorVersionDict["major"] = self.nCreatorMajorVersion
        self.creatorVersionDict["minor"] = self.nCreatorMinorVersion
        self.creatorVersionDict["bugfix"] = self.nCreatorBugfixVersion
        self.creatorVersionDict["build"] = self.nCreatorBuildVersion
        self.creatorVersionString = "%d.%d.%d.%d" % (self.creatorVersionDict["major"],
                                                     self.creatorVersionDict["minor"],
                                                     self.creatorVersionDict["bugfix"],
                                                     self.creatorVersionDict["build"])

        # format GUID
        guid = []
        for i in [3, 2, 1, 0, 5, 4, 7, 6, 8, 9, 10, 11, 12, 13, 14, 15]:
            guid.append("%.2X" % (self.uFileGUID[i]))
        for i in [4, 7, 10, 13]:
            guid.insert(i, "-")
        self.sFileGUID = "".join(guid)

        # format creation date
        if (self.lFileStartDate == 0):
            # if the value stored in the header is zero, it means this is a
            # very old ABF file which does not store creation date.
            # For files like this use the file creation date.
            self.abfDateTime = round(os.path.getctime(fb.name))
            timeStamp = datetime.datetime.fromtimestamp(self.abfDateTime)
        else:
            startTime = self.lFileStartTime
            startDate = str(self.lFileStartDate)
            try:
                startDate = datetime.datetime.strptime(startDate, "%Y%m%d")
            except:
                startDate = datetime.datetime.fromtimestamp(0)
            timeStamp = startDate + datetime.timedelta(seconds=startTime)
            timeStamp += datetime.timedelta(
                milliseconds=self.nFileStartMillisecs)

        self.abfDateTime = timeStamp
        try:
            self.abfDateTimeString = self.abfDateTime.strftime(DATETIME_FORMAT)
            self.abfDateTimeString = self.abfDateTimeString[:-3]
        except:
            self.abfDateTimeString = "ERROR"

        # read tags into memory
        self.lTagTime = [None]*self.lNumTagEntries
        self.sTagComment = [None]*self.lNumTagEntries
        self.nTagType = [None]*self.lNumTagEntries
        for i in range(self.lNumTagEntries):
            fb.seek(self.lTagSectionPtr*BLOCKSIZE + i * 64)
            self.lTagTime[i] = readStruct(fb, "i")
            self.sTagComment[i] = readStruct(fb, "56s")
            self.nTagType[i] = readStruct(fb, "h")
