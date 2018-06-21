"""
ABFheader - a python module to provide simple access to the content of ABF (Axon Binary Format) files.

GOAL:
    This standalone module is minimal and simplistic to facilitate learning and porting to other languages.
    Although other scripts in this project have complex dependencies (like numpy and matplotlib) this script 
    is entirely standalone and uses only standard python libraries.
    
NOTES:
    Only ABF2 is supported to keep things simple.
    
RESOURCES:
    Code here is a blend of original ideas and ideas compiled from reading others' code. For a full list of
    resources, see my Unofficial ABF File Format Guide (among other things) on the project homepage:
    https://github.com/swharden/pyABF/
"""

import os
import datetime
import struct
import collections

HEADER="""fFileSignature_4s,fFileVersionNumber_4b,uFileInfoSize_I,lActualEpisodes_I,uFileStartDate_I,
uFileStartTimeMS_I,uStopwatchTime_I,nFileType_H,nDataFormat_H,nSimultaneousScan_H,nCRCEnable_H,uFileCRC_I,
FileGUID_I,unknown1_I,unknown2_I,unknown3_I,uCreatorVersion_I,uCreatorNameIndex_I,uModifierVersion_I,
uModifierNameIndex_I,uProtocolPathIndex_I"""
SECTIONS="""ProtocolSection_IIl,ADCSection_IIl,DACSection_IIl,EpochSection_IIl,ADCPerDACSection_IIl,
EpochPerDACSection_IIl,UserListSection_IIl,StatsRegionSection_IIl,MathSection_IIl,StringsSection_IIl,
DataSection_IIl,TagSection_IIl,ScopeSection_IIl,DeltaSection_IIl,VoiceTagSection_IIl,SynchArraySection_IIl,
AnnotationSection_IIl,StatsSection_IIl"""
PROTO="""nOperationMode_h,fADCSequenceInterval_f,bEnableFileCompression_b,sUnused_3s,
uFileCompressionRatio_I,fSynchTimeUnit_f,fSecondsPerRun_f,lNumSamplesPerEpisode_i,lPreTriggerSamples_i,
lEpisodesPerRun_i,lRunsPerTrial_i,lNumberOfTrials_i,nAveragingMode_h,nUndoRunCount_h,nFirstEpisodeInRun_h,
fTriggerThreshold_f,nTriggerSource_h,nTriggerAction_h,nTriggerPolarity_h,fScopeOutputInterval_f,
fEpisodeStartToStart_f,fRunStartToStart_f,lAverageCount_i,fTrialStartToStart_f,nAutoTriggerStrategy_h,
fFirstRunDelayS_f,nChannelStatsStrategy_h,lSamplesPerTrace_i,lStartDisplayNum_i,lFinishDisplayNum_i,
nShowPNRawData_h,fStatisticsPeriod_f,lStatisticsMeasurements_i,nStatisticsSaveStrategy_h,fADCRange_f,
fDACRange_f,lADCResolution_i,lDACResolution_i,nExperimentType_h,nManualInfoStrategy_h,nCommentsEnable_h,
lFileCommentIndex_i,nAutoAnalyseEnable_h,nSignalType_h,nDigitalEnable_h,nActiveDACChannel_h,
nDigitalHolding_h,nDigitalInterEpisode_h,nDigitalDACChannel_h,nDigitalTrainActiveLogic_h,nStatsEnable_h,
nStatisticsClearStrategy_h,nLevelHysteresis_h,lTimeHysteresis_i,nAllowExternalTags_h,nAverageAlgorithm_h,
fAverageWeighting_f,nUndoPromptStrategy_h,nTrialTriggerSource_h,nStatisticsDisplayStrategy_h,
nExternalTagType_h,nScopeTriggerOut_h,nLTPType_h,nAlternateDACOutputState_h,nAlternateDigitalOutputState_h,
fCellID_3f,nDigitizerADCs_h,nDigitizerDACs_h,nDigitizerTotalDigitalOuts_h,nDigitizerSynchDigitalOuts_h,
nDigitizerType_h"""
ADC="""nADCNum_h,nTelegraphEnable_h,nTelegraphInstrument_h,fTelegraphAdditGain_f,
fTelegraphFilter_f,fTelegraphMembraneCap_f,nTelegraphMode_h,fTelegraphAccessResistance_f,nADCPtoLChannelMap_h,
nADCSamplingSeq_h,fADCProgrammableGain_f,fADCDisplayAmplification_f,fADCDisplayOffset_f,
fInstrumentScaleFactor_f,fInstrumentOffset_f,fSignalGain_f,fSignalOffset_f,fSignalLowpassFilter_f,
fSignalHighpassFilter_f,nLowpassFilterType_b,nHighpassFilterType_b,fPostProcessLowpassFilter_f,
nPostProcessLowpassFilterType_c,bEnabledDuringPN_b,nStatsChannelPolarity_h,lADCChannelNameIndex_i,
lADCUnitsIndex_i"""
DAC="""nDACNum_h,nTelegraphDACScaleFactorEnable_h,fInstrumentHoldingLevel_f,fDACScaleFactor_f,
fDACHoldingLevel_f,fDACCalibrationFactor_f,fDACCalibrationOffset_f,lDACChannelNameIndex_i,
lDACChannelUnitsIndex_i,lDACFilePtr_i,lDACFileNumEpisodes_i,nWaveformEnable_h,nWaveformSource_h,
nInterEpisodeLevel_h,fDACFileScale_f,fDACFileOffset_f,lDACFileEpisodeNum_i,nDACFileADCNum_h,nConditEnable_h,
lConditNumPulses_i,fBaselineDuration_f,fBaselineLevel_f,fStepDuration_f,fStepLevel_f,fPostTrainPeriod_f,
fPostTrainLevel_f,nMembTestEnable_h,nLeakSubtractType_h,nPNPolarity_h,fPNHoldingLevel_f,nPNNumADCChannels_h,
nPNPosition_h,nPNNumPulses_h,fPNSettlingTime_f,fPNInterpulse_f,nLTPUsageOfDAC_h,nLTPPresynapticPulses_h,
lDACFilePathIndex_i,fMembTestPreSettlingTimeMS_f,fMembTestPostSettlingTimeMS_f,nLeakSubtractADCIndex_h"""
EPPERDAC="""nEpochNum_h,nDACNum_h,nEpochType_h,fEpochInitLevel_f,fEpochLevelInc_f,
lEpochInitDuration_i,lEpochDurationInc_i,lEpochPulsePeriod_i,lEpochPulseWidth_i"""
TAGS="""lTagTime_i,sComment_56s,nTagType_h,nVoiceTagNumberorAnnotationIndex_h"""
EPSEC="""nEpochNum_h,nEpochDigitalOutput_h"""


class ABFheader:
    def __init__(self,abfFile,keepFileOpen=True):
        """
        Given an ABF (ABF2) file, return its header contents in a simple flat dictionary.
        abfFile could be a path (string) or an already-open file buffer (opened in rb mode)
        """
        self.abfFile = abfFile
        self.keepFileOpen = keepFileOpen
        
        # ensure our file is open in binary reading mode
        self.fileOpen(verify=True)
        
        # the header will be a dictionary maintained in order so section groups are easy to determine later
        self.header=collections.OrderedDict()
        
        # read the primary sections directly from the ABF file buffer
        self._fileReadStructMap(HEADER,sectionName="Header")
        self._fileReadStructMap(SECTIONS,76,16,sectionName="Section Map")
        self._fileReadSection('ProtocolSection',PROTO)
        self._fileReadSection('ADCSection',ADC)
        self._fileReadSection('DACSection',DAC)
        self._fileReadSection('EpochPerDACSection',EPPERDAC)
        self._fileReadSection('EpochSection',EPSEC)      
        self._fileReadSection('TagSection',TAGS)      
        if self.keepFileOpen is False:
            self._fileClose()
        
        # for lists with one element, simplify varName=[val] to varName=val
        for key in [key for key in self.header.keys() if len(self.header[key])==1]:
            self.header[key]=self.header[key][0]
        
        # add a few extra things I think are useful    
        self.header["### Extras ###"]=None
        self.header['abfFilePath']=os.path.abspath(self._fb.name)
        self.header['abfFileName']=os.path.basename(self._fb.name)
        self.header['abfID']=os.path.basename(self._fb.name)[:-4]
        dt=datetime.datetime.strptime(str(self.header['uFileStartDate']), "%Y%M%d")
        self.header['abfDatetime']=dt+datetime.timedelta(seconds=self.header['uFileStartTimeMS']/1000)
        self.header['dataByteStart']=self.header['DataSection'][0]*512
        self.header['timeSecPerPoint']=self.header['fADCSequenceInterval']/1e6
        self.header['timePointPerSec']=1e6/self.header['fADCSequenceInterval']
        self.header['rate']=1e6/self.header['fADCSequenceInterval']
        self.header['sweepPointCount']=self.header['lNumSamplesPerEpisode']
        self.header['sweepLengthSec']=self.header['sweepPointCount']*self.header['timeSecPerPoint']
        self.header['sweepCount']=self.header['lActualEpisodes']
        self.header['signalScale']=self.header['lADCResolution']/1e6
            
    ### FILE ACCESS AND STRUCT READING
    
    def fileOpen(self,verify=False):
        """Do what it takes to ensure our abf file is opened as a file buffer and is a valid ABF2 file"""
        if "_fb" in dir(self) and self._fb.__class__.__name__ == 'BufferedReader' and not self._fb.closed:
                return # already open and ready to go
        if type(self.abfFile) is str:
            self._fb = open(self.abfFile,'rb')
        elif self.abfFile.__class__.__name__ == 'BufferedReader':
            self._fb = self.abfFile
        else:
            raise ValueError('abfFile must be a path (string) or file buffer (opened in rb mode)')
        if verify and self._fb.read(4)!=b'ABF2':
            raise ValueError('abfFile must be an ABF2 file')
        return
    
    def fileClose(self):
        """If we opened the file earlier, be polite and close it as soon as possible"""
        self._fb.close()
        return
        
    def _fileReadStructMap(self,structMap,startByte=0,fixedOffset=None,sectionName=None):
        """Given a string of varName_varFormat structs, get the objects from the file."""
        if sectionName:
            self.header["### %s ###"%sectionName]=[None]
        self._fb.seek(startByte)
        for structCode in structMap.replace("\n","").split(","):
            varName,varFormat=structCode.strip().split("_")
            varVal=struct.unpack(varFormat,self._fb.read(struct.calcsize(varFormat)))
            varVal=varVal if len(varVal)>1 else varVal[0]
            self.header.setdefault(varName,[]).append(varVal) # pythonista
            if fixedOffset: 
                self._fb.read(fixedOffset-struct.calcsize(varFormat))

    def _fileReadSection(self,sectionName,structMap):
        """Read a structure map repeatedly according to its name in the section map."""
        self.header["### %s ###"%sectionName]=[None]
        entryStartBlock,entryBytes,entryCount=self.header[sectionName][0]
        for entryNumber in range(entryCount):
            self._fileReadStructMap(structMap,entryStartBlock*512+entryNumber*entryBytes)
            
            
    ### SIGNAL DATA RETRIEVAL
    
    def getData(self,firstPoint=0,lastPoint=None,channel=0):
        """Return an arbitrary amount of signal data. You must multiply by signalScale."""
        if channel>0:
            raise ValueError('multi-channel ABFs have not been added yet') #TODO: this
        if lastPoint is None:
            lastPoint = self.header['DataSection'][2]
        elif lastPoint > self.header['DataSection'][2]:
            raise ValueError('the lastPoint is bigger than the number of points in the ABF')
        self.fileOpen()
        self._fb.seek(int(self.header['dataByteStart']+firstPoint*2))
        data = self._fb.read((lastPoint-firstPoint)*2)
        data = struct.unpack("%dh"%(int(lastPoint-firstPoint)),data)
        if self.keepFileOpen is False:
            self.fileClose()
        return data
            
    def getDataSweep(self,sweep=0,channel=0):
        """Return the values from a single sweep (starting at zero). You must multiply by signalScale."""
        if channel>0:
            raise ValueError('multi-channel ABFs have not been added yet') #TODO: this
        firstPoint=sweep*self.header['sweepPointCount']
        lastPoint=(sweep+1)*self.header['sweepPointCount']
        return self.getData(firstPoint,lastPoint)
        
    ### FUNCTIONS TO DISPLAY HEADER INFORMATION
            
    def show(self):
        """Display the contents of the header to the console in an easy to read format."""
        for key in self.header.keys():
            if key.startswith("###"):
                print("\n%s"%key)
            else:
                print("%s = %s"%(key,self.header[key]))

    def saveHTML(self,fname="./_demo.html"):
        """Generate a HTML-formatted document with all header information."""
        html="<html><body><code>"
        for key in self.header.keys():
            if key.startswith("###"):
                key=key.replace("#","").strip()
                html+="<br><b style='font-size: 200%%;'>%s</b><br>"%key
            else:
                html+="%s = %s<br>"%(key,self.header[key])
        html+="</code></html></body>"
        with open(fname,'w') as f:
            f.write(html)
        print("wrote",os.path.abspath(fname))
        
    def saveMarkdown(self,fname="./_demo.md"):
        """Generate a markdown-formatted document with all header information."""
        out="# ABF Header Contents\n"
        for key in self.header.keys():
            if key.startswith("###"):
                key=key.replace("#","").strip()
                out+="\n## %s\n"%key
            else:
                out+="* %s = `%s`\n"%(key,self.header[key])
        with open(fname,'w') as f:
            f.write(out)
        print("wrote",os.path.abspath(fname))   


def checkSweepLoadTime(abfFileName,extractionCount=10,closeBetweenSweeps=False):
    """
    Pull the first sweep from an abf extractionCount times.
    Determine how long this takes when the file is left open vs opened/closed for each sweep.
    """
    import time
    import numpy as np
    
    abfHeader=ABFheader(abfFileName)
    nSweeps=abfHeader.header['sweepCount']
    print("\nTEST: load %d sweeps (%d times)"%(nSweeps,extractionCount),end="")
    print(" NOT"*(not closeBetweenSweeps),"closing the file between sweeps")
    
    timesLeftOpen=[]
    abfHeader.keepFileOpen=True
    for i in range(extractionCount):
        t1=time.perf_counter()
        for j in range(nSweeps):
            abfHeader.getDataSweep(j)
            if closeBetweenSweeps:
                abfHeader.fileClose()
        t2=time.perf_counter()
        timesLeftOpen.append((t2-t1)*1000000) # microseconds
    print(" AVG: %.02f microseconds per sweep"%(np.average(timesLeftOpen)/extractionCount/nSweeps))
        
    #timesOpenedAndClosed=[]
    

#def stressTest(repetitions=10):
#    import matplotlib.pyplot as plt
#    import numpy as np
#    import time
#    times=[]
#    for i in range(repetitions):
#        print("running %d of %d (%.02f%%)"%(i+1,repetitions,i/repetitions*100))
#        t1=time.process_time()
#        #### THIS BLOCK GETS TIMED ####
#        for sweepNumber in range(abfHeader.header['sweepCount']):
#            data=abfHeader.getDataSweep(sweepNumber)
#            data=np.array(data)*abfHeader.header['signalScale']        
#            abfHeader._fileClose()
#        ###############################        
#        t2=time.process_time()
#        times.append((t2-t1)*1000)
#    #print(times)
#    plt.figure(figsize=(5,5))
#    plt.grid(alpha=.2)
#    plt.title("ABFheader Stress Test")
#    plt.plot(times,'.',ms=20,alpha=.5)
#    plt.margins(.1,.3)
#    plt.axhline(np.average(times),ls='--',color='r',alpha=.5,lw=2,label="AVG: %s"%np.average(times))
#    plt.ylabel("Execution Time (ms)")
#    plt.xlabel("Run Number")
#    plt.legend()
#    plt.tight_layout()
#    plt.show()
    

if __name__=="__main__":   
    
    checkSweepLoadTime(R"../../../../data/16d05007_vc_tags.abf")
    checkSweepLoadTime(R"../../../../data/16d05007_vc_tags.abf",closeBetweenSweeps=True)
    
    ### LOAD AN ABF FILE
    #abfHeader=ABFheader(R"../../../../data/16d05007_vc_tags.abf")
    
    ### DISPLAY THE HEADER
    #abfHeader.show()
    #abfHeader.saveHTML()
    #abfHeader.saveMarkdown()
       
    ### TESTING ###    
    #stressTest()
    #abfHeader._fileClose()
    
    
    