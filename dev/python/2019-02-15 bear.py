"""
Test a file that Bear had trouble opening
"""

import os
import sys
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_DATA = os.path.abspath(PATH_HERE+"../../../data/abfs/")
PATH_SRC = os.path.abspath(PATH_HERE+"../../../src/")
sys.path.insert(0, PATH_SRC)

import matplotlib.pyplot as plt

import pyabf
import pyabf.filter

if __name__=="__main__":

    # load the ABF and show some info about it
    abf = pyabf.ABF(PATH_DATA+"/19212027.abf")
    print(abf)

    # apply a gentle filter because it's a bit noisy
    pyabf.filter.gaussian(abf, 2)

    # plot every sweep
    plt.figure(figsize=(8,4))
    plt.grid(alpha=.5, ls='--')
    for sweepNumber in abf.sweepList:
        abf.setSweep(sweepNumber)
        print(f"SWEEP {sweepNumber}: {abf.sweepY}")
        plt.plot(abf.sweepX, abf.sweepY)
    plt.title(abf.abfID)
    plt.xlabel(abf.sweepLabelX)
    plt.ylabel(abf.sweepLabelY)
    plt.tight_layout()
    plt.show()