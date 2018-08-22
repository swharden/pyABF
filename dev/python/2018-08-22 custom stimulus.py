"""
This code demonstrates how to determine where the stimulus waveform comes from.
The default is to auto-load it from the stimulus file defined in the ABF.

We can override this functionality, using an in-memory array, which is useful
when analyzing many files with the same stimulus as it prevents the need to
re-read data from the same stimulus file over and over.
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

if __name__ == "__main__":
    fname = os.path.join(PATH_DATA+"/171116sh_0017.abf")

    # stimulus waveform is loaded from ABF/ATF file when sweepC is called
    abf = pyabf.ABF(fname)
    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)
    ax1.set_title(abf.abfID)
    ax1.plot(abf.sweepX, abf.sweepY, color='b')
    ax2.set_title("1: stimulus waveform loaded automatically from ABF/ATF")
    ax2.plot(abf.sweepX, abf.sweepC, color='r')
    fig.tight_layout()
    
    # stimulus waveform can be applied manually by overwriting abf.sweepC
    abf.sweepC = np.round(np.sin(np.arange(100000)/10000)*3) # LIKE THIS
    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)
    ax1.set_title(abf.abfID)
    ax1.plot(abf.sweepX, abf.sweepY, color='b')
    ax2.set_title("2: stimulus waveform assigned manually")
    ax2.plot(abf.sweepX, abf.sweepC, color='r')
    fig.tight_layout()

    # now undo the custom waveform to revert the issue
    abf.sweepC = None # REVERT TO AUTOMATIC BEHAVIOR
    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)
    ax1.set_title(abf.abfID)
    ax1.plot(abf.sweepX, abf.sweepY, color='b')
    ax2.set_title("3: reverted behavior")
    ax2.plot(abf.sweepX, abf.sweepC, color='r')
    fig.tight_layout()

    plt.show()