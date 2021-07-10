"""
This file contains methods which calculate passive membrane properties from
voltage-clamp sweeps. These methods are not optimized for speed or accuracy
and are only provided for backwards compatibility. pyabf is intended to be
used just for reading ABF files, and users are encouraged to write their own
python code to perform analysis of ABF data.

This URL has useful discussion and code for calculating membrane properties:
https://swharden.com/blog/2020-10-11-model-neuron-ltspice
"""

import pyabf
import numpy as np


def _cm_ramp_points_and_voltages(abf):
    """
    Return [points, voltages] if the sweep contains a ramp suitable for 
    capacitance calculation using a matching doward and upward ramp.
    points is a list of 3 numbers depicting index values important to this
    ramp. The first number is the index at the start of the downward ramp, the
    second is the index of its nadir, and the third is the index where it
    returns to the original level.
    voltages is a list of 2 numbers: voltage before and during the ramp.
    """
    assert isinstance(abf, pyabf.ABF)

    if abf.sweepUnitsY != "pA":
        raise Exception("must be in voltage clamp configuration")

    for i, p1 in enumerate(abf.sweepEpochs.p1s):
        if i == 0:
            continue

        # ensure this sweep and the last are both ramps
        if abf.sweepEpochs.types[i] != "Ramp":
            continue
        if abf.sweepEpochs.types[i-1] != "Ramp":
            continue

        # ensure the levels are different
        if abf.sweepEpochs.levels[i] == abf.sweepEpochs.levels[i-1]:
            continue

        ptStart = abf.sweepEpochs.p1s[i-1]
        ptTransition = abf.sweepEpochs.p1s[i]
        ptEnd = abf.sweepEpochs.p2s[i]
        points = [ptStart, ptTransition, ptEnd]

        voltageBefore = abf.sweepEpochs.levels[i-1]
        voltageDuring = abf.sweepEpochs.levels[i]
        voltages = [voltageBefore, voltageDuring]

        return [points, voltages]

    return None


def currentSweepRamp(abf):
    """
    Calculate capacitance from a voltage clamp ramp.
    In theory any channel, any ramp, and even changing ramps will work.
    This expects a downward ramp followed by an upward ramp, each with the same
    duration and magnitude. This ramp can be anywhere in the sweep, and does
    not have to be the first epoch.
    """
    assert isinstance(abf, pyabf.ABF)
    cmInfo = _cm_ramp_points_and_voltages(abf)
    if not cmInfo:
        return np.nan
    rampPoints, rampVoltages = cmInfo
    deltaVoltage = rampVoltages[1]-rampVoltages[0]
    rampData = abf.sweepY[rampPoints[0]:rampPoints[2]]
    rampData = np.array(rampData)
    cm = _cm_ramp_calculate(rampData, abf.dataRate, deltaVoltage)
    cmAvg = np.mean(cm)
    return cm


def _cm_ramp_calculate(rampData, sampleRate, deltaVoltage, centerFrac=.3):
    """
    Given a v-shaped current trace in response to a symmetric voltage-clamp 
    ramp (its magnitude given by deltaVoltage), calculate and return the
    capacitance of the cell. Data units must be in pA, sampleRate in points/sec,
    and voltage in mV. Positive (upward) or negative (V-shaped) ramps are okay.
    centerFrac is the fractional time span to draw data from in the center of
    each ramp.
    """

    # ensure our values are of the correct types
    rampData = np.array(rampData)
    sampleRate = int(sampleRate)
    deltaVoltage = float(deltaVoltage)

    # isolate and rearrange the downward vs upward slopes
    trace1 = rampData[:int(len(rampData)/2)][::-1]
    trace2 = rampData[int(len(rampData)/2):]
    traceAvg = np.average((trace1, trace2), axis=0)
    if not len(trace1) == len(trace2):
        raise Exception("rampData length must be an even multiple of 2")

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

    # capacitance is always positive
    cm = np.abs(cm)

    # units don't require conversion, because pA is appropriately scaled for pF
    return cm


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


def currentSweepStep(abf):
    """
    Returns [Ih, Rm, Ra, Cm] from a step protocol of the current sweep.
    """
    assert isinstance(abf, pyabf.ABF)
    memTestFailResult = [np.nan]*4
    stepInfo = _step_points_and_voltages(abf)
    if not stepInfo:
        return memTestFailResult
    stepPoints, stepVoltages = stepInfo
    trace = abf.sweepY[stepPoints[0]:stepPoints[2]]
    trace = np.array(trace)
    traceStepPoint = stepPoints[1]-stepPoints[0]
    dV = stepVoltages[1]-stepVoltages[0]
    try:
        Ih, Rm, Ra, Cm = _step_calculate(abf, trace, traceStepPoint, dV=dV)
        return [Ih, Rm, Ra, Cm]
    except:
        print("ERROR: memtest failed on sweep", abf.sweepNumber)
        return memTestFailResult


def _step_calculate(abf, trace, traceStepPoint, dV=-10, stepAvgLastFrac=.2,
                    fitToFracUpper=.9):
    """
    Given a current trace depicting the resposne to a hyperpolarizing square 
    pulse voltage step, return membrane test information Ih, Rm, Ra, and Cm.
    A typical use is to give a trace which starts clamped at -70 mV, then gets
    clamped to -80 mV. The traceStepPoint is the index value at which the
    transition between -70 and -80 occurs.
    stepAvgLastFrac - defines what percentage of the end of the step to measure
    to calculate resting current.
    dV - step voltage change (mV)
    """
    assert isinstance(abf, pyabf.ABF)

    trace1 = trace[:traceStepPoint]
    trace2 = trace[traceStepPoint:]

    # calculate the holding current (assume we are starting there)
    Ih = np.mean(trace1)

    # calculate the resting current at the end of the step
    stepAvgLastPoint = int(len(trace2) - len(trace2)*stepAvgLastFrac)
    Istep = np.mean(trace2[stepAvgLastPoint:])
    Idelta = abs(Ih - Istep)

    # V=I*R, R=V/I, R=dV/dI
    Rm = (abs(dV)*(1e-3)) / (Idelta*(1e-12))*(1e-6)

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

    # regenerate fitted curve, allowing it to go negative
    fittedXs = np.arange(len(fitThis)+upperI)-upperI
    fitted = np.exp((-fittedXs/abf.dataRate)/tau)*fitThis[0]
    I0 = fitted[0]

    # Calculated Ra using I0 from the curve-fitted peak (Ra = dV/I0)
    Ra = ((dV*(1e-3)) / (I0*(1e-12)))*(1e-6)
    Ra = abs(Ra)

    # Calculate capacitance using our curve-fitted tau
    Cm = (tau/(Ra*(1e6)))*(1e12)

    return [Ih, Rm, Ra, Cm]


def _step_points_and_voltages(abf):
    """
    Return [stepPoints,stepVoltages] if the sweep contains a step suitable for 
    capacitance calculation using the first square step from holding command.
    stepPoints is a list of 3 numbers depicting index values important to this
    step. Typically the first number is the index of the trace clamped at -70, 
    the second number is index of the trace where it gets clamped to -80, and
    the final number is the index after settling at -80 for a while.
    stepVoltages is a list of 2 numbers: voltage before and during the step.
    """
    assert isinstance(abf, pyabf.ABF)

    if abf.sweepUnitsY != "pA":
        raise Exception("must be in voltage clamp configuration")

    for i, p1 in enumerate(abf.sweepEpochs.p1s):
        if i == 0:
            continue
        if abf.sweepEpochs.types[i] != "Step":
            continue
        if abf.sweepEpochs.levels[i] == abf.sweepEpochs.levels[i-1]:
            continue

        ptStart = abf.sweepEpochs.p1s[i-1]
        ptTransition = abf.sweepEpochs.p1s[i]
        ptEnd = abf.sweepEpochs.p2s[i]
        stepPoints = [ptStart, ptTransition, ptEnd]

        voltageBeforeStep = abf.sweepEpochs.levels[i-1]
        voltageDuringStep = abf.sweepEpochs.levels[i]
        stepVoltages = [voltageBeforeStep, voltageDuringStep]

        return [stepPoints, stepVoltages]

    return None
