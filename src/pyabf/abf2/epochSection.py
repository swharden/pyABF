from pyabf.abfReader import readStruct


class EpochSection:
    """
    This section contains the digital output signals for each epoch. This
    section has been overlooked by some previous open-source ABF-reading
    projects. Note that the digital output is a single byte, but represents
    8 bits corresponding to 8 outputs (7->0). When working with these bits,
    I convert it to a string like "10011101" for easy eyeballing.
    """

    def __init__(self, fb, sectionMap):
        blockStart, entrySize, entryCount = sectionMap.EpochSection
        byteStart = blockStart*512

        self.nEpochNum = [None]*entryCount
        self.nEpochDigitalOutput = [None]*entryCount

        for i in range(entryCount):
            fb.seek(byteStart + i*entrySize)
            self.nEpochNum[i] = readStruct(fb, "h")  # 0
            self.nEpochDigitalOutput[i] = readStruct(fb, "h")  # 2
