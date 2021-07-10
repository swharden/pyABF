"""
Code related to detection and measurement of action potentials (APs)
"""

import warnings
import logging
import numpy as np
import pyabf
import os
import sys
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_DATA = os.path.abspath(PATH_HERE+"../../../../data/abfs/")
PATH_SRC = os.path.abspath(PATH_HERE+"../../../")
sys.path.insert(0, PATH_SRC)


logging.basicConfig(level=logging.WARNING)
log = logging.getLogger(__name__)

warnings.warn("The pyabf package is designed for reading ABF files (not analyzing them). " +
              "This module is experimental, provided only for backwards compatibility, and its API may change in future releases. " +
              "Users are encouraged to write their own ABF analysis code.")


def _where_cross(data, threshold):
    """return a list of Is where the data first crosses above threshold."""
    Is = np.where(data > threshold)[0]
    Is = np.concatenate(([0], Is))
    Ds = Is[:-1]-Is[1:]+1
    return Is[np.where(Ds)[0]+1]


def ap_points_currentSweep(abf, dVthresholdPos=15, betweenSec1=None, betweenSec2=None):
    """
    Primitive AP detection. Returns index numbers of peaks of ap depolariztaion velocities.
    """
    assert isinstance(abf, pyabf.ABF)

    # calculate first derivative
    sweepDeriv = np.diff(abf.sweepY)

    # scale it to V/S (mV/ms)
    sweepDeriv = sweepDeriv * abf.dataRate / 1000

    # determine where crossings occur
    crossings = _where_cross(sweepDeriv, dVthresholdPos)

    # center APs on their positive dV peak and eliminate duplicates
    for i, pt in enumerate(crossings):
        derivFast = sweepDeriv[pt:pt+abf.dataPointsPerMs*2]
        ptMax = np.max(derivFast)
        crossings[i] = pt + np.where(derivFast == ptMax)[0][0]
    crossings = sorted(list(set(crossings)))

    # throw out crossings which don't go negative after 4ms
    dVthresholdNeg = -dVthresholdPos/2
    for i, pt in enumerate(crossings):
        derivFast = sweepDeriv[pt:pt+abf.dataPointsPerMs*2]
        if np.min(derivFast) > dVthresholdNeg:
            crossings[i] = 0
    crossings = [x for x in crossings if x]

    # if there are doubles, throw-out the second one
    for i in range(len(crossings)):
        if i == 0:
            continue
        dPoints = crossings[i] - crossings[i-1]
        if dPoints < abf.dataPointsPerMs*3:
            crossings[i] = 0
    crossings = [x for x in crossings if x]

    return crossings


def ap_freq_per_sweep(abf, singleEpoch=False):
    """
    Return [apFreqInBin, apFreqFirst] lists by sweep.
    """
    assert isinstance(abf, pyabf.ABF)

    if singleEpoch:
        epochPoints = pyabf.stimulus.epochPoints(abf)
        pt1, pt2 = epochPoints[singleEpoch], epochPoints[singleEpoch+1]
    else:
        pt1, pt2 = 0, abf.sweepPointCount

    apFreqInBin = [0]*abf.sweepCount
    apFreqFirst = [0]*abf.sweepCount
    for sweep in abf.sweepList:
        abf.setSweep(sweep)
        apPoints = ap_points_currentSweep(abf)
        apPoints = [x for x in apPoints if x > pt1 and x < pt2]
        timeSpanSec = (pt2-pt1)/abf.dataRate
        apFreqInBin[sweep] = len(apPoints)/timeSpanSec
        if len(apPoints) > 1:
            apFreqFirst[sweep] = abf.dataRate/(apPoints[1]-apPoints[0])
    return [apFreqInBin, apFreqFirst]


def extract_first_ap(abf, paddingMsec=50):
    for sweepNumber in abf.sweepList:
        abf.setSweep(sweepNumber)
        apPoints = pyabf.tools.ap.ap_points_currentSweep(abf)
        if (len(apPoints) > 0):
            i1 = apPoints[0] - paddingMsec*abf.dataPointsPerMs
            i2 = apPoints[0] + paddingMsec*abf.dataPointsPerMs
            if i1 < 0:
                i1 = 0
            if i2 >= len(abf.sweepY):
                i2 = len(abf.sweepY)-1
            return abf.sweepY[i1:i2]
    return None
