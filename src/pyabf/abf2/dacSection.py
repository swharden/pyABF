from pyabf.abfReader import readStruct

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
