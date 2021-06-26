from pyabf.abfReader import readStruct
from pyabf.abfHeader import BLOCKSIZE


class UserListSection:
    """
    Contains elements of the ABF2 user list.
    The user list allows custom values to be used as part of the epoch table.
    """

    def __init__(self, fb, sectionMap):
        blockStart, entrySize, entryCount = sectionMap.UserListSection
        byteStart = blockStart*BLOCKSIZE

        self.nULEnable = [None]*entryCount
        self.nULParamToVary = [None]*entryCount
        self.nULParamToVaryName = [None]*entryCount
        self.nULRepeat = [None]*entryCount
        self.nStringIndex = [None]*entryCount

        for i in range(entryCount):
            fb.seek(byteStart + i*entrySize)
            _ = readStruct(fb, "h")
            _ = readStruct(fb, "h")
            param = readStruct(fb, "h")
            repeat = readStruct(fb, "h")
            stringIndex = readStruct(fb, "h")

            if (param > 0):
                self.nULEnable[i] = 1
                self.nULParamToVary[i] = param
                self.nULRepeat[i] = repeat
                self.nStringIndex[i] = stringIndex
