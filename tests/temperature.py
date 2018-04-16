"""
This script demonstrates how to import pyABF (from ../src/pyABF, not requiring installation) and how to use
it for basic viewing of ABF header information and signal data.
"""

import sys
sys.path.insert(0,'../src/') # path to the pyabf folder (if not installed with pip)
import pyabf
import matplotlib.pyplot as plt

if __name__=="__main__":
    

    abf = pyabf.ABF("../data/180415_aaron_temp.abf")
    abf.setSweep(0, channel=0)
    voltage = abf.dataY
    timeSec = abf.dataX
    abf.setSweep(0, channel=1)
    temperature = abf.dataY
    temperatureAdjusted = 2.3 + 10* abf.dataY # manually adjust scale factor and offset
    
    plt.subplot(211)
    plt.plot(timeSec,voltage)
    plt.subplot(212)
    plt.plot(timeSec,temperatureAdjusted)
    plt.show()