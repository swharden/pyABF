"""Code to interact with ABF files. https://github.com/swharden/pyABF/ """

import sys
import numpy as np # OKAY INSIDE ABF CLASS
import matplotlib.pyplot as plt # HAVEN'T DECIDED IF WILL BE IN ABF CLASS

from header import ABFheader

class ABF:
    def __init__(self,abf):
        """
        The ABF class provides easy pythonic access to header and signal data in ABF2 files.
        Although it is typically instantiated with a path (string), you can also use an ABF or ABFheader.
        """
        
        # get our abfHeader in order depending on what type of object we were given
        if type(abf) is str:
            self._abfHeader = ABFheader(abf)
        elif str(type(abf)).endswith(".ABF'>"):
            self._abfHeader = abf._abfHeader
        elif str(type(abf)).endswith(".ABFheader'>"):
            self._abfHeader = abf
        else:
            raise ValueError('abf must be a file path (str), ABF object, or ABFheader object.')

        # remove this after you're done debugging
        self._abfHeader.saveHTML()
        
        ### Populate meaningful ABF attributes. Think about how you will use them: abf.something
        self.ID = self._abfHeader.header['abfID']
        self.filename = self._abfHeader.header['abfFilename']
        self.datetime = self._abfHeader.header['abfDatetime']
        self.pointDurSec = self._abfHeader.header['timeSecPerPoint']
        self.pointDurMS = self._abfHeader.header['timeSecPerPoint']*1000.0
        self.pointsPerSweep = self._abfHeader.header['sweepPointCount']
        self.pointsPerSec = self._abfHeader.header['rate']
        self.sweepCount = self._abfHeader.header['sweepCount']
        self.sweepList = np.arange(self.sweepCount)
        self.sweepLengthSec = self._abfHeader.header['sweepLengthSec']
        self.sweepPointCount = self._abfHeader.header['sweepPointCount']
        self.mode = self._abfHeader.header['mode']
        self.units = self._abfHeader.header['units']
        self.unitsLong = "Membrane Potential (mV)" if self.units is 'mV' else "Membrane Current (pA)"
        self.unitsCommand = self._abfHeader.header['unitsCommand']
        self.unitsCommandLong = "Clamp Potential (mV)" if self.unitsCommand is 'mV' else "Clamp Current (pA)"
        self.commandHoldingByDAC = self._abfHeader.header['commandHoldingByDAC']
        self.commandHold = self.commandHoldingByDAC[0]
        self.experimentLengthSec = self.sweepLengthSec*self.sweepCount
        self.unitsTime = "seconds"
        self.unitsTimeLong = "Signal Time (seconds)"
        
        ### Add information about the epochs / command waveform
        self.epochCount = len(self._abfHeader.header['nEpochType'])
        self.epochType = self._abfHeader.header['nEpochType']
        self.epochCommand = self._abfHeader.header['fEpochInitLevel']
        self.epochCommandDelta = self._abfHeader.header['fEpochLevelInc']
        self.epochDuration = self._abfHeader.header['lEpochInitDuration']
        self.epochDurationDelta = self._abfHeader.header['lEpochDurationInc']
        self.epochPulsePeriod = self._abfHeader.header['lEpochPulsePeriod']
        self.epochPulseWidth = self._abfHeader.header['lEpochPulseWidth']
        self.epochDigOut = self._abfHeader.header['nEpochDigitalOutput']
        
        ### Figure how to handle data - this will improve with performance testing
        # CURRENT STRATEGY: LOAD EVERYTHING IN TWO ARRAYS (DATA AND TIMES) AND SAMPLE IT WHEN REQUESTED
        # is this the best way to do this? Load the *FULL* experiment time of data and generate
        # just as much data for time time points. This comes to 
        self.signalData = self._abfHeader.data
        self.signalTimes = np.arange(len(self.signalData),dtype='float32')*self.pointDurSec
        bytesInMemory = sys.getsizeof(self.signalData)+sys.getsizeof(self.signalTimes)
        bytePerMin = (bytesInMemory/self.experimentLengthSec)*60
        print("memory usage rate: %.02f MB/min of ABF"%(bytePerMin/1e6)) # 1 min of ABF ~ 10MB memory
        # This is a lot of memory but I can't think of when/why I would run out!
        # It's faster to pull the bytes from a pre-made array than it is to recreate them every time
        
        ### Set to sweep 0 to kick us off
        
    def setSweep(self,sweepNumber=0,absoluteTime=False):
        """set all the self.data variables to contain data for a certain sweep"""
        self.dataSweepSelected = sweepNumber
        pointStart=sweepNumber*self.pointsPerSweep
        pointEnd=pointStart+self.pointsPerSweep
        self.dataY = self.signalData[pointStart:pointEnd]
        if absoluteTime:
            self.dataX = self.signalTimes[pointStart:pointEnd]
        else:
            self.dataX = self.signalTimes[0:self.pointsPerSweep]

    def help(self):
        """Show information about the ABF class which may be useful."""
        print("\n### ATTRIBUTES ###")
        for thing in [x for x in sorted(dir(self)) if not x.startswith("_")]:
            if not "bound method" in str(getattr(self,thing)):
                print("abf.%s = %s"%(thing,str(getattr(self,thing))))            
        print("\n### FUNCTIONS ###")
        for thing in [x for x in sorted(dir(self)) if not x.startswith("_")]:
            if "bound method" in str(getattr(self,thing)):
                print("abf.%s()"%(thing))
                
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
    plt.show()
    
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
    plt.show()
                
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
    plt.show()
    
if __name__=="__main__":   
    demo_plotSimple()
    demo_plotStacked()
    demo_plotOffset()