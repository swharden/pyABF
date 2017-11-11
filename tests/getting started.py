"""
This script demonstrates how to import pyABF (from ../src/pyABF, not requiring installation) and how to use
it for basic viewing of ABF header information and signal data.
"""

import sys
sys.path.insert(0,'../src/') # path to the pyabf folder (if not installed with pip)
import pyabf
import matplotlib.pyplot as plt

if __name__=="__main__":
    
    abf=pyabf.ABF("../data/17o05028_ic_steps.abf") # load an ABF
    abf.info() # show what commands are available
    
    ### Create an overlayed sweep graph
    plt.figure(figsize=(8,4))
    for sweepNumber in abf.sweepList:
        abf.setSweep(sweepNumber)
        plt.plot(abf.dataX,abf.dataY)
    plt.ylabel(abf.unitsLong)
    plt.xlabel(abf.unitsTimeLong)
    plt.title(abf.ID)
    plt.margins(0,.1)
    plt.show()