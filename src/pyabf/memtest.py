"""
Code here relates to the detection of cell membrane properties.

This includes:
  Ih (holding current)
  Ra (access resistance)
  Rm (membrane resistance)
  Cm (membrane capacitance)
  Tau (time constant)

"""

import numpy as np
import pyabf


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
    Return [rampPoints,rampVoltages] if the sweep contains a ramp
    suitable for capacitance calculation.
    """
    assert isinstance(abf, pyabf.ABF)

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

    return [rampPoints, rampVoltages]


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
    out += "Rm = %.02f +/- %.02f pA\n" % (np.mean(Rms), np.std(Rms))
    out += "Ra = %.02f +/- %.02f pA\n" % (np.mean(Ras), np.std(Ras))
    out += "Cm = %.02f +/- %.02f pA" % (np.mean(Cms), np.std(Cms))
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
    stepInfo = _step_points_and_voltages(abf)
    if not stepInfo:
        log.warn(f"{abf.abfID} sweep {abf.sweepNumber} couldnt be measured")
        return np.nan
    stepPoints, stepVoltages = stepInfo
    trace = abf.sweepY[stepPoints[0]:stepPoints[2]]
    traceStepPoint = stepPoints[1]-stepPoints[0]
    dV = stepVoltages[1]-stepVoltages[0]
    Ih, Rm, Ra, Cm = _step_calculate(abf, trace, traceStepPoint, dV=dV)
    log.info(f"Ih: {Ih}, Rm: {Rm}, Ra: {Ra}, Cm: {Cm}")
    return [Ih, Rm, Ra, Cm]


def _step_calculate(abf, trace, traceStepPoint, dV=-10, stepAvgLastFrac=.2,
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


def _step_points_and_voltages(abf):
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
