"""
Code here stores automatic analysis routines for ABF files given their protocol.

There are several analysis routines which are general (show all sweeps 
continuously, show sweeps stacked, show sweeps overlayed, etc) and can be used
for almost any protocol (or ABFs with unknown protocol).

Some analysis routines are specific for specific protocols.

These routines are highly specific to the nature of the scientific work I do,
and this document may not be useful to others beyond an example of how to use
pyABF to set-up an automatic analysis pipeline for electrophysiology data.
"""

import os
import pyabf
import numpy as np
import matplotlib.pyplot as plt

import logging
log = logging.getLogger(__name__)
log.debug(f"autoabf imported")
log.setLevel(level=logging.WARN)

# default size of the images being made
FIGSIZE = pyabf.plot.defaultFigsize
FIGSIZE_WIDE = (FIGSIZE[0]*1.6, FIGSIZE[1]*1)

# automatically generated figures are saved in this subfolder
from abfnav import DATAFOLDER

# Little operations to apply on graphs


def _secLookUp(abf, timeSec1, timeSec2, returnPoints=False):
    """returns tangible times in seconds."""
    assert isinstance(abf, pyabf.ABF)
    if timeSec1 is None:
        timeSec1 = 0
    if timeSec2 is None:
        timeSec2 = abf.sweepLengthSec
    if returnPoints:
        return int(timeSec1*abf.dataRate), int(timeSec2*abf.dataRate)
    else:
        return timeSec1, timeSec2


def shadeDigitalOutput(abf, digitalOutputChannel=4):
    """In sweep view, shade the epoch number."""
    digitalWaveforms = pyabf.stimulus.digitalWaveformEpochs(abf)
    epochPoints = pyabf.stimulus.epochPoints(abf)
    outputStateByEpoch = digitalWaveforms[digitalOutputChannel]
    for epochNumber, outputState in enumerate(outputStateByEpoch):
        if outputState == 1:
            t1 = epochPoints[epochNumber]*abf.dataSecPerPoint
            t2 = epochPoints[epochNumber+1]*abf.dataSecPerPoint
            plt.axvspan(t1, t2, color='r', alpha=.3, lw=0)


def shadeAllBackgrounds(color=(1.0, 1.0, 0.9)):
    """make the background color a certain color for every subplot."""
    for i, ax in enumerate(plt.gcf().axes):
        ax.set_facecolor(color)


def addComments(abf):
    """
    Call on a graph with a horizontal time in seconds to add vertical lines and
    labels to every abf comment.
    """
    assert isinstance(abf, pyabf.ABF)
    if not abf.tagComments:
        return
    for comment, timeSec in zip(abf.tagComments, abf.tagTimesSec):
        plt.axvline(timeSec, color='r', lw=2, alpha=.5, ls='--')
        X1, X2, Y1, Y2 = plt.axis()
        Y2 = Y2-abs(Y2-Y1)*.02
        plt.text(timeSec, Y2, comment, color='r', rotation='vertical',
                 ha='right', va='top', weight='bold', alpha=.5, size=8)

### Code here acts on the active matplotlib figure or subplot ###


def plotFigNew(abf, figsize=FIGSIZE):
    """create a figure"""
    plt.figure(figsize=figsize)
    return


def plotFigSave(abf, tag="", tight=True, closeToo=True, grid=True,
                unknown=False, title=None, labelAxes=True):
    """save a figure"""
    assert isinstance(abf, pyabf.ABF)

    # apply title only to single-subplot figures
    if len(plt.gcf().axes) == 1:
        if title:
            plt.title(title)

    if labelAxes:
        plt.ylabel(abf.sweepLabelY)
        plt.xlabel(abf.sweepLabelX)

    # apply a grid to all subplots
    if grid:
        for i, ax in enumerate(plt.gcf().axes):
            ax.grid(alpha=.5, ls="--")

    # decorate unknown plots in a special way
    shade_unknown_graphs = True
    if unknown:
        abf.protocol = abf.protocol + "(UNKNOWN)"
        protocolColor = "r"
    if unknown and shade_unknown_graphs:
        for i, ax in enumerate(plt.gcf().axes):
            ax.set_facecolor((1.0, 0.9, 0.9))
    else:
        protocolColor = '.5'

    # optionally tight
    if tight:
        plt.tight_layout()

    # add text to the lower corner
    plt.gcf().text(0.005, 0.005, f"{abf.abfID}\n{abf.protocol}",
                   transform=plt.gca().transAxes, fontsize=10,
                   verticalalignment='bottom', family='monospace',
                   color=protocolColor)

    abfDir = os.path.dirname(abf.abfFilePath)
    fnOut = abf.abfID+"_"+tag+".png"
    pathOut = os.path.join(abfDir, DATAFOLDER, fnOut)
    if not os.path.exists(os.path.dirname(pathOut)):
        log.info(f"creating {os.path.dirname(pathOut)}")
        os.mkdir(os.path.dirname(pathOut))
    log.debug(f"saving {fnOut}")
    plt.savefig(pathOut)
    if closeToo:
        plt.close()
    return

# Code here indicates how to make common graphs


def generic_ap_steps(abf):
    """Create a plot for generic AP steps."""
    assert isinstance(abf, pyabf.ABF)
    plotFigNew(abf)

    # all sweeps overlayed
    axOvr = plt.gcf().add_subplot(2, 2, 1)
    pyabf.plot.sweeps(abf, axis=axOvr, alpha=.5)
    axOvr.set_title(f"Sweep Overlay")

    # all sweeps stacked
    axStack = plt.gcf().add_subplot(2, 2, 2)
    pyabf.plot.sweeps(abf, axis=axStack, alpha=.5, offsetYunits=100)
    axStack.set_title(f"Sweeps Stacked")

    # first sweep with APs
    axAp = plt.gcf().add_subplot(2, 2, 3)
    p1, p2 = _secLookUp(abf, 0, 1, True)
    for sweep in abf.sweepList:
        abf.setSweep(sweep)
        if np.max(abf.sweepY[p1:p2]) > 10:
            break
    pyabf.plot.sweeps(abf, sweepNumbers=[abf.sweepNumber], axis=axAp, alpha=1)
    axAp.axis([p1/abf.dataRate, p2/abf.dataRate, None, None])
    axAp.set_title(f"First Action Potential")

    # AP gain curve
    axGain = plt.gcf().add_subplot(2, 2, 4)

    for epochNumber, color in zip([1, 4], ['C0', 'C1']):
        currents = pyabf.stimulus.epochValues(abf)[:, epochNumber]
        epochSec1 = pyabf.stimulus.epochPoints(abf)[epochNumber]/abf.dataRate
        epochSec2 = pyabf.stimulus.epochPoints(abf)[epochNumber+1]/abf.dataRate
        [apFreqInBin, apFreqFirst] = pyabf.ap.ap_freq_per_sweep(
            abf, epochNumber)
        axGain.plot(currents, apFreqInBin, '.-', color=color)
        axGain.plot(currents, apFreqFirst, '.:', color=color)
        axStack.axvspan(epochSec1, epochSec2, color=color, alpha=.1)
    axGain.set_title(f"AP Gain Curve")
    axGain.set_ylabel("AP Frequency (Hz)")
    axGain.set_xlabel("Applied Current (pA)")
    axGain.axhline(40, color='r', alpha=.2, ls='--', lw=2)
    plotFigSave(abf, tag="generic-overlay", labelAxes=False)


def generic_iv(abf, timeSec1, timeSec2, sweepStepMv, firstSweepMv, filter=True):
    """Create a graph plotting the I/V between two points."""

    # enable lowpass filter
    if filter:
        pyabf.filter.gaussian(abf, 2)

    # measure currents for each step
    currentAvg = pyabf.stats.rangeAverage(abf, timeSec1, timeSec2)
    currentErr = pyabf.stats.rangeStdev(abf, timeSec1, timeSec2)
    voltage = np.arange(abf.sweepCount)*sweepStepMv+firstSweepMv

    plotFigNew(abf, figsize=FIGSIZE_WIDE)  # double wide
    ax1 = plt.gcf().add_subplot(1, 2, 1)
    ax2 = plt.gcf().add_subplot(1, 2, 2)

    # create the overlay figure
    pyabf.plot.sweeps(abf, axis=ax1, linewidth=2, alpha=.8)
    ax1.axvspan(timeSec1, timeSec2, color='r', alpha=.1)
    ax1.set_title(f"{abf.abfID} I/V Source Sweeps")
    dY = (np.nanmax(currentAvg) - np.nanmin(currentAvg))*.2
    ax1.axis([None, None, np.nanmin(currentAvg)-dY, np.nanmax(currentAvg)+dY])

    # create the IV curve
    ax2.axhline(0, ls='--', alpha=.5, color='k')
    ax2.axvline(-70, ls='--', alpha=.5, color='k')
    ax2.plot(voltage, currentAvg, '.-', lw=2, ms=20)
    ax2.set_ylabel("Current (pA)")
    ax2.set_xlabel("Voltage (mV)")
    ax2.set_title(f"{abf.abfID} I/V Relationship")

    plotFigSave(abf, tag="IV")


def generic_overlay(abf, color=None, unknown=False, alpha=None):
    """plot every sweep semi-transparent on top of the next."""
    assert isinstance(abf, pyabf.ABF)
    plotFigNew(abf)
    for channel in abf.channelList:
        ax = plt.gcf().add_subplot(abf.channelCount, 1, channel+1)
        pyabf.plot.sweeps(abf, axis=ax, color=color,
                          channel=channel, alpha=alpha)
        ax.set_title(f"{abf.abfID} (Ch{channel+1}) Sweep Overlay")
    plotFigSave(abf, tag="generic-overlay", unknown=unknown)
    return


def generic_continuous(abf, unknown=False, alpha=1):
    """plot every sweep continuously through time."""
    assert isinstance(abf, pyabf.ABF)
    plotFigNew(abf)
    for channel in abf.channelList:
        ax = plt.gcf().add_subplot(abf.channelCount, 1, channel+1)
        pyabf.plot.sweeps(abf, axis=ax, continuous=True,
                          channel=channel, color='b', alpha=alpha,
                          linewidth=.5)
        ax.set_title(f"{abf.abfID} (Ch{channel+1}) Continuous Signal")
        addComments(abf)
    plotFigSave(abf, tag="generic-continuous", unknown=unknown)
    return


def generic_first_sweep(abf, timeSec1=None, timeSec2=None):
    """plot every sweep continuously through time."""
    assert isinstance(abf, pyabf.ABF)
    plotFigNew(abf)
    for channel in abf.channelList:
        ax = plt.gcf().add_subplot(abf.channelCount, 1, channel+1)
        pyabf.plot.sweeps(abf, sweepNumbers=[0], axis=ax,
                          channel=channel, color='b', alpha=1,
                          startAtSec=timeSec1, endAtSec=timeSec2)
        ax.set_title(f"{abf.abfID} (Ch{channel+1}) First Sweep")
    plotFigSave(abf, tag="generic-first-sweep")
    return


def generic_average_over_time(abf, timeSec1=None, timeSec2=None):
    """plot the average of every sweep continuously through time."""
    assert isinstance(abf, pyabf.ABF)
    plotFigNew(abf)
    for channel in abf.channelList:
        ax = plt.gcf().add_subplot(abf.channelCount, 1, channel+1)
        sweepTimes = np.arange(abf.sweepCount)*abf.sweepLengthSec
        sweepAvgs = pyabf.stats.rangeAverage(
            abf, timeSec1, timeSec2, channel=channel)
        sweepErr = pyabf.stats.rangeStdev(
            abf, timeSec1, timeSec2, channel=channel)
        ax.errorbar(sweepTimes, sweepAvgs, sweepErr,
                    ms=10, marker='.', ls='-', capsize=5)
        timeNote = "%.02f - %.02f sec" % (_secLookUp(abf, timeSec1, timeSec2))
        ax.set_title(f"{abf.abfID} (Ch{channel+1}) [{timeNote}]")
        addComments(abf)
    plotFigSave(abf, tag=f"generic-average-over-time")
    return


def generic_paired_pulse(abf, p1sec1, p1sec2, p2sec1, p2sec2):
    """single pulse or paired pulse analysis."""
    assert isinstance(abf, pyabf.ABF)
    sweepTimes = np.arange(abf.sweepCount)*abf.sweepLengthSec

    # PULSE 1
    plotFigNew(abf)
    ax = plt.gcf().add_subplot(2, 1, 1)
    sweepAvgs1 = pyabf.stats.rangeAverage(abf, p1sec1, p1sec2)
    sweepErr1 = pyabf.stats.rangeStdev(abf, p1sec1, p1sec2)
    ax.errorbar(sweepTimes, sweepAvgs1, sweepErr1, ms=10,
                marker='.', ls='-', capsize=5, color='r')
    timeNote = "%.02f - %.02f sec" % (_secLookUp(abf, p1sec1, p1sec2))
    ax.set_title(f"{abf.abfID} Pulse 1 [{timeNote}]")
    ax.set_ylabel(abf.sweepLabelY)
    ax.set_xlabel(abf.sweepLabelX)
    addComments(abf)

    # PULSE 2
    ax = plt.gcf().add_subplot(2, 1, 2)
    sweepAvgs2 = pyabf.stats.rangeAverage(abf, p2sec1, p2sec2)
    sweepErr2 = pyabf.stats.rangeStdev(abf, p2sec1, p2sec2)
    ax.errorbar(sweepTimes, sweepAvgs1, sweepErr2, ms=10,
                marker='.', ls='-', capsize=5, color='r')
    timeNote = "%.02f - %.02f sec" % (_secLookUp(abf, p2sec1, p2sec2))
    ax.set_title(f"{abf.abfID} Pulse 1 [{timeNote}]")
    addComments(abf)
    ax.set_ylabel(abf.sweepLabelY)
    ax.set_xlabel(abf.sweepLabelX)
    plotFigSave(abf, tag=f"generic-paired-pulses", labelAxes=False)

    # RATIO
    plotFigNew(abf)
    ax = plt.gcf().add_subplot(1, 1, 1)  # pulse2/pulse1 ratio
    ratioAvg = sweepAvgs2/sweepAvgs1
    # how should this be measured?
    ratioErr = np.sqrt(np.power(sweepErr1, 2)+np.power(sweepErr2, 2))
    ratioErr = sweepErr2*np.nan
    ax.errorbar(sweepTimes, ratioAvg, ratioErr, ms=20,
                marker='.', ls='-', capsize=5, color='r')
    ax.set_title(f"{abf.abfID} Paired Pulse Ratio [p2/p1]")
    addComments(abf)
    ax.set_ylabel(abf.sweepLabelY)
    ax.set_xlabel(abf.sweepLabelX)
    plotFigSave(abf, tag=f"generic-paired-pulse-ratio", labelAxes=False)

    return

# Code defines which routines or generic graphs to use for each protocol


def unknown(abf):
    """unknown protocol."""
    assert isinstance(abf, pyabf.ABF)
    totalLengthSec = abf.sweepCount*abf.sweepLengthSec
    if abf.sweepLengthSec < 10 and totalLengthSec < 60*2:
        generic_overlay(abf, unknown=True)
    else:
        generic_continuous(abf, unknown=True)
        generic_average_over_time(abf)


def protocol_0111(abf):
    """0111 continuous ramp.pro"""
    assert isinstance(abf, pyabf.ABF)
    msToPlot = 20
    ptToPlot = msToPlot*abf.dataPointsPerMs
    abf.setSweep(0)
    segY = abf.sweepY[0:ptToPlot]
    timeAPsec = 0

    # isolate the 1st AP we find
    for sweep in abf.sweepList:
        abf.setSweep(sweep)
        apPoints = pyabf.ap.ap_points_currentSweep(abf)
        # ignore APs close to the start of the sweep
        apPoints = [x for x in apPoints if x > ptToPlot]
        if len(apPoints):
            pt1 = int(apPoints[0]-ptToPlot/2)
            segY = abf.sweepY[pt1:pt1+ptToPlot]
            timeAPsec = apPoints[0]/abf.dataRate+sweep*abf.sweepLengthSec
            break

    # prepare the first derivative and X units
    segYd = np.diff(segY)
    segYd = np.append(segYd, segYd[-1])
    segYd = segYd * abf.dataRate / 1000
    segX = np.arange(len(segYd))-len(segYd)/2
    segX = segX/abf.dataRate*1000

    plotFigNew(abf)

    # plot the first AP (mV)
    ax1 = plt.gcf().add_subplot(2, 2, 1)
    pyabf.plot.sweeps(abf, continuous=True, axis=ax1,
                      linewidth=1, color='C0', alpha=1)
    zoomSec = .25
    ax1.set_title("First AP: Voltage")
    ax1.axis([timeAPsec-zoomSec, timeAPsec+zoomSec, None, None])

    # plot the first AP (V/sec)
    ax2 = plt.gcf().add_subplot(2, 2, 2)
    ax2.set_title("First AP: Velocity")
    ax2.set_ylabel("Velocity (mV/ms)")
    ax2.set_xlabel("time (ms)")
    ax2.axhline(-100, color='k', ls=':', lw=2, alpha=.2)
    ax2.plot(segX, segYd, color='r')
    ax2.margins(0, .05)

    # plot the whole ABF
    ax3 = plt.gcf().add_subplot(2, 2, 3)
    pyabf.plot.sweeps(abf, continuous=True, axis=ax3,
                      linewidth=1, color='C0', alpha=1)
    zoomSec = .25
    ax3.set_title("Full Signal")
    ax3.margins(0, .05)

    # plot the first AP (V/sec)
    ax4 = plt.gcf().add_subplot(2, 2, 4)
    ax4.set_title("First AP: Phase Plot")
    ax4.set_xlabel("Membrane Potential (mV)")
    ax4.set_ylabel("Velocity (mV/ms)")
    ax4.plot(segY, segYd, '.-', color='C1')
    ax4.margins(.1, .1)
    ax4.axis([ax1.axis()[2], ax1.axis()[3], ax2.axis()[2], ax2.axis()[3]])
    plotFigSave(abf, tag=f"rampAP", labelAxes=False)


def protocol_0112(abf):
    """0112 steps dual -50 to 150 step 10.pro"""
    assert isinstance(abf, pyabf.ABF)
    generic_ap_steps(abf)
    return


def protocol_0113(abf):
    """0113 steps dual -100 to 300 step 25.pro"""
    assert isinstance(abf, pyabf.ABF)
    generic_ap_steps(abf)
    return


def protocol_0114(abf):
    """0114 steps dual -100 to 2000 step 100.pro"""
    assert isinstance(abf, pyabf.ABF)
    generic_ap_steps(abf)
    return


def protocol_0121(abf):
    """0121 IC sine sweep 0 +- 20 pA.pro"""
    assert isinstance(abf, pyabf.ABF)
    generic_overlay(abf)
    return


def protocol_0201(abf):
    """0201 memtest.pro"""
    assert isinstance(abf, pyabf.ABF)

    if 2 in abf._epochPerDacSection.nEpochType:
        plotFigNew(abf)

        # plot the memtest
        ax1 = plt.gcf().add_subplot(121)
        pyabf.plot.sweeps(abf, axis=ax1)
        ax1.set_title("MemTest (with ramp)")

        # plot the ramp
        ax2 = plt.gcf().add_subplot(222)
        ax2.set_title("Cm Ramp (phase)")
        for sweepNumber in abf.sweepList:
            abf.setSweep(sweepNumber)
            cmInfo = pyabf.memtest._cm_ramp_points_and_voltages(abf)
            if not cmInfo:
                continue
            rampPoints, rampVoltages = cmInfo
            rampData = abf.sweepY[rampPoints[0]:rampPoints[2]]
            color = plt.get_cmap("winter")(sweepNumber/abf.sweepCount)
            trace1 = rampData[:int(len(rampData)/2)][::-1]
            trace2 = rampData[int(len(rampData)/2):]
            ax2.plot(trace1, color=color, alpha=.2)
            ax2.plot(trace2, color=color, alpha=.2)
        ax2.set_ylabel("current (pA)")
        ax2.set_xlabel("data point (index)")

        # plot the cms
        cms = pyabf.memtest.cm_ramp_valuesBySweep(abf)
        cmAvg = np.mean(cms)
        cmErr = np.std(cms)
        ax4 = plt.gcf().add_subplot(224)
        ax4.set_title("Cm = %.02f +/- %.02f pF" % (cmAvg, cmErr))
        ax4.set_ylabel("capacitance (pA)")
        ax4.set_xlabel("sweep number")
        ax4.plot(cms, '.', ms=10, alpha=.8)
        ax4.axhline(cmAvg, color='r', ls='--', lw=2, alpha=.5)
        plotFigSave(abf, tag="memtest", labelAxes=False)
    else:
        # there is no ramp
        plotFigNew(abf)
        ax1 = plt.gcf().add_subplot(111)
        pyabf.plot.sweeps(abf, axis=ax1)
        ax1.set_title("MemTest (without ramp)")
        plotFigSave(abf, tag="memtest")
    return


def protocol_0202(abf):
    """0202 IV dual"""
    assert isinstance(abf, pyabf.ABF)
    generic_iv(abf, .8, 1, 10, -110)
    return


def protocol_0203(abf):
    """0203 IV fast.pro"""
    assert isinstance(abf, pyabf.ABF)
    generic_iv(abf, .8, 1, 5, -110)
    return


def protocol_0204(abf):
    """0204 Cm ramp.pro"""
    assert isinstance(abf, pyabf.ABF)
    generic_overlay(abf, alpha=.5)
    return


def protocol_0221(abf):
    """0221 VC sine sweep 70 +- 5 mV.pro"""
    assert isinstance(abf, pyabf.ABF)
    generic_overlay(abf)
    return


def protocol_0401(abf):
    """0401 VC 2s MT-70.pro"""
    assert isinstance(abf, pyabf.ABF)
    generic_continuous(abf)
    generic_average_over_time(abf, timeSec1=1)
    return


def protocol_0402(abf):
    """0402 VC 2s MT-50.pro"""
    assert isinstance(abf, pyabf.ABF)
    generic_continuous(abf)
    generic_average_over_time(abf, timeSec1=1)
    return


def protocol_0404(abf):
    """0404 VC 2s MT2-70 ramp -110-50.pro"""
    assert isinstance(abf, pyabf.ABF)
    generic_continuous(abf)
    return


def protocol_0405(abf):
    """0404 VC 2s MT2-70 ramp -110-50.pro"""
    assert isinstance(abf, pyabf.ABF)
    generic_first_sweep(abf)
    generic_continuous(abf)
    generic_average_over_time(abf, timeSec1=1)
    return


def protocol_0406(abf):
    """0406 VC 10s MT-50.pro"""
    assert isinstance(abf, pyabf.ABF)
    generic_continuous(abf)
    return


def protocol_0409(abf):
    """0406 VC 10s MT-50.pro"""
    assert isinstance(abf, pyabf.ABF)
    generic_continuous(abf)
    generic_average_over_time(abf, 0, .4)
    return


def protocol_0501(abf):
    """0501 opto -50.pro"""
    assert isinstance(abf, pyabf.ABF)
    timeSec1, timeSec2 = 1.10, 1.30
    p1, p2 = int(timeSec1*abf.dataRate), int(timeSec2*abf.dataRate)

    # plot every sweep and the average of all sweeps
    plotFigNew(abf)
    shadeDigitalOutput(abf, 4)
    for sweep in abf.sweepList:
        abf.setSweep(sweep)
        abf.sweepY[:p1] = np.nan
        abf.sweepY[p2:] = np.nan
        plt.plot(abf.sweepX, abf.sweepY, alpha=.2, color='.5')
    avg = pyabf.sweep.averageTrace(abf, timeSec1=timeSec1, timeSec2=timeSec2)
    abf.sweepY *= np.nan
    abf.sweepY[p1:p2] = avg
    plt.plot(abf.sweepX, abf.sweepY)
    plotFigSave(abf, tag="opto-avg", labelAxes=True)

    # make stacked graph
    plotFigNew(abf)
    shadeDigitalOutput(abf, 4)
    vertOffset = False
    for sweep in abf.sweepList:
        abf.setSweep(sweep)
        if not vertOffset:
            vertOffset = np.max(abf.sweepY[p1:p2]) - np.min(abf.sweepY[p1:p2])
            vertOffset *= 1.2
        plt.plot(abf.sweepX[p1:p2], abf.sweepY[p1:p2] +
                 vertOffset*sweep, color='b', alpha=.7)
    plotFigSave(abf, tag="opto-stacked", labelAxes=True)
    return


def protocol_0912(abf):
    """0912 VC 20s stim PPR 40ms.pro"""
    assert isinstance(abf, pyabf.ABF)
    p1sec = 2.31703
    p2sec = p1sec + .05
    pulseWidth = .04
    generic_continuous(abf)
    generic_average_over_time(abf, timeSec1=5)
    generic_first_sweep(abf, 2, 3)
    generic_paired_pulse(abf, p1sec, p1sec+pulseWidth,
                         p2sec, p2sec+pulseWidth)


def protocol_0xxx(abf):
    """Protocols are tagged with this during development."""
    assert isinstance(abf, pyabf.ABF)
    if abf.protocol in ["0xxx VC 10s MT-50 stim", "0xxx VC 10s MT-70 stim"]:
        protocol_0912(abf)
    else:
        unknown(abf)
