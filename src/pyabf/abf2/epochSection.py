from pyabf.abf2.section import Section


class EpochSection(Section):
    """
    This section contains the digital output signals for each epoch. This
    section has been overlooked by some previous open-source ABF-reading
    projects. Note that the digital output is a single byte, but represents
    8 bits corresponding to 8 outputs (7->0). When working with these bits,
    I convert it to a string like "10011101" for easy eyeballing.
    """

    def __init__(self, fb):
        Section.__init__(self, fb, 124)

        self.nEpochNum = [None]*self._entryCount
        self.nEpochDigitalOutput = [None]*self._entryCount

        for i in range(self._entryCount):
            self.seek(self._byteStart + i*self._entrySize)
            self.nEpochNum[i] = self.readInt16()
            self.nEpochDigitalOutput[i] = self.readInt16()