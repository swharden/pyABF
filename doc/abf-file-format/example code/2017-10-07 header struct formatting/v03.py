"""Minimal-case demonstration how to read an ABF2 header and data. https://github.com/swharden/pyABF/"""

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
        self.header={}
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

    def headerMarkdown(self,saveAs=False):
        """Python ninjery to dump all header information into markdown-formatted text."""
        out="# %s Header\n\n"%(os.path.basename(self.abfFileName))
        flat={}
        for sectionName in [x for x in sorted(dir(self)) if x.startswith('sec')]:
            thing=getattr(self,sectionName)
            if type(thing) is list:
                out+="\n## %s (%d entries)\n"%(sectionName.replace("sec","Section: "),len(thing))
                originalList,thing=thing,{}
                for i,d in enumerate(originalList):
                    for key in sorted(d.keys()):
                        if not key in thing:
                            thing[key]=[]
                        thing[key]=thing[key]+[d[key]]
            else:
                out+="\n## %s\n"%(sectionName.replace("sec","Section: "))
            for key in sorted(thing.keys()):
                flat[key]=thing[key]
                out+="* %s: `%s`\n"%(key,thing[key])
        if saveAs:
            with open(saveAs,'w') as f:
                f.write(out)
            with open(saveAs+"_flat.md",'w') as f:
                out="# %s Header (flattened)\n\n"%(os.path.basename(self.abfFileName))
                for key in sorted(flat.keys()):
                    out+="* %s: `%s`\n"%(key,flat[key])
                f.write(out)                
        return out

if __name__=="__main__":
    abf=ABFheader(R"../../../../data/17o05028_ic_steps.abf")
    abf.headerMarkdown("sampleOutput.md")