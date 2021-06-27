from pyabf.abf2.section import Section


class UserListSection(Section):
    """
    Contains elements of the ABF2 user list.
    The user list allows custom values to be used as part of the epoch table.
    """

    def __init__(self, fb):
        Section.__init__(self, fb, 172)

        self.nULEnable = [None]*self._entryCount
        self.nULParamToVary = [None]*self._entryCount
        self.nULParamToVaryName = [None]*self._entryCount
        self.nULRepeat = [None]*self._entryCount
        self.nStringIndex = [None]*self._entryCount

        for i in range(self._entryCount):
            fb.seek(self._byteStart + i*self._entrySize)
            _ = self.readInt16()
            _ = self.readInt16()
            param = self.readInt16()
            repeat = self.readInt16()
            stringIndex = self.readInt16()

            if (param > 0):
                self.nULEnable[i] = 1
                self.nULParamToVary[i] = param
                self.nULRepeat[i] = repeat
                self.nStringIndex[i] = stringIndex
