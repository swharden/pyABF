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
    def __init__(self,abfFileName,loadDataIntoMemory=True):
        """
        The ABFheader class provides low-level access to ABF file contents (header values and signal data).
        You can pull all the information you need from abf.header and abf.data. Additional functions help
        display header data in various formats.
            
        See what information is available about the ABF
            >>> abfHeader=ABFheader("filename.abf")
            >>> abfHeader.show()
            ### Header ###
            fFileSignature = b'ABF2'
            fFileVersionNumber = (0, 0, 0, 2)
            uFileInfoSize = 512
            lActualEpisodes = 187
            uFileStartDate = 20161205
            ...
            
            * This will list values which can be pulled from the abf.header dictionary by their names
            
        Get a value from the header by its name:
            >>> abf.header['lActualEpisodes'] # number of sweeps (episodes)
            187
            
            * Each variable in the header has a special name, but it's not always obvious what it means.
            * Check the ABF Format PDF http://mdc.custhelp.com/euf/assets/content/ABFHelp.pdf for info
            
        Get recorded signal data:
            >>> abf.data
            [-70.123, -70.321, ..., -70.213, -70.031]
            
            * If numpy is available, abf.data will be a numpy.ndarray with a 32-bit float datatype.
            * If numpy is not available, abf.data will be a list of python integers
            * Note that this doesn't work sweep by sweep, it's ALL the data in one array!
            * Dividing data into sweeps is your job.
            
        Save a formatted header to file:
            >>> abf.saveHTML("someFile.html")
            >>> abf.saveMarkdown("someFile.md")

        """
        
        # start our performance timer
        t1=time.perf_counter() 
        
        # open the file in binary mode
        self._fb = open(abfFileName,'rb') 
        
        # ensure our file type is supported
        if self._fb.read(4)==b'ABF2':
            pass
        elif self._fb.read(4)!=b'ABF1':
            raise ValueError('ABF1 files are not yet supported')
        else:
            raise ValueError('invalid file (does not appear to be an ABF at all!)')
        
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
                   
        # read the signal data into memory and scale it   
        self.data=self._fileReadData() if loadDataIntoMemory else None
        
        # we are now done reading contents of the ABF file
        self._fb.close()
        
        # stop the performance counter and calculate the time it took to load/process the ABF file
        self.abfLoadTime=(time.perf_counter()-t1)
            
    ### FILE READING
        
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
            
    ### HEADER DISPLAY
            
    def show(self):
        """Display the contents of the header to the console in an easy to read format."""
        for key in self.header.keys():
            if key.startswith("###"):
                print("\n%s"%key)
            else:
                print("%s = %s"%(key,self.header[key]))
        print()

    def saveHTML(self,fname):
        """Generate a HTML-formatted document with all header information."""
        html="<html><body><code>"
        for key in self.header.keys():
            if key.startswith("###"):
                html+="<br><b style='font-size: 200%%;'>%s</b><br>"%(key.replace("#","").strip())
            else:
                html+="%s = %s<br>"%(key,self.header[key])
        html+="</code></html></body>"
        with open(fname,'w') as f:
            f.write(html)
        print("wrote",os.path.abspath(fname))
        
    def saveMarkdown(self,fname):
        """Generate a markdown-formatted document with all header information."""
        out="# ABF Header Contents\n"
        for key in self.header.keys():
            if key.startswith("###"):
                out+="\n## %s\n"%(key.replace("#","").strip())
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

if __name__=="__main__":    
    print("DO NOT RUN THIS PROGRAM DIRECTLY")    
    abfFolder=os.path.dirname(__file__)+"/../../data/"
    abfFiles=[abfFolder+x for x in os.listdir(abfFolder) if x.endswith('.abf')]
    abf=ABFheader(abfFiles[0])
    abf.show()