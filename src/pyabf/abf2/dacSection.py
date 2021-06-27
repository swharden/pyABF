from pyabf.abf2.section import Section


class DACSection(Section):
    """
    Information about the DAC (what gets clamped).
    There is 1 item per DAC.
    """

    def __init__(self, fb):
        Section.__init__(self, fb, 108)

        self.nDACNum = [None]*self._entryCount
        self.nTelegraphDACScaleFactorEnable = [None]*self._entryCount
        self.fInstrumentHoldingLevel = [None]*self._entryCount
        self.fDACScaleFactor = [None]*self._entryCount
        self.fDACHoldingLevel = [None]*self._entryCount
        self.fDACCalibrationFactor = [None]*self._entryCount
        self.fDACCalibrationOffset = [None]*self._entryCount
        self.lDACChannelNameIndex = [None]*self._entryCount
        self.lDACChannelUnitsIndex = [None]*self._entryCount
        self.lDACFilePtr = [None]*self._entryCount
        self.lDACFileNumEpisodes = [None]*self._entryCount
        self.nWaveformEnable = [None]*self._entryCount
        self.nWaveformSource = [None]*self._entryCount
        self.nInterEpisodeLevel = [None]*self._entryCount
        self.fDACFileScale = [None]*self._entryCount
        self.fDACFileOffset = [None]*self._entryCount
        self.lDACFileEpisodeNum = [None]*self._entryCount
        self.nDACFileADCNum = [None]*self._entryCount
        self.nConditEnable = [None]*self._entryCount
        self.lConditNumPulses = [None]*self._entryCount
        self.fBaselineDuration = [None]*self._entryCount
        self.fBaselineLevel = [None]*self._entryCount
        self.fStepDuration = [None]*self._entryCount
        self.fStepLevel = [None]*self._entryCount
        self.fPostTrainPeriod = [None]*self._entryCount
        self.fPostTrainLevel = [None]*self._entryCount
        self.nMembTestEnable = [None]*self._entryCount
        self.nLeakSubtractType = [None]*self._entryCount
        self.nPNPolarity = [None]*self._entryCount
        self.fPNHoldingLevel = [None]*self._entryCount
        self.nPNNumADCChannels = [None]*self._entryCount
        self.nPNPosition = [None]*self._entryCount
        self.nPNNumPulses = [None]*self._entryCount
        self.fPNSettlingTime = [None]*self._entryCount
        self.fPNInterpulse = [None]*self._entryCount
        self.nLTPUsageOfDAC = [None]*self._entryCount
        self.nLTPPresynapticPulses = [None]*self._entryCount
        self.lDACFilePathIndex = [None]*self._entryCount
        self.fMembTestPreSettlingTimeMS = [None]*self._entryCount
        self.fMembTestPostSettlingTimeMS = [None]*self._entryCount
        self.nLeakSubtractADCIndex = [None]*self._entryCount

        for i in range(self._entryCount):
            self.seek(self._byteStart + i*self._entrySize)
            self.nDACNum[i] = self.readInt16()  # 0
            self.nTelegraphDACScaleFactorEnable[i] = self.readInt16()  # 2
            self.fInstrumentHoldingLevel[i] = self.readSingle()  # 4
            self.fDACScaleFactor[i] = self.readSingle()  # 8
            self.fDACHoldingLevel[i] = self.readSingle()  # 12
            self.fDACCalibrationFactor[i] = self.readSingle()  # 16
            self.fDACCalibrationOffset[i] = self.readSingle()  # 20
            self.lDACChannelNameIndex[i] = self.readInt32()  # 24
            self.lDACChannelUnitsIndex[i] = self.readInt32()  # 28
            self.lDACFilePtr[i] = self.readInt32()  # 32
            self.lDACFileNumEpisodes[i] = self.readInt32()  # 36
            self.nWaveformEnable[i] = self.readInt16()  # 40
            self.nWaveformSource[i] = self.readInt16()  # 42
            self.nInterEpisodeLevel[i] = self.readInt16()  # 44
            self.fDACFileScale[i] = self.readSingle()  # 46
            self.fDACFileOffset[i] = self.readSingle()  # 50
            self.lDACFileEpisodeNum[i] = self.readInt32()  # 54
            self.nDACFileADCNum[i] = self.readInt16()  # 58
            self.nConditEnable[i] = self.readInt16()  # 60
            self.lConditNumPulses[i] = self.readInt32()  # 62
            self.fBaselineDuration[i] = self.readSingle()  # 66
            self.fBaselineLevel[i] = self.readSingle()  # 70
            self.fStepDuration[i] = self.readSingle()  # 74
            self.fStepLevel[i] = self.readSingle()  # 78
            self.fPostTrainPeriod[i] = self.readSingle()  # 82
            self.fPostTrainLevel[i] = self.readSingle()  # 86
            self.nMembTestEnable[i] = self.readInt16()  # 90
            self.nLeakSubtractType[i] = self.readInt16()  # 92
            self.nPNPolarity[i] = self.readInt16()  # 94
            self.fPNHoldingLevel[i] = self.readSingle()  # 96
            self.nPNNumADCChannels[i] = self.readInt16()  # 100
            self.nPNPosition[i] = self.readInt16()  # 102
            self.nPNNumPulses[i] = self.readInt16()  # 104
            self.fPNSettlingTime[i] = self.readSingle()  # 106
            self.fPNInterpulse[i] = self.readSingle()  # 110
            self.nLTPUsageOfDAC[i] = self.readInt16()  # 114
            self.nLTPPresynapticPulses[i] = self.readInt16()  # 116
            self.lDACFilePathIndex[i] = self.readInt32()  # 118
            self.fMembTestPreSettlingTimeMS[i] = self.readSingle()  # 122
            self.fMembTestPostSettlingTimeMS[i] = self.readSingle()  # 126
            self.nLeakSubtractADCIndex[i] = self.readInt16()  # 130
