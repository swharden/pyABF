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

def fileWriteBytes(filePath, bytePosition, byteValues):
    with open(filePath, 'r+b') as f:
        f.seek(bytePosition)
        f.write(bytes(byteValues))

def fileReadBytes(filePath, bytePosition, byteCount):
    with open(filePath, 'rb') as f:
        f.seek(bytePosition)
        return list(f.read(byteCount))

def bytePos_fInstrumentScaleFactor(filePath, channel=0):    
    byteVals = fileReadBytes(filePath, 92, struct.calcsize("IIl"))
    ADCSection = struct.unpack("IIl", bytes(byteVals))
    blockStart, entrySize, entryCount = ADCSection
    byteStart = blockStart*BLOCKSIZE
    assert channel < entryCount
    bytePosition = byteStart + channel*entrySize + 40
    return bytePosition

def ensureBackupExists(filePath):
    filePath2 = filePath+".backup"
    assert os.path.exists(filePath)
    if not os.path.exists(filePath2):
        shutil.copy(filePath, filePath2)

if __name__ == "__main__":
    #abf_file_folder = R"X:\Data\C57\BLA injection microspheres\technique development\abfs"
    abf_file_folder = PATH_HERE+"/demoABFs/"
    abfFiles = sorted(glob.glob(abf_file_folder+"/*.abf"))

    for fname in abfFiles:
        abf = pyabf.ABF(fname, preLoadData=False)

        # check if DAC and ADC units are the same
        if abf.adcUnits[0] == abf.dacUnits[0]:
            print(abf.abfID, "UNITS ERROR!!!")
            bytePos = bytePos_fInstrumentScaleFactor(fname)
            #print(fileReadBytes(fname, bytePos, 4))
            ensureBackupExists(fname)
            fileWriteBytes(fname, bytePos, [10, 215, 35, 60])
            print(abf.abfID, "MANUALLY DEFINED SCALE.")
        else:
            print(abf.abfID, "OK")
