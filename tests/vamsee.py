"""
This script demonstrates how to import pyABF (from ../src/pyABF, not requiring installation) and how to use
it for basic viewing of ABF header information and signal data.
"""

import sys
sys.path.insert(0,'../src/') # path to the pyabf folder (if not installed with pip)
import pyabf
import matplotlib.pyplot as plt
import numpy as np

if __name__=="__main__":
    
    abf = pyabf.ABF("../data/171117_HFMixFRET.abf")   

    # these are the bounds of the area to be measured (seconds)
    mark1=3.5
    mark2=4

    # make a plot of every sweep
    plt.figure(figsize=(8,6))
    for sweepNumber in abf.sweepList:

        plt.subplot(211)
        abf.setSweep(sweepNumber, channel=0)
        plt.plot(abf.dataX,abf.dataY,color='b')
        
        plt.subplot(212)
        abf.setSweep(sweepNumber, channel=1)
        plt.plot(abf.dataX,abf.dataY*5,color='b') #SCALE

    # decorate the plot

    plt.subplot(211)
    plt.ylabel("current (µA)")
    plt.xlabel("time (seconds)")
    plt.axvspan(mark1,mark2,alpha=.1,color='r')

    plt.subplot(212)
    plt.ylabel("actual voltage (mV)")
    plt.xlabel("time (seconds)")
    plt.axvspan(mark1,mark2,alpha=.1,color='r')

    # figure out the current and voltage for every sweep
    
    currents=np.empty(abf.sweepCount)*np.nan
    voltages=np.empty(abf.sweepCount)*np.nan

    for sweepNumber in abf.sweepList:
        abf.setSweep(sweepNumber, channel=0)
        currents[sweepNumber]=abf.average(t1=mark1,t2=mark2)
        abf.setSweep(sweepNumber, channel=1)
        voltages[sweepNumber]=abf.average(t1=mark1,t2=mark2)*5 #SCALE

    # "roll" the array so the first point becomes the last
    currents = np.roll(currents,-1)
    voltages = np.roll(voltages,-1)

    # show the currents and voltages
    print("Voltage (mV), Current (µA)")
    for i in range(len(currents)):
        print(voltages[i],currents[i])

    # plot the currents and voltages
    plt.figure(figsize=(8,6))
    plt.grid(ls='--',alpha=.5)
    plt.plot(voltages,currents,'.-',ms=10)
    plt.xlabel("voltage (mV)")
    plt.ylabel("current (µA)")

    plt.show()