"""
Refactor the AP detection module to provide a clean interface.
You can always refactor the core later.
"""

import os
import sys
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_DATA = os.path.abspath(PATH_HERE+"../../../data/abfs/")
PATH_SRC = os.path.abspath(PATH_HERE+"../../../src/")
sys.path.insert(0, PATH_SRC)

import matplotlib.pyplot as plt
import pyabf
import numpy as np


if __name__=="__main__":
    abf = pyabf.ABF(PATH_DATA+"/2019_05_02_DIC2_0011.abf")

    ax1 = plt.subplot(211)
    ax1.plot(abf.sweepX, abf.sweepY)
    ax1.set_ylabel(abf.sweepLabelY)

    ax2 = plt.subplot(212, sharex = ax1)
    ax2.plot(abf.sweepX, abf.sweepD(3), color='r')
    ax2.set_ylabel("TTL (V)")

    plt.tight_layout()
    plt.show()