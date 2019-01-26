"""
This script demonstrates how to plot membrane properties over time.
Passive membrane properties are calculated for every sweep.
Sweeps contain a brief hyperpolarizing square pulse from -70 mV to -80 mV.
See comments in the memtest module for theory and implimentation details.
"""

import os
import sys
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_DATA = os.path.abspath(PATH_HERE+"../../../data/abfs/")
PATH_SRC = os.path.abspath(PATH_HERE+"../../../src/")
sys.path.insert(0, PATH_SRC)

import matplotlib.pyplot as plt
import numpy as np

import pyabf
import pyabf.tools.memtest

if __name__=="__main__":
    abfFilePath = os.path.join(PATH_DATA, "vc_drug_memtest.abf")
    abf=pyabf.ABF(abfFilePath)
    Ihs, Rms, Ras, Cms = pyabf.tools.memtest.step_valuesBySweep(abf)
    times = np.arange(abf.sweepCount)*abf.sweepIntervalSec/60

    fig = plt.figure(figsize=(8, 6))

    ax1 = fig.add_subplot(221)
    ax1.grid(alpha=.2)
    ax1.plot(times, Ihs, ".", color='C0', alpha=.7, mew=0)
    ax1.set_title("Clamp Current")
    ax1.set_ylabel("Current (pA)")

    ax2 = fig.add_subplot(222)
    ax2.grid(alpha=.2)
    ax2.plot(times, Rms, ".", color='C3', alpha=.7, mew=0)
    ax2.set_title("Membrane Resistance")
    ax2.set_ylabel("Resistance (MOhm)")

    ax3 = fig.add_subplot(223)
    ax3.grid(alpha=.2)
    ax3.plot(times, Ras, ".", color='C1', alpha=.7, mew=0)
    ax3.set_title("Access Resistance")
    ax3.set_ylabel("Resistance (MOhm)")

    ax4 = fig.add_subplot(224)
    ax4.grid(alpha=.2)
    ax4.plot(times, Cms, ".", color='C2', alpha=.7, mew=0)
    ax4.set_title("Whole-Cell Capacitance")
    ax4.set_ylabel("Capacitance (pF)")

    for ax in [ax1, ax2, ax3, ax4]:
        ax.margins(0, .9)
        ax.set_xlabel("Experiment Time (minutes)")
        for tagTime in abf.tagTimesMin:
            ax.axvline(tagTime, color='k', ls='--')

    plt.tight_layout()
    plt.show()