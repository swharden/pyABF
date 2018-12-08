"""
ABF files contain data which is arranged on disk as one long continuous
recording. Scientists often divide-up records into sweeps even though the
data itself is not divided into sweeps.

To aid in working with sweeps, helper functions were created which take-in
ABF objects and populate them with useful objects to make working with sweeps
simpler. All sweep-related code lies here and is imported into the ABF class.
"""

import numpy as np

import logging
logging.basicConfig(level=logging.WARNING)
log = logging.getLogger(__name__)


def _timesToPoints(abf, timeSec1=None, timeSec2=None):
    """
    Given two times in seconds return two points in index values.
    """
    if timeSec1:
        p1 = int(timeSec1*abf.dataRate)
    else:
        p1 = 0

    if timeSec2:
        p2 = int(timeSec2*abf.dataRate)
    else:
        p2 = abf.sweepPointCount

    if p1 < 0 or p1 >= abf.sweepPointCount:
        log.critical("timeSec1 is outside the valid range for a sweep")
    if p2 <= p1 or p2 > abf.sweepPointCount:
        log.critical("timeSec2 is outside the valid range for a sweep")

    return [p1, p2]


def setSweep(abf, sweepNumber, channel=0, absoluteTime=False):
    """
    Args:
        sweepNumber: sweep number to load (starting at 0)
        channel: ABF channel (starting at 0)
        absoluteTime: if False, sweepX always starts at 0.
    """

    # basic error checking
    if not sweepNumber in abf.sweepList:
        msg = "Sweep %d not available (must be 0 - %d)" % (
            sweepNumber, abf.sweepCount-1)
        raise ValueError(msg)
    if not channel in abf.channelList:
        msg = "Channel %d not available (must be 0 - %d)" % (
            channel, abf.channelCount-1)
        raise ValueError(msg)

    if not "data" in (dir(abf)):
        log.debug("ABF data not preloaded. Loading now...")
        with open(abf.abfFilePath, 'rb') as fb:
            abf._loadAndScaleData(fb)

    # TODO: prevent re-loading of the same sweep.

    # determine data bounds for that sweep
    pointStart = abf.sweepPointCount*sweepNumber
    pointEnd = pointStart + abf.sweepPointCount

    # start updating class-level variables

    # sweep information
    abf.sweepNumber = sweepNumber
    abf.sweepChannel = channel
    abf.sweepUnitsY = abf.adcUnits[channel]
    abf.sweepUnitsC = abf.dacUnits[channel]
    abf.sweepUnitsX = "sec"

    # standard labels
    abf.sweepLabelY = "{} ({})".format(
        abf.adcNames[channel], abf.adcUnits[channel])
    abf.sweepLabelC = "{} ({})".format(
        abf.dacNames[channel], abf.dacUnits[channel])
    abf.sweepLabelX = "time (seconds)"

    # use fancy labels for known units
    if abf.sweepUnitsY == "pA":
        abf.sweepLabelY = "Clamp Current (pA)"
        abf.sweepLabelC = "Membrane Potential (mV)"
    elif abf.sweepUnitsY == "mV":
        abf.sweepLabelY = "Membrane Potential (mV)"
        abf.sweepLabelC = "Applied Current (pA)"

    # load the actual sweep data
    abf.sweepY = abf.data[channel, pointStart:pointEnd]
    abf.sweepX = np.arange(len(abf.sweepY))*abf.dataSecPerPoint
    if absoluteTime:
        abf.sweepX += sweepNumber * abf.sweepIntervalSec

    # default case is disabled
    if not hasattr(abf, '_sweepBaselinePoints'):
        log.debug("setSweep doesn't see baselinePoints, making False")
        abf._sweepBaselinePoints = False

    # if baseline subtraction is used, apply it
    if abf._sweepBaselinePoints:
        log.debug("setSweep is applying baseline subtraction")
        baseline = np.average(
            abf.sweepY[int(abf._sweepBaselinePoints[0]):int(abf._sweepBaselinePoints[1])])
        abf.sweepY = abf.sweepY-baseline
        abf.sweepLabelY = "Delta " + abf.sweepLabelY

    # make sure sweepPointCount is always accurate
    assert (abf.sweepPointCount == len(abf.sweepY))

@property
def sweepC(abf):
    """Generate the sweep command waveform."""
    if hasattr(abf, "_sweepC") and isinstance(abf._sweepC, np.ndarray):
        # someone set a custom waveform, so always return it
        return abf._sweepC
    else:
        # auto-generate (or auto-load) the waveform using the stimulus module
        stimulus = abf.stimulusByChannel[abf.sweepChannel]
        return stimulus.stimulusWaveform(abf.sweepNumber)

@sweepC.setter
def sweepC(abf, sweepData=None):
    """
    Manually define sweepC so the given sweepData will always be returned as
    sweepC and the stimulus waveform will no longer be automatically generated
    or loaded from file. Undo this by deleting "abf._sweepC".
    """
    if sweepData is None:
        del abf._sweepC
        return
    if not len(sweepData):
        raise ValueError("an array must be given when setting sweepC")
    sweepData = np.array(sweepData)
    if not sweepData.shape == abf.sweepY.shape:
        raise ValueError("sweepC.shape must match sweepY.shape")
    abf._sweepC = sweepData



def sweepBaseline(abf, timeSec1=None, timeSec2=None):
    """
    Call this to define a baseline region (in seconds). All subsequent
    data obtained from setSweep will be automatically baseline-subtracted
    to this region. Call this without arguments to reset baseline.
    """
    if not "sweepY" in dir(abf):
        abf.setSweep(0)
    if timeSec1 or timeSec2:
        if not timeSec1:
            timeSec1 = 0
        if not timeSec2:
            timeSec2 = abf.sweepLengthSec
        blPoint1 = timeSec1*abf.dataRate
        blPoint2 = timeSec2*abf.dataRate
        if blPoint1 < 0:
            blPoint1 = 0
        if blPoint2 >= len(abf.sweepY):
            blPoint2 = len(abf.sweepY)
        abf._sweepBaselineTimes = [timeSec1, timeSec2]
        abf._sweepBaselinePoints = [blPoint1, blPoint2]
    else:
        abf._sweepBaselineTimes = False
        abf._sweepBaselinePoints = False
    return (abf._sweepBaselineTimes)


def averageTrace(abf, sweepNumbers=[], channel=0, timeSec1=None, timeSec2=None, errorToo=False, stdErr=False):
    """
    Returns [AVG, STDEV] of the average signal from the given sweeps.
    If no sweeps are given, all sweeps are used.
    """
    if not isinstance(sweepNumbers, list) or len(sweepNumbers) == 0:
        sweepNumbers = abf.sweepList
    p1, p2 = _timesToPoints(abf, timeSec1, timeSec2)

    outputPoints = p2-p1
    sweepAvg = np.empty((len(sweepNumbers), outputPoints))
    for sweep in sweepNumbers:
        abf.setSweep(sweep, channel)
        sweepAvg[sweep] = abf.sweepY[p1:p2]
    sweepAvg = np.average(sweepAvg, 0)
    if errorToo is False:
        return sweepAvg
    else:
        sweepErr = np.std(sweepAvg, 0)
        if stdErr:
            sweepErr = sweepErr / np.sqrt(len(sweepNumbers))
        return [sweepAvg, sweepErr]


def sweepMeasureAverage(abf, timeSec1, timeSec2):
    """
    Return the average value between the two times in the sweep.
    """
    p1, p2 = _timesToPoints(abf, timeSec1, timeSec2)
    avg = np.average(abf.sweepY[p1:p2])
    return avg


def sweepMeasureArea(abf, timeSec1, timeSec2):
    """
    Return the area between the two times in the sweep. (in units * ms)
    """
    p1, p2 = _timesToPoints(abf, timeSec1, timeSec2)
    area = np.sum(abf.sweepY[p1:p2])
    area /= abf.dataRate
    area *= 1000.0
    return area


def sweepMeasureStdev(abf, timeSec1, timeSec2):
    """
    Return the standard deviation between the two times in the sweep.
    """
    p1, p2 = _timesToPoints(abf, timeSec1, timeSec2)
    stdev = np.std(abf.sweepY[p1:p2])
    return stdev


def sweepMeasureMax(abf, timeSec1, timeSec2):
    """
    Return the peak value between the two times in the sweep.
    """
    p1, p2 = _timesToPoints(abf, timeSec1, timeSec2)
    return np.max(abf.sweepY[p1:p2])


def sweepMeasureMin(abf, timeSec1, timeSec2):
    """
    Return the anti-peak value between the two times in the sweep.
    """
    p1, p2 = _timesToPoints(abf, timeSec1, timeSec2)
    return np.min(abf.sweepY[p1:p2])
