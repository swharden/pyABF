from pyabf.abfReader import readStruct


class SynchArraySection:
    """
    Contains start time (in fSynchTimeUnit units) and length (in 
    multiplexed samples) of each portion of the data if the data 
    are not part of a continuous gap-free acquisition. 
    """

    def __init__(self, fb, sectionMap):
        blockStart, entrySize, entryCount = sectionMap.SynchArraySection
        byteStart = blockStart*512

        self.lStart = [None]*entryCount
        self.lLength = [None]*entryCount

        for i in range(entryCount):
            fb.seek(byteStart + i*entrySize)
            self.lStart[i] = readStruct(fb, "i")
            self.lLength[i] = readStruct(fb, "i")
