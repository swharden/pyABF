R"""
Code here helps lock-in certain API functions.

Once functionality is added here, extreme efforts are taken never to remove
support for these functions.


##############################
Remove items here when they've been added to a test

    abfDateTime = 2014-10-08 16:43:18.203000
    abfDateTimeString = 2014-10-08T16:43:18.203000
    abfFileComment = SWH[loose60]
    abfFilePath = c:\Users\scott\Documents\GitHub\pyABF\data\abfs\14o08011_ic_pair.abf
    abfID = 14o08011_ic_pair
    abfVersion = {'major': 2, 'minor': 0, 'bugfix': 0, 'build': 0}
    abfVersionString = 2.0.0.0
    adcNames = ['IN 0', 'IN 1']
    adcUnits = ['mV', 'mV']
    channelCount = 2
    channelList = [0, 1]
    creatorVersion = {'major': 10, 'minor': 3, 'bugfix': 0, 'build': 2}
    dacNames = ['Cmd 0', 'Cmd 1']
    dacUnits = ['pA', 'pA']
    dataByteStart = 4608
    dataPointByteSize = 2
    dataPointCount = 3600000
    dataPointsPerMs = 10
    dataRate = 10000
    dataSecPerPoint = 0.0001
    fileGUID = {51FA9285-FBA0-4AB6-AFAC-F99493DA8A8A}
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

import logging
logging.basicConfig(level=logging.WARNING)
log = logging.getLogger(__name__)

def test_data(abf):
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

    log.debug("each row of abf.data is the full signal for that channel (not divided into sweeps)")
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
    assert abf.sweepX[0]==0
    dot()

    log.debug("go to second sweep, second channel, and use absolute time")
    abf.setSweep(sweepNumber=1, channel=1, absoluteTime=True)
    assert abf.sweepX[0]>0
    dot()

    log.debug("test generation of digital output waveforms")
    sweepD = abf.sweepD(0)
    if sweepD is False:
        log.debug(f"digital output not enabled")
    else:
        log.debug(f"digital output: {str(sweepD)}")
        assert isinstance(sweepD, np.ndarray)
    dot()
        
    assert isinstance(abf.sweepChannel,int)
    log.debug(f"abf.sweepChannel={abf.sweepChannel}")
    dot()

    assert isinstance(abf.sweepNumber,int)
    log.debug(f"abf.sweepNumber={abf.sweepNumber}")
    dot()

    assert isinstance(abf.sweepLabelC,str)
    log.debug(f"abf.sweepLabelC={abf.sweepLabelC}")
    dot()

    assert isinstance(abf.sweepLabelX,str)
    log.debug(f"abf.sweepLabelX={abf.sweepLabelX}")
    dot()

    assert isinstance(abf.sweepLabelY,str)
    log.debug(f"abf.sweepLabelY={abf.sweepLabelY}")
    dot()

    assert isinstance(abf.sweepUnitsC,str)
    log.debug(f"abf.sweepUnitsC={abf.sweepUnitsC}")
    dot()

    assert isinstance(abf.sweepUnitsX,str)
    log.debug(f"abf.sweepUnitsX={abf.sweepUnitsX}")
    dot()

    assert isinstance(abf.sweepUnitsY,str)
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
    assert isinstance(abf.tagComments,list)
    assert isinstance(abf.tagComments[0],str)
    assert len(abf.tagComments)==2
    dot()

    log.debug(f"abf.tagSweeps={abf.tagSweeps}")
    assert isinstance(abf.tagSweeps,list)
    assert isinstance(abf.tagSweeps[0],float)
    assert len(abf.tagSweeps)==2
    dot()

    log.debug(f"abf.tagTimesMin={abf.tagTimesMin}")
    assert isinstance(abf.tagTimesMin,list)
    assert isinstance(abf.tagTimesMin[0],float)
    assert len(abf.tagTimesMin)==2
    dot()

    log.debug(f"abf.tagTimesSec={abf.tagTimesSec}")
    assert isinstance(abf.tagTimesSec,list)
    assert isinstance(abf.tagTimesSec[0],float)
    assert len(abf.tagTimesSec)==2
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

if __name__=="__main__":
    #log.setLevel(logging.DEBUG)
    go()
    print("DONE")