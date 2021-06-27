from pyabf.abfReader import readStruct


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
            self.nEpochNum[i] = readStruct(fb, "h")  # 0
            self.nDACNum[i] = readStruct(fb, "h")  # 2
            self.nEpochType[i] = readStruct(fb, "h")  # 4
            self.fEpochInitLevel[i] = readStruct(fb, "f")  # 6
            self.fEpochLevelInc[i] = readStruct(fb, "f")  # 10
            self.lEpochInitDuration[i] = readStruct(fb, "i")  # 14
            self.lEpochDurationInc[i] = readStruct(fb, "i")  # 18
            self.lEpochPulsePeriod[i] = readStruct(fb, "i")  # 22
            self.lEpochPulseWidth[i] = readStruct(fb, "i")  # 26
