from pyabf.abfReader import AbfReader
import datetime
import os  # TODO: replace with pathutil


class HeaderV1(AbfReader):
    """
    The first several bytes of an ABF1 file contain variables
    located at specific byte positions from the start of the file.
    All ABF1 header values are read in this single block.
    Arrays which reference ADC entries are shown as read, no physical <-> logical
    channel mapping and interpretation of the sampling sequence is done.
    """

    def __init__(self, fb):
        AbfReader.__init__(self, fb)

        # GROUP 1 - File ID and size information. (40 bytes)
        self.lFileSignature = self.readStruct("i", 0)
        self.fFileVersionNumber = self.readStruct("f", 4)
        self.nOperationMode = self.readStruct("h", 8)
        self.lActualAcqLength = self.readStruct("i", 10)
        self.nNumPointsIgnored = self.readStruct("h", 14)
        self.lActualEpisodes = self.readStruct("i", 16)
        self.lFileStartDate = self.readStruct("i", 20)
        self.lFileStartTime = self.readStruct("i", 24)
        self.lStopwatchTime = self.readStruct("i", 28)
        self.fHeaderVersionNumber = self.readStruct("f", 32)
        self.nFileType = self.readStruct("h", 36)
        self.nMSBinFormat = self.readStruct("h", 38)

        # GROUP 2 - File Structure (78 bytes)
        self.lDataSectionPtr = self.readStruct("i", 40)
        self.lTagSectionPtr = self.readStruct("i", 44)
        self.lNumTagEntries = self.readStruct("i", 48)

        # missing entries

        self.lSynchArrayPtr = self.readStruct("i", 92)
        self.lSynchArraySize = self.readStruct("i", 96)
        self.nDataFormat = self.readStruct("h", 100)

        # missing entries

        # GROUP 3 - Trial hierarchy information (82 bytes)
        self.nADCNumChannels = self.readStruct("h", 120)
        self.fADCSampleInterval = self.readStruct("f", 122)
        # missing entries
        self.fSynchTimeUnit = self.readStruct("f", 130)
        # missing entries
        self.lNumSamplesPerEpisode = self.readStruct("i", 138)
        self.lPreTriggerSamples = self.readStruct("i", 142)
        self.lEpisodesPerRun = self.readStruct("i", 146)
        # missing entries

        # GROUP 4 - Display Parameters (44 bytes)
        # missing entries

        # GROUP 5 - Hardware information (16 bytes)
        self.fADCRange = self.readStruct("f", 244)
        self.fDACRange = self.readStruct("f", 248)
        self.lADCResolution = self.readStruct("i", 252)
        self.lDACResolution = self.readStruct("i", 256)

        # GROUP 6 - Environmental Information (118 bytes)
        self.nExperimentType = self.readStruct("h", 260)
        # missing entries
        self.sCreatorInfo = self.readStruct("16s", 294)
        self.sFileCommentOld = self.readStruct("56s", 310)
        self.nFileStartMillisecs = self.readStruct("h", 366)
        # missing entries

        # GROUP 7 - Multi-channel information (1044 bytes)
        self.nADCPtoLChannelMap = self.readStruct("16h", 378)
        self.nADCSamplingSeq = self.readStruct("16h", 410)
        self.sADCChannelName = self.readStruct("10s"*16, 442)
        self.sADCUnits = self.readStruct("8s"*16, 602)
        self.fADCProgrammableGain = self.readStruct("16f", 730)
        # missing entries
        self.fInstrumentScaleFactor = self.readStruct("16f", 922)
        self.fInstrumentOffset = self.readStruct("16f", 986)
        self.fSignalGain = self.readStruct("16f", 1050)
        self.fSignalOffset = self.readStruct("16f", 1114)
        self.sDACChannelName = self.readStruct("10s"*4, 1306)
        self.sDACChannelUnit = self.readStruct("8s"*4, 1346)
        # missing entries

        # GROUP 8 - Synchronous timer outputs (14 bytes)
        # missing entries
        # GROUP 9 - Epoch Waveform and Pulses (184 bytes)
        self.nDigitalEnable = self.readStruct("h", 1436)
        # missing entries
        self.nActiveDACChannel = self.readStruct("h", 1440)
        # missing entries
        self.nDigitalHolding = self.readStruct("h", 1584)
        self.nDigitalInterEpisode = self.readStruct("h", 1586)
        # missing entries
        self.nDigitalValue = self.readStruct("10h", 1588)

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
        self.lDACFilePtr = self.readStruct("2i", 2048)
        self.lDACFileNumEpisodes = self.readStruct("2i", 2056)
        # EXTENDED GROUP 3 - Trial Hierarchy
        # missing entries
        # EXTENDED GROUP 7 - Multi-channel information (62 bytes)
        self.fDACCalibrationFactor = self.readStruct("4f", 2074)
        self.fDACCalibrationOffset = self.readStruct("4f", 2090)

        # GROUP 17 - Trains parameters (160 bytes)
        # missing entries
        # EXTENDED GROUP 9 - Epoch Waveform and Pulses (412 bytes)
        self.nWaveformEnable = self.readStruct("2h", 2296)
        self.nWaveformSource = self.readStruct("2h", 2300)
        self.nInterEpisodeLevel = self.readStruct("2h", 2304)
        self.nEpochType = self.readStruct("20h", 2308)
        self.fEpochInitLevel = self.readStruct("20f", 2348)
        self.fEpochLevelInc = self.readStruct("20f", 2428)
        self.lEpochInitDuration = self.readStruct("20i", 2508)
        self.lEpochDurationInc = self.readStruct("20i", 2588)
        # missing entries

        # EXTENDED GROUP 10 - DAC Output File (552 bytes)
        self.fDACFileScale = self.readStruct("2f", 2708)
        self.fDACFileOffset = self.readStruct("2f", 2716)
        self.lDACFileEpisodeNum = self.readStruct("2i", 2724)
        self.nDACFileADCNum = self.readStruct("2h", 2732)
        self.sDACFilePath = self.readStruct("256s"*2, 2736)
        # EXTENDED GROUP 11 - Presweep (conditioning) pulse train (100 bytes)
        # missing entries
        # EXTENDED GROUP 12 - Variable parameter user list (1096 bytes)
        if self.fFileVersionNumber > 1.6:
            self.nULEnable = self.readStruct("4i", 3360)
            self.nULParamToVary = self.readStruct("4i", 3360)
            self.sULParamValueList = self.readStruct("1024s", 3360)
            self.nULRepeat = self.readStruct("1024s", 4400)
        else:
            self.nULEnable = []
            self.nULParamToVary = []
            self.sULParamValueList = []
            self.nULRepeat = []
        # EXTENDED GROUP 15 - On-line subtraction (56 bytes)
        # missing entries
        # EXTENDED GROUP 6 Environmental Information  (898 bytes)
        self.nTelegraphEnable = self.readStruct("16h", 4512)
        self.nTelegraphInstrument = self.readStruct("16h", 4544)
        self.fTelegraphAdditGain = self.readStruct("16f", 4576)
        self.fTelegraphFilter = self.readStruct("16f", 4640)
        self.fTelegraphMembraneCap = self.readStruct("16f", 4704)
        self.nTelegraphMode = self.readStruct("16h", 4768)
        self.nTelegraphDACScaleFactorEnable = self.readStruct("4h", 4800)
        # missing entries
        self.sProtocolPath = self.readStruct("256s", 4898)
        self.sFileCommentNew = self.readStruct("128s", 5154)
        self.fInstrumentHoldingLevel = self.readStruct("4f", 5298)
        self.ulFileCRC = self.readStruct("I", 5314)
        # missing entries
        self.nCreatorMajorVersion = self.readStruct("h", 5798)
        self.nCreatorMinorVersion = self.readStruct("h", 5800)
        self.nCreatorBugfixVersion = self.readStruct("h", 5802)
        self.nCreatorBuildVersion = self.readStruct("h", 5804)

        # EXTENDED GROUP 13 - Statistics measurements (388 bytes)
        # missing entries
        # GROUP 18 - Application version data (16 bytes)
        self.uFileGUID = self.readStruct("16B", 5282)
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
            self.abfDateTime = timeStamp
            self.abfDateTimeString = timeStamp.strftime('%Y-%m-%dT%H:%M:%S.%f')
        else:
            try:
                startTime = self.lFileStartTime
                startDate = str(self.lFileStartDate)
                startDate = datetime.datetime.strptime(startDate, "%Y%m%d")
                timeStamp = startDate + datetime.timedelta(seconds=startTime)
                timeStamp += datetime.timedelta(
                    milliseconds=self.nFileStartMillisecs)
                self.abfDateTime = timeStamp
                self.abfDateTimeString = timeStamp.strftime(
                    '%Y-%m-%dT%H:%M:%S.%f')
                self.abfDateTimeString = self.abfDateTimeString[:-3]
            except:
                self.abfDateTime = datetime.datetime(1, 1, 1)
                self.abfDateTimeString = "ERROR"

        # read tags into memory
        self.lTagTime = [None]*self.lNumTagEntries
        self.sTagComment = [None]*self.lNumTagEntries
        self.nTagType = [None]*self.lNumTagEntries
        for i in range(self.lNumTagEntries):
            fb.seek(self.lTagSectionPtr*512 + i * 64)
            self.lTagTime[i] = self.readStruct("i")
            self.sTagComment[i] = self.readStruct("56s")
            self.nTagType[i] = self.readStruct("h")
