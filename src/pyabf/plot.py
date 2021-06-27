"""
This file contains code to plot ABF data using matplotlib.

Users are typically encouraged to write their own plotting functions, but
I have added common tasks here to serve as a reference and potentially even
inspiration (for those who have not used matplotlib before).

Code in this module is mostly for testing and it is not actively developed.
"""

import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.warn("abf.plot is obsolete and should not be used")


def sweepDataRange(abf, fraction=1, sweepNumber=0, channel=0):
    """
    Return the magnitude of the range between the min and max points in the
    sweep. This is useful when determining how much to stack an ABF.
    """
    abf.setSweep(sweepNumber=0, channel=channel)
    firstSweepRange = np.max(abf.sweepY) - np.min(abf.sweepY)
    return firstSweepRange*fraction


def colorsBinned(bins, colormap="viridis", reverse=False):
    """
    Return a list of colors spanning the range of the given colormap.
    I like using these colormaps: Winter, Dark2, rainbow, viridis
    """
    colormap = plt.get_cmap(colormap)
    colors = []
    for binNumber in range(bins):
        colors.append(colormap(binNumber/bins))
    if reverse:
        colors.reverse()
    return colors


def sweeps(abf, sweepNumbers=None, continuous=False, offsetXsec=0,
           offsetYunits=0, channel=0, axis=None, color=None, alpha=.5,
           startAtSec=0, endAtSec=False, title=None, linewidth=1,
           defaultFigsize=(8, 6)):
    """
    This is a flexible sweep plotting function. Although it has many potential 
    uses, developers will most likely want to write their own plotting functions
    to suit their specific applications.
    """
    if sweepNumbers is None:
        sweepNumbers = abf.sweepList
    sweepNumbers = list(sweepNumbers)
    assert len(sweepNumbers) > 0

    if not startAtSec:
        startAtSec = 0
    i1 = int(abf.dataRate*startAtSec)
    if endAtSec:
        i2 = int(abf.dataRate*endAtSec)
    else:
        i2 = int(abf.dataRate*abf.sweepLengthSec)

    if color is None and len(sweepNumbers) > 1:
        colors = colorsBinned(len(sweepNumbers))
    else:
        colors = [color]*abf.sweepCount

    if axis is None:
        fig = plt.figure(figsize=defaultFigsize)
        axis = fig.add_subplot(111)
    axis.set_xmargin(0)
    for sweepNumber in sweepNumbers:
        abf.setSweep(sweepNumber=sweepNumber,
                     channel=channel, absoluteTime=continuous)
        axis.plot(
            abf.sweepX[i1:i2]+offsetXsec*sweepNumber,
            abf.sweepY[i1:i2]+offsetYunits*sweepNumber,
            color=colors[sweepNumber],
            alpha=alpha,
            linewidth=linewidth)
        axis.set_ylabel(abf.sweepLabelY)
        axis.set_xlabel(abf.sweepLabelX)

    if title is None:
        axis.set_title(f"{abf.abfID} (Ch{channel+1})")
    elif title is False:
        pass  # no title


def scalebar(abf=None, hideTicks=True, hideFrame=True, fontSize=8, scaleXsize=None, scaleYsize=None, scaleXunits="", scaleYunits="", lineWidth=2):
    """
    Add an L-shaped scalebar to the current figure.
    This removes current axis labels, ticks, and the figure frame.
    """

    # if an ABF objet is given, use its sweep units
    if abf:
        scaleXunits = abf.sweepUnitsX
        scaleYunits = abf.sweepUnitsY

    # calculate the current data area
    x1, x2, y1, y2 = plt.axis()  # bounds
    xc, yc = (x1+x2)/2, (y1+y2)/2  # center point
    xs, ys = abs(x2-x1), abs(y2-y1)  # span

    # determine how big we want the scalebar to be
    if not scaleXsize:
        scaleXsize = abs(plt.xticks()[0][1]-plt.xticks()[0][0])/2
    if not scaleYsize:
        scaleYsize = abs(plt.yticks()[0][1]-plt.yticks()[0][0])/2

    # create the scale bar labels
    lblX = str(scaleXsize)
    lblY = str(scaleYsize)

    # prevent units unecessarially ending in ".0"
    if lblX.endswith(".0"):
        lblX = lblX[:-2]
    if lblY.endswith(".0"):
        lblY = lblY[:-2]

    if scaleXunits == "sec" and "." in lblX:
        lblX = str(int(float(lblX)*1000))
        scaleXunits = "ms"

    # add units to the labels
    lblX = lblX+" "+scaleXunits
    lblY = lblY+" "+scaleYunits
    lblX = lblX.strip()
    lblY = lblY.strip()

    # determine the dimensions of the scalebar
    scaleBarPadX = 0.10
    scaleBarPadY = 0.05
    scaleBarX = x2-scaleBarPadX*xs
    scaleBarX2 = scaleBarX-scaleXsize
    scaleBarY = y1+scaleBarPadY*ys
    scaleBarY2 = scaleBarY+scaleYsize

    # determine the center of the scalebar (where text will go)
    scaleBarXc = (scaleBarX+scaleBarX2)/2
    scaleBarYc = (scaleBarY+scaleBarY2)/2

    # create a scalebar point array suitable for plotting as a line
    scaleBarXs = [scaleBarX2, scaleBarX, scaleBarX]
    scaleBarYs = [scaleBarY, scaleBarY, scaleBarY2]

    # the text shouldn't touch the scalebar, so calculate how much to pad it
    lblPadMult = .005
    lblPadMult += .002*lineWidth
    lblPadX = xs*lblPadMult
    lblPadY = ys*lblPadMult

    # hide the old tick marks
    if hideTicks:
        plt.gca().get_yaxis().set_visible(False)
        plt.gca().get_xaxis().set_visible(False)

    # hide the square around the image
    if hideFrame:
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['bottom'].set_visible(False)
        plt.gca().spines['left'].set_visible(False)

    # now do the plotting
    plt.plot(scaleBarXs, scaleBarYs, 'k-', lw=lineWidth)
    plt.text(scaleBarXc, scaleBarY-lblPadY, lblX,
             ha='center', va='top', fontsize=fontSize)
    plt.text(scaleBarX+lblPadX, scaleBarYc, lblY,
             ha='left', va='center', fontsize=fontSize)
