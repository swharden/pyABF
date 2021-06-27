from pyabf.abfReader import AbfReader


class Section(AbfReader):

    def __init__(self, fb, infoBytePosition):
        AbfReader.__init__(self, fb)
        self.seek(infoBytePosition)
        self._blockStart = self.readStruct("I")
        self._byteStart = self._blockStart*512
        self._entrySize = self.readStruct("I")
        self._entryCount = self.readStruct("i")
