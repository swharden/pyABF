"""
Code here relates to extraction of values from ABF1 and ABF2 file headers.
A purist interested in replicating (or porting) core functionality of ABF
reading code may desire to start here. Only standard libraries are used.
Variable names were chosen to be consistent with common names found in header
files released with the official SDK.

Code here is limited to the looking-up of data from the ABF header and its
gentle messaging to improve readability. Code related to analysis or dividing
data into sweeps does not belong in this file. 
"""

import io
import os
import struct
import logging
import datetime
logging.basicConfig(level=logging.WARNING)
log = logging.getLogger(__name__)

BLOCKSIZE = 512

DIGITIZERS = {
    0: "Unknown",
    1: "Demo",
    2: "MiniDigi",
    3: "DD132X",
    4: "OPUS",
    5: "PATCH",
    6: "Digidata 1440",
    7: "MINIDIGI2",
    8: "Digidata 1550"
}

TELEGRAPHS = {
    0: "Unknown instrument (manual or user defined telegraph table).",
    1: "Axopatch-1 with CV-4-1/100",
    2: "Axopatch-1 with CV-4-0.1/100",
    3: "Axopatch-1B(inv.) CV-4-1/100",
    4: "Axopatch-1B(inv) CV-4-0.1/100",
    5: "Axopatch 200 with CV 201",
    6: "Axopatch 200 with CV 202",
    7: "GeneClamp",
    8: "Dagan 3900",
    9: "Dagan 3900A",
    10: "Dagan CA-1  Im=0.1",
    11: "Dagan CA-1  Im=1.0",
    12: "Dagan CA-1  Im=10",
    13: "Warner OC-725",
    14: "Warner OC-725",
    15: "Axopatch 200B",
    16: "Dagan PC-ONE  Im=0.1",
    17: "Dagan PC-ONE  Im=1.0",
    18: "Dagan PC-ONE  Im=10",
    19: "Dagan PC-ONE  Im=100",
    20: "Warner BC-525C",
    21: "Warner PC-505",
    22: "Warner PC-501",
    23: "Dagan CA-1  Im=0.05",
    24: "MultiClamp 700",
    25: "Turbo Tec",
    26: "OpusXpress 6000A",
    27: "Axoclamp 900"
}

DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'


def abfFileFormat(fb):
    """
    This function returns 1 or 2 if the ABF file is v1 or v2.    
    This function returns False if the file is not an ABF file.

    The first few characters of an ABF file tell you its format.
    Storage of this variable is superior to reading the ABF header because
    the file format is required before a version can even be extracted.
    """
    fb.seek(0)
    code = fb.read(4)
    code = code.decode("ascii", errors='ignore')
    if code == "ABF ":
        return 1
    elif code == "ABF2":
        return 2
    else:
        return False


def readStruct(fb, structFormat, seek=False, cleanStrings=True):
    """
    Return a structured value in an ABF file as a Python object.
    If cleanStrings is enabled, ascii-safe strings are returned.
    """

    if seek:
        fb.seek(seek)

    varSize = struct.calcsize(structFormat)
    byteString = fb.read(varSize)
    vals = struct.unpack(structFormat, byteString)
    vals = list(vals)

    if cleanStrings:
        for i in range(len(vals)):
            if type(vals[i]) == type(b''):
                vals[i] = vals[i].decode("ascii", errors='ignore').strip()

    if len(vals) == 1:
        vals = vals[0]

    return vals


class HeaderV1:
    """
    The first several bytes of an ABF1 file contain variables
    located at specific byte positions from the start of the file.
    All ABF1 header values are read in this single block.
    """

    def __init__(self, fb):
        self.fFileSignature = readStruct(fb, "4s", 0)
        self.fFileVersionNumber = readStruct(fb, "f", 4)
        self.nOperationMode = readStruct(fb, "h", 8)
        self.lActualAcqLength = readStruct(fb, "i", 10)
        self.nNumPointsIgnored = readStruct(fb, "h", 14)
        self.lActualEpisodes = readStruct(fb, "i", 16)
        self.lFileStartDate = readStruct(fb, "i", 20)
        self.lFileStartTime = readStruct(fb, "i", 24)
        self.lDataSectionPtr = readStruct(fb, "i", 40)
        self.lTagSectionPtr = readStruct(fb, "i", 44)
        self.lNumTagEntries = readStruct(fb, "i", 48)
        self.lSynchArrayPtr = readStruct(fb, "i", 92)
        self.lSynchArraySize = readStruct(fb, "i", 96)
        self.nDataFormat = readStruct(fb, "h", 100)
        self.nADCNumChannels = readStruct(fb, "h", 120)
        self.fADCSampleInterval = readStruct(fb, "f", 122)
        self.fSynchTimeUnit = readStruct(fb, "f", 130)
        self.lNumSamplesPerEpisode = readStruct(fb, "i", 138)
        self.lPreTriggerSamples = readStruct(fb, "i", 142)
        self.lEpisodesPerRun = readStruct(fb, "i", 146)
        self.fADCRange = readStruct(fb, "f", 244)
        self.lADCResolution = readStruct(fb, "i", 252)
        self.nFileStartMillisecs = readStruct(fb, "h", 366)
        self.nADCPtoLChannelMap = readStruct(fb, "16h", 378)
        self.nADCSamplingSeq = readStruct(fb, "16h", 410)
        self.sADCChannelName = readStruct(fb, "10s"*16, 442)
        self.sADCUnits = readStruct(fb, "8s"*16, 602)
        self.fADCProgrammableGain = readStruct(fb, "16f", 730)
        self.fInstrumentScaleFactor = readStruct(fb, "16f", 922)
        self.fInstrumentOffset = readStruct(fb, "16f", 986)
        self.fSignalGain = readStruct(fb, "16f", 1050)
        self.fSignalOffset = readStruct(fb, "16f", 1114)
        self.nDigitalEnable = readStruct(fb, "h", 1436)
        self.nActiveDACChannel = readStruct(fb, "h", 1440)
        self.nDigitalHolding = readStruct(fb, "h", 1584)
        self.nDigitalInterEpisode = readStruct(fb, "h", 1586)
        self.nDigitalValue = readStruct(fb, "10h", 2588)
        self.lDACFilePtr = readStruct(fb, "2i", 2048)
        self.lDACFileNumEpisodes = readStruct(fb, "2i", 2056)
        self.fDACCalibrationFactor = readStruct(fb, "4f", 2074)
        self.fDACCalibrationOffset = readStruct(fb, "4f", 2090)
        self.nWaveformEnable = readStruct(fb, "2h", 2296)
        self.nWaveformSource = readStruct(fb, "2h", 2300)
        self.nInterEpisodeLevel = readStruct(fb, "2h", 2304)
        self.nEpochType = readStruct(fb, "20h", 2308)
        self.fEpochInitLevel = readStruct(fb, "20f", 2348)
        self.fEpochLevelInc = readStruct(fb, "20f", 2428)
        self.lEpochInitDuration = readStruct(fb, "20i", 2508)
        self.lEpochDurationInc = readStruct(fb, "20i", 2588)
        self.nTelegraphEnable = readStruct(fb, "16h", 4512)
        self.fTelegraphAdditGain = readStruct(fb, "16f", 4576)
        self.sProtocolPath = readStruct(fb, "384s", 4898)

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
        self.creatorVersionDict["major"] = 0
        self.creatorVersionDict["minor"] = 0
        self.creatorVersionDict["bugfix"] = 0
        self.creatorVersionDict["build"] = 0
        self.creatorVersionString = '0.0.0.0'

        # format creation date from values found in the header
        startTime = self.lFileStartTime
        startDate = str(self.lFileStartDate)
        startDate = datetime.datetime.strptime(startDate, "%Y%m%d")
        timeStamp = startDate + datetime.timedelta(seconds=startTime)
        self.abfDateTime = timeStamp
        self.abfDateTimeString = self.abfDateTime.strftime(DATETIME_FORMAT)
        self.abfDateTimeString = self.abfDateTimeString[:-3]

        # read tags into memory
        self.lTagTime = [None]*self.lNumTagEntries
        self.sComment = [None]*self.lNumTagEntries
        self.nTagType = [None]*self.lNumTagEntries
        for i in range(self.lNumTagEntries):
            fb.seek(self.lTagSectionPtr*BLOCKSIZE + i * 64)
            self.lTagTime[i] = readStruct(fb, "i")
            self.sComment[i] = readStruct(fb, "56s")
            self.nTagType[i] = readStruct(fb, "h")


class HeaderV2:
    """
    The first several bytes of an ABF2 file contain variables
    located at specific byte positions from the start of the file.
    """

    def __init__(self, fb):
        fb.seek(0)
        self.fFileSignature = readStruct(fb, "4s")  # 0
        self.fFileVersionNumber = readStruct(fb, "4b")  # 4
        self.uFileInfoSize = readStruct(fb, "I")  # 8
        self.lActualEpisodes = readStruct(fb, "I")  # 12
        self.uFileStartDate = readStruct(fb, "I")  # 16
        self.uFileStartTimeMS = readStruct(fb, "I")  # 20
        self.uStopwatchTime = readStruct(fb, "I")  # 24
        self.nFileType = readStruct(fb, "H")  # 28
        self.nDataFormat = readStruct(fb, "H")  # 30
        self.nSimultaneousScan = readStruct(fb, "H")  # 32
        self.nCRCEnable = readStruct(fb, "H")  # 34
        self.uFileCRC = readStruct(fb, "I")  # 36
        self.uFileGUID = readStruct(fb, "16B")  # 40
        self.uCreatorVersion = readStruct(fb, "4B")  # 56
        self.uCreatorNameIndex = readStruct(fb, "I")  # 60
        self.uModifierVersion = readStruct(fb, "I")  # 64
        self.uModifierNameIndex = readStruct(fb, "I")  # 68
        self.uProtocolPathIndex = readStruct(fb, "I")  # 72

        # format version number
        versionPartsInt = self.fFileVersionNumber[::-1]
        versionParts = [str(x) for x in versionPartsInt]
        self.abfVersionString = ".".join(versionParts)
        self.abfVersionFloat = int("".join(versionParts))/1000.0
        self.abfVersionDict = {}
        self.abfVersionDict["major"] = versionPartsInt[0]
        self.abfVersionDict["minor"] = versionPartsInt[1]
        self.abfVersionDict["bugfix"] = versionPartsInt[2]
        self.abfVersionDict["build"] = versionPartsInt[3]

        # format creator version
        versionPartsInt = self.uCreatorVersion[::-1]
        versionParts = [str(x) for x in versionPartsInt]
        self.creatorVersionString = ".".join(versionParts)
        self.creatorVersionFloat = int("".join(versionParts))/1000.0
        self.creatorVersionDict = {}
        self.creatorVersionDict["major"] = versionPartsInt[0]
        self.creatorVersionDict["minor"] = versionPartsInt[1]
        self.creatorVersionDict["bugfix"] = versionPartsInt[2]
        self.creatorVersionDict["build"] = versionPartsInt[3]

        # format GUID
        guid = []
        for i in [3, 2, 1, 0, 5, 4, 7, 6, 8, 9, 10, 11, 12, 13, 15, 15]:
            guid.append("%.2X" % (self.uFileGUID[i]))
        for i in [4, 7, 10, 13]:
            guid.insert(i, "-")
        self.sFileGUID = "{%s}" % ("".join(guid))

        # format creation date from values found in the header
        startDate = str(self.uFileStartDate)
        startTime = self.uFileStartTimeMS / 1000
        startDate = datetime.datetime.strptime(startDate, "%Y%m%d")
        timeStamp = startDate + datetime.timedelta(seconds=startTime)
        self.abfDateTime = timeStamp
        self.abfDateTimeString = self.abfDateTime.strftime(DATETIME_FORMAT)
        self.abfDateTimeString = self.abfDateTimeString[:-3]


class SectionMap:
    """
    Reading three numbers (int, int, long) at specific byte locations
    yields the block position, byte size, and item count of specific
    data stored in sections. Note that a block is 512 bytes. Some of
    these sections are not read by this class because they are either
    not useful for my applications, typically unused, or have an
    unknown memory structure.
    """

    def __init__(self, fb):
        self.ProtocolSection = readStruct(fb, "IIi", 76)
        self.ADCSection = readStruct(fb, "IIi", 92)
        self.DACSection = readStruct(fb, "IIi", 108)
        self.EpochSection = readStruct(fb, "IIi", 124)
        self.ADCPerDACSection = readStruct(fb, "IIi", 140)
        self.EpochPerDACSection = readStruct(fb, "IIi", 156)
        self.UserListSection = readStruct(fb, "IIi", 172)
        self.StatsRegionSection = readStruct(fb, "IIi", 188)
        self.MathSection = readStruct(fb, "IIi", 204)
        self.StringsSection = readStruct(fb, "IIi", 220)
        self.DataSection = readStruct(fb, "IIi", 236)
        self.TagSection = readStruct(fb, "IIi", 252)
        self.ScopeSection = readStruct(fb, "IIi", 268)
        self.DeltaSection = readStruct(fb, "IIi", 284)
        self.VoiceTagSection = readStruct(fb, "IIi", 300)
        self.SynchArraySection = readStruct(fb, "IIi", 316)
        self.AnnotationSection = readStruct(fb, "IIi", 332)
        self.StatsSection = readStruct(fb, "IIi", 348)


class ProtocolSection:
    """
    This section contains information about the recording settings.
    This is useful for determining things like sample rate and
    channel scaling factors.
    """

    def __init__(self, fb, sectionMap):
        seekTo = sectionMap.ProtocolSection[0]*BLOCKSIZE
        fb.seek(seekTo)
        self.nOperationMode = readStruct(fb, "h")  # 0
        self.fADCSequenceInterval = readStruct(fb, "f")  # 2
        self.bEnableFileCompression = readStruct(fb, "b")  # 6
        self.sUnused = readStruct(fb, "3c")  # 7
        self.uFileCompressionRatio = readStruct(fb, "I")  # 10
        self.fSynchTimeUnit = readStruct(fb, "f")  # 14
        self.fSecondsPerRun = readStruct(fb, "f")  # 18
        self.lNumSamplesPerEpisode = readStruct(fb, "i")  # 22
        self.lPreTriggerSamples = readStruct(fb, "i")  # 26
        self.lEpisodesPerRun = readStruct(fb, "i")  # 30
        self.lRunsPerTrial = readStruct(fb, "i")  # 34
        self.lNumberOfTrials = readStruct(fb, "i")  # 38
        self.nAveragingMode = readStruct(fb, "h")  # 42
        self.nUndoRunCount = readStruct(fb, "h")  # 44
        self.nFirstEpisodeInRun = readStruct(fb, "h")  # 46
        self.fTriggerThreshold = readStruct(fb, "f")  # 48
        self.nTriggerSource = readStruct(fb, "h")  # 52
        self.nTriggerAction = readStruct(fb, "h")  # 54
        self.nTriggerPolarity = readStruct(fb, "h")  # 56
        self.fScopeOutputInterval = readStruct(fb, "f")  # 58
        self.fEpisodeStartToStart = readStruct(fb, "f")  # 62
        self.fRunStartToStart = readStruct(fb, "f")  # 66
        self.lAverageCount = readStruct(fb, "i")  # 70
        self.fTrialStartToStart = readStruct(fb, "f")  # 74
        self.nAutoTriggerStrategy = readStruct(fb, "h")  # 78
        self.fFirstRunDelayS = readStruct(fb, "f")  # 80
        self.nChannelStatsStrategy = readStruct(fb, "h")  # 84
        self.lSamplesPerTrace = readStruct(fb, "i")  # 86
        self.lStartDisplayNum = readStruct(fb, "i")  # 90
        self.lFinishDisplayNum = readStruct(fb, "i")  # 94
        self.nShowPNRawData = readStruct(fb, "h")  # 98
        self.fStatisticsPeriod = readStruct(fb, "f")  # 100
        self.lStatisticsMeasurements = readStruct(fb, "i")  # 104
        self.nStatisticsSaveStrategy = readStruct(fb, "h")  # 108
        self.fADCRange = readStruct(fb, "f")  # 110
        self.fDACRange = readStruct(fb, "f")  # 114
        self.lADCResolution = readStruct(fb, "i")  # 118
        self.lDACResolution = readStruct(fb, "i")  # 122
        self.nExperimentType = readStruct(fb, "h")  # 126
        self.nManualInfoStrategy = readStruct(fb, "h")  # 128
        self.nCommentsEnable = readStruct(fb, "h")  # 130
        self.lFileCommentIndex = readStruct(fb, "i")  # 132
        self.nAutoAnalyseEnable = readStruct(fb, "h")  # 136
        self.nSignalType = readStruct(fb, "h")  # 138
        self.nDigitalEnable = readStruct(fb, "h")  # 140
        self.nActiveDACChannel = readStruct(fb, "h")  # 142
        self.nDigitalHolding = readStruct(fb, "h")  # 144
        self.nDigitalInterEpisode = readStruct(fb, "h")  # 146
        self.nDigitalDACChannel = readStruct(fb, "h")  # 148
        self.nDigitalTrainActiveLogic = readStruct(fb, "h")  # 150
        self.nStatsEnable = readStruct(fb, "h")  # 152
        self.nStatisticsClearStrategy = readStruct(fb, "h")  # 154
        self.nLevelHysteresis = readStruct(fb, "h")  # 156
        self.lTimeHysteresis = readStruct(fb, "i")  # 158
        self.nAllowExternalTags = readStruct(fb, "h")  # 162
        self.nAverageAlgorithm = readStruct(fb, "h")  # 164
        self.fAverageWeighting = readStruct(fb, "f")  # 166
        self.nUndoPromptStrategy = readStruct(fb, "h")  # 170
        self.nTrialTriggerSource = readStruct(fb, "h")  # 172
        self.nStatisticsDisplayStrategy = readStruct(fb, "h")  # 174
        self.nExternalTagType = readStruct(fb, "h")  # 176
        self.nScopeTriggerOut = readStruct(fb, "h")  # 178
        self.nLTPType = readStruct(fb, "h")  # 180
        self.nAlternateDACOutputState = readStruct(fb, "h")  # 182
        self.nAlternateDigitalOutputState = readStruct(fb, "h")  # 184
        self.fCellID = readStruct(fb, "3f")  # 186
        self.nDigitizerADCs = readStruct(fb, "h")  # 198
        self.nDigitizerDACs = readStruct(fb, "h")  # 200
        self.nDigitizerTotalDigitalOuts = readStruct(fb, "h")  # 202
        self.nDigitizerSynchDigitalOuts = readStruct(fb, "h")  # 204
        self.nDigitizerType = readStruct(fb, "h")  # 206

        # additional useful information
        if self.nDigitizerType in DIGITIZERS.keys():
            self.sDigitizerType = DIGITIZERS[self.nDigitizerType]
        else:
            log.debug("nDigitizerType not in list of digitizers")
            self.sDigitizerType = DIGITIZERS[0]


class ADCSection:
    """
    Information about the ADC (what gets recorded).
    There is 1 item per ADC.
    """

    def __init__(self, fb, sectionMap):
        blockStart, entrySize, entryCount = sectionMap.ADCSection
        byteStart = blockStart*BLOCKSIZE

        self.nADCNum = [None]*entryCount
        self.nTelegraphEnable = [None]*entryCount
        self.nTelegraphInstrument = [None]*entryCount
        self.sTelegraphInstrument = [None]*entryCount
        self.fTelegraphAdditGain = [None]*entryCount
        self.fTelegraphFilter = [None]*entryCount
        self.fTelegraphMembraneCap = [None]*entryCount
        self.nTelegraphMode = [None]*entryCount
        self.fTelegraphAccessResistance = [None]*entryCount
        self.nADCPtoLChannelMap = [None]*entryCount
        self.nADCSamplingSeq = [None]*entryCount
        self.fADCProgrammableGain = [None]*entryCount
        self.fADCDisplayAmplification = [None]*entryCount
        self.fADCDisplayOffset = [None]*entryCount
        self.fInstrumentScaleFactor = [None]*entryCount
        self.fInstrumentOffset = [None]*entryCount
        self.fSignalGain = [None]*entryCount
        self.fSignalOffset = [None]*entryCount
        self.fSignalLowpassFilter = [None]*entryCount
        self.fSignalHighpassFilter = [None]*entryCount
        self.nLowpassFilterType = [None]*entryCount
        self.nHighpassFilterType = [None]*entryCount
        self.fPostProcessLowpassFilter = [None]*entryCount
        self.nPostProcessLowpassFilterType = [None]*entryCount
        self.bEnabledDuringPN = [None]*entryCount
        self.nStatsChannelPolarity = [None]*entryCount
        self.lADCChannelNameIndex = [None]*entryCount
        self.lADCUnitsIndex = [None]*entryCount

        for i in range(entryCount):
            fb.seek(byteStart + i*entrySize)
            self.nADCNum[i] = readStruct(fb, "h")  # 0
            self.nTelegraphEnable[i] = readStruct(fb, "h")  # 2
            self.nTelegraphInstrument[i] = readStruct(fb, "h")  # 4
            self.fTelegraphAdditGain[i] = readStruct(fb, "f")  # 6
            self.fTelegraphFilter[i] = readStruct(fb, "f")  # 10
            self.fTelegraphMembraneCap[i] = readStruct(fb, "f")  # 14
            self.nTelegraphMode[i] = readStruct(fb, "h")  # 18
            self.fTelegraphAccessResistance[i] = readStruct(fb, "f")  # 20
            self.nADCPtoLChannelMap[i] = readStruct(fb, "h")  # 24
            self.nADCSamplingSeq[i] = readStruct(fb, "h")  # 26
            self.fADCProgrammableGain[i] = readStruct(fb, "f")  # 28
            self.fADCDisplayAmplification[i] = readStruct(fb, "f")  # 32
            self.fADCDisplayOffset[i] = readStruct(fb, "f")  # 36
            self.fInstrumentScaleFactor[i] = readStruct(fb, "f")  # 40
            self.fInstrumentOffset[i] = readStruct(fb, "f")  # 44
            self.fSignalGain[i] = readStruct(fb, "f")  # 48
            self.fSignalOffset[i] = readStruct(fb, "f")  # 52
            self.fSignalLowpassFilter[i] = readStruct(fb, "f")  # 56
            self.fSignalHighpassFilter[i] = readStruct(fb, "f")  # 60
            self.nLowpassFilterType[i] = readStruct(fb, "b")  # 64
            self.nHighpassFilterType[i] = readStruct(fb, "b")  # 65
            self.fPostProcessLowpassFilter[i] = readStruct(fb, "f")  # 66
            self.nPostProcessLowpassFilterType[i] = readStruct(fb, "c")  # 70
            self.bEnabledDuringPN[i] = readStruct(fb, "b")  # 71
            self.nStatsChannelPolarity[i] = readStruct(fb, "h")  # 72
            self.lADCChannelNameIndex[i] = readStruct(fb, "i")  # 74
            self.lADCUnitsIndex[i] = readStruct(fb, "i")  # 78

            # useful information
            nTelegraphInstrument = self.nTelegraphInstrument[i]
            if nTelegraphInstrument in TELEGRAPHS.keys():
                self.sTelegraphInstrument[i] = TELEGRAPHS[nTelegraphInstrument]
            else:
                log.debug("nTelegraphInstrument not in list of telegraphs")
                self.sTelegraphInstrument[i] = TELEGRAPHS[0]


class DACSection:
    """
    Information about the DAC (what gets clamped).
    There is 1 item per DAC.
    """

    def __init__(self, fb, sectionMap):
        blockStart, entrySize, entryCount = sectionMap.DACSection
        byteStart = blockStart*BLOCKSIZE

        self.nDACNum = [None]*entryCount
        self.nTelegraphDACScaleFactorEnable = [None]*entryCount
        self.fInstrumentHoldingLevel = [None]*entryCount
        self.fDACScaleFactor = [None]*entryCount
        self.fDACHoldingLevel = [None]*entryCount
        self.fDACCalibrationFactor = [None]*entryCount
        self.fDACCalibrationOffset = [None]*entryCount
        self.lDACChannelNameIndex = [None]*entryCount
        self.lDACChannelUnitsIndex = [None]*entryCount
        self.lDACFilePtr = [None]*entryCount
        self.lDACFileNumEpisodes = [None]*entryCount
        self.nWaveformEnable = [None]*entryCount
        self.nWaveformSource = [None]*entryCount
        self.nInterEpisodeLevel = [None]*entryCount
        self.fDACFileScale = [None]*entryCount
        self.fDACFileOffset = [None]*entryCount
        self.lDACFileEpisodeNum = [None]*entryCount
        self.nDACFileADCNum = [None]*entryCount
        self.nConditEnable = [None]*entryCount
        self.lConditNumPulses = [None]*entryCount
        self.fBaselineDuration = [None]*entryCount
        self.fBaselineLevel = [None]*entryCount
        self.fStepDuration = [None]*entryCount
        self.fStepLevel = [None]*entryCount
        self.fPostTrainPeriod = [None]*entryCount
        self.fPostTrainLevel = [None]*entryCount
        self.nMembTestEnable = [None]*entryCount
        self.nLeakSubtractType = [None]*entryCount
        self.nPNPolarity = [None]*entryCount
        self.fPNHoldingLevel = [None]*entryCount
        self.nPNNumADCChannels = [None]*entryCount
        self.nPNPosition = [None]*entryCount
        self.nPNNumPulses = [None]*entryCount
        self.fPNSettlingTime = [None]*entryCount
        self.fPNInterpulse = [None]*entryCount
        self.nLTPUsageOfDAC = [None]*entryCount
        self.nLTPPresynapticPulses = [None]*entryCount
        self.lDACFilePathIndex = [None]*entryCount
        self.fMembTestPreSettlingTimeMS = [None]*entryCount
        self.fMembTestPostSettlingTimeMS = [None]*entryCount
        self.nLeakSubtractADCIndex = [None]*entryCount

        for i in range(entryCount):
            fb.seek(byteStart + i*entrySize)
            self.nDACNum[i] = readStruct(fb, "h")  # 0
            self.nTelegraphDACScaleFactorEnable[i] = readStruct(fb, "h")  # 2
            self.fInstrumentHoldingLevel[i] = readStruct(fb, "f")  # 4
            self.fDACScaleFactor[i] = readStruct(fb, "f")  # 8
            self.fDACHoldingLevel[i] = readStruct(fb, "f")  # 12
            self.fDACCalibrationFactor[i] = readStruct(fb, "f")  # 16
            self.fDACCalibrationOffset[i] = readStruct(fb, "f")  # 20
            self.lDACChannelNameIndex[i] = readStruct(fb, "i")  # 24
            self.lDACChannelUnitsIndex[i] = readStruct(fb, "i")  # 28
            self.lDACFilePtr[i] = readStruct(fb, "i")  # 32
            self.lDACFileNumEpisodes[i] = readStruct(fb, "i")  # 36
            self.nWaveformEnable[i] = readStruct(fb, "h")  # 40
            self.nWaveformSource[i] = readStruct(fb, "h")  # 42
            self.nInterEpisodeLevel[i] = readStruct(fb, "h")  # 44
            self.fDACFileScale[i] = readStruct(fb, "f")  # 46
            self.fDACFileOffset[i] = readStruct(fb, "f")  # 50
            self.lDACFileEpisodeNum[i] = readStruct(fb, "i")  # 54
            self.nDACFileADCNum[i] = readStruct(fb, "h")  # 58
            self.nConditEnable[i] = readStruct(fb, "h")  # 60
            self.lConditNumPulses[i] = readStruct(fb, "i")  # 62
            self.fBaselineDuration[i] = readStruct(fb, "f")  # 66
            self.fBaselineLevel[i] = readStruct(fb, "f")  # 70
            self.fStepDuration[i] = readStruct(fb, "f")  # 74
            self.fStepLevel[i] = readStruct(fb, "f")  # 78
            self.fPostTrainPeriod[i] = readStruct(fb, "f")  # 82
            self.fPostTrainLevel[i] = readStruct(fb, "f")  # 86
            self.nMembTestEnable[i] = readStruct(fb, "h")  # 90
            self.nLeakSubtractType[i] = readStruct(fb, "h")  # 92
            self.nPNPolarity[i] = readStruct(fb, "h")  # 94
            self.fPNHoldingLevel[i] = readStruct(fb, "f")  # 96
            self.nPNNumADCChannels[i] = readStruct(fb, "h")  # 100
            self.nPNPosition[i] = readStruct(fb, "h")  # 102
            self.nPNNumPulses[i] = readStruct(fb, "h")  # 104
            self.fPNSettlingTime[i] = readStruct(fb, "f")  # 106
            self.fPNInterpulse[i] = readStruct(fb, "f")  # 110
            self.nLTPUsageOfDAC[i] = readStruct(fb, "h")  # 114
            self.nLTPPresynapticPulses[i] = readStruct(fb, "h")  # 116
            self.lDACFilePathIndex[i] = readStruct(fb, "i")  # 118
            self.fMembTestPreSettlingTimeMS[i] = readStruct(fb, "f")  # 122
            self.fMembTestPostSettlingTimeMS[i] = readStruct(fb, "f")  # 126
            self.nLeakSubtractADCIndex[i] = readStruct(fb, "h")  # 130


class EpochPerDACSection:
    """
    This section contains waveform protocol information. These are most of
    the values set when using the epoch the waveform editor. Note that digital
    output signals are not stored here, but are in EpochSection.
    """

    def __init__(self, fb, sectionMap):
        blockStart, entrySize, entryCount = sectionMap.EpochPerDACSection
        byteStart = blockStart*BLOCKSIZE

        self.nEpochNum = [None]*entryCount
        self.nDACNum = [None]*entryCount
        self.nEpochType = [None]*entryCount
        self.fEpochInitLevel = [None]*entryCount
        self.fEpochLevelInc = [None]*entryCount
        self.lEpochInitDuration = [None]*entryCount
        self.lEpochDurationInc = [None]*entryCount
        self.lEpochPulsePeriod = [None]*entryCount
        self.lEpochPulseWidth = [None]*entryCount

        for i in range(entryCount):
            fb.seek(byteStart + i*entrySize)
            self.nEpochNum[i] = readStruct(fb, "h")  # 0
            self.nDACNum[i] = readStruct(fb, "h")  # 2
            self.nEpochType[i] = readStruct(fb, "h")  # 4
            self.fEpochInitLevel[i] = readStruct(fb, "f")  # 6
            self.fEpochLevelInc[i] = readStruct(fb, "f")  # 10
            self.lEpochInitDuration[i] = readStruct(fb, "i")  # 14
            self.lEpochDurationInc[i] = readStruct(fb, "i")  # 18
            self.lEpochPulsePeriod[i] = readStruct(fb, "i")  # 22
            self.lEpochPulseWidth[i] = readStruct(fb, "i")  # 26


class EpochSection:
    """
    This section contains the digital output signals for each epoch. This
    section has been overlooked by some previous open-source ABF-reading
    projects. Note that the digital output is a single byte, but represents
    8 bits corresponding to 8 outputs (7->0). When working with these bits,
    I convert it to a string like "10011101" for easy eyeballing.
    """

    def __init__(self, fb, sectionMap):
        blockStart, entrySize, entryCount = sectionMap.EpochSection
        byteStart = blockStart*BLOCKSIZE

        self.nEpochNum = [None]*entryCount
        self.nEpochDigitalOutput = [None]*entryCount

        for i in range(entryCount):
            fb.seek(byteStart + i*entrySize)
            self.nEpochNum[i] = readStruct(fb, "h")  # 0
            self.nEpochDigitalOutput[i] = readStruct(fb, "h")  # 2


class TagSection:
    """
    Tags are comments placed in ABF files during the recording. Physically
    they are located at the end of the file (after the data).

    Later we will populate the times and sweeps (human-understandable units)
    by multiplying the lTagTime by fSynchTimeUnit from the protocol section.
    """

    def __init__(self, fb, sectionMap):
        blockStart, entrySize, entryCount = sectionMap.TagSection
        byteStart = blockStart*BLOCKSIZE

        self.lTagTime = [None]*entryCount
        self.sComment = [None]*entryCount
        self.nTagType = [None]*entryCount
        self.nVoiceTagNumberorAnnotationIndex = [None]*entryCount

        self.timesSec = [None]*entryCount
        self.timesMin = [None]*entryCount
        self.sweeps = [None]*entryCount

        for i in range(entryCount):
            fb.seek(byteStart + i*entrySize)
            self.lTagTime[i] = readStruct(fb, "i")
            self.sComment[i] = readStruct(fb, "56s")
            self.nTagType[i] = readStruct(fb, "h")
            self.nVoiceTagNumberorAnnotationIndex[i] = readStruct(fb, "h")


class StringsSection:
    """
    Part of the ABF file contains long strings. Some of these can be broken
    apart into indexed strings.

    The first string is the only one which seems to contain useful information.
    This contains information like channel names, channel units, and abf
    protocol path and comments. The other strings are very large and I do not
    know what they do.

    Strings which contain indexed substrings are separated by \\x00 characters.
    """

    def __init__(self, fb, sectionMap):
        blockStart, entrySize, entryCount = sectionMap.StringsSection
        byteStart = blockStart*BLOCKSIZE
        self.strings = [None]*entryCount
        for i in range(entryCount):
            fb.seek(byteStart + i*entrySize)
            structFormat = "%ss" % entrySize
            self.strings[i] = readStruct(fb, structFormat, cleanStrings=False)


class StringsIndexed:
    """
    This object provides easy access to strings which are scattered around
    the header files. The StringsSection contains strings, but various headers
    contain values which point to a certain string index. This class connects
    the two, and provides direct access to those strings by their indexed name.
    """

    def __init__(self, headerV2, protocolSection, adcSection, dacSection, stringsSection):

        indexedStrings = stringsSection.strings[0]
        indexedStrings = indexedStrings[indexedStrings.rfind(b'\x00\x00'):]
        indexedStrings = indexedStrings.replace(b'\xb5', b"\x75")  # make mu u
        indexedStrings = indexedStrings.split(b'\x00')[1:]
        indexedStrings = [x.decode("ascii", errors='replace').strip()
                          for x in indexedStrings]

        # headerv2
        self.uCreatorName = indexedStrings[headerV2.uCreatorNameIndex]
        self.uModifierName = indexedStrings[headerV2.uModifierNameIndex]
        self.uProtocolPath = indexedStrings[headerV2.uProtocolPathIndex]

        # ProtocolSection
        self.lFileComment = indexedStrings[protocolSection.lFileCommentIndex]

        # ADCSection
        self.lADCChannelName = []
        self.lADCUnits = []
        for i in range(len(adcSection.lADCChannelNameIndex)):
            self.lADCChannelName.append(
                indexedStrings[adcSection.lADCChannelNameIndex[i]])
            self.lADCUnits.append(indexedStrings[adcSection.lADCUnitsIndex[i]])

        # DACSection
        self.lDACChannelName = []
        self.lDACChannelUnits = []
        self.lDACFilePath = []
        self.nLeakSubtractADC = []

        for i in range(len(dacSection.lDACChannelNameIndex)):
            self.lDACChannelName.append(
                indexedStrings[dacSection.lDACChannelNameIndex[i]])
            self.lDACChannelUnits.append(
                indexedStrings[dacSection.lDACChannelUnitsIndex[i]])
            self.lDACFilePath.append(
                indexedStrings[dacSection.lDACFilePathIndex[i]])
            self.nLeakSubtractADC.append(
                indexedStrings[dacSection.nLeakSubtractADCIndex[i]])
