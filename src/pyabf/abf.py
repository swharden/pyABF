"""Code to interact with ABF files. https://github.com/swharden/pyABF/ """

import numpy as np
np.set_printoptions(suppress=True) # don't use scientific notation
import matplotlib.pyplot as plt
    
from pyabf.header import ABFheader

class ABF:
    def __init__(self,abf):
        """The ABF class provides easy pythonic access to header and signal 
        data in ABF files. Although it is typically instantiated with a path
        (string), you can also use an ABF or ABFheader. This will reset that
        ABF to default values without re-loading original data from the file.
        
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
        self.pointsPerMS = self.pointsPerSec/1000
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
        
        ### Preload signal and time data (totalling ~10MB of memory per minute of 20kHz recording)
        self.signalData = self._abfHeader.data/self.dataChannels
        self.signalTimes = np.arange(len(self.signalData),dtype='float32')*self.pointDurSec
                          
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
            self.epochDuration = self._abfHeader.header['lEpochInitDuration'] # in points
            self.epochDurationDelta = self._abfHeader.header['lEpochDurationInc']
            self.epochPulsePeriod = self._abfHeader.header['lEpochPulsePeriod']
            self.epochPulseWidth = self._abfHeader.header['lEpochPulseWidth']
            self.epochDigOut = self._abfHeader.header['nEpochDigitalOutput']
            self.epochStartPoint = [self.pointsPerSweep/64]
            for i,duration in enumerate(self.epochDuration):
                self.epochStartPoint.append(self.epochStartPoint[-1]+duration+self.epochDurationDelta[i]*i)
            self.epochStartSec=[self.signalTimes[int(x)] for x in self.epochStartPoint]
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
            self.epochStartSec = []
            self.epochStartPoint = []
                  
        ### Go ahead and set sweep zero to populate command signal trace
        self.setSweep(0)

    def help(self):
        """Launch the pyABF website in a web browser."""
        import webbrowser
        webbrowser.open('https://github.com/swharden/pyABF')
                                    
    def info(self,silent=False):
        """
        Display (and return) a long message indicating what you can access
        and do with the ABF class.
        """
        functions,attributes,lists,data=[],[],[],[]
        for itemName in dir(self):
            if itemName.startswith("_"):
                continue
            itemType=str(type(getattr(self,itemName))).split("'")[1]
            if itemType in ['str','float','int','bool']:
                attributes.append(itemName)
            elif itemType =='list':
                lists.append(itemName)
            elif itemType =='numpy.ndarray':
                data.append(itemName)
            elif itemType =='method':
                functions.append(itemName)
            elif itemType in ['datetime','datetime.datetime']:
                continue
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
        """
        Load a particular sweep (and times and command trace) into memory.
        This populates self.dataX, self.dataY, and self.dataC.
        
        If absoluteTime is used, self.dataX will reflect the time points
        (in seconds) of the sweep relative to the total experiment. If it is
        not used, self.dataX will always start at 0 (and display "sweep time").
        """
        #TODO: make function to get sweep-offset time
        #TODO: command signal not supported if using multi-channel
        if sweepNumber is None:
            return
        if sweepNumber<0:
            sweepNumber=self.sweepList[sweepNumber]
        if not sweepNumber in self.sweepList:
            raise ValueError("Sweep %d not found (last sweep is %d)"%(sweepNumber,self.sweepList[-1]))
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
        if self.gaussianSigma:
            self.dataY = self._filterGaussian(self.dataY)
            
    def _updateCommandWaveform(self):
        """Read the epochs and populate self.dataC with the command signal."""
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
        
    ### FILTERING
    
    gaussianSigma=0
    gaussianLeft=False
    gaussianRight=True
    
    def _filterGaussian(self,signal,sigma=None):
        """Perform gaussian smoothing on a 1d array."""
        if self.gaussianLeft and self.gaussianRight:
            raise ValueError("can't set both gaussianLeft and gaussianRight")
        if sigma is None:
            sigma=self.gaussianSigma
        if self.gaussianLeft or self.gaussianRight:
            sigma*=2
        size=sigma*10
        points=np.exp(-np.power(np.arange(size)-size/2,2)/(2*np.power(sigma,2)))
        if self.gaussianLeft:
            points[-int(len(points)/2):]=0
        if self.gaussianRight:
            points[0:int(len(points)/2)]=0            
        kernel=points/sum(points)
        return np.convolve(signal,kernel,mode='same')
    
    def _filterSimple(self,signal,sigma):
        """return a Gaussian filtered signal."""
        size=sigma*10
        points=np.exp(-np.power(np.arange(size)-size/2,2)/(2*np.power(sigma,2)))
        kernel=points/sum(points)
        return np.convolve(signal,kernel,mode='same')
    
    ### ANALYSIS
    
    def rms(self,chunkMS=10,quietestMS=100):
        """
        Return the RMS value of the noise floor. RMS = stdev when mean is 0.
        The noise floor is defined as the quietest parts of the signal.
        """
        chunkSize=chunkMS*self.pointsPerMS
        chunkCount=int(len(self.dataY)/chunkSize)
        stdev=np.empty(chunkCount)
        for chunkNumber in range(chunkCount):
            i1=int(chunkSize*chunkNumber)
            i2=int(chunkSize*(chunkNumber+1))
            stdev[chunkNumber]=np.std(self.dataY[i1:i2])
        countToAverage=int(quietestMS/chunkMS)
        rms=np.mean(sorted(stdev)[:countToAverage])
        return rms
    
    def _tonic(self,data,binSize=.1,fitAboveFrac=.25):
        """
        Return a polynomial-fitted peak of the histogram of the given data.
        Only histogram points above "fitAboveFrac" are fitted.
        """
        padSize=int(200/binSize)*2
        pad=np.arange(padSize)*binSize
        bins = np.concatenate((data[0]-pad[::-1],data[0]+pad))
        histCount,histBins=np.histogram(data,bins=bins)
        histBins=histBins[:-1]
        validIs=histCount>np.max(histCount)*fitAboveFrac
        histBins=histBins[validIs]
        histCount=histCount[validIs]
        fit = np.poly1d(np.polyfit(histBins,histCount,6))
        histFitVals = fit(histBins)
        histFitPeakVal=np.max(histFitVals)
        histFitPeakI=np.where(histFitVals==histFitPeakVal)[0]
        tonicValue=histBins[histFitPeakI]
        return float(tonicValue)
    
    def tonicPhasic(self,t1=0,t2=None):
        """
        Return [tonic, phasicNeg, and phasicPos] of the selected sweep.
        Tonic is the peak value of the polynomial-fitted histogram.
        Phasic is the average value of all points below or above the tonic 
        value. All 3 are in abf.units units.
        """
        if not t2:
            t2=self.sweepLengthSec
        i1,i2=int(t1*self.pointsPerSec),int(t2*self.pointsPerSec)
        data=self.dataY[i1:i2]
        tonicValue=self._tonic(data)
        phasicNeg=tonicValue-np.average(data[data<tonicValue])
        phasicPos=np.average(data[data>tonicValue])-tonicValue
        return [tonicValue,phasicNeg,phasicPos]
    
    def average(self,t1=0,t2=None,setSweep=False,tonic=False):
        """
        Return the average value of the selected sweep. If t1 and/or t2 are 
        given, data between those times (seconds) will be measured. If tonic
        is True, the tonic (histogram fit) method will be used instead of
        a true average.
        """
        if not setSweep is False:
            self.setSweep(setSweep)
        if not t2:
            t2=self.sweepLengthSec
        i1=int(t1*self.pointsPerSec)
        i2=int(t2*self.pointsPerSec)
        if tonic:
            return self._tonic(self.dataY[i1:i2])
        else:
            return np.nanmean(self.dataY[i1:i2])
    
    def averageEpoch(self,epoch,firstFrac=False,lastFrac=False,setSweep=False,
                     tonic=False):
        """
        Return the average of some fraction of an epoch. Similar to average(), 
        but uses an epoch number and fraction rather than time points.
        
        Example: return the average of the last 25% of epoch B
            >>> abf.averageEpoch(epoch=1,lastFrac=.25)
            
        """
        if not setSweep is False:
            self.setSweep(setSweep)
        if firstFrac and lastFrac:
            raise ValueError("can't set both a first and last fraction")
        epochs=self.epochStartPoint+[self.pointsPerSweep]
        if epoch<(len(self.epochStartPoint)-1):
            i2=epochs[epoch+1]
            i1=i2-self.epochDuration[epoch]
        else:
            i2=self.pointsPerSweep
            i1=epochs[epoch]
        dur=i2-i1
        if firstFrac:
            i2=i1+dur*firstFrac
        if lastFrac:
            i1=i2-dur*lastFrac
        if tonic:
            return self._tonic(self.dataY[int(i1):int(i2)])
        else:
            return np.nanmean(self.dataY[int(i1):int(i2)])
    
    def stdev(self,t1=0,t2=None):
        """
        Return the standard deviation of current sweep between two times (sec)
        """
        if not t2:
            t2=self.sweepLengthSec
        i1=int(t1*self.pointsPerSec)
        i2=int(t2*self.pointsPerSec)
        return np.nanstd(self.dataY[i1:i2])
    
    def stderr(self,t1=0,t2=None):
        """
        Return the standard error of current sweep between two times (sec)
        """
        if not t2:
            t2=self.sweepLengthSec
        i1=int(t1*self.pointsPerSec)
        i2=int(t2*self.pointsPerSec)
        return np.nanstd(self.dataY[i1:i2])/np.math.sqrt(i2-i1)
    
#    def sweepSpan(self,t1=0,t2=None):
#        """
#        Return just the dataY between two time points (sec)
#        """
#        if not t2:
#            t2=self.sweepLengthSec
#        i1=int(t1*self.pointsPerSec)
#        i2=int(t2*self.pointsPerSec)
#        return self.dataY[i1:i2]
            
    ### EVENT DETECTION
        
    
    def eventsDeriv(self, setSweep=None, t1=0, t2=None, dTms=1, threshold=-10, 
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
        if not setSweep is None:
            self.setSweep(setSweep)
        if not t2:
            t2=self.sweepLengthSec
        i1,i2=int(t1*self.pointsPerSec),int(t2*self.pointsPerSec)
        
        # load the data and calculate its derivative
        strip=self.dataY[i1:i2]
        Xs=self.dataX[i1:i2]
        dT=int(self.pointsPerMS*dTms)
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
            revertPoints=int(self.pointsPerMS*mustRevertMS)
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
            plt.title("sweep %d (raw signal, %s)"%(self.sweepSelected,self.units))
            plt.plot(Xs,strip)
            for eventI in [int(self.pointsPerSec*x) for x in eventTimes]:
                plt.axvline(self.dataX[eventI],color='r',alpha=.5)
            plt.subplot(212,sharex=ax1)
            plt.title("first derivative (%s / ms)"%self.units)
            plt.plot(Xs,deriv)
            plt.axhline(threshold,color='r',alpha=.5)
            for eventI in [int(self.pointsPerSec*x) for x in eventTimes]:
                plt.axvline(self.dataX[eventI],color='r',alpha=.5)
            plt.margins(0,.1)
            plt.tight_layout()                
            plt.show()
        
        return eventTimes
    
    ### PLOTTING
    
    def plotEpochs(self):
        """
        Display a matplotlib figure of the current sweep highlighting epochs.
        """
        epochBoundsSec = self.epochStartSec + [self.sweepLengthSec]
        command = self.epochCommand + [self.commandHold]
        plt.plot(self.dataX,self.dataY,'k-')
        for i in range(len(self.epochStartSec)):
            plt.axvspan(epochBoundsSec[i],epochBoundsSec[i+1],alpha=.3,color=self._sweepColor(i),
                        lw=0,label=("%s: (%s %s)"%(chr(65+i),command[i],self.unitsCommand)))
        plt.legend(fontsize=8)
        self.plotDecorate(zoomYstdev=True)
    
    colormap="jet_r"
    def _sweepColor(self,sweep=None):
        """
        Return a colorcode of the current sweep using abf.colormap
        """
        if sweep is None:
            sweep=self.dataSweepSelected
        frac = sweep/self.sweepCount
        return plt.cm.get_cmap(self.colormap)(frac)
    
    def plotSweeps(self,sweeps=None,offsetX=0,offsetY=0,useColormap=False,
                   color='b'):
        """
        Plot signal data using matplotlib.If sweeps is a list of numbers, 
        only plot those sweeps. Also accepts an integer to plot one sweep.
        """
        if type(sweeps)==list:
            pass
        elif sweeps == None or sweeps == False:
            sweeps=self.sweepList
        else:
            sweeps=[sweeps]
        
        for sweepNumber in sweeps:
            self.setSweep(sweepNumber)            
            if useColormap:
                color=self._sweepColor()
            plt.plot(self.dataX+offsetX*sweepNumber,
                     self.dataY+offsetY*sweepNumber,
                     color=color)
            
        plt.margins(0,.1)
        
        
    def plotDecorate(self,command=False,title=True,xlabel=True,ylabel=True,
                     zoomYstdev=False,legend=False,axis=None):
        """
        Add axis labels and a title to the already-drawn matplotlib figure.
        
        Arguments: 
            * zoomYstdev - optionally zoom in vertically to a certain number
                           of standard deviations from the mean.
            * axis - if provided, resize to this axis [X1,X2,Y1,Y2]
        """
                
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
        
        if zoomYstdev:
            if zoomYstdev is True:
                zoomYstdev=3
            else:
                zoomYstdev=int(zoomYstdev)
            av=np.nanmean(self.dataY)
            stdev=np.nanstd(self.dataY)
            plt.axis([None,None,av-stdev*zoomYstdev,av+stdev*zoomYstdev])
            
        if legend:
            if type(legend) is int:
                plt.legend(legend)
            else:
                plt.legend()
        
        if axis:
            plt.axis(axis)
        
        plt.tight_layout()

    def memtest(self,lastFrac=.5,fracFirst=False,plot=False):
        """
        When called on a voltage-clamp trace, this function will detect the
        first voltage step and use it to determine Rm and Ra. lastFrac
        indicates what fraction of the last portion of a step will be used
        for measurement. If firstFrac is false, the pre-step region will
        not be fractionated prior to measurement.
        """
        if not abf.units=="pA":
            raise ValueError("memtest should only be run on VC traces")
            
        # determine which epoch has the first voltage step
        for epochNumber in range(abf.epochCount):
            if abf.epochCommand[epochNumber]==abf.commandHold:
                continue
            else:
                #print("epoch %d steps to %.02f %s"%(epochNumber,abf.epochCommand[epochNumber],abf.units))
                break
        else:
            raise ValueError("no epoch step found")
            
        # Calculate T1, T2, and T3 bounding two epochs
        #print("first epoch with a step:",epochNumber)
        i2=int(abf.epochStartPoint[epochNumber])
        i3=int(i2+abf.epochDuration[epochNumber])
        if epochNumber==0:
            i1=0
        else:
            i1=int(abf.epochStartPoint[epochNumber-1])
            
        #print("index bounds:",i1,i2,i3)
        if fracFirst:
            step1i1=int(i2-(i2-i1)*lastFrac)
        else:
            step1i1=i1
        step1i2=i2
        step2i1=int(i3-(i3-i2)*lastFrac)
        step2i2=i3
        
        step1=abf.dataY[step1i1:step1i2]
        step2=abf.dataY[step2i1:step2i2]
        step1level=self._tonic(step1)
        step2level=self._tonic(step2)
        step1command=self.dataC[step1i1+1]
        step2command=self.dataC[step2i1+1]
        
        dV=np.abs(step2command-step1command)/1e3
        dI=np.abs(step2level-step1level)/1e9
        #V=IR, R=V/I, R=dv/dI
        r=dV/dI
        print(r/1e6)
        
        
        if plot:
            plt.plot(abf.dataY[:i3])
            plt.axvspan(step1i1,step1i2,alpha=.2)
            plt.axvspan(step2i1,step2i2,alpha=.2)
            plt.axhline(step1level,color='r',ls='--')
            plt.axhline(step2level,color='r',ls='--')
            plt.axis([i1,i3,-25,0])
            plt.title("sweep %d"%self.dataSweepSelected)
            plt.ylabel(abf.units)
            plt.show()
        
        #i1=int(i2-step1width*lastFrac)
        

def listDemoFiles():
    import glob
    for fname in sorted(glob.glob("../../data/*.abf")):
        print(fname)
    
if __name__=="__main__":   
    print("do not run this script directly.")
    #listDemoFiles()
    
    
    #abf=ABF(R"../../data/17o05024_vc_steps.abf")
    abf=ABF(R"../../data/16d05007_vc_tags.abf")
    #plt.plot(abf.dataY)
    np.save("../../cookbook/memtest.npy",abf.dataY[:7000])
#    for sweep in abf.sweepList:
#        abf.setSweep(sweep)
#        abf.memtest(plot=True)

        
    
    print("DONE")    