"""
Code here directly reads data Axon Binary Format (ABF) Files.
This module is part of the pyABF project by Scott W Harden
https://github.com/swharden/pyABF/
"""

import struct
import os
import glob
import io
import numpy as np
np.set_printoptions(suppress=True)

class HeaderReader:
    """
    Reads header values from ABF1 and ABF2 files.
    """

    def __init__(self, abfFileBuffer, seekTo=False):

        # ensure the ABF is an open binary file buffer
        assert isinstance(abfFileBuffer, io.BufferedReader)
        assert abfFileBuffer.mode == 'rb'
        self.fb = abfFileBuffer
        self.readValues(seekTo)

    def readStruct(self, structFormat, seek=False):

        # optionally go to a specific byte location
        if seek:
            self.fb.seek(seek)

        # read the value(s) into a list
        varSize = struct.calcsize(structFormat)
        byteString = self.fb.read(varSize)
        vals = struct.unpack(structFormat, byteString)
        vals = list(vals)

        # convert bytestrings to regular strings
        for i in range(len(vals)):
            if type(vals[i]) == type(b''):
                vals[i] = vals[i].decode("ascii", errors='ignore')

        # Don 't return a list unless we need to
        if len(vals) == 1:
            vals = vals[0]

        return vals

    def showThings(self):
        varNames = [x for x in dir(self) if not x.startswith("_")]
        for excludedVar in ['fb']:
            if excludedVar in varNames:
                varNames.remove(excludedVar)
        for varName in varNames:
            thing = getattr(self, varName)
            if "method" in str(type(thing)):
                continue
            print("%s.%s = %s" % (self.__class__.__name__, varName, thing))


class ABF1header(HeaderReader):
    """
    In ABF1 files, the same values are always at the same byte locations.
    Most of these variables are the same as those in the ProtocolSection 
    of ABF2 files.
    """

    def readValues(self, seekTo):
        self.fb.seek(0)
        self.fFileSignature = self.readStruct("4s")
        self.fb.seek(4)
        self.fFileVersionNumber = self.readStruct("f")
        self.fb.seek(8)
        self.nOperationMode = self.readStruct("h")
        self.fb.seek(10)
        self.lActualAcqLength = self.readStruct("i")
        self.fb.seek(14)
        self.nNumPointsIgnored = self.readStruct("h")
        self.fb.seek(16)
        self.lActualEpisodes = self.readStruct("i")
        self.fb.seek(24)
        self.lFileStartTime = self.readStruct("i")
        self.fb.seek(40)
        self.lDataSectionPtr = self.readStruct("i")
        self.fb.seek(44)
        self.lTagSectionPtr = self.readStruct("i")
        self.fb.seek(48)
        self.lNumTagEntries = self.readStruct("i")
        self.fb.seek(92)
        self.lSynchArrayPtr = self.readStruct("i")
        self.fb.seek(96)
        self.lSynchArraySize = self.readStruct("i")
        self.fb.seek(100)
        self.nDataFormat = self.readStruct("h")
        self.fb.seek(120)
        self.nADCNumChannels = self.readStruct("h")
        self.fb.seek(122)
        self.fADCSampleInterval = self.readStruct("f")
        self.fb.seek(130)
        self.fSynchTimeUnit = self.readStruct("f")
        self.fb.seek(138)
        self.lNumSamplesPerEpisode = self.readStruct("i")
        self.fb.seek(142)
        self.lPreTriggerSamples = self.readStruct("i")
        self.fb.seek(146)
        self.lEpisodesPerRun = self.readStruct("i")
        self.fb.seek(244)
        self.fADCRange = self.readStruct("f")
        self.fb.seek(252)
        self.lADCResolution = self.readStruct("i")
        self.fb.seek(366)
        self.nFileStartMillisecs = self.readStruct("h")
        self.fb.seek(378)
        self.nADCPtoLChannelMap = self.readStruct("16h")
        self.fb.seek(410)
        self.nADCSamplingSeq = self.readStruct("16h")
        self.fb.seek(442)
        self.sADCChannelName = self.readStruct(
            "10s10s10s10s10s10s10s10s10s10s10s10s10s10s10s10s")
        self.fb.seek(602)
        self.sADCUnits = self.readStruct("8s8s8s8s8s8s8s8s8s8s8s8s8s8s8s8s")
        self.fb.seek(730)
        self.fADCProgrammableGain = self.readStruct("16f")
        self.fb.seek(922)
        self.fInstrumentScaleFactor = self.readStruct("16f")
        self.fb.seek(986)
        self.fInstrumentOffset = self.readStruct("16f")
        self.fb.seek(1050)
        self.fSignalGain = self.readStruct("16f")
        self.fb.seek(1114)
        self.fSignalOffset = self.readStruct("16f")
        self.fb.seek(1436)
        self.nDigitalEnable = self.readStruct("h")
        self.fb.seek(1440)
        self.nActiveDACChannel = self.readStruct("h")
        self.fb.seek(1584)
        self.nDigitalHolding = self.readStruct("h")
        self.fb.seek(1586)
        self.nDigitalInterEpisode = self.readStruct("h")
        self.fb.seek(2588)
        self.nDigitalValue = self.readStruct("10h")
        self.fb.seek(2048)
        self.lDACFilePtr = self.readStruct("2i")
        self.fb.seek(2056)
        self.lDACFileNumEpisodes = self.readStruct("2i")
        self.fb.seek(2074)
        self.fDACCalibrationFactor = self.readStruct("4f")
        self.fb.seek(2090)
        self.fDACCalibrationOffset = self.readStruct("4f")
        self.fb.seek(2296)
        self.nWaveformEnable = self.readStruct("2h")
        self.fb.seek(2300)
        self.nWaveformSource = self.readStruct("2h")
        self.fb.seek(2304)
        self.nInterEpisodeLevel = self.readStruct("2h")
        self.fb.seek(2308)
        self.nEpochType = self.readStruct("20h")
        self.fb.seek(2348)
        self.fEpochInitLevel = self.readStruct("20f")
        self.fb.seek(2428)
        self.fEpochLevelInc = self.readStruct("20f")
        self.fb.seek(2508)
        self.lEpochInitDuration = self.readStruct("20i")
        self.fb.seek(2588)
        self.lEpochDurationInc = self.readStruct("20i")
        self.fb.seek(4512)
        self.nTelegraphEnable = self.readStruct("16h")
        self.fb.seek(4576)
        self.fTelegraphAdditGain = self.readStruct("16f")
        self.fb.seek(4898)
        self.sProtocolPath = self.readStruct("384s")


class AbfHeader(HeaderReader):
    def readValues(self, seekTo):
        self.fb.seek(seekTo)
        self.fFileSignature = self.readStruct("4s")
        self.fFileVersionNumber = self.readStruct("4b")
        self.uFileInfoSize = self.readStruct("I")
        self.lActualEpisodes = self.readStruct("I")
        self.uFileStartDate = self.readStruct("I")
        self.uFileStartTimeMS = self.readStruct("I")
        self.uStopwatchTime = self.readStruct("I")
        self.nFileType = self.readStruct("H")
        self.nDataFormat = self.readStruct("H")
        self.nSimultaneousScan = self.readStruct("H")
        self.nCRCEnable = self.readStruct("H")
        self.uFileCRC = self.readStruct("I")
        self.FileGUID = self.readStruct("I")
        self.unknown1 = self.readStruct("I")
        self.unknown2 = self.readStruct("I")
        self.unknown3 = self.readStruct("I")
        self.uCreatorVersion = self.readStruct("I")
        self.uCreatorNameIndex = self.readStruct("I")
        self.uModifierVersion = self.readStruct("I")
        self.uModifierNameIndex = self.readStruct("I")
        self.uProtocolPathIndex = self.readStruct("I")


class SectionMap(HeaderReader):
    def readValues(self, seekTo):
        """
        In ABF2 files, header data for each section is at specific byte locations
        which can be looked up according to the map generated by this class.
        The 3 numbers are the block number (1 block = 512 bytes), entry size (bytes),
        and entry count of the item.
        """
        self.fb.seek(seekTo)
        self.ProtocolSection = self.readStruct("IIl", 76)
        self.ADCSection = self.readStruct("IIl", 92)
        self.DACSection = self.readStruct("IIl", 108)
        self.EpochSection = self.readStruct("IIl", 124)
        self.ADCPerDACSection = self.readStruct("IIl", 140)
        self.EpochPerDACSection = self.readStruct("IIl", 156)
        self.UserListSection = self.readStruct("IIl", 172)
        self.StatsRegionSection = self.readStruct("IIl", 188)
        self.MathSection = self.readStruct("IIl", 204)
        self.StringsSection = self.readStruct("IIl", 220)
        self.DataSection = self.readStruct("IIl", 236)
        self.TagSection = self.readStruct("IIl", 252)
        self.ScopeSection = self.readStruct("IIl", 268)
        self.DeltaSection = self.readStruct("IIl", 284)
        self.VoiceTagSection = self.readStruct("IIl", 300)
        self.SynchArraySection = self.readStruct("IIl", 316)
        self.AnnotationSection = self.readStruct("IIl", 332)
        self.StatsSection = self.readStruct("IIl", 348)


class SectionProtocol(HeaderReader):
    def readValues(self, seekTo):
        self.fb.seek(seekTo)
        self.nOperationMode = self.readStruct("h")
        self.fADCSequenceInterval = self.readStruct("f")
        self.bEnableFileCompression = self.readStruct("b")
        self.sUnused = self.readStruct("3s")
        self.uFileCompressionRatio = self.readStruct("I")
        self.fSynchTimeUnit = self.readStruct("f")
        self.fSecondsPerRun = self.readStruct("f")
        self.lNumSamplesPerEpisode = self.readStruct("i")
        self.lPreTriggerSamples = self.readStruct("i")
        self.lEpisodesPerRun = self.readStruct("i")
        self.lRunsPerTrial = self.readStruct("i")
        self.lNumberOfTrials = self.readStruct("i")
        self.nAveragingMode = self.readStruct("h")
        self.nUndoRunCount = self.readStruct("h")
        self.nFirstEpisodeInRun = self.readStruct("h")
        self.fTriggerThreshold = self.readStruct("f")
        self.nTriggerSource = self.readStruct("h")
        self.nTriggerAction = self.readStruct("h")
        self.nTriggerPolarity = self.readStruct("h")
        self.fScopeOutputInterval = self.readStruct("f")
        self.fEpisodeStartToStart = self.readStruct("f")
        self.fRunStartToStart = self.readStruct("f")
        self.lAverageCount = self.readStruct("i")
        self.fTrialStartToStart = self.readStruct("f")
        self.nAutoTriggerStrategy = self.readStruct("h")
        self.fFirstRunDelayS = self.readStruct("f")
        self.nChannelStatsStrategy = self.readStruct("h")
        self.lSamplesPerTrace = self.readStruct("i")
        self.lStartDisplayNum = self.readStruct("i")
        self.lFinishDisplayNum = self.readStruct("i")
        self.nShowPNRawData = self.readStruct("h")
        self.fStatisticsPeriod = self.readStruct("f")
        self.lStatisticsMeasurements = self.readStruct("i")
        self.nStatisticsSaveStrategy = self.readStruct("h")
        self.fADCRange = self.readStruct("f")
        self.fDACRange = self.readStruct("f")
        self.lADCResolution = self.readStruct("i")
        self.lDACResolution = self.readStruct("i")
        self.nExperimentType = self.readStruct("h")
        self.nManualInfoStrategy = self.readStruct("h")
        self.nCommentsEnable = self.readStruct("h")
        self.lFileCommentIndex = self.readStruct("i")
        self.nAutoAnalyseEnable = self.readStruct("h")
        self.nSignalType = self.readStruct("h")
        self.nDigitalEnable = self.readStruct("h")
        self.nActiveDACChannel = self.readStruct("h")
        self.nDigitalHolding = self.readStruct("h")
        self.nDigitalInterEpisode = self.readStruct("h")
        self.nDigitalDACChannel = self.readStruct("h")
        self.nDigitalTrainActiveLogic = self.readStruct("h")
        self.nStatsEnable = self.readStruct("h")
        self.nStatisticsClearStrategy = self.readStruct("h")
        self.nLevelHysteresis = self.readStruct("h")
        self.lTimeHysteresis = self.readStruct("i")
        self.nAllowExternalTags = self.readStruct("h")
        self.nAverageAlgorithm = self.readStruct("h")
        self.fAverageWeighting = self.readStruct("f")
        self.nUndoPromptStrategy = self.readStruct("h")
        self.nTrialTriggerSource = self.readStruct("h")
        self.nStatisticsDisplayStrategy = self.readStruct("h")
        self.nExternalTagType = self.readStruct("h")
        self.nScopeTriggerOut = self.readStruct("h")
        self.nLTPType = self.readStruct("h")
        self.nAlternateDACOutputState = self.readStruct("h")
        self.nAlternateDigitalOutputState = self.readStruct("h")
        self.fCellID = self.readStruct("3f")
        self.nDigitizerADCs = self.readStruct("h")
        self.nDigitizerDACs = self.readStruct("h")
        self.nDigitizerTotalDigitalOuts = self.readStruct("h")
        self.nDigitizerSynchDigitalOuts = self.readStruct("h")
        self.nDigitizerType = self.readStruct("h")


class SectionReader(HeaderReader):
    def __init__(self, abfFileBuffer, sectionMap):

        # ensure the ABF is an open binary file buffer
        assert isinstance(abfFileBuffer, io.BufferedReader)
        assert abfFileBuffer.mode == 'rb'
        self.fb = abfFileBuffer
        self.readValues(sectionMap)

    def readValues(self, sectionMap):
        self.clearValues()
        blockStart, entrySize, entryCount = sectionMap
        for entryNumber in range(entryCount):
            self.fb.seek(blockStart*512+entrySize*entryNumber)
            self.appendValues(sectionMap)


class SectionADC(SectionReader):
    def clearValues(self):
        self.nADCNum = []
        self.nTelegraphEnable = []
        self.nTelegraphInstrument = []
        self.fTelegraphAdditGain = []
        self.fTelegraphFilter = []
        self.fTelegraphMembraneCap = []
        self.nTelegraphMode = []
        self.fTelegraphAccessResistance = []
        self.nADCPtoLChannelMap = []
        self.nADCSamplingSeq = []
        self.fADCProgrammableGain = []
        self.fADCDisplayAmplification = []
        self.fADCDisplayOffset = []
        self.fInstrumentScaleFactor = []
        self.fInstrumentOffset = []
        self.fSignalGain = []
        self.fSignalOffset = []
        self.fSignalLowpassFilter = []
        self.fSignalHighpassFilter = []
        self.nLowpassFilterType = []
        self.nHighpassFilterType = []
        self.fPostProcessLowpassFilter = []
        self.nPostProcessLowpassFilterType = []
        self.bEnabledDuringPN = []
        self.nStatsChannelPolarity = []
        self.lADCChannelNameIndex = []
        self.lADCUnitsIndex = []

    def appendValues(self, sectionMap):
        self.nADCNum.append(self.readStruct("h"))
        self.nTelegraphEnable.append(self.readStruct("h"))
        self.nTelegraphInstrument.append(self.readStruct("h"))
        self.fTelegraphAdditGain.append(self.readStruct("f"))
        self.fTelegraphFilter.append(self.readStruct("f"))
        self.fTelegraphMembraneCap.append(self.readStruct("f"))
        self.nTelegraphMode.append(self.readStruct("h"))
        self.fTelegraphAccessResistance.append(self.readStruct("f"))
        self.nADCPtoLChannelMap.append(self.readStruct("h"))
        self.nADCSamplingSeq.append(self.readStruct("h"))
        self.fADCProgrammableGain.append(self.readStruct("f"))
        self.fADCDisplayAmplification.append(self.readStruct("f"))
        self.fADCDisplayOffset.append(self.readStruct("f"))
        self.fInstrumentScaleFactor.append(self.readStruct("f"))
        self.fInstrumentOffset.append(self.readStruct("f"))
        self.fSignalGain.append(self.readStruct("f"))
        self.fSignalOffset.append(self.readStruct("f"))
        self.fSignalLowpassFilter.append(self.readStruct("f"))
        self.fSignalHighpassFilter.append(self.readStruct("f"))
        self.nLowpassFilterType.append(self.readStruct("b"))
        self.nHighpassFilterType.append(self.readStruct("b"))
        self.fPostProcessLowpassFilter.append(self.readStruct("f"))
        self.nPostProcessLowpassFilterType.append(self.readStruct("c"))
        self.bEnabledDuringPN.append(self.readStruct("b"))
        self.nStatsChannelPolarity.append(self.readStruct("h"))
        self.lADCChannelNameIndex.append(self.readStruct("i"))
        self.lADCUnitsIndex.append(self.readStruct("i"))


class SectionDAC(SectionReader):
    def clearValues(self):
        self.nDACNum = []
        self.nTelegraphDACScaleFactorEnable = []
        self.fInstrumentHoldingLevel = []
        self.fDACScaleFactor = []
        self.fDACHoldingLevel = []
        self.fDACCalibrationFactor = []
        self.fDACCalibrationOffset = []
        self.lDACChannelNameIndex = []
        self.lDACChannelUnitsIndex = []
        self.lDACFilePtr = []
        self.lDACFileNumEpisodes = []
        self.nWaveformEnable = []
        self.nWaveformSource = []
        self.nInterEpisodeLevel = []
        self.fDACFileScale = []
        self.fDACFileOffset = []
        self.lDACFileEpisodeNum = []
        self.nDACFileADCNum = []
        self.nConditEnable = []
        self.lConditNumPulses = []
        self.fBaselineDuration = []
        self.fBaselineLevel = []
        self.fStepDuration = []
        self.fStepLevel = []
        self.fPostTrainPeriod = []
        self.fPostTrainLevel = []
        self.nMembTestEnable = []
        self.nLeakSubtractType = []
        self.nPNPolarity = []
        self.fPNHoldingLevel = []
        self.nPNNumADCChannels = []
        self.nPNPosition = []
        self.nPNNumPulses = []
        self.fPNSettlingTime = []
        self.fPNInterpulse = []
        self.nLTPUsageOfDAC = []
        self.nLTPPresynapticPulses = []
        self.lDACFilePathIndex = []
        self.fMembTestPreSettlingTimeMS = []
        self.fMembTestPostSettlingTimeMS = []
        self.nLeakSubtractADCIndex = []

    def appendValues(self, sectionMap):
        self.nDACNum.append(self.readStruct("h"))
        self.nTelegraphDACScaleFactorEnable.append(self.readStruct("h"))
        self.fInstrumentHoldingLevel.append(self.readStruct("f"))
        self.fDACScaleFactor.append(self.readStruct("f"))
        self.fDACHoldingLevel.append(self.readStruct("f"))
        self.fDACCalibrationFactor.append(self.readStruct("f"))
        self.fDACCalibrationOffset.append(self.readStruct("f"))
        self.lDACChannelNameIndex.append(self.readStruct("i"))
        self.lDACChannelUnitsIndex.append(self.readStruct("i"))
        self.lDACFilePtr.append(self.readStruct("i"))
        self.lDACFileNumEpisodes.append(self.readStruct("i"))
        self.nWaveformEnable.append(self.readStruct("h"))
        self.nWaveformSource.append(self.readStruct("h"))
        self.nInterEpisodeLevel.append(self.readStruct("h"))
        self.fDACFileScale.append(self.readStruct("f"))
        self.fDACFileOffset.append(self.readStruct("f"))
        self.lDACFileEpisodeNum.append(self.readStruct("i"))
        self.nDACFileADCNum.append(self.readStruct("h"))
        self.nConditEnable.append(self.readStruct("h"))
        self.lConditNumPulses.append(self.readStruct("i"))
        self.fBaselineDuration.append(self.readStruct("f"))
        self.fBaselineLevel.append(self.readStruct("f"))
        self.fStepDuration.append(self.readStruct("f"))
        self.fStepLevel.append(self.readStruct("f"))
        self.fPostTrainPeriod.append(self.readStruct("f"))
        self.fPostTrainLevel.append(self.readStruct("f"))
        self.nMembTestEnable.append(self.readStruct("h"))
        self.nLeakSubtractType.append(self.readStruct("h"))
        self.nPNPolarity.append(self.readStruct("h"))
        self.fPNHoldingLevel.append(self.readStruct("f"))
        self.nPNNumADCChannels.append(self.readStruct("h"))
        self.nPNPosition.append(self.readStruct("h"))
        self.nPNNumPulses.append(self.readStruct("h"))
        self.fPNSettlingTime.append(self.readStruct("f"))
        self.fPNInterpulse.append(self.readStruct("f"))
        self.nLTPUsageOfDAC.append(self.readStruct("h"))
        self.nLTPPresynapticPulses.append(self.readStruct("h"))
        self.lDACFilePathIndex.append(self.readStruct("i"))
        self.fMembTestPreSettlingTimeMS.append(self.readStruct("f"))
        self.fMembTestPostSettlingTimeMS.append(self.readStruct("f"))
        self.nLeakSubtractADCIndex.append(self.readStruct("h"))


class SectionEpoch(SectionReader):
    def clearValues(self):
        self.nEpochNum = []
        self.nEpochDigitalOutput = []

    def appendValues(self, sectionMap):
        self.nEpochNum.append(self.readStruct("h"))
        self.nEpochDigitalOutput.append(self.readStruct("h"))


class SectionEpochPerDac(SectionReader):
    def clearValues(self):
        self.nEpochNum = []
        self.nDACNum = []
        self.nEpochType = []
        self.fEpochInitLevel = []
        self.fEpochLevelInc = []
        self.lEpochInitDuration = []
        self.lEpochDurationInc = []
        self.lEpochPulsePeriod = []
        self.lEpochPulseWidth = []

    def appendValues(self, sectionMap):
        self.nEpochNum.append(self.readStruct("h"))
        self.nDACNum.append(self.readStruct("h"))
        self.nEpochType.append(self.readStruct("h"))
        self.fEpochInitLevel.append(self.readStruct("f"))
        self.fEpochLevelInc.append(self.readStruct("f"))
        self.lEpochInitDuration.append(self.readStruct("i"))
        self.lEpochDurationInc.append(self.readStruct("i"))
        self.lEpochPulsePeriod.append(self.readStruct("i"))
        self.lEpochPulseWidth.append(self.readStruct("i"))


class SectionTag(SectionReader):
    def clearValues(self):
        self.lTagTime = []
        self.sComment = []
        self.nTagType = []
        self.nVoiceTagNumberorAnnotationIndex = []

    def appendValues(self, sectionMap):
        self.lTagTime.append(self.readStruct("i"))
        self.sComment.append(self.readStruct("56s"))
        self.nTagType.append(self.readStruct("h"))
        self.nVoiceTagNumberorAnnotationIndex.append(self.readStruct("h"))


class SectionStrings(SectionReader):
    def clearValues(self):
        self.strings = []

    def appendValues(self, sectionMap):
        entrySize = sectionMap[1]
        code = "%ds" % entrySize
        self.strings.append(self.readStruct(code))

