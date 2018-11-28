
"""
Code here relates to analytical methods performed on ABFs.
Typically the same analysis is performed once per sweep and returned as an array
where every element represents a sweep
"""

import numpy as np

import logging
logging.basicConfig(level=logging.WARNING)
log = logging.getLogger(__name__)

def rangeAverage(abf, timeSec1=None, timeSec2=None, sweepNumbers=[], channel=0):
    """
    Returns [AVGS] between two time points for the given sweeps.
    If no sweeps are given, all sweeps are used.
    """
    if not isinstance(sweepNumbers, list) or len(sweepNumbers) == 0:
        sweepNumbers = abf.sweepList
    vals = np.full(len(sweepNumbers), np.nan)
    for sweepNumber in sweepNumbers:
        abf.setSweep(sweepNumber=sweepNumber, channel=channel)
        vals[sweepNumber] = abf.sweepAvg(timeSec1, timeSec2)
    return vals

def rangeStdev(abf, timeSec1=None, timeSec2=None, sweepNumbers=[], channel=0):
    """
    Returns [STDEVS] between two time points for the given sweeps.
    If no sweeps are given, all sweeps are used.
    """
    if not isinstance(sweepNumbers, list) or len(sweepNumbers) == 0:
        sweepNumbers = abf.sweepList
    vals = np.full(len(sweepNumbers), np.nan)
    for sweepNumber in sweepNumbers:
        abf.setSweep(sweepNumber=sweepNumber, channel=channel)
        vals[sweepNumber] = abf.sweepStdev(timeSec1, timeSec2)
    return vals

def rangeMax(abf, timeSec1=None, timeSec2=None, sweepNumbers=[], channel=0):
    """
    Returns [PEAKS] between two time points for the given sweeps.
    If no sweeps are given, all sweeps are used.
    """
    if not isinstance(sweepNumbers, list) or len(sweepNumbers) == 0:
        sweepNumbers = abf.sweepList
    peaks = np.full(len(sweepNumbers), np.nan)
    for sweepNumber in sweepNumbers:
        abf.setSweep(sweepNumber=sweepNumber, channel=channel)
        peaks[sweepNumber] = abf.sweepMax(timeSec1, timeSec2)
    return peaks

def rangeMin(abf, timeSec1=None, timeSec2=None, sweepNumbers=[], channel=0):
    """
    Returns [ANTIPEAKS] between two time points for the given sweeps.
    If no sweeps are given, all sweeps are used.
    """
    if not isinstance(sweepNumbers, list) or len(sweepNumbers) == 0:
        sweepNumbers = abf.sweepList
    peaks = np.full(len(sweepNumbers), np.nan)
    for sweepNumber in sweepNumbers:
        abf.setSweep(sweepNumber=sweepNumber, channel=channel)
        peaks[sweepNumber] = abf.sweepMin(timeSec1, timeSec2)
    return peaks