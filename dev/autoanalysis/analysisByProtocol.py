"""
Code here stores automatic analysis routines for ABF files given their protocol.

There are several analysis routines which are general (show all sweeps 
continuously, show sweeps stacked, show sweeps overlayed, etc) and can be used
for almost any protocol (or ABFs with unknown protocol).

Some analysis routines are specific for specific protocols.
"""

import os
import pyabf
import numpy as np
import matplotlib.pyplot as plt

import logging
log = logging.getLogger(__name__)
log.debug(f"autoabf imported")
log.setLevel(level=logging.WARN)

FIGSIZE = (8, 6)
DATAFOLDER = "autoanalysis"

# Little operations to apply on graphs


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


def plotFigNew(abf):
    """create a figure"""
    plt.figure(figsize=FIGSIZE)
    return


def plotFigSave(abf, tag="", tight=True, closeToo=True, grid=True, unknown=False, title=None):
    """save a figure"""
    assert isinstance(abf, pyabf.ABF)

        
    # applt title only to single-subplot figures
    if len(plt.gcf().axes)==1:
        if title:
            plt.title(title)
        elif title is None:
            plt.title(f"{abf.abfID} (Ch1)")
        elif title is False:
            plt.title(None)

    # apply a grid to all subplots
    if grid:
        for i, ax in enumerate(plt.gcf().axes):
            ax.grid(alpha=.5, ls="--")

    # decorate unknown plots in a special way
    if unknown:
        abf.protocol = abf.protocol + "(UNKNOWN)"
        protocolColor = "r"
        # for i, ax in enumerate(plt.gcf().axes):
        #ax.set_facecolor((1.0, 0.9, 0.9))
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
    log.info(f"saving {fnOut}")
    plt.savefig(pathOut)
    if closeToo:
        plt.close()
    return

# Code here indicates how to make common graphs


def generic_overlay(abf, color=None, unknown=False, alpha=None):
    """plot every sweep semi-transparent on top of the next."""
    assert isinstance(abf, pyabf.ABF)
    plotFigNew(abf)
    for channel in abf.channelList:
        ax = plt.gcf().add_subplot(abf.channelCount, 1, channel+1)
        ax.set_title(f"{abf.abfID} (Ch{channel+1})")
        pyabf.plot.sweeps(abf, axis=ax, color=color,
                          channel=channel, alpha=alpha)
    plotFigSave(abf, tag="generic-overlay", unknown=unknown)
    return


def generic_continuous(abf, unknown=False, alpha=1):
    """plot every sweep continuously through time."""
    assert isinstance(abf, pyabf.ABF)
    plotFigNew(abf)
    for channel in abf.channelList:
        ax = plt.gcf().add_subplot(abf.channelCount, 1, channel+1)
        ax.set_title(f"{abf.abfID} (Ch{channel+1})")
        pyabf.plot.sweeps(abf, axis=ax, continuous=True,
                          channel=channel, color='b', alpha=alpha,
                          linewidth=.5)
    addComments(abf)
    plotFigSave(abf, tag="generic-continuous", unknown=unknown)
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


def protocol_0111(abf):
    """0111 continuous ramp.pro"""
    assert isinstance(abf, pyabf.ABF)
    generic_continuous(abf)
    return


def protocol_0112(abf):
    """0112 steps dual -50 to 150 step 10.pro"""
    assert isinstance(abf, pyabf.ABF)
    generic_overlay(abf)
    return


def protocol_0113(abf):
    """0113 steps dual -100 to 300 step 25.pro"""
    assert isinstance(abf, pyabf.ABF)
    generic_overlay(abf)
    return


def protocol_0114(abf):
    """0114 steps dual -100 to 2000 step 100.pro"""
    assert isinstance(abf, pyabf.ABF)
    generic_overlay(abf)
    return


def protocol_0121(abf):
    """0121 IC sine sweep 0 +- 20 pA.pro"""
    assert isinstance(abf, pyabf.ABF)
    generic_overlay(abf)
    return


def protocol_0201(abf):
    """0201 memtest.pro"""
    assert isinstance(abf, pyabf.ABF)
    generic_overlay(abf, color='b', alpha=.5)
    return


def protocol_0202(abf):
    """0202 IV dual"""
    assert isinstance(abf, pyabf.ABF)

    # enable lowpass filter
    pyabf.filter.gaussian(abf)

    # zoom determine an interesting vertical range
    abf.setSweep(abf.sweepList[0])
    valMin = abf.sweepMin(0.7, 1.0)
    abf.setSweep(abf.sweepList[-1])
    valMax = abf.sweepMax(0.7, 1.0)
    valDiff = valMax-valMin
    viewDiff = valDiff*.2
    axis = [None, None, valMin-viewDiff, valMax+viewDiff]

    # create the figure
    plotFigNew(abf)
    pyabf.plot.sweeps(abf, axis=plt.gca())
    plt.axis(axis)
    plotFigSave(abf, tag="overlay")
    return


def protocol_0203(abf):
    """0203 IV fast.pro"""
    assert isinstance(abf, pyabf.ABF)
    generic_overlay(abf)
    return


def protocol_0204(abf):
    """0204 Cm ramp.pro"""
    assert isinstance(abf, pyabf.ABF)
    generic_overlay(abf, color='b', alpha=.5)
    return


def protocol_0221(abf):
    """0221 VC sine sweep 70 +- 5 mV.pro"""
    assert isinstance(abf, pyabf.ABF)
    generic_overlay(abf)
    return


def protocol_0402(abf):
    """0402 VC 2s MT-50.pro"""
    assert isinstance(abf, pyabf.ABF)
    generic_continuous(abf)
    return


def protocol_0404(abf):
    """0404 VC 2s MT2-70 ramp -110-50.pro"""
    assert isinstance(abf, pyabf.ABF)
    generic_continuous(abf)
    return


def protocol_0406(abf):
    """0406 VC 10s MT-50.pro"""
    assert isinstance(abf, pyabf.ABF)
    generic_continuous(abf)
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
    plotFigSave(abf, tag="opto-avg")

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
    plt.ylabel(abf.sweepLabelY)
    plt.xlabel(abf.sweepLabelX)
    plotFigSave(abf, tag="opto-stacked")
    return
