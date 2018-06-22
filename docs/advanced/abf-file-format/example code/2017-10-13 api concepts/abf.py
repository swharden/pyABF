"""Code to interact with ABF files. https://github.com/swharden/pyABF/ """

import sys
import numpy as np # OKAY INSIDE ABF CLASS
import matplotlib.pyplot as plt # HAVEN'T DECIDED IF WILL BE IN ABF CLASS

from header import ABFheader

class ABF:
    def __init__(self,abf):
        """The ABF class provides easy pythonic access to header and signal data in ABF2 files.
        
        * Although it is typically instantiated with a path (string), you can also use an ABF or ABFheader.
        
        Quick start:
            >>> abf = ABF("/path/to/file.abf")
            >>> abf.setSweep(0) # load data from the first sweep
            >>> print(abf.dataY) # signal data
            >>> print(abf.dataX) # timestamps
            >>> print(abf.dataC) # command waveform

        See all the properties available to you:
            >>> abf.help()
            
        Developers can access the ABFheader class features:
            >>> abf._abfHeader.saveHTML()
        
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
        
        ### Preload signal and time data (totalling ~10MB of memory per minute of 20kHz recording)
        self.signalData = self._abfHeader.data
        self.signalTimes = np.arange(len(self.signalData),dtype='float32')*self.pointDurSec
        
    def setSweep(self,sweepNumber=0,absoluteTime=False):
        """set all the self.data variables to contain data for a certain sweep"""
        self.dataSweepSelected = sweepNumber
        self.sweepSelected = sweepNumber
        pointStart=sweepNumber*self.pointsPerSweep
        pointEnd=pointStart+self.pointsPerSweep
        self.dataY = self.signalData[pointStart:pointEnd]
        if absoluteTime:
            self.dataX = self.signalTimes[pointStart:pointEnd]
        else:
            self.dataX = self.signalTimes[0:self.pointsPerSweep]
        self.updateCommandWaveform()
            
    def updateCommandWaveform(self):
        """Read the epochs and figure out how to fill self.dataC with the command signal."""
        self.dataC = np.empty(self.dataX.size) # start as random data
        position=0 # start at zero here for clarity
        position+=int(self.pointsPerSweep/64) # the first 1/64th is pre-epoch (why???)
        self.dataC[:position]=self.commandHold # fill the pre-epoch with the command holding
        for epochNumber in range(self.epochCount):
            pointCount=self.epochDuration[epochNumber]
            deltaCommand=self.epochCommandDelta[epochNumber]*self.sweepSelected
            self.dataC[position:position+pointCount]=self.epochCommand[epochNumber]+deltaCommand
            position+=pointCount
        self.dataC[position:]=self.commandHold # set the post-epoch to the command holding
       
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
    
if __name__=="__main__":   
    abf=ABF(R"../../../../data/17o05028_ic_steps.abf")
    #abf=ABF(R"../../../../data/17o05024_vc_steps.abf")
    #demo_trace_and_protocol(abf)
    #abf.setSweep(0)
    print("DONE")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    