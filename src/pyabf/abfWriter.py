"""
Code here relates to modification and de-novo creation of ABF files.
Files are saved as ABF1 format ABFs, which are easy to create because their
headers are simpler than ABF2 files. 

Many values (e.g., epoch waveform table) are left blank, so when they are read 
by an ABF reader their values may not make sense (especially when converted to 
floating-point numbers).
"""

import os
import time
import struct
import pyabf.generate
import numpy as np
import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

def writeABF1(sweepData, filename, units='pA'):
    """
    Create an ABF1 file from scratch and write it to disk.
    Files created with this function are compatible with MiniAnalysis.
    Data is expected to be a 2D numpy array (each row is a sweep).
    """

    assert isinstance(sweepData, np.ndarray)

    # constants for ABF1 files
    BLOCKSIZE = 512
    HEADER_BLOCKS = 4

    # determine dimensions of data
    sweepCount = sweepData.shape[0]
    sweepPointCount = sweepData.shape[1]
    dataPointCount = sweepPointCount*sweepCount

    # predict how large our file must be and create a byte array of that size
    bytesPerPoint = 2
    dataBlocks = int(dataPointCount * bytesPerPoint / BLOCKSIZE) + 1
    data = bytearray((dataBlocks + HEADER_BLOCKS) * BLOCKSIZE)
    log.info("Creating an ABF1 file %.02f MB in size ..." % (len(data)/1e6))

    # populate only the useful header data values
    struct.pack_into('4s', data, 0, b'ABF ')  # fFileSignature
    struct.pack_into('f', data, 4, 1.3)  # fFileVersionNumber
    struct.pack_into('h', data, 8, 5)  # nOperationMode (5 is episodic)
    struct.pack_into('i', data, 10, dataPointCount)  # lActualAcqLength
    struct.pack_into('i', data, 16, sweepCount)  # lActualEpisodes
    struct.pack_into('i', data, 40, HEADER_BLOCKS)  # lDataSectionPtr
    struct.pack_into('h', data, 100, 0)  # nDataFormat is 1 for float32
    struct.pack_into('h', data, 120, 1)  # nADCNumChannels
    struct.pack_into('f', data, 122, 50)  # fADCSampleInterval (CUSTOMIZE!!!)
    struct.pack_into('i', data, 138, sweepPointCount)  # lNumSamplesPerEpisode

    # These ADC adjustments are used for integer conversion. It's a good idea
    # to populate these with non-zero values even when using float32 notation
    # to avoid divide-by-zero errors when loading ABFs.

    fSignalGain = 1  # always 1
    fADCProgrammableGain = 1  # always 1
    lADCResolution = 2**15  # 16-bit signed = +/- 32768

    # determine the peak data deviation from zero
    maxVal = np.max(np.abs(sweepData))
    log.debug("maximum data value: %f"%(maxVal))

    # set the scaling factor to be the biggest allowable to accomodate the data
    fInstrumentScaleFactor = 100
    for i in range(10):
        fInstrumentScaleFactor /= 10
        fADCRange = 10
        valueScale = lADCResolution / fADCRange * fInstrumentScaleFactor
        maxDeviationFromZero = 32767 / valueScale
        if (maxDeviationFromZero<maxVal):
            log.debug("scaling factor %f is too small (max %f)"%(valueScale, 
                maxDeviationFromZero))
        else:
            log.debug("scaling factor %f will be used"%(valueScale))
            break
        
    log.debug("maximum allowed data value: %f"%(maxDeviationFromZero))
    log.debug("first value (float): %f"%(sweepData[0][0]))
    log.debug("first value (scaled int): %f"%(int(sweepData[0][0]*valueScale)))

    # prepare units as a space-padded 8-byte string
    unitString = units
    while len(unitString)<8:
        unitString = unitString + " "

    # store the scale data in the header
    struct.pack_into('i', data, 252, lADCResolution)
    struct.pack_into('f', data, 244, fADCRange)
    for i in range(16):
        struct.pack_into('f', data, 922+i*4, fInstrumentScaleFactor)
        struct.pack_into('f', data, 1050+i*4, fSignalGain)
        struct.pack_into('f', data, 730+i*4, fADCProgrammableGain)
        struct.pack_into('8s', data, 602+i*8, unitString.encode())

    # fill data portion with scaled data from signal
    dataByteOffset = BLOCKSIZE * HEADER_BLOCKS
    for sweepNumber, sweepSignal in enumerate(sweepData):
        sweepByteOffset = sweepNumber * sweepPointCount * bytesPerPoint
        for valueNumber, value in enumerate(sweepSignal):
            valueByteOffset = valueNumber * bytesPerPoint
            bytePosition = dataByteOffset + sweepByteOffset + valueByteOffset
            struct.pack_into('h', data, bytePosition, int(value*valueScale))

    # save the byte array to disk
    with open(filename, 'wb') as f:
        f.write(data)
        log.info("wrote %s"%(filename))
    return


def _demo_sweep_data(sweeps=3, sweepLengthSec=5, sampleRate=20000):
    """crete a 2D numpy array of data to test ABF creation."""
    sweepData = np.empty((sweeps, sweepLengthSec*sampleRate))
    for i in range(sweeps):
        log.info("Generating sweep %d of %d ..."%(i+1, sweeps))
        sweep = generate.SynthSweep()
        sweep.addOffset(-123)
        sweep.addWobble(2)
        sweep.addNoise(3)
        sweep.addGlutamate(frequencyHz=10, maxMagnitude=20)  # glutamate
        sweep.addGABA(frequencyHz=20, maxMagnitude=5)  # GABA
        sweepData[i] = sweep.sweepY
    return sweepData


if __name__ == "__main__":
    print("DO NOT RUN THIS SCRIPT DIRECTLY")

    # test this script by generating random data and saving it
    sweepData = _demo_sweep_data()
    filename = R"C:\Users\scott\Documents\temp\test_%f.abf"%(time.time())
    writeABF1(sweepData, filename)
    os.system(filename) # launch in clampfit
    print("DONE")