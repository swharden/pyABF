**NOTES ABOUT EXAMPLE CODE:** This folder contains a standalone collection of code created from a snapshot of a work-in-progress project. It is meant for educational purposes only, and better code which does the same things may be found elsewhere
in this project.

# Ultra-Slim ABF2 Header Reader
After getting to know the ABF2 file format better, I wrote a new ABFheader class from scratch. This time it is increadibly light. Notable improvements are:
* **Lighter struct format:** multi-line CSV format (spaces and line breaks are ignroed)
* **Simpler file read functions:** Now there are just two (read map, read section) instad of four (read bytes, read struct, read map, read section).
* **Separate sections do not require separate functions:** I leaned heavy on the string parsing style structure reading and got every section to load easily with a single function.
* **Header information can be viewed as plain text:** It currently outputs markdown-formatted text which is easy to read, but could be very easily converted to HTML.
* **Alternative header structure:** Since every variable name in each section is globally unique, do we really need to have a separate variable for each section? 
  * Consider an ABF with 7 epochs. There is an epochs list which contains 7 dictionaries (all with the same key names, and each key holds a single value). 
  * _traditional method:_ To get a holding current for each epoch, you have to know which variable that key is in and get `epochListVariable[epochNumber]['fEpochInitLevel']` in a loop changing `epochNumber` for every epoch.
  * I did a little Python ninjery to re-arrange a list of dicts to a dict of lists. Now each key appears only once and yields a list. This massively simplifies data access. 
  * _new method:_ To get holding current for all epochs, just get `allSections['fEpochInitLevel']` and it returns the list.
  * This new format (all header information in a single flat dictionary) may make it easier to pass header information between files or programs.

### Sample Output
* [Hybrid structure](sampleOutput.md) (useful for text output)
* [Experimental flat dictionary structure](sampleOutput.md_flat.md)

### Example Code
The source code is in this folder, but it's so short I might as well list it (minus the code to create the markdown-formatted output). **The ABFheader class is 34 lines long!** I will consider putting the structures in their own file since now they are more than half the length of the full program...

```python
import os
import struct
STRUCTS_HEADER="""fFileSignature_4s,fFileVersionNumber_4b,uFileInfoSize_I,lActualEpisodes_I,uFileStartDate_I,
uFileStartTimeMS_I,uStopwatchTime_I,nFileType_H,nDataFormat_H,nSimultaneousScan_H,nCRCEnable_H,uFileCRC_I,
FileGUID_I,unknown1_I,unknown2_I,unknown3_I,uCreatorVersion_I,uCreatorNameIndex_I,uModifierVersion_I,
uModifierNameIndex_I,uProtocolPathIndex_I"""
STRUCTS_SECTIONS="""ProtocolSection_IIl,ADCSection_IIl,DACSection_IIl,EpochSection_IIl,ADCPerDACSection_IIl,
EpochPerDACSection_IIl,UserListSection_IIl,StatsRegionSection_IIl,MathSection_IIl,StringsSection_IIl,
DataSection_IIl,TagSection_IIl,ScopeSection_IIl,DeltaSection_IIl,VoiceTagSection_IIl,SynchArraySection_IIl,
AnnotationSection_IIl,StatsSection_IIl"""
STRUCTS_SEC_PROTO="""nOperationMode_h,fADCSequenceInterval_f,bEnableFileCompression_b,sUnused_3s,
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
STRUCTS_SEC_ADC="""nADCNum_h,nTelegraphEnable_h,nTelegraphInstrument_h,fTelegraphAdditGain_f,
fTelegraphFilter_f,fTelegraphMembraneCap_f,nTelegraphMode_h,fTelegraphAccessResistance_f,nADCPtoLChannelMap_h,
nADCSamplingSeq_h,fADCProgrammableGain_f,fADCDisplayAmplification_f,fADCDisplayOffset_f,
fInstrumentScaleFactor_f,fInstrumentOffset_f,fSignalGain_f,fSignalOffset_f,fSignalLowpassFilter_f,
fSignalHighpassFilter_f,nLowpassFilterType_b,nHighpassFilterType_b,fPostProcessLowpassFilter_f,
nPostProcessLowpassFilterType_c,bEnabledDuringPN_b,nStatsChannelPolarity_h,lADCChannelNameIndex_i,
lADCUnitsIndex_i"""
STRUCTS_SEC_DAC="""nDACNum_h,nTelegraphDACScaleFactorEnable_h,fInstrumentHoldingLevel_f,fDACScaleFactor_f,
fDACHoldingLevel_f,fDACCalibrationFactor_f,fDACCalibrationOffset_f,lDACChannelNameIndex_i,
lDACChannelUnitsIndex_i,lDACFilePtr_i,lDACFileNumEpisodes_i,nWaveformEnable_h,nWaveformSource_h,
nInterEpisodeLevel_h,fDACFileScale_f,fDACFileOffset_f,lDACFileEpisodeNum_i,nDACFileADCNum_h,nConditEnable_h,
lConditNumPulses_i,fBaselineDuration_f,fBaselineLevel_f,fStepDuration_f,fStepLevel_f,fPostTrainPeriod_f,
fPostTrainLevel_f,nMembTestEnable_h,nLeakSubtractType_h,nPNPolarity_h,fPNHoldingLevel_f,nPNNumADCChannels_h,
nPNPosition_h,nPNNumPulses_h,fPNSettlingTime_f,fPNInterpulse_f,nLTPUsageOfDAC_h,nLTPPresynapticPulses_h,
lDACFilePathIndex_i,fMembTestPreSettlingTimeMS_f,fMembTestPostSettlingTimeMS_f,nLeakSubtractADCIndex_h"""
STRUCTS_SEC_EPOCH_PER_DAC="""nEpochNum_h,nDACNum_h,nEpochType_h,fEpochInitLevel_f,fEpochLevelInc_f,
lEpochInitDuration_i,lEpochDurationInc_i,lEpochPulsePeriod_i,lEpochPulseWidth_i"""
STRUCTS_SEC_EPOCH_DIG="""nEpochNum_h,nEpochDigitalOutput_h"""
STRUCTS_SEC_TAGS="""lTagTime_i,sComment_56s,nTagType_h,nVoiceTagNumberorAnnotationIndex_h"""
STRUCTS_UNKNOWN="""unknown_c"""

class ABFheader:
    def __init__(self,abfFileName):
        """Given an ABF2 file, provide simple access to its header and data."""
        self.abfFileName=abfFileName
        self.fb = open(abfFileName,'rb')
        self.secHeader=self.fileReadStructMap(STRUCTS_HEADER)
        self.secMap=self.fileReadStructMap(STRUCTS_SECTIONS,76,16)                  
        self.secProtocol=self.fileReadSection('ProtocolSection',STRUCTS_SEC_PROTO)
        self.secADC=self.fileReadSection('ADCSection',STRUCTS_SEC_ADC)
        self.secDAC=self.fileReadSection('DACSection',STRUCTS_SEC_DAC)
        self.secEpochPerDac=self.fileReadSection('EpochPerDACSection',STRUCTS_SEC_EPOCH_PER_DAC)
        self.secEpochDig=self.fileReadSection('EpochSection',STRUCTS_SEC_EPOCH_DIG)      
        self.secTags=self.fileReadSection('TagSection',STRUCTS_SEC_TAGS)        
        self.fb.close()
        
    def fileReadStructMap(self,structMap,startByte=0,fixedOffset=None):
        """Given a string of varName_varFormat structs, read the ABF file and return the objects."""
        values={}
        self.fb.seek(startByte)
        for structCode in structMap.replace("\n","").split(","):
            varName,varFormat=structCode.strip().split("_")
            varVal=struct.unpack(varFormat,self.fb.read(struct.calcsize(varFormat)))
            values[varName]=varVal if len(varVal)>1 else varVal[0]
            if fixedOffset:
                self.fb.read(fixedOffset-struct.calcsize(varFormat))
        return values

    def fileReadSection(self,sectionName,structMap):
        entries=[]
        entryStartBlock,entryBytes,entryCount=self.secMap[sectionName]
        for entryNumber in range(entryCount):
            entries.append(self.fileReadStructMap(structMap,entryStartBlock*512+entryNumber*entryBytes))
        if len(entries)==1: entries=entries[0]
        return entries
		
if __name__=="__main__":
    abf=ABFheader(R"../../../../data/17o05028_ic_steps.abf")
```