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
        
        Separate multichannel data (it's just interleaved):
            >>> abf=ABFheader(abfFileName)
            >>> for i in range(abf.header['dataChannels']):
            >>>     print(abf.data[i::abf.header['dataChannels']])
            [-146.34 -144.96 -145.65 ..., -117.11 -116.55 -117.37]
            [ 624.13  624.06  624.19 ...,  624.32  624.45 624.45]
            
        Save a formatted header to file:
            >>> abf.saveHTML("someFile.html")
            >>> abf.saveMarkdown("someFile.md")

        """
        
        t1=time.perf_counter() 
        self._fb = open(abfFileName,'rb')
        self._fileSignature=self._fb.read(4)
        if self._fileSignature==b'ABF ':
            self._readHeaderABF1()
        elif self._fileSignature==b'ABF2':
            self._readHeaderABF2()
        else:
            raise ValueError('invalid file (does not appear to be an ABF at all!)')
                           
        # read the signal data into memory and scale it   
        self.data=None
        if loadDataIntoMemory:
            self._fileReadData()
        
        # we are now done reading contents of the ABF file
        self._fb.close()
        
        # stop the performance counter and calculate the time it took to load/process the ABF file
        self.abfLoadTime=(time.perf_counter()-t1)
        
    ### HEADER READING AND VALUE TOUCHUP
        
    def _readHeaderABF1(self):
        """populate self.header with values read the ABF1 header. Not many extra keys are added."""
        self.header=collections.OrderedDict()
        self.header["### ABF1 Header ###"]=[None]
        for key,offset,varFormat in HEADERV1:
            self._fb.seek(offset)
            varVal=list(struct.unpack(varFormat,self._fb.read(struct.calcsize(varFormat))))
            for i,item in enumerate(varVal):
                if type(item)==bytes:
                    varVal[i]=item.decode().strip() #TODO: this for ABF2 comments
            self.header[key]=varVal
        for key in [key for key in self.header.keys() if len(self.header[key])==1]:
            self.header[key]=self.header[key][0] # flatten lists with just 1 element

        # add a few extra things I think are useful. This list isn't as extensive as ABF2
        sz = struct.calcsize("2i") if self.header['nDataFormat'] == 0 else struct.calcsize("4f")
        self.header['dataByteStart']=self.header['lDataSectionPtr']*512+self.header['nNumPointsIgnored']*sz
        self.header['dataPointCount']=self.header['lActualAcqLength']
        self.header['dataChannels']=self.header['nADCNumChannels']
        self.header['timeSecPerPoint']=self.header['fADCSampleInterval']/1e6
        self.header['timePointPerSec']=1e6/self.header['fADCSampleInterval']
        self.header['abfFilename']=os.path.abspath(self._fb.name)
        self.header['abfID']=os.path.basename(self._fb.name)[:-4]
        self.header['abfDatetime']="ABF1 not sure"
        self.header['sweepPointCount']=int(self.header['lNumSamplesPerEpisode']/self.header['dataChannels'])
        self.header['rate']=1e6/self.header['fADCSampleInterval']
        self.header['sweepCount']=self.header['lActualEpisodes']
        self.header['sweepLengthSec']=self.header['sweepPointCount']*self.header['timeSecPerPoint']
        self.header['mode']="IC" if self.header['sADCUnits'][0]=="mV" else "VC"
        self.header['units']="mV" if self.header['mode']=="IC" else "pA"
        self.header['unitsCommand']="pA" if self.header['mode']=="IC" else "mV"
        self.header['commandHoldingByDAC']=self.header['fEpochInitLevel']
        self.header['lEpochPulsePeriod']=None #pulses unsupported in ABF1
        self.header['lEpochPulseWidth']=None #pulses unsupported in ABF1
        self.header['nEpochDigitalOutput']=self.header['nDigitalValue']        
        self.header['dataScale']=self.header['lADCResolution']/1e6        
        self.header['protocolPath']=self._readHeaderProtocol()
        self.header['protocol']=os.path.basename(self.header['protocolPath'])
        self._calculateScaleFactor()
        #TODO: make ABF1 header items the same as ABF2 headers. There are so many commonalities.
        return
    
    def _readHeaderABF2(self):
        """populate self.header with values read the ABF2 header. Extra helpful keys are added too."""
        
        # pull values out of the header
        self.header=collections.OrderedDict()
        self._byteMap=collections.OrderedDict()
        self._fileReadStructMap(HEADER,sectionName="Header")
        self._fileReadStructMap(SECTIONS,76,16,sectionName="Section Map")
        self._fileReadSection('ProtocolSection',PROTO)
        self._fileReadSection('ADCSection',ADC)
        self._fileReadSection('DACSection',DAC)
        self._fileReadSection('EpochPerDACSection',EPPERDAC)
        self._fileReadSection('EpochSection',EPSEC)      
        self._fileReadSection('TagSection',TAGS)

        # strings section takes extra effort
        STRINGS="strings_%ds"%(self.header["StringsSection"][0][1])
        self._fileReadSection('StringsSection',STRINGS)
        for i,s in enumerate(self.header["strings"]):
            s=s.strip(chr(0).encode("ascii"))
            s=s.split(chr(0).encode("ascii"))
            while b' ' in s:
                s.remove(b' ')
            for j in range(len(s)):
                s[j]=s[j].decode("ascii", errors='ignore')
            s=",".join(s)
            self.header["string_%02d"%(i)]=s
        
        # take extra care of the first string, as it contains unit info
        s = self.header["string_00"]
        while ",," in s:
            s=s[1:]
        indexedUnits = s.split(",")
        for i in range(len(indexedUnits)):
            self.header["indexedUnit_%02d"%(i)]=indexedUnits[i]

        # misc indexed strings
        self.header["uCreatorName"]=indexedUnits[self.header["uCreatorNameIndex"][0]]
        self.header["uModifierNameIndex"]=indexedUnits[self.header["uModifierNameIndex"][0]]
        self.header["uProtocolPathIndex"]=indexedUnits[self.header["uProtocolPathIndex"][0]]
        self.header["lFileCommentIndex"]=indexedUnits[self.header["lFileCommentIndex"][0]]

        # create lists of units (ADC)
        if type(self.header["lADCUnitsIndex"]) == int:
            self.header["lADCUnitsIndex"] = [self.header["lADCUnitsIndex"]]
        self.header["lADCUnits"]=[indexedUnits[x] for x in self.header["lADCUnitsIndex"]]
        
        if type(self.header["lADCChannelNameIndex"]) == int:
            self.header["lADCChannelNameIndex"] = [self.header["lADCChannelNameIndex"]]
        self.header["lADCChannelNames"]=[indexedUnits[x] for x in self.header["lADCChannelNameIndex"]]
        
        # create lists of units (DAC)
        if type(self.header["lDACChannelUnitsIndex"]) == int:
            self.header["lDACChannelUnitsIndex"] = [self.header["lDACChannelUnitsIndex"]]
        self.header["lDACChannelUnits"]=[indexedUnits[x] for x in self.header["lDACChannelUnitsIndex"]]
        
        if type(self.header["lDACChannelNameIndex"]) == int:
            self.header["lDACChannelNameIndex"] = [self.header["lDACChannelNameIndex"]]
        self.header["lDACChannelNames"]=[indexedUnits[x] for x in self.header["lDACChannelNameIndex"]]

        # clean up extra string units we dont need
        keysToDelete=["strings"]
        for key in self.header.keys():
            if key.startswith("indexedUnit") or key.startswith("string_"):
                keysToDelete.append(key)
        for key in keysToDelete:
            del self.header[key]         
        
        # touch-up comments
        if 'sComment' in self.header.keys():
            self.header['sComment']=[x.decode().strip() for x in self.header['sComment']]

        # make values that are a list with just 1 element just the element (no list required)      
        for key in [key for key in self.header.keys() if len(self.header[key])==1]:
            self.header[key]=self.header[key][0]
            
        # add a few extra things I think are useful.
        self.header["### Extras ###"]=None
        self.header['abfFilename']=os.path.abspath(self._fb.name)
        self.header['abfID']=os.path.basename(self._fb.name)[:-4]
        dt=datetime.datetime.strptime(str(self.header['uFileStartDate']), "%Y%M%d")
        self.header['abfDatetime']=dt+datetime.timedelta(seconds=self.header['uFileStartTimeMS']/1000)
        self.header['dataByteStart']=self.header['DataSection'][0]*512
        self.header['dataPointCount']=self.header['DataSection'][2]
        self.header['dataChannels']=self.header['ADCSection'][2]
        self.header['timeSecPerPoint']=self.header['fADCSequenceInterval']/1e6
        self.header['timePointPerSec']=1e6/self.header['fADCSequenceInterval']
        self.header['rate']=1e6/self.header['fADCSequenceInterval']
        self.header['sweepCount']=self.header['lActualEpisodes']
        self.header['sweepPointCount']=int(self.header['lNumSamplesPerEpisode']/self.header['dataChannels'])
        if self.header['sweepCount'] == 0: # gap free mode
            self.header['sweepPointCount']=int(self.header['dataPointCount']/self.header['dataChannels'])
        self.header['sweepLengthSec']=self.header['sweepPointCount']*self.header['timeSecPerPoint']
        self.header['gain']=self.header['fTelegraphAdditGain']
        self.header['mode']="IC" if self.header['nTelegraphMode'] else "VC"
        self.header['units']="mV" if self.header['mode']=="IC" else "pA"
        self.header['unitsCommand']="pA" if self.header['mode']=="IC" else "mV"
        self.header['commandHoldingByDAC']=self.header['fDACHoldingLevel']
        self.header['protocolPath']=self._readHeaderProtocol()
        self.header['protocol']=os.path.basename(self.header['protocolPath'])

        # improve units
        if type(self.header["lADCUnits"]) == str: 
            self.header['units'] = self.header["lADCUnits"]
        else:
            self.header['units'] = self.header["lADCUnits"][0]

        if type(self.header["lDACChannelUnits"]) == str: 
            self.header['unitsCommand'] = self.header["lDACChannelUnits"]
        else:
            self.header['unitsCommand'] = self.header["lDACChannelUnits"][0]
        
        
        self._calculateScaleFactor()
        
    def _readHeaderProtocol(self):
        """read the the protocol filename out of the ABF header"""
        self._fb.seek(0)
        raw=self._fb.read(self.header['dataByteStart'])
        match=b".pro"
        matchI=raw.find(match)
        if matchI:
            chunk=raw[matchI-256:matchI+len(match)]
            proto=chunk.split(b"\x00")[-1]
            return proto.decode()
        else:
            return None
        
    def _calculateScaleFactor(self):
        """
        Populates header['dataScale'] with a data scale multiplier. Note this only reports for channel 0, 
        and multi-channel recordings may need to calculate this for each channel individually.
        """
        dataScale = 1
        dataScale /= self._first(self.header['fInstrumentScaleFactor'])
        dataScale /= self._first(self.header['fSignalGain'])
        dataScale /= self._first(self.header['fADCProgrammableGain'])
        if self.header['nTelegraphEnable'] :
        	dataScale /= self._first(self.header['fTelegraphAdditGain'])
        dataScale *= self._first(self.header['fADCRange'])
        dataScale /= self._first(self.header['lADCResolution'])
        dataScale += self._first(self.header['fInstrumentOffset'])
        dataScale -= self._first(self.header['fSignalOffset'])
        self.header['dataScale']=dataScale
        
    def _first(self,thing):
        """If a thing is just a thing, return it. If a thing is a list, return the first thing."""
        if type(thing) in [int, float]:
            return thing
        if type(thing) is list:
            return thing[0]
        if len(thing):
            return thing[0]
        return thing
            
    ### FILE READING
        
    def _fileReadStructMap(self,structMap,startByte=0,fixedOffset=None,sectionName=None):
        """Given a string of varName_varFormat structs, get the objects from the file."""
        if sectionName:
            self.header["### %s ###"%sectionName]=[None]
            self._byteMap["### %s (fixed byte positions) ###"%sectionName]=[None]
        self._fb.seek(startByte)
        for structCode in structMap.replace("\n","").split(","):
            varName,varFormat=structCode.strip().split("_")
            if sectionName:
                self._byteMap.setdefault(varName,[]).append("%d"%(self._fb.tell()))
            else:
                self._byteMap.setdefault(varName,[]).append("+%d"%(self._fb.tell()-startByte))
            varVal=struct.unpack(varFormat,self._fb.read(struct.calcsize(varFormat)))
            varVal=varVal if len(varVal)>1 else varVal[0]
            self.header.setdefault(varName,[]).append(varVal)            
            if fixedOffset: 
                self._fb.read(fixedOffset-struct.calcsize(varFormat))

    def _fileReadSection(self,sectionName,structMap):
        """Read a structure map repeatedly according to its name in the section map."""
        self.header["### %s ###"%sectionName]=[None]
        self._byteMap["### %s (section byte offsets) ###"%sectionName]=[None]
        entryStartBlock,entryBytes,entryCount=self.header[sectionName][0]
        for entryNumber in range(entryCount):
            self._fileReadStructMap(structMap,entryStartBlock*512+entryNumber*entryBytes)
    
    def _fileReadData(self):
        """
        Read the full file data into memory. Scale it too. Uses numpy if available.
        If the signal is multiple channels (dataChannels) it's your responsability to reshape the ouptut.
        """
        self._fb.seek(self.header['dataByteStart'])
        pointCount = self.header['dataPointCount']
        scaleFactor = self.header['dataScale']
        if True:
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


### Data structures for ABF2 files:
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

### Data structures for ABF1 files:
HEADERV1 = [('fFileSignature',0,'4s'),('fFileVersionNumber',4,'f'),('nOperationMode',8,'h'),
('lActualAcqLength',10,'i'),('nNumPointsIgnored',14,'h'),('lActualEpisodes',16,'i'),('lFileStartTime',24,'i'),
('lDataSectionPtr',40,'i'),('lTagSectionPtr',44,'i'),('lNumTagEntries',48,'i'),('lSynchArrayPtr',92,'i'),
('lSynchArraySize',96,'i'),('nDataFormat',100,'h'),('nADCNumChannels',120,'h'),('fADCSampleInterval',122,'f'),
('fSynchTimeUnit',130,'f'),('lNumSamplesPerEpisode',138,'i'),('lPreTriggerSamples',142,'i'),
('lEpisodesPerRun',146,'i'),('fADCRange',244,'f'),('lADCResolution',252,'i'),('nFileStartMillisecs',366,'h'),
('nADCPtoLChannelMap',378,'16h'),('nADCSamplingSeq',410,'16h'),('sADCChannelName',442,'10s'*16),
('sADCUnits',602,'8s'*16),('fADCProgrammableGain',730,'16f'),('fInstrumentScaleFactor',922,'16f'),
('fInstrumentOffset',986,'16f'),('fSignalGain',1050,'16f'),('fSignalOffset',1114,'16f'),
('nDigitalEnable',1436,'h'),('nActiveDACChannel',1440,'h'),('nDigitalHolding',1584,'h'),
('nDigitalInterEpisode',1586,'h'),('nDigitalValue',2588,'10h'),('lDACFilePtr',2048,'2i'),
('lDACFileNumEpisodes',2056,'2i'),('fDACCalibrationFactor',2074,'4f'),('fDACCalibrationOffset',2090,'4f'),
('nWaveformEnable',2296,'2h'),('nWaveformSource',2300,'2h'),('nInterEpisodeLevel',2304,'2h'),
('nEpochType',2308,'20h'),('fEpochInitLevel',2348,'20f'),('fEpochLevelInc',2428,'20f'),
('lEpochInitDuration',2508,'20i'),('lEpochDurationInc',2588,'20i'),('nTelegraphEnable',4512,'16h'),
('fTelegraphAdditGain',4576,'16f'),('sProtocolPath',4898,'384s')]

def _compareHeaders(abfFile1,abfFile2):
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

def _graphSomeData(abfFileName):
    """Graph data from a file. Exclusively used for testing."""
    import matplotlib.pyplot as plt
    abf=ABFheader(abfFileName)
    plt.figure(figsize=(10,2))
    for i in range(abf.header['dataChannels']):
        Ys=abf.data[i::abf.header['dataChannels']]
        Ys=Ys[20000*13:20000*19]
        Xs=np.arange(len(Ys))*abf.header['timeSecPerPoint']
        plt.plot(Xs,Ys,label="channel %d"%(i+1))
    plt.legend(fontsize=8)
    plt.margins(0,.1)
    plt.tight_layout()
    plt.show()
    

if __name__=="__main__":
    warnings.warn("This file is meant to be imported, not run directly.")    
    #_graphSomeData("../../data/14o08011_ic_pair.abf")
    #_compareHeaders("../../data/14o16001_vc_pair_step.abf","../../data/17o05024_vc_steps.abf")
    
    # test an ABF submitted by Kim
    #abf=ABFheader(R"../../data/16d22006_kim_gapfree.abf") # time course experiment
    #abf.saveHTML("test.html")    