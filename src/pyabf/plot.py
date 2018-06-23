"""
This file contains code to plot ABF data using matplotlib.

Users are typically encouraged to write their own plotting functions, but
I have added common tasks here for my own convenience. It is mostly for testing
and it is not actively developed.
"""

import os
import sys
import glob
import warnings

import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
    warnings.warn("DO NOT RUN THIS FILE DIRECTLY!")
    sys.path.append(os.path.dirname(__file__)+"/../")

import pyabf

defaultFigsize = (8, 6)


def sweepDataRange(abf, fraction=1, sweepNumber=0, channel=0):
    """
    Return the magnitude of the range between the min and max points in the 
    sweep. This is useful when determining how much to stack an ABF.
    """
    abf.setSweep(sweepNumber=0, channel=channel)
    firstSweepRange = np.max(abf.sweepY) - np.min(abf.sweepY)
    return firstSweepRange*fraction


def colorsBinned(bins, colormap="winter", reverse=False):
    """
    I like using these colormaps:

        Winter, Dark2
        
    """
    colormap = plt.get_cmap(colormap)
    colors = []
    for binNumber in range(bins):
        colors.append(colormap(binNumber/bins))
    if reverse:
        colors.reverse()
    return colors


def sweeps(abf, sweepNumbers=None, continuous=False, offsetXsec=0, offsetYunits=0, channel=0, axis=None, color=None, alpha=.5):
    if sweepNumbers is None:
        sweepNumbers = abf.sweepList
    sweepNumbers = list(sweepNumbers)
    assert len(sweepNumbers) > 0

    if color is None:
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
            abf.sweepX+offsetXsec*sweepNumber,
            abf.sweepY+offsetYunits*sweepNumber,
            color=colors[sweepNumber],
            alpha=alpha)
        axis.set_ylabel(abf.sweepLabelY)
        axis.set_xlabel(abf.sweepLabelX)

        axis.set_title(f"{abf.abfID} (Ch{channel+1})")


if __name__ == "__main__":

    PATH_HERE = os.path.abspath(os.path.dirname(__file__))
    PATH_DATA = os.path.abspath(PATH_HERE+"/../../data/abfs/")

    for fname in sorted(glob.glob(PATH_DATA+"/*.abf"))[5:8]:
        abf = pyabf.ABF(fname)
        sweeps(abf, offsetXsec=abf.sweepLengthSec/20,
               offsetYunits=sweepDataRange(abf, .05))
    plt.show()

    print("DONE")
