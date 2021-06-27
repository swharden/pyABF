from pyabf.abf2.section import Section


class SynchArraySection(Section):
    """
    Contains start time (in fSynchTimeUnit units) and length (in 
    multiplexed samples) of each portion of the data if the data 
    are not part of a continuous gap-free acquisition. 
    """

    def __init__(self, fb):
        Section.__init__(self, fb, 316)

        self.lStart = [None]*self._entryCount
        self.lLength = [None]*self._entryCount

        for i in range(self._entryCount):
            fb.seek(self._byteStart + i*self._entrySize)
            self.lStart[i] = self.readInt32()
            self.lLength[i] = self.readInt32()