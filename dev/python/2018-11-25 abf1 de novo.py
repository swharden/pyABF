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


def create_abf1_from_scratch():
    """See how barebones we can get to make a file ClampFit can still open."""

    # load simulated ephys data from NPY file (could easly be ABF2)
    signalSweeps = np.load(DEMO_NPY)
    sweepCount = signalSweeps.shape[0]
    sweepPointCount = signalSweeps.shape[1]
    dataPointCount = sweepPointCount*sweepCount

    # predict how large our file must be and create a byte array of that size
    dataBlocks = int(dataPointCount * 4 / BLOCKSIZE)+1
    headerBlocks = 4
    data = bytearray((dataBlocks + headerBlocks) * BLOCKSIZE)
    print(f"Creating an ABF1 file {len(data)/1e6} MB in size ...")

    # populate only the useful header data values
    struct.pack_into('4s', data, 0, b'ABF ')  # fFileSignature
    struct.pack_into('f', data, 4, 1.765)  # fFileVersionNumber
    struct.pack_into('h', data, 8, 5)  # nOperationMode (5 is episodic)
    struct.pack_into('i', data, 10, dataPointCount)  # lActualAcqLength
    struct.pack_into('i', data, 16, sweepCount)  # lActualEpisodes
    struct.pack_into('i', data, 40, 4)  # lDataSectionPtr (always 4?)
    struct.pack_into('h', data, 100, 1)  # must be 1 for float32
    struct.pack_into('h', data, 120, 1)  # nADCNumChannels
    struct.pack_into('f', data, 122, 20)  # fADCSampleInterval (CUSTOMIZE!!!)
    struct.pack_into('i', data, 138, sweepPointCount)  # lNumSamplesPerEpisode

    # fill data portion with data from signal
    dataByteOffset = BLOCKSIZE*4
    for sweepNumber, sweepSignal in enumerate(signalSweeps):
        sweepByteOffset = sweepNumber * sweepPointCount * 4
        for valueNumber, value in enumerate(sweepSignal):
            valueByteOffset = valueNumber * 4
            bytePosition = dataByteOffset + sweepByteOffset + valueByteOffset
            struct.pack_into('f', data, bytePosition, value)

    # save the byte array to disk
    with open(DEMO_ABF, 'wb') as f:
        f.write(data)
        print(f"wrote {DEMO_ABF}")


if __name__ == "__main__":
    create_abf1_from_scratch()
    print("DONE")
