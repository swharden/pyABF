from pyabf.abf2.section import Section


class TagSection(Section):
    """
    Tags are comments placed in ABF files during the recording. Physically
    they are located at the end of the file (after the data).

    Later we will populate the times and sweeps (human-understandable units)
    by multiplying the lTagTime by fSynchTimeUnit from the protocol section.
    """

    def __init__(self, fb):
        Section.__init__(self, fb, 252)

        self.lTagTime = [None]*self._entryCount
        self.sComment = [None]*self._entryCount
        self.nTagType = [None]*self._entryCount
        self.nVoiceTagNumberorAnnotationIndex = [None]*self._entryCount

        self.timesSec = [None]*self._entryCount
        self.timesMin = [None]*self._entryCount
        self.sweeps = [None]*self._entryCount

        for i in range(self._entryCount):
            fb.seek(self._byteStart + i*self._entrySize)
            self.lTagTime[i] = self.readInt32()
            self.sComment[i] = self.readString(56)
            self.nTagType[i] = self.readInt16()
            self.nVoiceTagNumberorAnnotationIndex[i] = self.readInt16()
