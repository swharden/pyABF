"""
Code here identifies ABFs with mismatched ADC/DAC settings.
"""

import os
import sys
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_SRC = os.path.abspath(PATH_HERE+"../../../../src/")
sys.path.insert(0, PATH_SRC)  # useful for imports
import pyabf
import glob
import shutil
import struct

BLOCKSIZE = 512


class ABFmodify:
    def __init__(self, abfFilePath, backup=True):
        """
        The ABFmodify class is intended to simplify the act of modifyinig
        the contents of ABF files. Typically this means modifying header values.

        If backup is enabled, ABFs will be backed-up before modifying them.
        The backup is the original filename with a .abf.backup extension.
        """
        assert isinstance(abfFilePath, str)
        self.abfFilePath = os.path.abspath(abfFilePath)
        assert os.path.exists(abfFilePath)
        self.backup = backup

    def ensureBackupExists(self):
        backupFilePath = self.abfFilePath+".backup"
        if not os.path.exists(backupFilePath):
            print("creating", os.path.basename(backupFilePath))
            shutil.copy(self.abfFilePath, backupFilePath)

    def bytesWrite(self, bytePosition, byteValues):
        self.ensureBackupExists()
        #print("WRITING", byteValues, "at byte", bytePosition)
        with open(self.abfFilePath, 'r+b') as f:
            f.seek(bytePosition)
            f.write(bytes(byteValues))

    def bytesRead(self, bytePosition, byteCount):
        with open(self.abfFilePath, 'rb') as f:
            f.seek(bytePosition)
            values = f.read(byteCount)
        return values

    def structRead(self, bytePosition, structFormat):
        byteCount = struct.calcsize(structFormat)
        byteValues = self.bytesRead(bytePosition, byteCount)
        values = struct.unpack(structFormat, byteValues)
        return values

    def getScaleFactor(self):
        """
        fInstrumentScaleFactor is a 4-byte float.
        It's located at the start of each ADCSection + 40 bytes
        """

        ADCSection = self.structRead(92, "IIl")
        blockStart, entrySize, entryCount = ADCSection
        byteStart = blockStart*BLOCKSIZE

        for channel in range(entryCount):
            bytePosition = byteStart + channel*entrySize + 40
            byteValues = self.bytesRead(bytePosition, 4)
            scaleFactorFloat = struct.unpack("f", byteValues)[0]
            print(os.path.basename(self.abfFilePath), "Ch", channel,
                  "fInstrumentScaleFactor =", list(byteValues), "=",
                  scaleFactorFloat)

    def setScaleFactor(self, byteVals=[], channel=0):
        """
        fInstrumentScaleFactor is a 4-byte float.
        It's located at the start of each ADCSection + 40 bytes
        """

        assert isinstance(byteVals, list)
        assert len(byteVals) == 4

        ADCSection = self.structRead(92, "IIl")
        blockStart, entrySize, entryCount = ADCSection
        byteStart = blockStart*BLOCKSIZE
        bytePosition = byteStart + channel*entrySize + 40
        self.bytesWrite(bytePosition, byteVals)


if __name__ == "__main__":
    #abf_file_folder = R"X:\Data\C57\BLA injection microspheres\technique development\abfs"
    abf_file_folder = PATH_HERE+"/demoABFs/"
    abfFiles = glob.glob(abf_file_folder+"/*.abf")

    for abfNumber, fname in enumerate(sorted(abfFiles)):
        msg = f"Analyzing ({abfNumber}/{len(abfFiles)})"
        print(f"{msg} {os.path.basename(fname)}", end=" ... ")

        abf = pyabf.ABF(fname, loadData=False)

        # ensure units arent the same
        if abf.adcUnits[0] == abf.dacUnits[0]:
            print("ERROR ... ", end="")
            abfMod = ABFmodify(abf.abfFilePath)
            abfMod.setScaleFactor([10, 215, 35, 60])
            print("FIXED!")
        else:
            print("OK")
