from pyabf.abfReader import readStruct
from pyabf.abfHeader import BLOCKSIZE

class TagSection:
    """
    Tags are comments placed in ABF files during the recording. Physically
    they are located at the end of the file (after the data).

    Later we will populate the times and sweeps (human-understandable units)
    by multiplying the lTagTime by fSynchTimeUnit from the protocol section.
    """

    def __init__(self, fb, sectionMap):
        blockStart, entrySize, entryCount = sectionMap.TagSection
        byteStart = blockStart*BLOCKSIZE

        self.lTagTime = [None]*entryCount
        self.sComment = [None]*entryCount
        self.nTagType = [None]*entryCount
        self.nVoiceTagNumberorAnnotationIndex = [None]*entryCount

        self.timesSec = [None]*entryCount
        self.timesMin = [None]*entryCount
        self.sweeps = [None]*entryCount

        for i in range(entryCount):
            fb.seek(byteStart + i*entrySize)
            self.lTagTime[i] = readStruct(fb, "i")
            self.sComment[i] = readStruct(fb, "56s")
            self.nTagType[i] = readStruct(fb, "h")
            self.nVoiceTagNumberorAnnotationIndex[i] = readStruct(fb, "h")

