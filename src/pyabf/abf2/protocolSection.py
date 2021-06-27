from pyabf.abf2.section import Section
from pyabf.names import getDigitizerName


class ProtocolSection(Section):
    """
    This section contains information about the recording settings.
    This is useful for determining things like sample rate and
    channel scaling factors.
    """

    def __init__(self, fb):
        Section.__init__(self, fb, 76)
        self.seek(self._byteStart)
        self.nOperationMode = self.readInt16()  # 0
        self.fADCSequenceInterval = self.readSingle()  # 2
        self.bEnableFileCompression = self.readByte()  # 6
        self._sUnused = self.readBytes(3)  # 7
        self.uFileCompressionRatio = self.readInt32()  # 10
        self.fSynchTimeUnit = self.readSingle()  # 14
        self.fSecondsPerRun = self.readSingle()  # 18
        self.lNumSamplesPerEpisode = self.readInt32()  # 22
        self.lPreTriggerSamples = self.readInt32()  # 26
        self.lEpisodesPerRun = self.readInt32()  # 30
        self.lRunsPerTrial = self.readInt32()  # 34
        self.lNumberOfTrials = self.readInt32()  # 38
        self.nAveragingMode = self.readInt16()  # 42
        self.nUndoRunCount = self.readInt16()  # 44
        self.nFirstEpisodeInRun = self.readInt16()  # 46
        self.fTriggerThreshold = self.readSingle()  # 48
        self.nTriggerSource = self.readInt16()  # 52
        self.nTriggerAction = self.readInt16()  # 54
        self.nTriggerPolarity = self.readInt16()  # 56
        self.fScopeOutputInterval = self.readSingle()  # 58
        self.fEpisodeStartToStart = self.readSingle()  # 62
        self.fRunStartToStart = self.readSingle()  # 66
        self.lAverageCount = self.readInt32()  # 70
        self.fTrialStartToStart = self.readSingle()  # 74
        self.nAutoTriggerStrategy = self.readInt16()  # 78
        self.fFirstRunDelayS = self.readSingle()  # 80
        self.nChannelStatsStrategy = self.readInt16()  # 84
        self.lSamplesPerTrace = self.readInt32()  # 86
        self.lStartDisplayNum = self.readInt32()  # 90
        self.lFinishDisplayNum = self.readInt32()  # 94
        self.nShowPNRawData = self.readInt16()  # 98
        self.fStatisticsPeriod = self.readSingle()  # 100
        self.lStatisticsMeasurements = self.readInt32()  # 104
        self.nStatisticsSaveStrategy = self.readInt16()  # 108
        self.fADCRange = self.readSingle()  # 110
        self.fDACRange = self.readSingle()  # 114
        self.lADCResolution = self.readInt32()  # 118
        self.lDACResolution = self.readInt32()  # 122
        self.nExperimentType = self.readInt16()  # 126
        self.nManualInfoStrategy = self.readInt16()  # 128
        self.nCommentsEnable = self.readInt16()  # 130
        self.lFileCommentIndex = self.readInt32()  # 132
        self.nAutoAnalyseEnable = self.readInt16()  # 136
        self.nSignalType = self.readInt16()  # 138
        self.nDigitalEnable = self.readInt16()  # 140
        self.nActiveDACChannel = self.readInt16()  # 142
        self.nDigitalHolding = self.readInt16()  # 144
        self.nDigitalInterEpisode = self.readInt16()  # 146
        self.nDigitalDACChannel = self.readInt16()  # 148
        self.nDigitalTrainActiveLogic = self.readInt16()  # 150
        self.nStatsEnable = self.readInt16()  # 152
        self.nStatisticsClearStrategy = self.readInt16()  # 154
        self.nLevelHysteresis = self.readInt16()  # 156
        self.lTimeHysteresis = self.readInt32()  # 158
        self.nAllowExternalTags = self.readInt16()  # 162
        self.nAverageAlgorithm = self.readInt16()  # 164
        self.fAverageWeighting = self.readSingle()  # 166
        self.nUndoPromptStrategy = self.readInt16()  # 170
        self.nTrialTriggerSource = self.readInt16()  # 172
        self.nStatisticsDisplayStrategy = self.readInt16()  # 174
        self.nExternalTagType = self.readInt16()  # 176
        self.nScopeTriggerOut = self.readInt16()  # 178
        self.nLTPType = self.readInt16()  # 180
        self.nAlternateDACOutputState = self.readInt16()  # 182
        self.nAlternateDigitalOutputState = self.readInt16()  # 184
        self.fCellID = self.readSingles(3)  # 186
        self.nDigitizerADCs = self.readInt16()  # 198
        self.nDigitizerDACs = self.readInt16()  # 200
        self.nDigitizerTotalDigitalOuts = self.readInt16()  # 202
        self.nDigitizerSynchDigitalOuts = self.readInt16()  # 204
        self.nDigitizerType = self.readInt16()  # 206
        self.sDigitizerType = getDigitizerName(self.nDigitizerType)
