"""
Demonstrate how to calculate Cm from a ramp protocol.

INPUT:
    model_vc_ramp.abf is from Patch-1U Model Cell (33 pF +/- 10%)

OUTPUT:
    model_vc_ramp as a capacitance of 30.88 +/- 0.20 pF
    171116sh_0014 as a capacitance of 202.32 +/- 11.49 pF
    2018_08_23_0009 as a capacitance of 170.90 +/- 13.54 pF
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

import logging
logging.basicConfig(level=logging.WARNING)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def cm_ramp_fromAllSweeps(abf):
    """
    return an array of membrane capacitance values calculated from the ramp 
    found in every sweep in the abf.
    """
    assert isinstance(abf, pyabf.ABF)
    cms = np.full(abf.sweepCount, np.nan)
    for sweepNumber in abf.sweepList:
        abf.setSweep(sweepNumber)
        cms[sweepNumber] = cm_ramp_fromThisSweep(abf)
    log.info(f"%s as a capacitance of %.02f +/- %.02f pF" %
             (abf.abfID, np.mean(cms), np.std(cms)))
    return cms


def cm_ramp_fromThisSweep(abf):
    """
    Calculate capacitance from a voltage clamp ramp.

    In theory any channel, any ramp, and even changing ramps will work.

    This expects a downward ramp followed by an upward ramp, each with the same
    duration and magnitude. This ramp can be anywhere in the sweep, and does
    not have to be the first epoch.
    """
    assert isinstance(abf, pyabf.ABF)

    log.debug(f"calculating Cm from ramp on {abf.abfID}.abf")

    if abf.sweepUnitsY != "pA":
        log.critical("must be in voltage clamp configuration")
        return

    epochTypes = abf._epochPerDacSection.nEpochType
    if epochTypes.count(2) < 2:
        log.critical("protocol must have at least 2 ramps")
        return

    for epochNumber in range(len(epochTypes)-1):
        if epochTypes[epochNumber] == 2 and epochTypes[epochNumber+1] == 2:
            log.debug(f"ramp starts at epoch: {epochNumber}")
            break
    else:
        log.critical("protocol must 2 ramps back to back!")
        return

    # determine the voltages at the 3 points of the ramp
    epochValues = pyabf.stimulus.epochValues(abf)[abf.sweepChannel]
    rampVoltages = [abf.holdingCommand[abf.sweepChannel]]
    rampVoltages.append(epochValues[epochNumber])
    rampVoltages.append(epochValues[epochNumber+1])
    if epochNumber > 0:
        rampVoltages[0] = epochValues[epochNumber-1]
    log.debug(f"ramp voltages (mV): {rampVoltages}")
    deltaVoltage = rampVoltages[1]-rampVoltages[0]
    log.debug(f"delta voltage (mV): {deltaVoltage}")
    if rampVoltages[0] != rampVoltages[2]:
        log.critical("ramp must deviate then return to the same voltage")
        return
    if rampVoltages[0] == rampVoltages[1]:
        log.critical("ramp must have magnitude")
        return

    # determine the data index positions at the 3 points of the ramp
    epochPoints = pyabf.stimulus.epochPoints(abf)
    rampPoints = [epochPoints[epochNumber],
                  epochPoints[epochNumber+1],
                  epochPoints[epochNumber+2]]
    log.debug(f"ramp epochs start at (points): {rampPoints}")

    # isolate the useful data and perform the calculation
    rampData = abf.sweepY[rampPoints[0]:rampPoints[2]]
    cm = cm_ramp_calculate(rampData, abf.dataRate, deltaVoltage)
    log.debug(f"Cm detected as: {cm} pF")

    return cm


def cm_ramp_calculate(rampData, sampleRate, deltaVoltage, centerFrac=.3):
    """
    Given a v-shaped current trace in response to a symmetric voltage-clamp 
    ramp (its magnitude given by deltaVoltage), calculate and return the
    capacitance of the cell. Data units must be in pA, sampleRate in points/sec,
    and voltage in mV. Positive (upward) or negative (V-shaped) ramps are okay.

    centerFrac is the fractional time span to draw data from in the center of
    each ramp.
    """

    msg = f"analyzing Cm ramp (centerfrac={centerFrac}) "
    msg += f"sample ({len(rampData)} points) at {sampleRate} Hz "
    msg += f"with dV={deltaVoltage}"
    log.debug(msg)

    # ensure our values are of the correct types
    rampData = np.array(rampData)
    sampleRate = int(sampleRate)
    deltaVoltage = int(deltaVoltage)

    # isolate and rearrange the downward vs upward slopes
    trace1 = rampData[:int(len(rampData)/2)][::-1]
    trace2 = rampData[int(len(rampData)/2):]
    traceAvg = np.average((trace1, trace2), axis=0)
    if not len(trace1) == len(trace2):
        log.critical("rampData length must be an even multiple of 2")
        return

    # figure out the middle of the data we wish to sample from
    centerPoint = int(len(trace1))/2
    centerLeft = int(centerPoint-len(trace1)*centerFrac/2)
    centerRight = int(centerPoint+len(trace1)*centerFrac/2)

    # determine the slope of the ramp (mV/ms)
    rampSlideTimeMs = (len(rampData)/2)/sampleRate*1000
    slope = deltaVoltage/rampSlideTimeMs

    # determine the average slope deviation (distance from the mean)
    traceDiff = trace1-trace2
    traceDeviation = traceDiff/2

    # calculate the deviation just for the center
    deviationCenter = traceDeviation[centerLeft:centerRight]
    deviation = np.mean(deviationCenter)

    # capacitance is isolated capacitive transient divided by the command slope
    cm = deviation/slope

    # units don't require conversion, because pA is appropriately scaled for pF
    return cm


if __name__ == "__main__":
    abfFilesToTest = []
    abfFilesToTest.append(PATH_DATA+"/171116sh_0014.abf")
    abfFilesToTest.append(PATH_DATA+"/model_vc_ramp.abf")
    abfFilesToTest.append(PATH_DATA+"/2018_08_23_0009.abf")
    for abfFile in abfFilesToTest:
        abf = pyabf.ABF(abfFile)
        cms = cm_ramp_fromAllSweeps(abf)
    plt.show()
