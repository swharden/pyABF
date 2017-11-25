"""
Code here is just be practing event detection.
Nothing in here should actually be used (yet).
"""

from pyabf.abf import ABF

import numpy as np
import matplotlib.pyplot as plt

def detectDeriv(abf, setSweep=None, t1=0, t2=None, dTms=1, threshold=-10, 
                alignToDerivPeak=True, alignToRawPeak=False, plot=False,
                mustRevertMS=False):
    """
    Derivative-threshold-based event detection. Return a list of times for this
    sweep where the first derivative threshold was exceeded. This event
    detection routine is minimal and simplistic, and can be used for APs, 
    EPSCs, and IPSCs.
    
    You may want to enable gaussian filtering before calling this function.
    
    setSweep: 
        which sweep to use
    
    t1 and t2:
        time range (in seconds) to perform event detection
        
    dTms and threshold:
        Events are points where the threshold is exceeded over the change in 
        time in milliseconds (dTms). Threshold can be positive or negative.
        
    alignToDerivPeak and alignToRawPeak:
        If disabled, the event times will be the first point where the
        derivative was first crossed. If enabled, the event times will be
        aligned to the peak derivative (rather than the threshold) or the
        peak of the raw trace.
    
    Common settings:
        Action potential detection: dTms = 1, threshold = 10, mustRevertMS = 5
        
    """
    
    # determine detection details
    abf.setSweep(setSweep)
    if not t2:
        t2=abf.sweepLengthSec
    i1,i2=int(t1*abf.pointsPerSec),int(t2*abf.pointsPerSec)
    
    # load the data and calculate its derivative
    strip=abf.dataY[i1:i2]
    Xs=abf.dataX[i1:i2]
    dT=int(abf.pointsPerMS*dTms)
    deriv=(strip[dT:]-strip[:-dT])/dTms
    deriv=np.concatenate((deriv,[deriv[-1]]*dT))
    
    # find first-crossings of points where the derivative was crossed
    if threshold>0:
        crossed = deriv > threshold
    else:
        crossed = deriv < threshold
    crossed[1:][crossed[:-1] & crossed[1:]] = False
    eventIs=np.where(crossed)[0]#+dT
    
    # remove events which are less than one dT together
    for i in range(1,len(eventIs)):
        if eventIs[i]-eventIs[i-1]<=dT:
            eventIs[i]=False
    eventIs=eventIs[np.where(eventIs)[0]]
        
    # optionally align to the peak of the first derivative
    if alignToDerivPeak:
        for n,i in enumerate(eventIs):
            if threshold>0:
                while deriv[i]>deriv[i-1]:
                    i+=1
                eventIs[n]=i-1
            else:
                while deriv[i]<deriv[i-1]:
                    i+=1
                eventIs[n]=i-1

    # optionally align to the peak of the raw trace
    if alignToRawPeak:
        for n,i in enumerate(eventIs):
            if threshold>0:
                while strip[i]>strip[i-1]:
                    i+=1
                eventIs[n]=i
            else:
                while strip[i]<strip[i-1]:
                    i+=1
                eventIs[n]=i

    if mustRevertMS:
        revertPoints=int(abf.pointsPerMS*mustRevertMS)
        for n,i in enumerate(eventIs):
            if threshold>0:
                if not np.min(deriv[i:i+revertPoints])<0:
                    eventIs[n]=False
            else:
                if not np.max(deriv[i:i+revertPoints])>0:
                    eventIs[n]=False
        eventIs=eventIs[np.where(eventIs)[0]]

    eventIs=np.unique(eventIs)
    eventTimes=Xs[eventIs]
        
    if plot:
        plt.figure()
        ax1=plt.subplot(211)
        plt.title("sweep %d (raw signal, %s)"%(abf.sweepSelected,abf.units))
        plt.plot(Xs,strip)
        for eventI in [int(abf.pointsPerSec*x) for x in eventTimes]:
            #plt.plot(abf.dataX[eventI],abf.dataY[eventI],'r.')
            plt.axvline(abf.dataX[eventI],color='r',alpha=.5)
        plt.subplot(212,sharex=ax1)
        plt.title("first derivative (%s / ms)"%abf.units)
        plt.plot(Xs,deriv)
        plt.axhline(threshold,color='r',alpha=.5)
        for eventI in [int(abf.pointsPerSec*x) for x in eventTimes]:
            #plt.plot(abf.dataX[eventI],abf.dataY[eventI],'r.')
            plt.axvline(abf.dataX[eventI],color='r',alpha=.5)
        plt.margins(0,.1)
        plt.tight_layout()
        
        
        plt.show()
    
    return eventTimes

def plotAroundTimes(abf,eventTimes,padMS=50):
    pad=int(abf.pointsPerMS*padMS)
    traces=np.empty((len(eventTimes),pad*2))
    for i,t in enumerate(eventTimes):
        eventCenter=int(t*abf.pointsPerSec)
        traces[i]=abf.dataY[eventCenter-pad:eventCenter+pad]
        plt.plot(traces[i],color='.5',alpha=.1)        
    plt.plot(np.average(traces,axis=0))

def plotTraceTimes(abf,eventTimes):
    plt.figure()
    plt.plot(abf.dataX,abf.dataY)
    for i in eventTimes:
        #plt.axvline(i,color='r',ls='--')
        eventI=int(abf.pointsPerSec*i)
        plt.plot(abf.dataX[eventI],abf.dataY[eventI],'r.')
    plt.margins(0,.1)
    plt.tight_layout()
    abf.plotDecorate(title="sweep %d"%abf.sweepSelected)
    plt.show()


def analyzeAP(abf,timePoint):
    """return details about the AP at a single time point of the currently-
    selected sweep."""
    return

if __name__=="__main__":
    
    # list available files
    import glob
    print("\n".join(sorted(glob.glob("../../data/*.abf"))))
    
#    # action potential demo
#    abf=ABF("../../data/17o05028_ic_steps.abf")
#    for sweep in [6]:
#        eventTimes=detectDeriv(abf,setSweep=sweep,threshold=4)
    
    #abf=ABF("../../data/17o05026_vc_stim.abf")  
    #abf.gaussianSigma=abf.pointsPerMS/4
    #eventTimes=eventDetectDerivative(abf,t1=.5,t2=10,threshold=2)
    #plotAroundTimes(abf,eventTimes)
    #plotTraceTimes(abf,eventTimes)
    
#    abf=ABF("../../data/17o05026_vc_stim.abf")  
#    for sweep in abf.sweepList:
#        abf.setSweep(sweep)
#        tonicPhasic(abf)
    
    

    
#    abf=ABF("../../data/17o05026_vc_stim.abf")  
#    abf.gaussianSigma=abf.pointsPerMS/4
#    eventDetectThreshold(abf,setSweep=1,t1=5,t2=10)
    
    print("DONE")