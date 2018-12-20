"""
Generate a stimulus waveform which is EPSCs of increasing frequency.
"""

import os
import sys
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_DATA = os.path.abspath(PATH_HERE+"../../../data/abfs/")
PATH_SRC = os.path.abspath(PATH_HERE+"../../../src/")
sys.path.insert(0, PATH_SRC)
import pyabf
import pyabf.tools.generate
import glob
import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
    synth = pyabf.tools.generate.SynthSweep(sampleRate=20000, sweepLengthSec=20)
    timeSec = 5
    amplitude = 100
    tau = 180
    for eventNumber in range(20):
        synth.addEvent(timeSec, amplitude, tau, False)
        timeDelta = 1.0/(eventNumber+1)
        timeSec += timeDelta
        freq = 1.0/timeDelta
        print(f"event {eventNumber+1} frquency: {freq} Hz")

    # create a plot
    plt.figure(figsize = (10, 3))
    plt.plot(synth.sweepX, synth.sweepY, color='r')
    plt.axis([4, 9, None, None])
    plt.title("EPSC Stimulus of Increasing Frequency (1-20 Hz)")
    plt.ylabel("Current (pA)")
    plt.xlabel("Sweep Time (seconds)")
    plt.tight_layout()
    plt.savefig(__file__+".png")
    
    # write the data to an ABF1 file
    dataToWrite = np.array([synth.sweepY])
    pyabf.abfWriter.writeABF1(dataToWrite, __file__+".abf")