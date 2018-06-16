"""
Code here simplifies access to ABF file contents.

This module is part of the pyABF project by Scott W Harden
https://github.com/swharden/pyABF/
"""

from pyabf.header import AbfHeader
from pyabf.header import ABF1header
from pyabf.header import SectionMap
from pyabf.header import SectionADC
from pyabf.header import SectionDAC
from pyabf.header import SectionEpoch
from pyabf.header import SectionEpochPerDac
from pyabf.header import SectionTag
from pyabf.header import SectionStrings
from pyabf.header import SectionProtocol

import struct
import os
import glob
import io
import numpy as np
np.set_printoptions(suppress=True)

from matplotlib import pyplot as plt

def getData(fb, dataByteStart, dataPointCount, nChannels, scaleFactors):
    """
    Given an open ABF file (fb mode), return its data (by channel).
    """
    fb.seek(dataByteStart)
    data = np.fromfile(fb, dtype=np.int16, count=dataPointCount)
    data = np.reshape(data, (int(len(data)/nChannels), nChannels))
    data = np.rot90(data)
    data2 = np.empty(data.shape, dtype='float32')
    for i in range(len(scaleFactors)):
        data2[i] = np.multiply(data[i], scaleFactors[i], dtype='float32')
    return data2


class ABFcore:
    def __init__(self, abfFile):
        """
        This class provides direct access to the contents of ABF1 and ABF2 files.
        Upon instantiation, the entire ABF file is read (header values and data).
        Header values are lightly massaged to simplify their use.
        Data is provided by channel already scaled.
        """

        self.fb = open(abfFile, 'rb')

        self.header = AbfHeader(self.fb)
        if self.header.fFileSignature == "ABF ":
            self.readABF1()
        elif self.header.fFileSignature == "ABF2":
            self.readABF2()
        else:
            print("FILE ERROR")

        self.fb.close()

    def readABF1(self):
        self.abf1header = ABF1header(self.fb, 0)

        self.nChannels = self.abf1header.nADCNumChannels
        firstByte = self.abf1header.lDataSectionPtr*512
        dataLength = self.abf1header.lActualAcqLength

        self.scaleFactors = [None]*self.nChannels
        for channel in range(self.nChannels):
            self.scaleFactors[channel] = self.abf1header.lADCResolution/1e6

        self.data = getData(self.fb, firstByte, dataLength,
                            self.nChannels, self.scaleFactors)

    def readABF2(self):
        self.map = SectionMap(self.fb, 0)
        self.adc = SectionADC(self.fb, self.map.ADCSection)
        self.dac = SectionDAC(self.fb, self.map.DACSection)
        self.epoch = SectionEpoch(self.fb, self.map.EpochSection)
        self.epochPerDac = SectionEpochPerDac(
            self.fb, self.map.EpochPerDACSection)
        self.tag = SectionTag(self.fb, self.map.TagSection)
        self.strings = SectionStrings(self.fb, self.map.StringsSection)
        self.protocol = SectionProtocol(
            self.fb, self.map.ProtocolSection[0]*512)

        self.nChannels = self.map.ADCSection[2]  # number of ADC channels
        firstByte = self.map.DataSection[0]*512
        dataLength = self.map.DataSection[1]*self.map.DataSection[2]

        self.scaleFactors = [None]*self.nChannels
        for channel in range(self.nChannels):
            scaleFactor = 1.0
            scaleFactor /= self.adc.fInstrumentScaleFactor[channel]
            scaleFactor /= self.adc.fSignalGain[channel]
            scaleFactor /= self.adc.fADCProgrammableGain[channel]
            if self.adc.nTelegraphEnable:
                scaleFactor /= self.adc.fTelegraphAdditGain[channel]
            scaleFactor *= self.protocol.fADCRange
            scaleFactor /= self.protocol.lADCResolution
            scaleFactor += self.adc.fInstrumentOffset[channel]
            scaleFactor -= self.adc.fSignalOffset[channel]
            self.scaleFactors[channel] = scaleFactor

        self.data = getData(self.fb, firstByte, dataLength,
                            self.nChannels, self.scaleFactors)


class ABF:
    def __init__(self,abfFile):
        self.core = ABFcore(abfFile)
        self.nChannels = self.core.nChannels
        self.nSweeps = 123
        self.data = self.core.data

