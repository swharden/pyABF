"""Code to interact with ABF files. https://github.com/swharden/pyABF/ """

import numpy as np
np.set_printoptions(suppress=True) # don't use scientific notation
import matplotlib.pyplot as plt
    
from pyabf.header import ABFheader

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
        self.dataChannels = self._abfHeader.header['dataChannels']
        self.sweepCount = self._abfHeader.header['sweepCount']
        self.sweepList = np.arange(self.sweepCount)
        self.sweepLengthSec = self._abfHeader.header['sweepLengthSec']
        self.sweepPointCount = self._abfHeader.header['sweepPointCount']
        self.mode = self._abfHeader.header['mode']
        self.units = self._abfHeader.header['units']
        self.unitsLong = "Membrane Potential (mV)" if self.units is 'mV' else "Membrane Current (pA)"
        self.unitsCommand = self._abfHeader.header['unitsCommand']
        self.unitsCommandLong = "Command Potential (mV)" if self.unitsCommand is 'mV' else "Command Current (pA)"
        self.commandHoldingByDAC = self._abfHeader.header['commandHoldingByDAC']
        self.commandHold = self.commandHoldingByDAC[0]
        self.experimentLengthSec = self.sweepLengthSec*self.sweepCount
        self.unitsTime = "seconds"
        self.unitsTimeLong = "Signal Time (seconds)"
        
        ### Add information about the epochs / command waveform - we will always expect epochs to be lists.
        if "nEpochType" in self._abfHeader.header.keys():
            # ensure epochs which are just a single epoch still come out as lists
            for key in ["nEpochType","fEpochInitLevel","fEpochLevelInc","lEpochInitDuration",
                        "lEpochDurationInc","lEpochPulsePeriod","lEpochPulseWidth","nEpochDigitalOutput"]:
                if not type(self._abfHeader.header[key]) == list:
                    self._abfHeader.header[key]=[self._abfHeader.header[key]]
            self.epochCount = len(self._abfHeader.header['nEpochType'])
            self.epochType = self._abfHeader.header['nEpochType']
            self.epochCommand = self._abfHeader.header['fEpochInitLevel']
            self.epochCommandDelta = self._abfHeader.header['fEpochLevelInc']
            self.epochDuration = self._abfHeader.header['lEpochInitDuration']
            self.epochDurationDelta = self._abfHeader.header['lEpochDurationInc']
            self.epochPulsePeriod = self._abfHeader.header['lEpochPulsePeriod']
            self.epochPulseWidth = self._abfHeader.header['lEpochPulseWidth']
            self.epochDigOut = self._abfHeader.header['nEpochDigitalOutput']
        else:
            # this ABF has no epochs at all, so make all epoch stuff empty lists
            self.epochCount = 0
            self.epochType = []
            self.epochCommand = []
            self.epochCommandDelta = []
            self.epochDuration = []
            self.epochDurationDelta = []
            self.epochPulsePeriod = []
            self.epochPulseWidth = []
            self.epochDigOut = []
        
        ### Preload signal and time data (totalling ~10MB of memory per minute of 20kHz recording)
        self.signalData = self._abfHeader.data/self.dataChannels
        self.signalTimes = np.arange(len(self.signalData),dtype='float32')*self.pointDurSec
                                    
        ### Go ahead and set sweep zero to populate command signal trace
        self.setSweep(0)

    def help(self):
        """Launch the documentation in a web browser."""
        import webbrowser
        webbrowser.open('https://github.com/swharden/pyABF')
                                    
    def info(self,silent=False):
        """Display (and return) a long message indicating what you can access/do with the ABF class."""
        functions,attributes,lists,data=[],[],[],[]
        for itemName in dir(self):
            if itemName.startswith("_"):
                continue
            itemType=str(type(getattr(self,itemName))).split("'")[1]
            if itemType in ['str','float','int']:
                attributes.append(itemName)
            elif itemType =='list':
                lists.append(itemName)
            elif itemType =='numpy.ndarray':
                data.append(itemName)
            elif itemType =='method':
                functions.append(itemName)
            else:
                print(itemType,itemName)
            
        msg=""
        msg+="\n### INSTANTIATION ###\n"
        msg+="abf=pyabf.ABF(R'%s')\n"%self.filename
        
        msg+="\n### VALUES ###\n"
        for itemName in sorted(attributes):
            itemValue=str(getattr(self,itemName))
            msg+="* abf.%s = %s\n"%(itemName,itemValue)
        
        msg+="\n### LISTS ###\n"
        for itemName in sorted(lists):
            itemValue=str(getattr(self,itemName))
            msg+="* abf.%s = %s\n"%(itemName,itemValue)
            
        msg+="\n### SIGNAL STUFF###\n"
        for itemName in sorted(data):
            itemValue=getattr(self,itemName)
            if 'float' in str(itemValue.dtype):
                itemValue=np.array(getattr(self,itemName),dtype=np.float)
                itemValue=np.round(itemValue,decimals=5)
            msg+="* abf.%s = %s\n"%(itemName,itemValue)
            
        msg+="\n### FUNCTIONS ###\n"
        for itemName in sorted(functions):
            msg+="* abf.%s()\n"%(itemName)
        if not silent:
            print(msg)
        return msg
        
    def setSweep(self,sweepNumber=0,absoluteTime=False,channel=0):
        """set all the self.data variables to contain data for a certain sweep"""
        #TODO: make function to get sweep-offset time
        #TODO: command signal not supported if using multi-channel
        self.dataSweepSelected = sweepNumber
        self.sweepSelected = sweepNumber
        pointStart=sweepNumber*(self.pointsPerSweep*self.dataChannels)
        pointEnd=pointStart+(self.pointsPerSweep*self.dataChannels)
        self.dataY = self.signalData[int(pointStart):int(pointEnd)]
        if absoluteTime:
            self.dataX = self.signalTimes[int(pointStart):int(pointEnd)]
        else:
            self.dataX = self.signalTimes[0:int(self.pointsPerSweep)]
        if self.dataChannels>1:
            self.dataY=self.dataY[channel::self.dataChannels]*self.dataChannels
        self._updateCommandWaveform()
            
    def _updateCommandWaveform(self):
        """Read the epochs and figure out how to fill self.dataC with the command signal."""
        #TODO: don't update if the command doesn't change from sweep to sweep
        self.dataC = np.empty(self.dataX.size) # start as random data
        position=0 # start at zero here for clarity
        position+=int(self.pointsPerSweep/64) # the first 1/64th is pre-epoch (why???)
        self.dataC[:position]=self.commandHold # fill the pre-epoch with the command holding
        for epochNumber in range(self.epochCount):
            if self.epochType[epochNumber]==0:
                continue # it's a disabled epoch
            if epochNumber>=len(self.epochDuration):
                print("ran out of epoch")
                break # ran out?
            pointCount=self.epochDuration[epochNumber]
            deltaCommand=self.epochCommandDelta[epochNumber]*self.sweepSelected
            self.dataC[position:position+pointCount]=self.epochCommand[epochNumber]+deltaCommand
            position+=pointCount
        self.dataC[position:]=self.commandHold # set the post-epoch to the command holding
        
    def plotDecorate(self,command=False,title=True,xlabel=True,ylabel=True):
        """add axis labels and a title."""
        
        # title
        if title is True:
            plt.title(self.ID, fontsize=16)
        elif title:
            plt.title(str(title), fontsize=16)
            
        # x label
        if xlabel is True:
            plt.xlabel(self.unitsTimeLong)
        elif xlabel:
            plt.xlabel(str(xlabel))
        
        # y label
        if ylabel is True:
            if command:
                plt.ylabel(self.unitsCommandLong)
            else:
                plt.ylabel(self.unitsLong)
        elif ylabel:
            plt.ylabel(str(ylabel))
            
        plt.margins(0,.1)
        plt.tight_layout()
    
if __name__=="__main__":   
    #abf=ABF(R"../../data/17o05028_ic_steps.abf")
#    abf=ABF(R"C:\Users\scott\Documents\GitHub\pyABF\data\14o08011_ic_pair.abf")
    #abf=ABF(R"../../data/17o05024_vc_steps.abf")
    #abf.info()
    
    
    abf=ABF("../../data/14o08011_ic_pair.abf")
    abf.setSweep(0,channel=0)
    plt.plot(abf.dataX,abf.dataY,label="Ch1")
    abf.setSweep(0,channel=1)
    plt.plot(abf.dataX,abf.dataY,label="Ch2")
    plt.axis([25,40,None,None])
    plt.legend()
    plt.show()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    