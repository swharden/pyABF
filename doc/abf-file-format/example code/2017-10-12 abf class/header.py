"""
ABFheader - a python module to provide simple access to header content of ABF (Axon Binary Format) files.

GOAL:
    This standalone module is minimal and simplistic to facilitate learning and porting to other languages.
    Although other scripts in this project have complex dependencies (like numpy and matplotlib) this script 
    is entirely standalone and uses only standard python libraries.
    
NOTE ABOUT NUMPY:
    When it comes time to read values out of ABF files and scale them, numpy-optimized vector math offers
    a massive performance improvement! I'm not making numpy required to use this code. Everything will
    work without numpy. BUT, if numpy is found, it will use it when doing vector operations on signals.
    
RESOURCES:
    Code here is a blend of original ideas and ideas compiled from reading others' code. For a full list of
    resources, see my Unofficial ABF File Format Guide (among other things) on the project homepage:
    https://github.com/swharden/pyABF/
"""

import os
import time
import datetime
import struct
import collections
import warnings

try:
    import numpy as np
except:
    np=False

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
    def __init__(self,abfFile,silent=False):
        """
        The ABFheader class provides low-level access to ABF file contents (header values and signal data).
        The given abfFile could be a path (string) or an already-open file buffer (opened in rb mode).
        If loadRawData is enabled, all data (signals) will be read from the ABF file up front. This will
        cause instantiation to take a little longer, but prevent file locking and bottlenecks later.
        """
        
        t1=time.perf_counter()
        self._abfFile = abfFile
        
        # ensure our file is open in binary reading mode
        self._fileOpen()
        
        # ensure our file is an ABF2 file
        if self._fb.read(4)!=b'ABF2':
            raise ValueError('abfFile must be an ABF2 file')
        
        # read all header contents into an ordered dictionary
        self.header=collections.OrderedDict()
        self._fileReadStructMap(HEADER,sectionName="Header")
        self._fileReadStructMap(SECTIONS,76,16,sectionName="Section Map")
        self._fileReadSection('ProtocolSection',PROTO)
        self._fileReadSection('ADCSection',ADC)
        self._fileReadSection('DACSection',DAC)
        self._fileReadSection('EpochPerDACSection',EPPERDAC)
        self._fileReadSection('EpochSection',EPSEC)      
        self._fileReadSection('TagSection',TAGS) 
        
        # if a header item is a list with one item, just make it that item
        for key in [key for key in self.header.keys() if len(self.header[key])==1]:
            self.header[key]=self.header[key][0]
        
        # improve comments by making them strings (not bytestrings) and stripping whitespace
        if 'sComment' in self.header.keys():
            self.header['sComment']=[x.decode().strip() for x in self.header['sComment']]
        
        # add a few extra things I think are useful    
        self.header["### Extras ###"]=None
        self.header['abfFilename']=os.path.abspath(self._fb.name)
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
        self.header['gain']=self.header['fTelegraphAdditGain']
        self.header['mode']="IC" if self.header['nTelegraphMode'] else "VC"
        self.header['units']="mV" if self.header['mode']=="IC" else "pA"
        self.header['unitsCommand']="pA" if self.header['mode']=="IC" else "mV"
        self.header['filterKHz']=self.header['fTelegraphFilter']/1e3
        self.header['commandHoldingByDAC']=self.header['fDACHoldingLevel']
                   
        # read the signal data and scale it
        self._fileReadData()
        
        # release the ABF file - we are totally done with it!
        self._fileClose()
        
        # display info
        loadTime=(time.perf_counter()-t1)*1000 #ms
        if not silent:
            print("%s loaded (%.02f ms)"%(os.path.basename(self.header['abfFilename']),loadTime))
            
    ### FILE ACCESS AND STRUCT READING
    
    def _fileOpen(self):
        """Do what it takes to ensure our abf file is opened as a file buffer and is a valid ABF2 file"""
        if "_fb" in dir(self) and self._fb.__class__.__name__ == 'BufferedReader' and not self._fb.closed:
                return # already open and ready to go
        if type(self._abfFile) is str:
            self._fb = open(self._abfFile,'rb')
        elif self._abfFile.__class__.__name__ == 'BufferedReader':
            self._fb = self._abfFile
        else:
            raise ValueError('abfFile must be a path (string) or file buffer (opened in rb mode)')
        return
    
    def _fileClose(self):
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
    
    def _fileReadData(self):
        """Read the full file data into memory. Scale it too. Uses numpy if available."""
        self._fb.seek(self.header['dataByteStart'])
        pointCount = self.header['DataSection'][2]
        scaleFactor = self.header['lADCResolution'] / 1e6
        if np:
            self.data = np.fromfile(self._fb, dtype=np.int16, count=pointCount)
            self.data = np.multiply(self.data,scaleFactor,dtype='float32')
        else:
            warnings.warn("Numpy is not installed. We can go without it, but performance will suffer.")
            self.data = struct.unpack("%dh"%(pointCount), self._fb.read(pointCount*2))
            self.data = [point*scaleFactor for point in self.data]
            
    def getSweepData(self,sweep=0):
        """Return the scaled values from a sweep (starting at sweep zero)."""
        firstPoint=sweep*self.header['sweepPointCount']
        lastPoint=(sweep+1)*self.header['sweepPointCount']
        return self.data[firstPoint:lastPoint]
    
    def getSweepTimes(self,sweep=0):
        if np:
            times = np.arange(self.header['sweepPointCount'])*self.header['timeSecPerPoint']
            times = times+sweep*self.header['sweepLengthSec']
        else:
            times = range(self.header['sweepPointCount'])
            times = [x*self.header['timeSecPerPoint']+sweep*self.header['sweepLengthSec'] for x in times]
        return times
            
    def show(self):
        """Display the contents of the header to the console in an easy to read format."""
        for key in self.header.keys():
            if key.startswith("###"):
                print("\n%s"%key)
            else:
                print("%s = %s"%(key,self.header[key]))
        print()

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

def compareHeaders(abfFile1,abfFile2):
    """Given two ABF filenames, show how their headers are different."""
    header1=ABFheader(abfFile1).header
    header2=ABFheader(abfFile2).header
    for key in header1.keys():
        if not key in header2.keys():
            continue
        if key.startswith("#"):
            print("\n"+key)
        if header1[key]==header2[key]:
            continue
        if type(header1[key]) in [list, tuple]:
            continue
        else:
            print(key,header1[key],header2[key])

def _demo_plot():
    """
    Demonstrate how to use matplotlib and the ABFheader class to display some data.
    A higher level ABF class should really be in charge of things like this, but it's here for example.
    """
    import matplotlib.pyplot as plt
    abfHeader=ABFheader(R"../../../../data/17o05028_ic_steps.abf")
    plt.figure(figsize=(8,4))
    plt.grid(alpha=.2)
    times = abfHeader.getSweepTimes()
    for sweepNumber in [0,5,10,15]:
        data = abfHeader.getSweepData(sweepNumber)
        plt.plot(times,data,lw=.7,alpha=.8,label="sweep %d"%sweepNumber)
    plt.margins(0,.1)
    plt.legend(fontsize=8)
    plt.title("Demonstrating the ABFheader Class")
    plt.ylabel("Membrane Potential (mV)")
    plt.xlabel("Time (seconds)")
    plt.tight_layout()
    plt.savefig("_demo.png")
    plt.show()

if __name__=="__main__":    
    print("DO NOT RUN THIS PROGRAM DIRECTLY")
    
    _demo_plot()
    
    #abfHeader=ABFheader(R"../../../../data/17o05028_ic_steps.abf")
    #abfHeader.show()
    #abfHeader.saveHTML()
    #abfHeader.saveMarkdown()