from pyabf.abfReader import readStruct
from pyabf.abfHeader import BLOCKSIZE
from pyabf.abfHeader import TELEGRAPHS

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

