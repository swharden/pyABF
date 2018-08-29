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
logging.basicConfig(level=logging.WARN)
log = logging.getLogger(__name__)
log.setLevel(logging.WARN)


def _tauMonoExpFit(data, rateHz=20000, tau=.1, step=.1):
    """
    Given some data which decays to zero, return its time constant 
    (found by successive approximation) in seconds.
    """
    if len(data) == 0:
        return np.nan
    errs = [np.inf]
    normed = data/data[0]
    Xs = np.arange(len(normed))/rateHz
    while(len(errs)) < 50:
        assert len(Xs) == len(data)
        tau = np.max((0.000001, tau))
        errs.append(np.sum(np.exp(-Xs/tau)-normed))
        if np.abs(errs[-1]) < 0.01:
            return tau
        if (errs[-1] > 0 and errs[-2] < 0) or (errs[-1] < 0 and errs[-2] > 0):
            step /= 2
        if errs[-1] < 0:
            tau += step
        elif errs[-1] > 0:
            tau -= step
    return tau


def cm_step_summary(abf):
    """
    Return a message displaying average stats
    formatted like 'Cm = 34.56 +/- 3.21 pF'
    """
    Ihs, Rms, Ras, Cms = cm_step_valuesBySweep(abf)
    out = ""
    out += "Ih = %.02f +/- %.02f pA\n" % (np.mean(Ihs), np.std(Ihs))
    out += "Rm = %.02f +/- %.02f pA\n" % (np.mean(Rms), np.std(Rms))
    out += "Ra = %.02f +/- %.02f pA\n" % (np.mean(Ras), np.std(Ras))
    out += "Cm = %.02f +/- %.02f pA" % (np.mean(Cms), np.std(Cms))
    return out


def cm_step_valuesBySweep(abf):
    """
    return an array of membrane capacitance values calculated from the step 
    found in every sweep in the abf. Returns [Ihs, Rms, Ras, Cms]
    """
    assert isinstance(abf, pyabf.ABF)

    Ihs = np.full(abf.sweepCount, np.nan)
    Rms = np.full(abf.sweepCount, np.nan)
    Ras = np.full(abf.sweepCount, np.nan)
    Cms = np.full(abf.sweepCount, np.nan)

    for sweepNumber in abf.sweepList:
        abf.setSweep(sweepNumber)
        Ih, Rm, Ra, Cm = _cm_step_fromThisSweep(abf)
        Ihs[sweepNumber] = Ih
        Rms[sweepNumber] = Rm
        Ras[sweepNumber] = Ra
        Cms[sweepNumber] = Cm

    return [Ihs, Rms, Ras, Cms]


def _cm_step_fromThisSweep(abf):
    """returns [Ih, Rm, Ra, Cm]"""
    assert isinstance(abf, pyabf.ABF)
    stepInfo = _cm_step_points_and_voltages(abf)
    if not stepInfo:
        log.warn(f"{abf.abfID} sweep {abf.sweepNumber} couldnt be measured")
        return np.nan
    stepPoints, stepVoltages = stepInfo
    trace = abf.sweepY[stepPoints[0]:stepPoints[2]]
    traceStepPoint = stepPoints[1]-stepPoints[0]
    dV = stepVoltages[1]-stepVoltages[0]
    Ih, Rm, Ra, Cm = _cm_step_calculate(abf, trace, traceStepPoint, dV=dV)
    log.info(f"Ih: {Ih}, Rm: {Rm}, Ra: {Ra}, Cm: {Cm}")
    return [Ih, Rm, Ra, Cm]


def _cm_step_calculate(abf, trace, traceStepPoint, dV=-10, stepAvgLastFrac=.2,
                       fitToFracUpper=.9):
    """
    Given a current clamp trace depicting a voltage step, return membrane test
    information Ih, Rm, Ra, and Cm.

    stepAvgLastFrac - defines what percentage of the end of the step to measure
    to calculate resting current.
    dV - step voltage change (mV)
    """
    assert isinstance(abf, pyabf.ABF)

    log.debug(f"dV={dV} mV")

    trace1 = trace[:traceStepPoint]
    trace2 = trace[traceStepPoint:]

    # calculate the holding current (assume we are starting there)
    Ih = np.mean(trace1)
    log.debug(f"Ih={Ih} pA")

    # calculate the resting current at the end of the step
    stepAvgLastPoint = int(len(trace2) - len(trace2)*stepAvgLastFrac)
    Istep = np.mean(trace2[stepAvgLastPoint:])
    Idelta = abs(Ih - Istep)
    log.debug(f"dI={Idelta} pA")

    # V=I*R, R=V/I, R=dV/dI
    Rm = (abs(dV)*(1e-3)) / (Idelta*(1e-12))*(1e-6)
    log.debug(f"Rm={Rm} MOhm")

    # To prepare for curve fitting, make negative steps look positive.
    if (dV < 0):
        trace2 *= -1
        Istep *= -1

    # To prepare for curve fitting, isolate just the fast transient
    trace2 = trace2[:abf.dataPointsPerMs*50]

    # Start the trace at the peak
    tracePeak = np.max(trace2)
    tracePeakPos = np.where(trace2 == tracePeak)[0][0]
    trace2 = trace2[tracePeakPos:]

    # Subtract the trace so it terminates at zero
    trace2 -= Istep

    # cut off the trace where it hits zero
    zeroI = np.where(trace2 <= 0)[0]
    if len(zeroI):
        zeroI = zeroI[0]
        trace2 = trace2[:zeroI]

    # Start and end the trace at certain fractions of its height
    upperFracVal = fitToFracUpper*trace2[0]
    upperI = np.where(trace2 < upperFracVal)[0][0]
    fitThis = trace2[upperI:]
    fitThisXs = np.arange(len(fitThis))

    # do a curve fit with successive approximation
    tau = _tauMonoExpFit(fitThis, abf.dataRate)
    tauMs = tau*1000
    log.debug(f"Tau={tauMs} ms")

    # regenerate fitted curve, allowing it to go negative
    fittedXs = np.arange(len(fitThis)+upperI)-upperI
    fitted = np.exp((-fittedXs/abf.dataRate)/tau)*fitThis[0]
    I0 = fitted[0]
    log.debug(f"I0={I0} pA")

    # Calculated Ra using I0 from the curve-fitted peak (Ra = dV/I0)
    Ra = ((dV*(1e-3)) / (I0*(1e-12)))*(1e-6)
    Ra = abs(Ra)
    log.debug(f"Ra={Ra} MOhm")

    # Calculate capactance using our curve-fitted tau
    Cm = (tau/(Ra*(1e6)))*(1e12)
    log.debug(f"Cm={Cm} pF")

    return [Ih, Rm, Ra, Cm]


def _cm_step_points_and_voltages(abf):
    """
    Return [stepPoints,stepVoltages] if the sweep contains a step suitable for 
    capacitance calculation using the first square step from holding command.
    """
    assert isinstance(abf, pyabf.ABF)

    if abf.sweepUnitsY != "pA":
        log.critical("must be in voltage clamp configuration")
        return

    epochTypes = abf._epochPerDacSection.nEpochType
    if epochTypes.count(1) == 0:
        log.critical("protocol must have at least 1 step")
        return

    # get epoch time and clamp information
    epochValues = pyabf.stimulus.epochValues(abf)
    epochValues = epochValues[abf.sweepNumber]

    # find the first step epoch that deviates from holding voltage
    voltageBeforeStep = abf.holdingCommand[abf.sweepChannel]
    for epochNumber, epochType in enumerate(epochTypes):
        voltageAfterStep = epochValues[epochNumber]
        if epochType == 1 and voltageAfterStep != voltageBeforeStep:
            break
    else:
        log.critical("no step from holding voltage found")
        return
    stepVoltages = [voltageBeforeStep, voltageAfterStep]
    log.debug(f"step voltages (mV): {stepVoltages}")

    # determine the index points encapsulating the step
    stepPoints = pyabf.stimulus.epochPoints(abf)[:epochNumber+1]
    if len(stepPoints) == 1:
        stepPoints = [0, stepPoints[0]]
    stepDurations = abf._epochPerDacSection.lEpochInitDuration
    stepPoints.append(stepPoints[-1]+stepDurations[epochNumber])
    log.debug(f"points encapsulating step: {stepPoints}")

    return [stepPoints, stepVoltages]


if __name__ == "__main__":
    abfFilesToTest = []
    abfFilesToTest.append(PATH_DATA+"/model_vc_step.abf")
    abfFilesToTest.append(PATH_DATA+"/171116sh_0011.abf")
    abfFilesToTest.append(PATH_DATA+"/18808025.abf")
    abfFilesToTest.append(PATH_DATA+"/2018_08_23_0009.abf")
    abfFilesToTest.append(PATH_DATA+"/171116sh_0012.abf")

    for abfFile in abfFilesToTest:
        abf = pyabf.ABF(abfFile)
        print()
        print(cm_step_summary(abf))
    plt.show()
