"""
These tests ensure the ABF object contains the expected contents.
It also tests sweep setting and stimulus waveform generation on all ABFs.
"""

import sys
from numpy.core.numeric import array_equal
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
    str = basestring  # hack to ignore unicode strings in Python 2.7


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
    assert (isinstance(abf.sampleRate, int))
    assert (array_equal(abf.dataRate, abf.sampleRate))

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

            # time units are manually defined
            assert isinstance(abf.sweepUnitsX, str)
            assert abf.sweepUnitsX == "sec"

            # labels are pyabf inventions and will always be present
            assert isinstance(abf.sweepLabelX, str)
            assert isinstance(abf.sweepLabelY, str)
            assert isinstance(abf.sweepLabelC, str)

            # ADC labels are likely available for every channel
            if (abf.sweepLabelY is not None):
                assert isinstance(abf.sweepUnitsY, str)

            # DAC labels are likely available for every channel
            # but may not if there are more ADCs than DACs
            if (abf.sweepUnitsC is not None):
                assert isinstance(abf.sweepUnitsC, str)
                assert isinstance(abf.sweepD(0), np.ndarray)


def test_uuid_isExpectedValue():
    abf = pyabf.ABF("data/abfs/2019_07_24_0055_fsi.abf")
    assert abf.fileGUID == "5689DB34-B07E-456A-811C-44E9BE92FBC6"
    assert abf.fileUUID == "834CBF1D-372E-3D19-225E-31E718BCD04D"
    assert abf.md5 == "834CBF1D372E3D19225E31E718BCD04D"


def test_userList_isExpectedValue():

    assert pyabf.ABF("data/abfs/171117_HFMixFRET.abf").userList == [
        -100.0, 180.0, 160.0, 140.0, 120.0, 100.0, 80.0, 60.0, 40.0, 20.0, 0.0, -20.0, -60.0]

    assert pyabf.ABF("data/abfs/19212027.abf").userList == [
        -50.0, -55.0, -60.0, -65.0, -70.0, -75.0, -80.0, -85.0, -90.0, -95.0, -100.0, -105.0, -110.0, -115.0, -120.0]

    assert pyabf.ABF("data/abfs/2020_03_02_0000.abf").userList == [
        -200.0, -150.0, -100.0, -50.0, 0.0, 25.0, 50.0, 100.0, 150.0, 200.0, 250.0, 300.0, 350.0, 400.0, 500.0, 600.0]
