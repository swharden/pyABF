"""
A growing collection of demos. These will serve as tests too. 
If any fail, it means I made a change that broke backwards compatability.
"""

from abf import ABF

import numpy as np
import matplotlib.pyplot as plt
        
def demo_plotSimple():
    abf=ABF(R"../../../../data/17o05028_ic_steps.abf")  
    plt.figure(figsize=(10,4))
    plt.title("pyABF Demonstration: Simple Plot")
    plt.grid(alpha=.2)
    for sweepNumber in [0,5,10,15]:
        abf.setSweep(sweepNumber)
        plt.plot(abf.dataX,abf.dataY,linewidth=.7,alpha=.8,label="sweep %d"%(sweepNumber))
    plt.margins(0,.1)
    plt.legend(fontsize=8)
    plt.ylabel(abf.unitsLong)
    plt.xlabel(abf.unitsTimeLong)
    plt.tight_layout()
    plt.savefig("_demo_plotSimple")
    #plt.show()
    
def demo_plotStacked():
    abf=ABF(R"../../../../data/17o05028_ic_steps.abf") 
    plt.figure(figsize=(6,6))
    plt.title("pyABF Demonstration: Plot with offsets")
    plt.grid(alpha=.2)
    for sweepNumber in [0,5,10,15]:
        abf.setSweep(sweepNumber)
        plt.plot(abf.dataX,abf.dataY+(sweepNumber*30),linewidth=.7,color='b')
    plt.margins(0,.1)
    plt.ylabel(abf.unitsLong)
    plt.xlabel(abf.unitsTimeLong)
    plt.tight_layout()
    plt.savefig("_demo_offset1")
    #plt.show()
                
def demo_plotOffset():
    abf=ABF(R"../../../../data/17o05026_vc_stim.abf") 
    plt.figure(figsize=(10,4))
    plt.title("pyABF Demonstration: Plot with offsets")
    plt.grid(alpha=.2)
    for sweepNumber in range(8):
        abf.setSweep(sweepNumber)
        color=plt.cm.get_cmap('winter')(sweepNumber/abf.sweepCount)
        abf.dataY[:len(abf.dataY)-.5*abf.pointsPerSec]=np.nan
        plt.plot(abf.dataX+(sweepNumber*.02),abf.dataY+(sweepNumber*3),linewidth=.7,alpha=.5,color=color)
    plt.margins(.02,.1)
    plt.ylabel(abf.unitsLong)
    plt.xlabel(abf.unitsTimeLong)
    plt.tight_layout()
    plt.savefig("_demo_offset2")
    #plt.show()
    
def demo_trace_and_protocol_shift():
    abf=ABF(R"../../../../data/17o05024_vc_steps.abf")
    plt.figure(figsize=(6,6))
    
    ax1=plt.subplot(211)
    plt.title("Shifting Epoch Command 1/64th of the Sweep Length")
    plt.grid(alpha=.2)
    abf.setSweep(0)
    plt.plot(abf.dataX,abf.dataY,'b')
    plt.ylabel(abf.unitsLong)
    plt.setp(ax1.get_xticklabels(), visible=False)

    plt.subplot(212,sharex=ax1)
    plt.grid(alpha=.2)
    plt.plot(abf.dataX,np.roll(abf.dataC,-int(abf.pointsPerSweep/64)),color='r',ls=':',alpha=.5,label="default")
    plt.plot(abf.dataX,abf.dataC,color='r',alpha=.5,label="shifted")
    plt.ylabel(abf.unitsCommandLong)
    plt.xlabel(abf.unitsTimeLong)
    plt.legend(fontsize=8)
    plt.axis([1.96,2.09,None,None])    
    
    plt.tight_layout()
    plt.subplots_adjust(hspace=.05)
    plt.savefig("_demo_protocol_shift")
    #plt.show()

def demo_trace_and_protocol_stack():
    abf=ABF(R"../../../../data/17o05028_ic_steps.abf")
    
    plt.figure(figsize=(6,6))
    
    for sweepNumber in abf.sweepList[::5]:
        abf.setSweep(sweepNumber)
        color=plt.cm.get_cmap('jet')(sweepNumber/abf.sweepCount)
    
        ax1=plt.subplot(211)
        plt.title("Command vs. Signal")
        plt.plot(abf.dataX,abf.dataY,alpha=.5,color=color)
        plt.ylabel(abf.unitsLong)
        plt.margins(0,.1)
        plt.setp(ax1.get_xticklabels(), visible=False)
    
        plt.subplot(212,sharex=ax1)
        plt.plot(abf.dataX,abf.dataC,alpha=.5,color=color)
        plt.ylabel(abf.unitsCommandLong)
        plt.xlabel(abf.unitsTimeLong)   
        plt.margins(0,.1)
    
    plt.tight_layout()
    plt.subplots_adjust(hspace=.05)
    plt.savefig("_demo_protocol")
    #plt.show()

if __name__=="__main__":
    
    #run every function in this module starting with demo_
    for functionName in [x for x in dir() if x.startswith("demo_")]:
        print("running",functionName,"...")
        globals()[functionName]()
        plt.close('all')
        
    print("DONE!")