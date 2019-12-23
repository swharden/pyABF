"""
These tests ensure the ABF object contains the expected contents.
It also tests sweep setting and stimulus waveform generation on all ABFs.
"""

import sys
import pytest
import datetime
import inspect
import numpy as np
import glob

try:
    # this ensures pyABF is imported from this specific path
    sys.path.insert(0, "src")
    import pyabf
except:
    raise ImportError("couldn't import local pyABF")


allABFs = glob.glob("data/abfs/*.abf")

if sys.version_info[0] < 3:
    str = basestring # hack to ignore unicode strings in Python 2.7

@pytest.mark.parametrize("abfPath", allABFs)
def test_Load_headerOnly(abfPath):
    abf = pyabf.ABF(abfPath, loadData=False)
    print(abf)


@pytest.mark.parametrize("abfPath", allABFs)
def test_ABF_properties(abfPath):

    abf = pyabf.ABF(abfPath)

    # file info
    assert isinstance(abf.abfDateTime, datetime.datetime)
    assert isinstance(abf.abfDateTimeString, str)
    assert isinstance(abf.abfFileComment, str)
    assert isinstance(abf.abfFilePath, str)
    assert isinstance(abf.abfID, str)
    assert isinstance(abf.fileGUID, str)
    assert isinstance(abf.protocol, str)
    assert isinstance(abf.protocolPath, str)

    # file version
    assert isinstance(abf.abfVersion, dict)
    assert isinstance(abf.abfVersion["major"], int)
    assert isinstance(abf.abfVersion["minor"], int)
    assert isinstance(abf.abfVersion["bugfix"], int)
    assert isinstance(abf.abfVersion["build"], int)
    assert isinstance(abf.abfVersionString, str)

    # abf creator version info
    assert isinstance(abf.creatorVersion["major"], int)
    assert isinstance(abf.creatorVersion["minor"], int)
    assert isinstance(abf.creatorVersion["bugfix"], int)
    assert isinstance(abf.creatorVersion["build"], int)
    assert isinstance(abf.creatorVersionString, str)

    # ADC names and units
    assert isinstance(abf.adcNames, list)
    for adcName in abf.adcNames:
        assert isinstance(adcName, str)
    assert isinstance(abf.adcUnits, list)
    for adcUnit in abf.adcUnits:
        assert isinstance(adcUnit, str)
    assert isinstance(abf.channelCount, int)
    assert isinstance(abf.channelList, list)

    # DAC names and units
    assert isinstance(abf.dacNames, list)
    for dacName in abf.dacNames:
        assert isinstance(dacName, str)
    assert isinstance(abf.dacUnits, list)
    for dacUnit in abf.dacUnits:
        assert isinstance(dacUnit, str)

    # data info
    assert (isinstance(abf.dataByteStart, int))
    assert (isinstance(abf.dataPointByteSize, int))
    assert (isinstance(abf.dataPointCount, int))
    assert (isinstance(abf.dataPointsPerMs, int))
    assert (isinstance(abf.dataRate, int))
    assert (isinstance(abf.dataSecPerPoint, float))
    assert (isinstance(abf.sweepCount, int))
    assert (isinstance(abf.sweepLengthSec, float))
    assert (isinstance(abf.sweepList, list))
    assert (isinstance(abf.sweepPointCount,  int))

    # holding level
    assert (isinstance(abf.holdingCommand, list))
    for value in abf.holdingCommand:
        assert isinstance(value, float) or isinstance(value, int)

    # data array size and shape
    assert isinstance(abf.data, np.ndarray)
    assert len(abf.data) == abf.channelCount
    assert len(abf.data[0]) == abf.dataPointCount/abf.channelCount

    # comments
    assert isinstance(abf.tagComments, list)
    assert isinstance(abf.tagSweeps, list)
    assert isinstance(abf.tagTimesMin, list)
    assert isinstance(abf.tagTimesSec, list)
    for i in range(len(abf.tagComments)):
        assert isinstance(abf.tagComments[i], str)
        assert isinstance(abf.tagSweeps[i], float)
        assert isinstance(abf.tagTimesMin[i], float)
        assert isinstance(abf.tagTimesSec[i], float)

    # sweeps
    for channel in abf.channelList:
        for sweep in abf.sweepList:
            abf.setSweep(sweep, channel)
            assert isinstance(abf.sweepChannel, int)
            assert isinstance(abf.sweepNumber, int)
            assert isinstance(abf.sweepLabelC, str)
            assert isinstance(abf.sweepLabelX, str)
            assert isinstance(abf.sweepLabelY, str)
            assert isinstance(abf.sweepUnitsC, str)
            assert isinstance(abf.sweepUnitsX, str)
            assert isinstance(abf.sweepUnitsY, str)

            sweepD = abf.sweepD(0)  # digital output generation
            assert isinstance(sweepD, np.ndarray)
