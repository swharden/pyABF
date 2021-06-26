from pyabf.abfReader import readStruct
from pyabf.abfHeader import BLOCKSIZE

class StringsSection:
    """
    Part of the ABF file contains long strings. Some of these can be broken
    apart into indexed strings.

    The first string is the only one which seems to contain useful information.
    This contains information like channel names, channel units, and abf
    protocol path and comments. The other strings are very large and I do not
    know what they do.

    Strings which contain indexed substrings are separated by \\x00 characters.
    """

    def __init__(self, fb, sectionMap):
        blockStart, entrySize, entryCount = sectionMap.StringsSection
        byteStart = blockStart*BLOCKSIZE
        self.strings = [None]*entryCount
        for i in range(entryCount):
            fb.seek(byteStart + i*entrySize)
            structFormat = "%ss" % entrySize
            self.strings[i] = readStruct(fb, structFormat, cleanStrings=False)
