"""
Code here relates to extraction of header values from ABF1 and ABF2 file headers.
"""

import io
import struct


def readStruct(fb, structFormat, seek=False, cleanStrings=True):
    """
    Return a structured value in an ABF file as a Python object.
    """

    if not isinstance(fb, io.BufferedReader):
        raise ValueError("require an ABF file open in 'fb' mode")

    if seek:
        fb.seek(seek)

    varSize = struct.calcsize(structFormat)
    byteString = fb.read(varSize)
    vals = struct.unpack(structFormat, byteString)
    vals = list(vals)

    if cleanStrings:
        for i in range(len(vals)):
            if type(vals[i]) == type(b''):
                vals[i] = vals[i].decode("ascii", errors='replace').strip()

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


class HeaderV2:
    """
    The first several bytes of an ABF2 file contain variables
    located at specific byte positions from the start of the file.
    """
    def __init__(self, fb):
        fb.seek(0)
        self.fFileSignature = readStruct(fb, "4s")
        self.fFileVersionNumber = readStruct(fb, "4b")
        self.uFileInfoSize = readStruct(fb, "I")
        self.lActualEpisodes = readStruct(fb, "I")
        self.uFileStartDate = readStruct(fb, "I")
        self.uFileStartTimeMS = readStruct(fb, "I")
        self.uStopwatchTime = readStruct(fb, "I")
        self.nFileType = readStruct(fb, "H")
        self.nDataFormat = readStruct(fb, "H")
        self.nSimultaneousScan = readStruct(fb, "H")
        self.nCRCEnable = readStruct(fb, "H")
        self.uFileCRC = readStruct(fb, "I")
        self.FileGUID = readStruct(fb, "I")
        self.unknown1 = readStruct(fb, "I")
        self.unknown2 = readStruct(fb, "I")
        self.unknown3 = readStruct(fb, "I")
        self.uCreatorVersion = readStruct(fb, "I")
        self.uCreatorNameIndex = readStruct(fb, "I")
        self.uModifierVersion = readStruct(fb, "I")
        self.uModifierNameIndex = readStruct(fb, "I")
        self.uProtocolPathIndex = readStruct(fb, "I")


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
        self.ProtocolSection = readStruct(fb, "IIl", 76)
        self.ADCSection = readStruct(fb, "IIl", 92)
        self.DACSection = readStruct(fb, "IIl", 108)
        self.EpochSection = readStruct(fb, "IIl", 124)
        self.ADCPerDACSection = readStruct(fb, "IIl", 140)
        self.EpochPerDACSection = readStruct(fb, "IIl", 156)
        self.UserListSection = readStruct(fb, "IIl", 172)
        self.StatsRegionSection = readStruct(fb, "IIl", 188)
        self.MathSection = readStruct(fb, "IIl", 204)
        self.StringsSection = readStruct(fb, "IIl", 220)
        self.DataSection = readStruct(fb, "IIl", 236)
        self.TagSection = readStruct(fb, "IIl", 252)
        self.ScopeSection = readStruct(fb, "IIl", 268)
        self.DeltaSection = readStruct(fb, "IIl", 284)
        self.VoiceTagSection = readStruct(fb, "IIl", 300)
        self.SynchArraySection = readStruct(fb, "IIl", 316)
        self.AnnotationSection = readStruct(fb, "IIl", 332)
        self.StatsSection = readStruct(fb, "IIl", 348)


class ProtocolSection:
    """
    This section contains information about the recording settings.
    This is useful for determining things like sample rate and
    channel scaling factors.
    """
    def __init__(self, fb, sectionMap):
        seekTo = sectionMap.ProtocolSection[0]*512
        fb.seek(seekTo)
        self.nOperationMode = readStruct(fb, "h")
        self.fADCSequenceInterval = readStruct(fb, "f")
        self.bEnableFileCompression = readStruct(fb, "b")
        self.sUnused = readStruct(fb, "3s")
        self.uFileCompressionRatio = readStruct(fb, "I")
        self.fSynchTimeUnit = readStruct(fb, "f")
        self.fSecondsPerRun = readStruct(fb, "f")
        self.lNumSamplesPerEpisode = readStruct(fb, "i")
        self.lPreTriggerSamples = readStruct(fb, "i")
        self.lEpisodesPerRun = readStruct(fb, "i")
        self.lRunsPerTrial = readStruct(fb, "i")
        self.lNumberOfTrials = readStruct(fb, "i")
        self.nAveragingMode = readStruct(fb, "h")
        self.nUndoRunCount = readStruct(fb, "h")
        self.nFirstEpisodeInRun = readStruct(fb, "h")
        self.fTriggerThreshold = readStruct(fb, "f")
        self.nTriggerSource = readStruct(fb, "h")
        self.nTriggerAction = readStruct(fb, "h")
        self.nTriggerPolarity = readStruct(fb, "h")
        self.fScopeOutputInterval = readStruct(fb, "f")
        self.fEpisodeStartToStart = readStruct(fb, "f")
        self.fRunStartToStart = readStruct(fb, "f")
        self.lAverageCount = readStruct(fb, "i")
        self.fTrialStartToStart = readStruct(fb, "f")
        self.nAutoTriggerStrategy = readStruct(fb, "h")
        self.fFirstRunDelayS = readStruct(fb, "f")
        self.nChannelStatsStrategy = readStruct(fb, "h")
        self.lSamplesPerTrace = readStruct(fb, "i")
        self.lStartDisplayNum = readStruct(fb, "i")
        self.lFinishDisplayNum = readStruct(fb, "i")
        self.nShowPNRawData = readStruct(fb, "h")
        self.fStatisticsPeriod = readStruct(fb, "f")
        self.lStatisticsMeasurements = readStruct(fb, "i")
        self.nStatisticsSaveStrategy = readStruct(fb, "h")
        self.fADCRange = readStruct(fb, "f")
        self.fDACRange = readStruct(fb, "f")
        self.lADCResolution = readStruct(fb, "i")
        self.lDACResolution = readStruct(fb, "i")
        self.nExperimentType = readStruct(fb, "h")
        self.nManualInfoStrategy = readStruct(fb, "h")
        self.nCommentsEnable = readStruct(fb, "h")
        self.lFileCommentIndex = readStruct(fb, "i")
        self.nAutoAnalyseEnable = readStruct(fb, "h")
        self.nSignalType = readStruct(fb, "h")
        self.nDigitalEnable = readStruct(fb, "h")
        self.nActiveDACChannel = readStruct(fb, "h")
        self.nDigitalHolding = readStruct(fb, "h")
        self.nDigitalInterEpisode = readStruct(fb, "h")
        self.nDigitalDACChannel = readStruct(fb, "h")
        self.nDigitalTrainActiveLogic = readStruct(fb, "h")
        self.nStatsEnable = readStruct(fb, "h")
        self.nStatisticsClearStrategy = readStruct(fb, "h")
        self.nLevelHysteresis = readStruct(fb, "h")
        self.lTimeHysteresis = readStruct(fb, "i")
        self.nAllowExternalTags = readStruct(fb, "h")
        self.nAverageAlgorithm = readStruct(fb, "h")
        self.fAverageWeighting = readStruct(fb, "f")
        self.nUndoPromptStrategy = readStruct(fb, "h")
        self.nTrialTriggerSource = readStruct(fb, "h")
        self.nStatisticsDisplayStrategy = readStruct(fb, "h")
        self.nExternalTagType = readStruct(fb, "h")
        self.nScopeTriggerOut = readStruct(fb, "h")
        self.nLTPType = readStruct(fb, "h")
        self.nAlternateDACOutputState = readStruct(fb, "h")
        self.nAlternateDigitalOutputState = readStruct(fb, "h")
        self.fCellID = readStruct(fb, "3f")
        self.nDigitizerADCs = readStruct(fb, "h")
        self.nDigitizerDACs = readStruct(fb, "h")
        self.nDigitizerTotalDigitalOuts = readStruct(fb, "h")
        self.nDigitizerSynchDigitalOuts = readStruct(fb, "h")
        self.nDigitizerType = readStruct(fb, "h")


class ADCSection:
    """
    Information about the ADC (what gets recorded). 
    There is 1 item per ADC.
    """
    def __init__(self, fb, sectionMap):
        blockStart, entrySize, entryCount = sectionMap.ADCSection
        byteStart = blockStart*512

        self.nADCNum = [None]*entryCount
        self.nTelegraphEnable = [None]*entryCount
        self.nTelegraphInstrument = [None]*entryCount
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
            self.nADCNum[i] = readStruct(fb, "h")
            self.nTelegraphEnable[i] = readStruct(fb, "h")
            self.nTelegraphInstrument[i] = readStruct(fb, "h")
            self.fTelegraphAdditGain[i] = readStruct(fb, "f")
            self.fTelegraphFilter[i] = readStruct(fb, "f")
            self.fTelegraphMembraneCap[i] = readStruct(fb, "f")
            self.nTelegraphMode[i] = readStruct(fb, "h")
            self.fTelegraphAccessResistance[i] = readStruct(fb, "f")
            self.nADCPtoLChannelMap[i] = readStruct(fb, "h")
            self.nADCSamplingSeq[i] = readStruct(fb, "h")
            self.fADCProgrammableGain[i] = readStruct(fb, "f")
            self.fADCDisplayAmplification[i] = readStruct(fb, "f")
            self.fADCDisplayOffset[i] = readStruct(fb, "f")
            self.fInstrumentScaleFactor[i] = readStruct(fb, "f")
            self.fInstrumentOffset[i] = readStruct(fb, "f")
            self.fSignalGain[i] = readStruct(fb, "f")
            self.fSignalOffset[i] = readStruct(fb, "f")
            self.fSignalLowpassFilter[i] = readStruct(fb, "f")
            self.fSignalHighpassFilter[i] = readStruct(fb, "f")
            self.nLowpassFilterType[i] = readStruct(fb, "b")
            self.nHighpassFilterType[i] = readStruct(fb, "b")
            self.fPostProcessLowpassFilter[i] = readStruct(fb, "f")
            self.nPostProcessLowpassFilterType[i] = readStruct(fb, "c")
            self.bEnabledDuringPN[i] = readStruct(fb, "b")
            self.nStatsChannelPolarity[i] = readStruct(fb, "h")
            self.lADCChannelNameIndex[i] = readStruct(fb, "i")
            self.lADCUnitsIndex[i] = readStruct(fb, "i")


class DACSection:
    """
    Information about the DAC (what gets clamped). 
    There is 1 item per DAC.
    """
    def __init__(self, fb, sectionMap):
        blockStart, entrySize, entryCount = sectionMap.DACSection
        byteStart = blockStart*512

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
            self.nDACNum[i] = readStruct(fb, "h")
            self.nTelegraphDACScaleFactorEnable[i] = readStruct(fb, "h")
            self.fInstrumentHoldingLevel[i] = readStruct(fb, "f")
            self.fDACScaleFactor[i] = readStruct(fb, "f")
            self.fDACHoldingLevel[i] = readStruct(fb, "f")
            self.fDACCalibrationFactor[i] = readStruct(fb, "f")
            self.fDACCalibrationOffset[i] = readStruct(fb, "f")
            self.lDACChannelNameIndex[i] = readStruct(fb, "i")
            self.lDACChannelUnitsIndex[i] = readStruct(fb, "i")
            self.lDACFilePtr[i] = readStruct(fb, "i")
            self.lDACFileNumEpisodes[i] = readStruct(fb, "i")
            self.nWaveformEnable[i] = readStruct(fb, "h")
            self.nWaveformSource[i] = readStruct(fb, "h")
            self.nInterEpisodeLevel[i] = readStruct(fb, "h")
            self.fDACFileScale[i] = readStruct(fb, "f")
            self.fDACFileOffset[i] = readStruct(fb, "f")
            self.lDACFileEpisodeNum[i] = readStruct(fb, "i")
            self.nDACFileADCNum[i] = readStruct(fb, "h")
            self.nConditEnable[i] = readStruct(fb, "h")
            self.lConditNumPulses[i] = readStruct(fb, "i")
            self.fBaselineDuration[i] = readStruct(fb, "f")
            self.fBaselineLevel[i] = readStruct(fb, "f")
            self.fStepDuration[i] = readStruct(fb, "f")
            self.fStepLevel[i] = readStruct(fb, "f")
            self.fPostTrainPeriod[i] = readStruct(fb, "f")
            self.fPostTrainLevel[i] = readStruct(fb, "f")
            self.nMembTestEnable[i] = readStruct(fb, "h")
            self.nLeakSubtractType[i] = readStruct(fb, "h")
            self.nPNPolarity[i] = readStruct(fb, "h")
            self.fPNHoldingLevel[i] = readStruct(fb, "f")
            self.nPNNumADCChannels[i] = readStruct(fb, "h")
            self.nPNPosition[i] = readStruct(fb, "h")
            self.nPNNumPulses[i] = readStruct(fb, "h")
            self.fPNSettlingTime[i] = readStruct(fb, "f")
            self.fPNInterpulse[i] = readStruct(fb, "f")
            self.nLTPUsageOfDAC[i] = readStruct(fb, "h")
            self.nLTPPresynapticPulses[i] = readStruct(fb, "h")
            self.lDACFilePathIndex[i] = readStruct(fb, "i")
            self.fMembTestPreSettlingTimeMS[i] = readStruct(fb, "f")
            self.fMembTestPostSettlingTimeMS[i] = readStruct(fb, "f")
            self.nLeakSubtractADCIndex[i] = readStruct(fb, "h")


class EpochPerDACSection:
    """
    This section contains waveform protocol information. These are most of
    the values set when using the epoch the waveform editor. Note that digital
    output signals are not stored here, but are in EpochSection.
    """
    def __init__(self, fb, sectionMap):
        blockStart, entrySize, entryCount = sectionMap.EpochPerDACSection
        byteStart = blockStart*512

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
            self.nEpochNum[i] = readStruct(fb, "h")
            self.nDACNum[i] = readStruct(fb, "h")
            self.nEpochType[i] = readStruct(fb, "h")
            self.fEpochInitLevel[i] = readStruct(fb, "f")
            self.fEpochLevelInc[i] = readStruct(fb, "f")
            self.lEpochInitDuration[i] = readStruct(fb, "i")
            self.lEpochDurationInc[i] = readStruct(fb, "i")
            self.lEpochPulsePeriod[i] = readStruct(fb, "i")
            self.lEpochPulseWidth[i] = readStruct(fb, "i")


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
        byteStart = blockStart*512

        self.nEpochNum = [None]*entryCount
        self.nEpochDigitalOutput = [None]*entryCount

        for i in range(entryCount):
            fb.seek(byteStart + i*entrySize)
            self.nEpochNum[i] = readStruct(fb, "h")
            self.nEpochDigitalOutput[i] = readStruct(fb, "h")


class TagSection:
    """
    Tags are comments placed in ABF files during the recording. Physically
    they are located at the end of the file (after the data).

    Later we will populate the times and sweeps (human-understandable units)
    by multiplying the lTagTime by fSynchTimeUnit from the protocol section.
    """

    def __init__(self, fb, sectionMap):
        blockStart, entrySize, entryCount = sectionMap.TagSection
        byteStart = blockStart*512

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

    Strings which contain indexed substrings are separated by \x00 characters.
    """

    def __init__(self, fb, sectionMap):
        blockStart, entrySize, entryCount = sectionMap.StringsSection
        byteStart = blockStart*512
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
