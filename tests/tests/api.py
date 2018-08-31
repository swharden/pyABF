R"""
Code here helps lock-in certain API functions.

Once functionality is added here, extreme efforts are taken never to remove
support for these functions.


##############################
Remove items here when they've been added to a test

    
    holdingCommand = [0.0, -80.0, 0.0, 0.0]
    protocol = pair-loose-60
    protocolPath = X:\Protocols\Scott\SWHlab\paired\pair-loose-60.pro
    stimulusByChannel = [ChannelEpochs(ABF, 0), ChannelEpochs(ABF, 1)]
    sweepCount = 3
    sweepLengthSec = 60.0
    sweepList = [0, 1, 2]
    sweepPointCount = 600000
"""

import os
import sys
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_PROJECT = os.path.abspath(PATH_HERE+"/../../")
PATH_DATA = os.path.abspath(PATH_PROJECT+"/data/abfs/")
sys.path.insert(0, PATH_PROJECT+"/src/")
import pyabf
import glob
import numpy as np
import inspect
import datetime

import logging
logging.basicConfig(level=logging.WARNING)
log = logging.getLogger(__name__)


def test_ABF_core_objects(abf):
    """
    ### ABF object properties
    _Extreme efforts are taken to prevent modification of these components._

    * abfDateTime - the exact time (or best guess) for when the ABF was made
    * abfDateTimeString - abfDateTime formatted as str
    * abfFileComment - comment defined in the waveform editor
    * abfFilePath - full path to the ABF file
    * abfID - abf filename (basename) without extension
    * abfVersion - dictionary containing 4 levels of version information
    * abfVersionString - version string formatted as 'x.x.x.x'
    * adcNames - list containing names of each ADC channel
    * adcUnits - list containing units of each ADC channel
    * channelCount - numer of ADC channels
    * channelList - a list of ADC channels (range(channelCount))
    * creatorVersion - dictionary containing 4 levels of version information
    * creatorVersionString - creatorVersion string formatted as 'x.x.x.x'
    * dataByteStart - location of first byte of data in the file
    * dataPointByteSize - byte size of each data point
    * dataPointCount - number of total data points
    * dataPointsPerMs - rate / 1000
    * dataRate - data points per second
    * dataSecPerPoint - inverse of rate
    * fileGUID - globally unique file identifier (string formatted)
    * protocol - the filename (basename) of the protocol file without extension
    * protocolPath - full path to the protocol file
    * sweepCount - number of sweeps in the file
    * sweepLengthSec - length of each sweep in seconds
    * sweepList - a list of ADC channels (range(sweepCount))
    * sweepPointCount - number of data points in each sweep

    #### MAY CHANGE:
    _These components may change in the future._
    
    * holdingCommand - a list of holding values (one per DAC)
    * stimulusByChannel - special class to work with epoch and custom stimuli

    """
    assert isinstance(abf, pyabf.ABF)

    log.debug("abf file info")
    assert isinstance(abf.abfDateTime, datetime.datetime)
    assert isinstance(abf.abfDateTimeString, str)
    assert isinstance(abf.abfFileComment, str)
    assert isinstance(abf.abfFilePath, str)
    assert isinstance(abf.abfID, str)
    assert isinstance(abf.fileGUID, str)
    assert isinstance(abf.protocol, str)
    assert isinstance(abf.protocolPath, str)
    dot()

    log.debug("abf file version info")
    assert isinstance(abf.abfVersion, dict)
    assert isinstance(abf.abfVersion["major"], int)
    assert isinstance(abf.abfVersion["minor"], int)
    assert isinstance(abf.abfVersion["bugfix"], int)
    assert isinstance(abf.abfVersion["build"], int)
    assert isinstance(abf.abfVersionString, str)
    dot()
    
    log.debug("abf creator version info")
    assert isinstance(abf.creatorVersion["major"], int)
    assert isinstance(abf.creatorVersion["minor"], int)
    assert isinstance(abf.creatorVersion["bugfix"], int)
    assert isinstance(abf.creatorVersion["build"], int)
    assert isinstance(abf.creatorVersionString, str)
    dot()
    
    log.debug("ADC names and units")
    assert isinstance(abf.adcNames, list)
    for adcName in abf.adcNames:
        assert isinstance(adcName,str)
    assert isinstance(abf.adcUnits, list)
    for adcUnit in abf.adcUnits:
        assert isinstance(adcUnit,str)
    assert isinstance(abf.channelCount, int)
    assert isinstance(abf.channelList, list)
    dot()
    
    log.debug("DAC names and units")
    assert isinstance(abf.dacNames, list)
    for dacName in abf.dacNames:
        assert isinstance(adcName,str)
    assert isinstance(abf.dacUnits, list)
    for dacUnit in abf.dacUnits:
        assert isinstance(dacUnit,str)
    dot()

    log.debug("data size and shape")
    assert (isinstance(abf.dataByteStart, int))
    assert (isinstance(abf.dataPointByteSize, int))
    assert (isinstance(abf.dataPointCount, int))
    assert (isinstance(abf.dataPointsPerMs, int))
    assert (isinstance(abf.dataRate, int))
    assert (isinstance(abf.dataSecPerPoint, float))
    assert (isinstance(abf.sweepCount, int))
    assert (isinstance(abf.sweepLengthSec, float))
    assert (isinstance(abf.sweepList, list))
    assert (isinstance(abf.sweepPointCount, int))
    dot()

    log.debug("holding command levels")
    #TODO: rename to abf.adcHolding?
    assert (isinstance(abf.holdingCommand, list))
    for value in abf.holdingCommand:
        assert isinstance(value, float)
    dot()


def test_data_access(abf):
    """
    ## Direct access to signal data

    Direct signal data exists in abf.data.
    Its rows are channels.
    It's one continuous array for the entire data.
    It is not divided into sweeps.
    """
    assert isinstance(abf, pyabf.ABF)

    log.debug("abf.data is an array containing all signal data in the ABF")
    assert isinstance(abf.data, np.ndarray)
    dot()

    log.debug("abf.data rows represent channels")
    assert len(abf.data) == abf.channelCount
    dot()

    log.debug(
        "each row of abf.data is the full signal for that channel (not divided into sweeps)")
    assert len(abf.data[0]) == abf.dataPointCount/abf.channelCount
    dot()


def test_setSweep(abf):
    """
    ## setSweep (and associated sweep data)

    abf.setSweep() pulls data from abf.data and populates:
        abf.sweepX - time of the sweep 
        abf.sweepY - values of the sweep
        abf.sweepC - command waveform for this sweep
        abf.sweepD(outChannel) - generate waveform a digital output

    Passing absoluteTime=True means abf.sweepX is returned in absolute time
    units (the time position of the sweep in the recording), otherwise 
    abf.sweepX always starts at zero.

    Extra values populated by setSweep() include:
        abf.sweepChannel - channel of the set sweep
        abf.sweepNumber - number of the set sweep
        abf.sweepLabelX - time label (suitable for X axis label)
        abf.sweepLabelC - command waveform label (suitable for Y axis label)
        abf.sweepLabelY - signal label (suitable for Y axis label)
        abf.sweepUnitsX - sweep time units (usually 's')
        abf.sweepUnitsC - sweep command units (usually 'pA' or 'mV')
        abf.sweepUnitsY - sweep signal units (usually 'pA' or 'mV')
    """
    assert isinstance(abf, pyabf.ABF)

    log.debug("go to second sweep, second channel, default to regular time")
    abf.setSweep(sweepNumber=1, channel=1)
    assert abf.sweepX[0] == 0
    dot()

    log.debug("go to second sweep, second channel, and use absolute time")
    abf.setSweep(sweepNumber=1, channel=1, absoluteTime=True)
    assert abf.sweepX[0] > 0
    dot()

    log.debug("test generation of digital output waveforms")
    sweepD = abf.sweepD(0)
    if sweepD is False:
        log.debug(f"digital output not enabled")
    else:
        log.debug(f"digital output: {str(sweepD)}")
        assert isinstance(sweepD, np.ndarray)
    dot()

    assert isinstance(abf.sweepChannel, int)
    log.debug(f"abf.sweepChannel={abf.sweepChannel}")
    dot()

    assert isinstance(abf.sweepNumber, int)
    log.debug(f"abf.sweepNumber={abf.sweepNumber}")
    dot()

    assert isinstance(abf.sweepLabelC, str)
    log.debug(f"abf.sweepLabelC={abf.sweepLabelC}")
    dot()

    assert isinstance(abf.sweepLabelX, str)
    log.debug(f"abf.sweepLabelX={abf.sweepLabelX}")
    dot()

    assert isinstance(abf.sweepLabelY, str)
    log.debug(f"abf.sweepLabelY={abf.sweepLabelY}")
    dot()

    assert isinstance(abf.sweepUnitsC, str)
    log.debug(f"abf.sweepUnitsC={abf.sweepUnitsC}")
    dot()

    assert isinstance(abf.sweepUnitsX, str)
    log.debug(f"abf.sweepUnitsX={abf.sweepUnitsX}")
    dot()

    assert isinstance(abf.sweepUnitsY, str)
    log.debug(f"abf.sweepUnitsY={abf.sweepUnitsY}")
    dot()

    return


def specialTest_comments(fname):
    """
    ## Comments (comment tags)

    comments (comment tags) can be accessed with:
        abf.tagComments - a list of comment tags (strings)
        abf.tagSweeps - time of each comment in sweep units (e.g., sweep 3.42)
        abf.tagTimesMin - time of each comment in minutes
        abf.tagTimesSec - time of each comment in seconds

    """
    abf = pyabf.ABF(fname)

    log.debug(f"abf.tagComments={abf.tagComments}")
    assert isinstance(abf.tagComments, list)
    assert isinstance(abf.tagComments[0], str)
    assert len(abf.tagComments) == 2
    dot()

    log.debug(f"abf.tagSweeps={abf.tagSweeps}")
    assert isinstance(abf.tagSweeps, list)
    assert isinstance(abf.tagSweeps[0], float)
    assert len(abf.tagSweeps) == 2
    dot()

    log.debug(f"abf.tagTimesMin={abf.tagTimesMin}")
    assert isinstance(abf.tagTimesMin, list)
    assert isinstance(abf.tagTimesMin[0], float)
    assert len(abf.tagTimesMin) == 2
    dot()

    log.debug(f"abf.tagTimesSec={abf.tagTimesSec}")
    assert isinstance(abf.tagTimesSec, list)
    assert isinstance(abf.tagTimesSec[0], float)
    assert len(abf.tagTimesSec) == 2
    dot()

    return


def dot():
    """print a dot to the screen indicating a test completed okay."""
    print(".", end="")
    sys.stdout.flush()


def go():
    print("Testing core API", end=" ")

    abf1 = pyabf.ABF(PATH_DATA+"/05210017_vc_abf1.abf")
    abf2 = pyabf.ABF(PATH_DATA+"/18702001-ramp.abf")

    log.debug("Testing generic calls which work on any ABF")

    for functionName in sorted(globals()):
        if not functionName.startswith("test_"):
            continue

        log.debug(f"Running {functionName}() on {abf1.abfID} (ABF1)")
        globals()[functionName](abf1)

        log.debug(f"Running {functionName}() on {abf2.abfID} (ABF2)")
        globals()[functionName](abf2)

    log.debug("Testing calls work best on specific ABFs")
    specialTest_comments(PATH_DATA+"/16d05007_vc_tags.abf")

    print(" OK")


if __name__ == "__main__":
    # log.setLevel(logging.DEBUG)
    go()
    print("DONE")
