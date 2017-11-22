import sys
sys.path.append("../")
import pyabf.abf

import matplotlib.pyplot as plt
import numpy as np

def color(number,total=10):
    frac = number/total
    return plt.cm.get_cmap("jet_r")(frac)

def inspectEpoch(abf):
    """display a matplotlib picture revealing which epoch is which."""
    epochBoundsSec = abf.epochStartSec + [abf.sweepLengthSec]
    command = abf.epochCommand + [abf.commandHold]
    plt.plot(abf.dataX,abf.dataY,'k-')
    for i in range(len(abf.epochStartSec)):
        c=color(i,len(abf.epochStartSec))
        plt.axvspan(epochBoundsSec[i],epochBoundsSec[i+1],alpha=.3,color=c,lw=0,
                    label=("%s: (%s %s)"%(chr(65+i),command[i],abf.unitsCommand)))
    plt.legend(fontsize=8)
    abf.plotDecorate(zoomYstdev=True)
    
def IVcurve(abf,epochNumber=1,firstFrac=False,lastFrac=False):
    plt.axhline(0,ls='--',color='k')
    plt.axvline(-70,ls='--',color='k')
    voltages = [abf.epochCommand[epochNumber]+abf.epochCommandDelta[epochNumber]*x for x in abf.sweepList]       
    currents = []
    for sweep in abf.sweepList:
        abf.setSweep(sweep)
        currents.append(abf.averageEpoch(epochNumber,firstFrac,lastFrac))    
    plt.grid(alpha=.2)
    plt.plot(voltages,currents,'.-',ms=20)
    plt.ylabel("Clamp Current (pA)")
    plt.xlabel("Membrane Potential (mV)")
    plt.title("I/V Curve for %s"%abf.ID)

if __name__=="__main__":
    abf=pyabf.abf.ABF("../../data/17o05026_vc_stim.abf")

    abf.setSweep(5,gaussianSigma=0)
    plt.plot(abf.dataX,abf.dataY,color='.8')
    
    print("SIGMA:",abf.pointsPerMS/4)
    abf.setSweep(5,gaussianSigma=abf.pointsPerMS/4)
    plt.plot(abf.dataX,abf.dataY,color='k')
    
    abf.plotDecorate()
    plt.axis([4.37,4.45,-20,0])
    
    
    print("DONE")    

