"""
Code here analyzes data from within the selected sweep. Code here does not
involve cross-sweep operations (e.g., averaging several sweeps together).
"""

import numpy as np


def _timesToPoints(abf, timeSec1, timeSec2):
    """
    Given two times in seconds return two points in index values.
    """
    p1 = int(timeSec1*abf.dataRate)
    p2 = int(timeSec2*abf.dataRate)
    return [p1, p2]


def average(abf, timeSec1, timeSec2):
    """
    Return the average value between the two times in the sweep.
    """
    p1, p2 = _timesToPoints(abf, timeSec1, timeSec2)
    avg = np.average(abf.sweepY[p1:p2])
    return avg


def area(abf, timeSec1, timeSec2):
    """
    Return the area between the two times in the sweep.
    """
    p1, p2 = _timesToPoints(abf, timeSec1, timeSec2)
    area = np.sum(abf.sweepY[p1:p2])
    return area


def stdev(abf, timeSec1, timeSec2):
    """
    Return the standard deviation between the two times in the sweep.
    """
    p1, p2 = _timesToPoints(abf, timeSec1, timeSec2)
    stdev = np.std(abf.sweepY[p1:p2])
    return stdev


def stdErr(abf, timeSec1, timeSec2):
    """
    Return the standard error between the two times in the sweep.
    """
    p1, p2 = _timesToPoints(abf, timeSec1, timeSec2)
    stdev = np.std(abf.sweepY[p1:p2])
    stdErr = stdev / np.sqrt(p2-p1)
    return stdErr
