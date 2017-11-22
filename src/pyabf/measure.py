import sys
sys.path.append("../")
import pyabf.abf

import matplotlib.pyplot as plt
import numpy as np

def color(number,total=10):
    frac = number/total
    return plt.cm.get_cmap("jet")(frac)

def inspectEpochs(abf):
    """display a matplotlib picture revealing which epoch is which."""
    epochBoundsSec = abf.epochStartSec + [abf.sweepLengthSec]
    command = abf.epochCommand + [abf.commandHold]
    for i in range(len(abf.epochStartSec)):
        c=color(i,len(abf.epochStartSec))
        plt.axvspan(epochBoundsSec[i],epochBoundsSec[i+1],alpha=.2,color=c,lw=0,
                    label=("%s: (%s %s)"%(chr(65+i),command[i],abf.unitsCommand)))
    plt.plot(abf.dataX,abf.dataY,'k-')
    plt.legend(fontsize=8)
    abf.plotDecorate(zoomYstdev=True)
    plt.show()

if __name__=="__main__":
    abf=pyabf.abf.ABF("../../data/17o05024_vc_steps.abf")
    inspectEpochs(abf)
    #print("\n".join([x for x in dir(abf) if not x.startswith("_")]))
        

