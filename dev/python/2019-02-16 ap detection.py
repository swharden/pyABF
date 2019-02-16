"""
Test crude AP detection
"""

import os
import sys
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_DATA = os.path.abspath(PATH_HERE+"../../../data/abfs/")
PATH_SRC = os.path.abspath(PATH_HERE+"../../../src/")
sys.path.insert(0, PATH_SRC)

import matplotlib.pyplot as plt

import pyabf
import pyabf.tools.ap

if __name__=="__main__":
    abf = pyabf.ABF(PATH_DATA+"/171116sh_0018.abf")

    # display AP frequency by sweep
    apFirstFreq, apFreqAvg = pyabf.tools.ap.ap_freq_per_sweep(abf)
    for sweepNumber, apFreq in enumerate(apFreqAvg):
        print(f"Sweep {sweepNumber} fires at {apFreq} Hz")
    
    # make a plot showing AP detection
    abf.setSweep(12)
    plt.figure(figsize=(10,4))
    plt.plot(abf.sweepX, abf.sweepY)
    for apPoint in pyabf.tools.ap.ap_points_currentSweep(abf):
        plt.axvline(abf.sweepX[apPoint], color='r', alpha=.2, ls='--')
    plt.tight_layout()
    plt.show()
    