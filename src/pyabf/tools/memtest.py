"""
Code here relates to the detection of cell membrane properties.

This includes:
  Ih (holding current)
  Ra (access resistance)
  Rm (membrane resistance)
  Cm (membrane capacitance)
  Tau (time constant)

Note:
Expected values for 2018_08_23_0009.abf are:
    Ih: -134.365 pA
    Ra: 14.936 MOhm
    Rm: 122.472 MOhm
    Cm (step): 135.111 pF
    Cm (ramp): 170.719 pF
"""

import os
import sys
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_DATA = os.path.abspath(PATH_HERE+"../../../../data/abfs/")
PATH_SRC = os.path.abspath(PATH_HERE+"../../../")
sys.path.insert(0, PATH_SRC)
import pyabf

import numpy as np

import logging
logging.basicConfig(level=logging.WARNING)
log = logging.getLogger(__name__)


def cm_ramp_summary(abf):
    """return average Cm as a string like 'Cm = 34.56 +/- 3.21 pF'"""
    cms = cm_ramp_valuesBySweep(abf)
    mean = np.mean(cms)
    stdev = np.std(cms)
    return "Cm = %.02f +/- %.02f pF" % (mean, stdev)


def cm_ramp_valuesBySweep(abf):
    """
    return an array of membrane capacitance values calculated from the ramp 
    found in every sweep in the abf.
    """
    assert isinstance(abf, pyabf.ABF)
    cms = np.full(abf.sweepCount, np.nan)
    for sweepNumber in abf.sweepList:
        abf.setSweep(sweepNumber)
        cms[sweepNumber] = _cm_ramp_fromThisSweep(abf)
    log.info(f"%s has a capacitance of %.02f +/- %.02f pF" %
             (abf.abfID, np.mean(cms), np.std(cms)))
    return cms


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
        log.critical("must be in voltage clamp configuration")
        return

    for i, p1 in enumerate(abf.sweepEpochs.p1s):
        if i==0:
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

    log.critical("ABF must have at least 2 voltage ramps to use memtest")
    return None


def _cm_ramp_fromThisSweep(abf):
    """
    Calculate capacitance from a voltage clamp ramp.

    In theory any channel, any ramp, and even changing ramps will work.

    This expects a downward ramp followed by an upward ramp, each with the same
    duration and magnitude. This ramp can be anywhere in the sweep, and does
    not have to be the first epoch.
    """
    assert isinstance(abf, pyabf.ABF)
    log.debug(f"calculating Cm from ramp on {abf.abfID}.abf")
    cmInfo = _cm_ramp_points_and_voltages(abf)
    if not cmInfo:
        log.debug("ABF file has improper Cm ramp")
        return np.nan
    rampPoints, rampVoltages = cmInfo
    deltaVoltage = rampVoltages[1]-rampVoltages[0]
    rampData = abf.sweepY[rampPoints[0]:rampPoints[2]]
    rampData = np.array(rampData)
    cm = _cm_ramp_calculate(rampData, abf.dataRate, deltaVoltage)
    cmAvg = np.mean(cm)
    log.debug(f"Avareage Cm detected as: {cmAvg} pF")
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

    msg = f"analyzing Cm ramp (centerfrac={centerFrac}) "
    msg += f"sample ({len(rampData)} points) at {sampleRate} Hz "
    msg += f"with dV={deltaVoltage}"
    log.debug(msg)

    # ensure our values are of the correct types
    rampData = np.array(rampData)
    sampleRate = int(sampleRate)
    deltaVoltage = float(deltaVoltage)

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


def step_summary(abf):
    """
    Return a message displaying average stats
    formatted like 'Cm = 34.56 +/- 3.21 pF'
    """
    Ihs, Rms, Ras, Cms = step_valuesBySweep(abf)
    out = ""
    out += "Ih = %.02f +/- %.02f pA\n" % (np.mean(Ihs), np.std(Ihs))
    out += "Rm = %.02f +/- %.02f MOhm\n" % (np.mean(Rms), np.std(Rms))
    out += "Ra = %.02f +/- %.02f MOhm\n" % (np.mean(Ras), np.std(Ras))
    out += "Cm = %.02f +/- %.02f pF" % (np.mean(Cms), np.std(Cms))
    return out


def step_valuesBySweep(abf):
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
        Ih, Rm, Ra, Cm = _step_fromThisSweep(abf)
        Ihs[sweepNumber] = Ih
        Rms[sweepNumber] = Rm
        Ras[sweepNumber] = Ra
        Cms[sweepNumber] = Cm

    return [Ihs, Rms, Ras, Cms]


def _step_fromThisSweep(abf):
    """returns [Ih, Rm, Ra, Cm]"""
    assert isinstance(abf, pyabf.ABF)
    memTestFailResult = [np.nan]*4
    stepInfo = _step_points_and_voltages(abf)
    if not stepInfo:
        log.warn(f"{abf.abfID} sweep {abf.sweepNumber} couldnt be measured (odd sweep info)")
        return memTestFailResult
    stepPoints, stepVoltages = stepInfo
    trace = abf.sweepY[stepPoints[0]:stepPoints[2]]
    trace = np.array(trace)
    traceStepPoint = stepPoints[1]-stepPoints[0]
    dV = stepVoltages[1]-stepVoltages[0]
    try:
        Ih, Rm, Ra, Cm = _step_calculate(abf, trace, traceStepPoint, dV=dV)
        log.info(f"Ih: {Ih}, Rm: {Rm}, Ra: {Ra}, Cm: {Cm}")
        return [Ih, Rm, Ra, Cm]
    except:
        log.warn(f"{abf.abfID} sweep {abf.sweepNumber} couldnt be measured (exception in memtest)")
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
        log.critical("must be in voltage clamp configuration")
        return

    for i, p1 in enumerate(abf.sweepEpochs.p1s):
        if i==0:
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

    log.critical("ABF must have at least 1 voltage step to use memtest")
    return None