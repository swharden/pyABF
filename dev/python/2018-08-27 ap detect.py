"""
quick and dirty derivative threshold detection for APs
"""

import os
import sys
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_DATA = os.path.abspath(PATH_HERE+"../../../data/abfs/")
PATH_SRC = os.path.abspath(PATH_HERE+"../../../src/")
sys.path.insert(0, PATH_SRC)
import pyabf
import glob
import numpy as np
import matplotlib.pyplot as plt

def where_cross(data,threshold):
    """return a list of Is where the data first crosses above threshold."""
    Is=np.where(data>threshold)[0]
    Is=np.concatenate(([0],Is))
    Ds=Is[:-1]-Is[1:]+1
    return Is[np.where(Ds)[0]+1]

def ap_points_currentSweep(abf, dVthresholdPos=10, betweenSec1=None, betweenSec2=None):
    """
    Primitive AP detection. Returns index numbers of peaks of ap depolariztaion velocities.
    """
    assert isinstance(abf,pyabf.ABF)

    # calculate first derivative
    sweepDeriv = np.diff(abf.sweepY)
    
    # scale it to V/S (mV/ms)
    sweepDeriv = sweepDeriv * abf.dataRate / 1000

    # determine where crossings occur
    crossings = where_cross(sweepDeriv,dVthresholdPos)

    # center APs on their positive dV peak and eliminate duplicates
    for i, pt in enumerate(crossings):
        derivFast = sweepDeriv[pt:pt+abf.dataPointsPerMs*2]
        ptMax = np.max(derivFast)
        crossings[i] = pt + np.where(derivFast==ptMax)[0][0]
    crossings = sorted(list(set(crossings)))

    # throw out crossings which don't go negative after 4ms
    dVthresholdNeg = -dVthresholdPos/2
    for i, pt in enumerate(crossings):
        derivFast = sweepDeriv[pt:pt+abf.dataPointsPerMs*2]
        if np.min(derivFast)>dVthresholdNeg:
            crossings[i]=0
    crossings = [x for x in crossings if x]

    # if there are doubles, throw-out the second one
    for i in range(len(crossings)):
        if i==0:
            continue
        dPoints = crossings[i] - crossings[i-1]
        if dPoints<abf.dataPointsPerMs*3:
            crossings[i]=0
    crossings = [x for x in crossings if x]

    return crossings

def ap_freq_per_sweep_dirty(abf):
    assert isinstance(abf, pyabf.ABF)
    apFreq = [0]*abf.sweepCount
    epochPoints = pyabf.stimulus.epochPoints(abf)
    pt1,pt2 = epochPoints[1],epochPoints[2]
    for sweep in abf.sweepList:
        abf.setSweep(sweep)
        apPoints = ap_points_currentSweep(abf)
        apPoints = [x for x in apPoints if x>pt1 and x<pt2]

        # method 1: frequency in bin (#APs / time span)
        timeSpanSec = (pt2-pt1)/abf.dataRate
        apFreq[sweep] = len(apPoints)/timeSpanSec

        # method 2: true frequency (#APs / time between 1st and last AP)
        #if len(apPoints)>1:
            #timeSpanSec = (apPoints[-1]-apPoints[0])/abf.dataRate
            #apFreq[sweep] = len(apPoints)/timeSpanSec

    return apFreq

if __name__=="__main__":
    abfFile = R"X:\Data\F344\Aging BLA\basal excitability round2\abfs\171113ts_0005.abf"
    abf = pyabf.ABF(abfFile)
    print(ap_freq_per_sweep_dirty(abf))
    print("DONE")