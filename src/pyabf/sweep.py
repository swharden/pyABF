"""
ABF files contain data which is arranged on disk as one long continuous
recording. Scientists often divide-up records into sweeps even though the
data itself is not divided into sweeps.

To aid in working with sweeps, helper functions were created which take-in
ABF objects and populate them with useful objects to make working with sweeps
simpler. All sweep-related code lies here and is imported into the ABF class.
"""

import numpy as np


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
        print("ABF data not preloaded. Loading now...")
        abf._fileOpen()
        abf._loadAndScaleData()
        abf._fileClose()

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
        abf.sweepX += sweepNumber * abf.sweepLengthSec

    # default case is disabled
    if not "baselinePoints" in vars():
        abf._sweepBaselinePoints = False

    # if baseline subtraction is used, apply it
    if abf._sweepBaselinePoints:
        baseline = np.average(
            abf.sweepY[int(abf._sweepBaselinePoints[0]):int(abf._sweepBaselinePoints[1])])
        abf.sweepY = abf.sweepY-baseline
        abf.sweepLabelY = "Δ " + abf.sweepLabelY

    # make sure sweepPointCount is always accurate
    assert (abf.sweepPointCount == len(abf.sweepY))


@property
def sweepC(abf):
    """Generate the sweep command waveform."""
    # TODO: support custom stimulus waveforms
    sweepEpochs = abf.epochsByChannel[abf.sweepChannel]
    return sweepEpochs.stimulusWaveform(abf.sweepNumber)


def sweepBaseline(abf, timeSec1=None, timeSec2=None):
    """
    Call this to define a baseline region (in seconds). All subsequent
    data obtained from setSweep will be automatically baseline-subtracted
    to this region. Call this without arguments to reset baseline.
    """
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


def _timesToPoints(abf, timeSec1, timeSec2):
    """
    Given two times in seconds return two points in index values.
    """
    p1 = int(timeSec1*abf.dataRate)
    p2 = int(timeSec2*abf.dataRate)
    return [p1, p2]


def averageWithinSweep(abf, timeSec1, timeSec2):
    """
    Return the average value between the two times in the sweep.
    """
    p1, p2 = _timesToPoints(abf, timeSec1, timeSec2)
    avg = np.average(abf.sweepY[p1:p2])
    return avg


def areaWithinSweep(abf, timeSec1, timeSec2):
    """
    Return the area between the two times in the sweep. (in units * ms)
    """
    p1, p2 = _timesToPoints(abf, timeSec1, timeSec2)
    area = np.sum(abf.sweepY[p1:p2])
    area /= abf.dataRate
    area *= 1000.0
    return area


def stdevWithinSweep(abf, timeSec1, timeSec2):
    """
    Return the standard deviation between the two times in the sweep.
    """
    p1, p2 = _timesToPoints(abf, timeSec1, timeSec2)
    stdev = np.std(abf.sweepY[p1:p2])
    return stdev


def stdErrWithinSweep(abf, timeSec1, timeSec2):
    """
    Return the standard error between the two times in the sweep.
    """
    p1, p2 = _timesToPoints(abf, timeSec1, timeSec2)
    stdev = np.std(abf.sweepY[p1:p2])
    stdErr = stdev / np.sqrt(p2-p1)
    return stdErr
