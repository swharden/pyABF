"""
ABF2 Header Reader - A pure-python ABF file reader which uses no external libraries by Scott Harden.

PURPOSE:
    This class is not feature rich, but it aims to demonstrate how to read ABF header and data without
    any external libraries. This should be very easy to port to other languages. A more advanced
    implementation is realized in the pyABF python package and documented on its project page, but this
    script is kept intentionally minimalistic to make it easy to read and learn from.

ADDITIONAL RESOURCES:
    https://github.com/swharden/pyABF/
    https://github.com/swharden/SWHLab/

"""

import os
import struct
import datetime

KEYS_SECTIONS=['ProtocolSection_IIl','ADCSection_IIl','DACSection_IIl',
    'EpochSection_IIl','ADCPerDACSection_IIl','EpochPerDACSection_IIl','UserListSection_IIl',
    'StatsRegionSection_IIl','MathSection_IIl','StringsSection_IIl','DataSection_IIl',
    'TagSection_IIl','ScopeSection_IIl','DeltaSection_IIl','VoiceTagSection_IIl',
    'SynchArraySection_IIl','AnnotationSection_IIl','StatsSection_IIl']
KEYS_HEADER=['fFileSignature_4s','fFileVersionNumber_4b','uFileInfoSize_I','lActualEpisodes_I',
    'uFileStartDate_I','uFileStartTimeMS_I','uStopwatchTime_I','nFileType_H','nDataFormat_H',
    'nSimultaneousScan_H','nCRCEnable_H','uFileCRC_I','FileGUID_I','unknown1_I','unknown2_I',
    'unknown3_I','uCreatorVersion_I','uCreatorNameIndex_I','uModifierVersion_I',
    'uModifierNameIndex_I','uProtocolPathIndex_I']
KEYS_PROTOCOL=['nOperationMode_h','fADCSequenceInterval_f','bEnableFileCompression_b','sUnused_3s',
    'uFileCompressionRatio_I','fSynchTimeUnit_f','fSecondsPerRun_f','lNumSamplesPerEpisode_i',
    'lPreTriggerSamples_i','lEpisodesPerRun_i','lRunsPerTrial_i','lNumberOfTrials_i','nAveragingMode_h',
    'nUndoRunCount_h','nFirstEpisodeInRun_h','fTriggerThreshold_f','nTriggerSource_h','nTriggerAction_h',
    'nTriggerPolarity_h','fScopeOutputInterval_f','fEpisodeStartToStart_f','fRunStartToStart_f',
    'lAverageCount_i','fTrialStartToStart_f','nAutoTriggerStrategy_h','fFirstRunDelayS_f',
    'nChannelStatsStrategy_h','lSamplesPerTrace_i','lStartDisplayNum_i','lFinishDisplayNum_i',
    'nShowPNRawData_h','fStatisticsPeriod_f','lStatisticsMeasurements_i','nStatisticsSaveStrategy_h',
    'fADCRange_f','fDACRange_f','lADCResolution_i','lDACResolution_i','nExperimentType_h',
    'nManualInfoStrategy_h','nCommentsEnable_h','lFileCommentIndex_i','nAutoAnalyseEnable_h',
    'nSignalType_h','nDigitalEnable_h','nActiveDACChannel_h','nDigitalHolding_h','nDigitalInterEpisode_h',
    'nDigitalDACChannel_h','nDigitalTrainActiveLogic_h','nStatsEnable_h','nStatisticsClearStrategy_h',
    'nLevelHysteresis_h','lTimeHysteresis_i','nAllowExternalTags_h','nAverageAlgorithm_h',
    'fAverageWeighting_f','nUndoPromptStrategy_h','nTrialTriggerSource_h','nStatisticsDisplayStrategy_h',
    'nExternalTagType_h','nScopeTriggerOut_h','nLTPType_h','nAlternateDACOutputState_h',
    'nAlternateDigitalOutputState_h','fCellID_3f','nDigitizerADCs_h','nDigitizerDACs_h',
    'nDigitizerTotalDigitalOuts_h','nDigitizerSynchDigitalOuts_h','nDigitizerType_h']
KEYS_TAGS=['lTagTime_i','sComment_56s','nTagType_h','nVoiceTagNumberorAnnotationIndex_h']
KEYS_EPDESC=['nEpochNum_h','nEpochDigitalOutput_h']
KEYS_EPINFO=['nEpochNum_h','nDACNum_h','nEpochType_h','fEpochInitLevel_f','fEpochLevelInc_f',
    'lEpochInitDuration_i','lEpochDurationInc_i','lEpochPulsePeriod_i','lEpochPulseWidth_i']
KEYS_ADCINFO=['nADCNum_h','nTelegraphEnable_h','nTelegraphInstrument_h','fTelegraphAdditGain_f',
    'fTelegraphFilter_f','fTelegraphMembraneCap_f','nTelegraphMode_h','fTelegraphAccessResistance_f',
    'nADCPtoLChannelMap_h','nADCSamplingSeq_h','fADCProgrammableGain_f','fADCDisplayAmplification_f',
    'fADCDisplayOffset_f','fInstrumentScaleFactor_f','fInstrumentOffset_f','fSignalGain_f',
    'fSignalOffset_f','fSignalLowpassFilter_f','fSignalHighpassFilter_f','nLowpassFilterType_b',
    'nHighpassFilterType_b','fPostProcessLowpassFilter_f','nPostProcessLowpassFilterType_c',
    'bEnabledDuringPN_b','nStatsChannelPolarity_h','lADCChannelNameIndex_i','lADCUnitsIndex_i']
KEYS_DACINFO=['nDACNum_h','nTelegraphDACScaleFactorEnable_h','fInstrumentHoldingLevel_f',
     'fDACScaleFactor_f','fDACHoldingLevel_f','fDACCalibrationFactor_f','fDACCalibrationOffset_f',
     'lDACChannelNameIndex_i','lDACChannelUnitsIndex_i','lDACFilePtr_i','lDACFileNumEpisodes_i',
     'nWaveformEnable_h','nWaveformSource_h','nInterEpisodeLevel_h','fDACFileScale_f','fDACFileOffset_f',
     'lDACFileEpisodeNum_i','nDACFileADCNum_h','nConditEnable_h','lConditNumPulses_i','fBaselineDuration_f',
     'fBaselineLevel_f','fStepDuration_f','fStepLevel_f','fPostTrainPeriod_f','fPostTrainLevel_f',
     'nMembTestEnable_h','nLeakSubtractType_h','nPNPolarity_h','fPNHoldingLevel_f','nPNNumADCChannels_h',
     'nPNPosition_h','nPNNumPulses_h','fPNSettlingTime_f','fPNInterpulse_f','nLTPUsageOfDAC_h',
     'nLTPPresynapticPulses_h','lDACFilePathIndex_i','fMembTestPreSettlingTimeMS_f',
     'fMembTestPostSettlingTimeMS_f','nLeakSubtractADCIndex_h']

class ABFheader:
    def __init__(self,abfFileName):
        """Given an ABF file, learn everything we can about its contents."""
        self.abfFileName=abfFileName

        # when initialized, update all the header information
        self.fb = open(abfFileName,'rb') # open the file for direct reading (binary mode)
        self.updateHeader() # Read the ABF header and confirm it is an ABF2 file
        self.updateSectionMap() # Create section map noting byte locations of all sections
        self.updateStringsSection() # Pull strings from StringsSection
        self.updateProtocolSection() # Pull ABF acquisition information from ProtocolSection
        self.updateTagSection() # Pull comment tags from TagSection
        self.updateEpochSections() # Pull epoch data from EpochSection and EpochPerDACSection
        self.udateADCandDACInfo() # Add to the epoch chart using ADCSection and DACSection
        self.updateInfo() # Create a simple dictionary with just the important stuff
        self.updateEpochs() # Create a simple dictionary with epoch information
        self.fb.close() # be courteous and close the file as quickly as possible

    ### FILE ACCESS

    def fileRead(self,bytePosition,nBytes):
        """Return bytestring from a specific position in the open file."""
        self.fb.seek(bytePosition)
        return self.fb.read(nBytes)

    def fileReadStruct(self,bytePosition,structFormat,allowByteString=False):
        """Given a file position and a struct code, return the object(s)."""
        self.fb.seek(bytePosition)
        val = struct.unpack(structFormat, self.fb.read(struct.calcsize(structFormat)))
        val = val[0] if len(val)==1 else list(val)
        if structFormat.endswith("s") and allowByteString==False:
            val=self.forceUnicode(val)
        return val

    def fileReadSectionKeys(self,bytePosition,sectionKeys,fixedOffsetBytes=False,allowByteString=False):
        """Given a list of "name_struct"-formatted keys, create and return the list of objects."""
        self.fb.seek(bytePosition)
        items={}
        for key in sectionKeys:
            varName,structFormat=key.split("_")
            items[varName]=self.fileReadStruct(bytePosition,structFormat,allowByteString)
            if fixedOffsetBytes:
                bytePosition+=fixedOffsetBytes
            else:
                bytePosition+=struct.calcsize(structFormat)
        return items

    def fileReadMappedSection(self,sectionName,sectionKeys):
        """Given the name of a mapped section (in self.sectionMap) return a list of all its elements."""
        entries=[]
        if not sectionName in self.sectionMap.keys():
            print("ERROR:",sectionName,"is not in the section map!")
            return
        else:
            entryFirstPosition=self.sectionMap[sectionName]['byteStart']
            entrySize=self.sectionMap[sectionName]['entrySize']
            entryCount=self.sectionMap[sectionName]['entryCount']
            for entryNumber in range(entryCount):
                bytePosition=entryFirstPosition+entrySize*entryNumber
                entries.append(self.fileReadSectionKeys(bytePosition,sectionKeys))
        return entries

    ### HEADER DATA EXTRACTION

    def updateHeader(self):
        """Read the header starting at the beginning of the file."""
        self.header = self.fileReadSectionKeys(0,KEYS_HEADER)

    def updateSectionMap(self):
        """Read create a map of all byte locations related to the various sections in the ABF file."""
        self.sectionMap={}
        BLOCKSIZE=512
        #TODO: modify struct to be 'iilb' or something
        sections=self.fileReadSectionKeys(76,KEYS_SECTIONS,fixedOffsetBytes=16)
        for sectionName in sections.keys():
            blockIndex, entrySize, entryCount = sections[sectionName]
            self.sectionMap[sectionName]={}
            self.sectionMap[sectionName]['byteStart']=blockIndex*BLOCKSIZE
            self.sectionMap[sectionName]['entrySize']=entrySize
            self.sectionMap[sectionName]['entryCount']=entryCount
            self.sectionMap[sectionName]['byteLast']=blockIndex*BLOCKSIZE+entrySize*entryCount
            self.sectionMap[sectionName]['sizeBytes']=entrySize*entryCount

    def updateStringsSection(self):
        """Read the strings as a 1d list."""
        self.strings=[]
        self.stringsAll=[] # will contain all strings (some gibberish)
        stringPos0=self.sectionMap['StringsSection']['byteStart']
        stringCount=self.sectionMap['StringsSection']['entryCount']
        stringLength=self.sectionMap['StringsSection']['entrySize']
        STRINGS_KEYS=["string%03d_%ds"%(x,stringLength) for x in range(stringCount)]
        byteStrings=self.fileReadSectionKeys(stringPos0,STRINGS_KEYS,allowByteString=True).values()
        for stringText in byteStrings:
            self.stringsAll.append(self.forceUnicode(stringText))
            for key in [b'AXENGN',b'clampex',b'Clampex',b'CLAMPEX',b'axoscope']:
                if key in stringText:
                    parsableText = stringText.split(key)[1].split(b'\x00')
                    for line in [x for x in parsableText if len(x.strip())]:
                        self.strings.append(self.forceUnicode(line))

    def updateProtocolSection(self):
        """Read the protocol information dictionary."""
        self.protocol = self.fileReadMappedSection('ProtocolSection',KEYS_PROTOCOL)

    def updateTagSection(self):
        """Read the tags as a 1d list of dictionaries."""
        self.tags = self.fileReadMappedSection('TagSection',KEYS_TAGS)

    def updateEpochSections(self):
        """Read information about epochs (modified in the waveform editor tab)."""
        self.epochPerDac = self.fileReadMappedSection('EpochPerDACSection',KEYS_EPINFO)
        self.epochSection = self.fileReadMappedSection('EpochSection',KEYS_EPDESC) # added by Scott
        for epochNumber, digOutCode in enumerate([list(x.values())[1] for x in self.epochSection]):
            self.epochPerDac[epochNumber]['sDigitalOutput']=format(digOutCode, 'b').rjust(8,'0')

    def udateADCandDACInfo(self):
        """blah."""
        self.dac = self.fileReadMappedSection('DACSection',KEYS_DACINFO)
        self.adc = self.fileReadMappedSection('ADCSection',KEYS_ADCINFO)

    ### CUSTOM HEADER SUPPLEMENTATION

    def updateInfo(self):
        """Update self.info (dictionary) with additional useful information the author likes to have."""
        self.info={}
        self.info['abfFilename']=self.abfFileName
        self.info['abfID']=os.path.basename(self.abfFileName)[::-1].split(".")[1][::-1]
        version=[str(x) for x in self.header['fFileVersionNumber'][::-1]]
        self.info['abfVersion']=float("".join(version))/1000
        self.info['abfSignature']=self.header['fFileSignature']
        self.info['samplesRate']=int(1e6/self.protocol[0]['fADCSequenceInterval'])
        dataPoints=self.sectionMap['DataSection']['sizeBytes']/self.sectionMap['DataSection']['entrySize']
        self.info['experimentLengthSec']=dataPoints/self.info['samplesRate']
        self.info['sweepCount']=self.header['lActualEpisodes']
        self.info['sweepLengthSec']=self.info['experimentLengthSec']/self.info['sweepCount']
        dt=datetime.datetime.strptime(str(self.header['uFileStartDate']), "%Y%M%d")
        self.info['abfDatetime']=dt+datetime.timedelta(seconds=self.header['uFileStartTimeMS']/1000)
        self.info['abfProtocol']=self.strings[0]
        nSigs=len(self.adc)
        self.info['signalCount']=nSigs
        self.info['signalLabels']=self.strings[3::2][:nSigs]
        self.info['signalUnits']=self.strings[2::2][:nSigs]
        if self.info['signalUnits'][0]=='pA':
            #TODO: is there a better way to determine VC/IC than using the strings to get this?
            self.info['unitsSignal'],self.info['unitsCommand']='pA','mV'
        else:
            self.info['unitsSignal'],self.info['unitsCommand']='mV','pA'
        self.info['signalHolds']=[self.dac[x]['fDACHoldingLevel'] for x in range(nSigs)][:nSigs]

    def updateEpochs(self):
        """Create a custom epochs dictionary (self.epochs) with more logically-organized values."""
        self.epochs={}
        nEpochs=len(self.epochPerDac)
        for epochIndex,epoch in enumerate(self.epochPerDac):
            for key in sorted(epoch.keys()):
                if not key in self.epochs.keys():
                    self.epochs[key]=[None]*nEpochs
                self.epochs[key][epochIndex]=epoch[key]

        # let's improve these names
        self.epochs["command"] = self.epochs.pop("fEpochInitLevel")
        self.epochs["commandDelta"] = self.epochs.pop("fEpochLevelInc")
        self.epochs["durationMS"] = self.epochs.pop("lEpochInitDuration")
        self.epochs["durationDelta"] = self.epochs.pop("lEpochDurationInc")
        self.epochs["pulsePeriod"] = self.epochs.pop("lEpochPulsePeriod")
        self.epochs["pulseWidth"] = self.epochs.pop("lEpochPulseWidth")
        self.epochs["digitalOut"] = self.epochs.pop("sDigitalOutput")
        self.epochs["epochNumber"] = self.epochs.pop("nEpochNum")
        self.epochs["epochName"] = [chr(65+x) for x in range(nEpochs)]
        self.epochs["epochType"] = self.epochs.pop("nEpochType")
        self.epochs["epochDAC"] = self.epochs.pop("nDACNum")
        self.epochs["epochCount"]=nEpochs

        # TODO: look up more epoch types
        epochTypes=[str(x) for x in range(10)]
        epochTypes[1]="step"
        epochTypes[2]="ramp"
        self.epochs["epochType"] = [epochTypes[x] for x in self.epochs["epochType"]]

    ### MISC TOOLS

    def forceUnicode(self,bytestring,replaceWith="?"):
        """given a bytestring, return just the ASCII components."""
        chars=list(bytestring)
        if not len(chars): return ""
        if type(chars[0]) is str: return str(bytestring)
        for position,letter in enumerate(chars):
            charVal=int(chars[position])
            if charVal>=32 and charVal<128: chars[position]=chr(charVal)
            else: chars[position]=replaceWith
        return "".join(chars).strip()

    def showInfo(self):
        """Display information about the ABF we loaded."""
        print("\n\n"+"#"*3,os.path.basename(self.abfFileName),"#"*3)
        print("INFO:")
        for key in sorted(self.info): print("  %s = %s"%(key,self.info[key]))
        print("EPOCHS:")
        for key in sorted(self.epochs): print("  %s = %s"%(key,self.epochs[key]))

    ### SIGNAL DATA ACCESS

    def getSweep(self,sweepNumber=0):
        """Returns data values for a given channel and sweep. Numpy memmap should be considered for this."""
        sweepNumber=max(0,min((sweepNumber,self.header['lActualEpisodes']-1))) # make sure it's a real sweep
        dataPos0=self.sectionMap['DataSection']['byteStart']
        sweepPointCount=self.protocol[0]['lNumSamplesPerEpisode']
        sweepByteCount=sweepPointCount*2 # assuming 16-bit (2-byte) data points
        sweepByteStart=int(dataPos0+sweepNumber*sweepByteCount)
        dataScale=header.protocol[0]['lADCResolution']/1e6 # multiply this by the data
        with open(self.abfFileName,'rb') as f:
            f.seek(sweepByteStart)
            data=f.read(sweepByteCount)
        f.close()
        sweepData=struct.unpack('%dh'%(sweepByteCount/2),data)
        sweepData=[x*dataScale for x in data]
        return(sweepData)

if __name__=="__main__":
    print("DO NOT RUN THIS SCRIPT DIRECTLY.")
    header=ABFheader(R"C:\path\to\some\file.abf")
    header.showInfo() # display useful header information
    data=header.getSweep(5) # get data from sweep 5
    print("First few data points:",data[:5],'...')