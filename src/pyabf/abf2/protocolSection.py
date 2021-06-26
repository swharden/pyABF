from pyabf.abfReader import readStruct
from pyabf.abfHeader import BLOCKSIZE
from pyabf.abfHeader import DIGITIZERS


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
            self.sDigitizerType = DIGITIZERS[0]
