from pyabf.abf2.section import Section


class EpochPerDACSection(Section):
    """
    This section contains waveform protocol information. These are most of
    the values set when using the epoch the waveform editor. Note that digital
    output signals are not stored here, but are in EpochSection.
    """

    def __init__(self, fb):
        Section.__init__(self, fb, 156)

        self.nEpochNum = [None]*self._entryCount
        self.nDACNum = [None]*self._entryCount
        self.nEpochType = [None]*self._entryCount
        self.fEpochInitLevel = [None]*self._entryCount
        self.fEpochLevelInc = [None]*self._entryCount
        self.lEpochInitDuration = [None]*self._entryCount
        self.lEpochDurationInc = [None]*self._entryCount
        self.lEpochPulsePeriod = [None]*self._entryCount
        self.lEpochPulseWidth = [None]*self._entryCount

        for i in range(self._entryCount):
            self.seek(self._byteStart + i*self._entrySize)
            self.nEpochNum[i] = self.readInt16()  # 0
            self.nDACNum[i] = self.readInt16()  # 2
            self.nEpochType[i] = self.readInt16()  # 4
            self.fEpochInitLevel[i] = self.readSingle()  # 6
            self.fEpochLevelInc[i] = self.readSingle()  # 10
            self.lEpochInitDuration[i] = self.readInt32()  # 14
            self.lEpochDurationInc[i] = self.readInt32()  # 18
            self.lEpochPulsePeriod[i] = self.readInt32()  # 22
            self.lEpochPulseWidth[i] = self.readInt32()  # 26
