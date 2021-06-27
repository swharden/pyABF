import struct

class AbfReader:

    def __init__(self, fb):
        self._fb = fb

    def seek(self, position):
        self._fb.seek(position)

    def readUInt32(self):
        bytes = self._fb.read(4)
        values = struct.unpack("I", bytes)
        return values[0]

    def readInt32(self):
        bytes = self._fb.read(4)
        values = struct.unpack("i", bytes)
        return values[0]

    def readUInt16(self):
        bytes = self._fb.read(2)
        values = struct.unpack("H", bytes)
        return values[0]

    def readInt16(self):
        bytes = self._fb.read(2)
        values = struct.unpack("h", bytes)
        return values[0]

    def readSingle(self):
        bytes = self._fb.read(4)
        values = struct.unpack("f", bytes)
        return values[0]

    def readSingles(self, length):
        return [self.readSingle() for _ in range(length)]

    def readByte(self):
        bytes = self._fb.read(1)
        values = struct.unpack("B", bytes)
        return int(values[0])

    def readBytes(self, length):
        return [self.readByte() for _ in range(length)]

    def readChar(self):
        bytes = self._fb.read(1)
        values = struct.unpack("c", bytes)
        return values[0].decode("ascii", errors='ignore')

    def readString(self, length, clean=True):
        bytes = self._fb.read(length)
        values = struct.unpack(f"{length}s", bytes)[0]
        string = values.decode("ascii", errors='ignore').strip()
        return string

    def readStruct(self, structFormat, seek=False, cleanStrings=True):
        """
        Return a structured value in an ABF file as a Python object.
        If cleanStrings is enabled, ascii-safe strings are returned.
        """

        if seek:
            self._fb.seek(seek)

        varSize = struct.calcsize(structFormat)
        byteString = self._fb.read(varSize)
        values = struct.unpack(structFormat, byteString)
        values = list(values)

        if cleanStrings:
            values = [self._cleanString(x) for x in values]

        if len(values) == 1:
            values = values[0]

        return values

    def _cleanString(self, value):
        if type(value) == type(b''):
            return value.decode("ascii", errors='ignore').strip()
        else:
            return value

    def readStruct(self, structFormat, seek=False, cleanStrings=True):
        """
        Return a structured value in an ABF file as a Python object.
        If cleanStrings is enabled, ascii-safe strings are returned.
        """

        if seek:
            self._fb.seek(seek)

        varSize = struct.calcsize(structFormat)
        byteString = self._fb.read(varSize)
        values = struct.unpack(structFormat, byteString)
        values = list(values)

        if cleanStrings:
            for i in range(len(values)):
                if type(values[i]) == type(b''):
                    values[i] = values[i].decode("ascii", errors='ignore').strip()

        if len(values) == 1:
            values = values[0]

        return values
