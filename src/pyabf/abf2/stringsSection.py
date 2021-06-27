from pyabf.abf2.section import Section


class StringsSection(Section):
    """
    Part of the ABF file contains long strings. Some of these can be broken
    apart into indexed strings.

    The first string is the only one which seems to contain useful information.
    This contains information like channel names, channel units, and abf
    protocol path and comments. The other strings are very large and I do not
    know what they do.

    Strings which contain indexed substrings are separated by \\x00 characters.
    """

    def __init__(self, fb):
        Section.__init__(self, fb, 220)

        self.strings = [None]*self._entryCount
        self._stringsRaw = [None]*self._entryCount

        for i in range(self._entryCount):
            fb.seek(self._byteStart + i*self._entrySize)

            # store raw strings for advanced access later
            values = bytearray(self.readBytes(self._entrySize))
            self._stringsRaw[i] = values

            # store cleaned strings for typical use
            values = values.replace(b'\xb5', b'\x75')  # make mu u
            values = values.decode("ascii", errors='ignore').strip()
            self.strings[i] = values

        # take the first string and further split it apart
        indexedStrings = self._stringsRaw[0]
        indexedStrings = indexedStrings[indexedStrings.rfind(b'\x00\x00'):]
        indexedStrings = indexedStrings.replace(b'\xb5', b"\x75")  # make mu u
        indexedStrings = indexedStrings.split(b'\x00')[1:]
        indexedStrings = [x.decode("ascii", errors='replace').strip()
                          for x in indexedStrings]
        self._indexedStrings = indexedStrings