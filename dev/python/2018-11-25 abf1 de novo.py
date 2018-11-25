"""
Code here will demonstrate how to create an ABF1 file de novo (from scratch).
It will be episodic, and its source data will be the NPY created yesterday.
"""

import os
import numpy as np
import struct
import random

FOLDER_HERE = os.path.abspath(os.path.dirname(__file__))
DEMO_NPY = os.path.join(FOLDER_HERE, "2018-11-24 simulated data.npy")
DEMO_ABF = os.path.join(FOLDER_HERE, "2018-11-25 abf1 de novo.abf")
BLOCKSIZE = 512
HEADER_BLOCKS = 4


def create_abf1_from_scratch():
    """See how barebones we can get to make a file ClampFit can still open."""

    # load simulated ephys data from NPY file (could easly be ABF2)
    signalSweeps = np.load(DEMO_NPY)
    sweepCount = signalSweeps.shape[0]
    sweepPointCount = signalSweeps.shape[1]
    dataPointCount = sweepPointCount*sweepCount

    # predict how large our file must be and create a byte array of that size
    bytesPerPoint = 2
    dataBlocks = int(dataPointCount * bytesPerPoint / BLOCKSIZE) + 1
    data = bytearray((dataBlocks + HEADER_BLOCKS) * BLOCKSIZE)
    print(f"Creating an ABF1 file {len(data)/1e6} MB in size ...")

    # populate only the useful header data values
    struct.pack_into('4s', data, 0, b'ABF ')  # fFileSignature
    struct.pack_into('f', data, 4, 1.299)  # fFileVersionNumber
    struct.pack_into('h', data, 8, 5)  # nOperationMode (5 is episodic)
    struct.pack_into('i', data, 10, dataPointCount)  # lActualAcqLength
    struct.pack_into('i', data, 16, sweepCount)  # lActualEpisodes
    struct.pack_into('i', data, 40, HEADER_BLOCKS)  # lDataSectionPtr
    # struct.pack_into('h', data, 100, 1)  # nDataFormat is 1 for float32
    struct.pack_into('h', data, 120, 1)  # nADCNumChannels
    struct.pack_into('f', data, 122, 20)  # fADCSampleInterval (CUSTOMIZE!!!)
    struct.pack_into('i', data, 138, sweepPointCount)  # lNumSamplesPerEpisode

    # These ADC adjustments are used for integer conversion. It's a good idea
    # to populate these with non-zero values even when using float32 notation
    # to avoid divide-by-zero errors when loading ABFs.

    fSignalGain = 1 # always 1
    fADCProgrammableGain = 1 # always 1
    lADCResolution = 2**15 # 16-bit signed = +/- 32768
    fInstrumentScaleFactor = .0005
    fADCRange = 10
    valueScale = lADCResolution / fADCRange * fInstrumentScaleFactor
    print("value scale:", valueScale)
    for i in range(16):
        struct.pack_into('f', data, 922+i*4, fInstrumentScaleFactor)
        struct.pack_into('f', data, 1050+i*4, fSignalGain)
        struct.pack_into('f', data, 730+i*4, fADCProgrammableGain)
        struct.pack_into('f', data, 244+i*4, fADCRange)
        struct.pack_into('i', data, 252+i*4, lADCResolution)
        #struct.pack_into('h', data, 378+i, i) # nADCPtoLChannelMap 
        #struct.pack_into('8s', data, 602+i*8, b'pA') # sADCUnits 
        #struct.pack_into('h', data, 410+i, -1) # nADCSamplingSeq 
    #struct.pack_into('h', data, 410, 0) # nADCSamplingSeq 
 
    # fill data portion with data from signal
    dataByteOffset = BLOCKSIZE * HEADER_BLOCKS
    for sweepNumber, sweepSignal in enumerate(signalSweeps):
        sweepByteOffset = sweepNumber * sweepPointCount * bytesPerPoint
        for valueNumber, value in enumerate(sweepSignal):
            valueByteOffset = valueNumber * bytesPerPoint
            bytePosition = dataByteOffset + sweepByteOffset + valueByteOffset
            struct.pack_into('h', data, bytePosition, int(value*valueScale))

    # save the byte array to disk
    with open(DEMO_ABF, 'wb') as f:
        f.write(data)
        print(f"wrote {DEMO_ABF}")
        print("launching in ClampFit...")
        cmd = f'explorer "{DEMO_ABF}"'
        print(cmd)
        os.system(cmd)


if __name__ == "__main__":
    create_abf1_from_scratch()
    print("DONE")
