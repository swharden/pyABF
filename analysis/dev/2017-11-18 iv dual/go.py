import sys
import numpy as np
import matplotlib.pyplot as plt

sys.path.append("../../../src/")
sys.path.insert(0,sys.path.pop())
import pyabf

if __name__=="__main__":
    #_compareHeaders(,"../../data/17o05024_vc_steps.abf")
    abf=pyabf.ABF("../../../data/14o16001_vc_pair_step.abf")
    plt.figure(figsize=(6,8))
    for sweep in range(abf.sweepCount):
        abf.setSweep(sweep)
        plt.subplot(211)
        plt.plot(abf.dataY,lw=.5,color='b')
        plt.subplot(212)
        plt.plot(abf.dataC,lw=.5,color='r')
    plt.tight_layout()
    plt.show()
    plt.close('all')
    print("DONE")
    