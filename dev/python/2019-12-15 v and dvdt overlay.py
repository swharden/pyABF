"""
Demonstrate how to overlay voltage and dV/dt plots
"""

import os
import sys
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_DATA = os.path.abspath(PATH_HERE+"../../../data/abfs/")
PATH_SRC = os.path.abspath(PATH_HERE+"../../../src/")
sys.path.insert(0, PATH_SRC)

import pyabf

import matplotlib.pyplot as plt
import numpy as np

if __name__=="__main__":
    abf = pyabf.ABF(PATH_DATA+"/17o05028_ic_steps.abf")

    plt.figure(figsize = (4, 4))

    ax1 = plt.gca()
    ax1.plot(abf.sweepX, abf.sweepY, color='k')
    ax1.axis([2.714, 2.722, -60, 60])
    ax1.set_ylabel("mV", fontsize = 18)
    
    ax2 = plt.gca().twinx()
    msPerSecond = 1000
    ax2.plot(abf.sweepX, abf.sweepDerivative / msPerSecond, color='b')
    ax2.set_ylabel("mV/ms", fontsize = 18, color = "b")

    plt.tight_layout()
    plt.show()