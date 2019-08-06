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

abf = pyabf.ABF(PATH_DATA+"/2019_07_24_0055_fsi.abf")
abf.setSweep(12)

sweepDeltaY = np.diff(abf.sweepY) * abf.dataRate / 1000 # V/s

fig = plt.figure(figsize=(6, 4))
ax1 = fig.add_subplot(111)
ax2 = ax1.twinx()

ax1.plot(abf.sweepX*1000, abf.sweepY, color='C0')
ax1.set_xlabel(R"Time (ms)", fontsize=16)
ax1.set_ylabel(R"Voltage (mV)", color='C0', fontsize=16)
ax1.tick_params(axis='y', colors='C0')

ax2.plot(abf.sweepX[1:]*1000, sweepDeltaY, color='C1')
ax2.set_ylabel(R"$\Delta$ Voltage (V/s)", color='C1', fontsize=16)
ax2.tick_params(axis='y', colors='C1')

ax2.spines['left'].set_color('C0')
ax2.spines['right'].set_color('C1')

plt.axis([380, 414, None, None])
plt.tight_layout()
plt.show()
