"""
Example code demonstrating how to interact with the pyabf.ABF object
"""

# import the pyabf module from this development folder
import os
import sys
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_SRC = os.path.abspath(PATH_HERE+"/../src/")
PATH_DATA = os.path.abspath(PATH_HERE+"/../data/abfs/")
sys.path.insert(0, PATH_SRC)  # for importing
sys.path.append("../src/")  # for your IDE
import pyabf
pyabf.info()
import datetime
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('bmh')  # alternative color scheme

# now you are free to import additional modules
import glob


def sweepNumbersByTime(abf, timeSec1, timeSec2):
    """
    Returns a list of sweeps containing data between the two times.
    """
    return [1, 2, 3]

# sweep operations


def sweepAverage(abf, sweepNumbers=None, baselineTimeSec1=False, baselineTimeSec2=False, stdErr=True):
    """
    Returns the average of the given sweeps. 
    This returns a whole sweep, not just a single number.
    """
    return [1, 2, 3, 4, 5, 6]

# measure operations


def measureSweep(abf, timeSec1, timeSec2, sweepNumbers=None, channel=0, stdErr=True):
    """
    Return [AVs, ERs] between two time points for the given sweeps.
    """
    if sweepNumbers is None:
        sweepNumbers = abf.sweepList
    sweepNumbers = list(sweepNumbers)
    assert len(sweepNumbers) > 0

    point1 = int(timeSec1*abf.dataRate)
    point2 = int(timeSec2*abf.dataRate)

    avs = np.full(len(sweepNumbers), np.nan)
    ers = np.full(len(sweepNumbers), np.nan)

    for sweepNumber in sweepNumbers:
        abf.setSweep(sweepNumber=sweepNumber, channel=channel)
        avs[sweepNumber] = np.average(abf.sweepY[point1:point2])
        ers[sweepNumber] = np.std(abf.sweepY[point1:point2])

    if stdErr:
        ers = ers / np.sqrt(len(sweepNumbers))

    return [avs, ers]


def measureCommand(abf, timeSec, sweepNumbers, channel=0):
    """
    Return [AVs, ERs] between two time points for the given sweeps.
    """
    return [1, 2, 3]


if __name__ == "__main__":

    allFiles = sorted(glob.glob(PATH_DATA+"/*.abf"))

    fnames = []
    # fnames.append(PATH_DATA+"/model_vc_step.abf")  # VC memtest
    fnames.append(PATH_DATA+"/17o05026_vc_stim.abf")  # VC opto
    # fnames.append(PATH_DATA+"/14o08011_ic_pair.abf")  # IC pair
    # fnames.append(PATH_DATA+"/171116sh_0012.abf")  # VC pair

    for fname in fnames:
        abf = pyabf.ABF(fname)
        print(abf.abfID)

        # define a baseline
        abf.baseline(1,2)

        # define two marker regions
        m1a, m1b = 0.09, 0.12
        m2a, m2b = 0.30, 0.33

        # calculate the average of these regions
        avs1,ers1=measureSweep(abf, m1a, m1b, [0])
        avs2,ers2=measureSweep(abf, m2a, m2b, [0])

        # plot our analyzed data
        pyabf.plot.sweeps(abf,[0],color='k')
        plt.axvspan(m1a,m1b,color='b',alpha=.1)
        plt.axvspan(m2a,m2b,color='r',alpha=.1)
        plt.axhline(avs1[0],color='b',ls='--')
        plt.axhline(avs2[0],color='r',ls='--')
        plt.axis([0,.5,-80,40])
        plt.show()

    print("DONE")
