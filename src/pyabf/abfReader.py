import struct

def abfFileFormat(fb):
    """
    This function returns 1 or 2 if the ABF file is v1 or v2.
    This function returns False if the file is not an ABF file.

    The first few characters of an ABF file tell you its format.
    Storage of this variable is superior to reading the ABF header because
    the file format is required before a version can even be extracted.
    """
    fb.seek(0)
    code = fb.read(4)
    code = code.decode("ascii", errors='ignore')
    if code == "ABF ":
        return 1
    elif code == "ABF2":
        return 2
    else:
        return False


def readStruct(fb, structFormat, seek=False, cleanStrings=True):
    """
    Return a structured value in an ABF file as a Python object.
    If cleanStrings is enabled, ascii-safe strings are returned.
    """

    if seek:
        fb.seek(seek)

    varSize = struct.calcsize(structFormat)
    byteString = fb.read(varSize)
    values = struct.unpack(structFormat, byteString)
    values = list(values)

    if cleanStrings:
        for i in range(len(values)):
            if type(values[i]) == type(b''):
                values[i] = values[i].decode("ascii", errors='ignore').strip()

    if len(values) == 1:
        values = values[0]

    return values
