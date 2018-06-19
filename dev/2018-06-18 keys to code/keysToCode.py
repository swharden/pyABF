
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

import os

def keysFlat(keys,title):
    text="\n### %s ###\n"%title
    for key in keys.split(","):
        name,structFormat=key.strip().split("_")
        text+=('self.%s = readStruct(fb, "%s")\n'%(name,structFormat))
    print(text)
    return text

def keysFlat2(keys,title):
    text="\n### %s ###\n"%title
    for item in keys:
        name,byteLocation,structFormat = item
        text+=('self.%s = readStruct(fb, "%s", %d)\n'%(name,structFormat,byteLocation))
    print(text)
    return text

def keysMap(keys,title):
    text="\n### %s ###\n"%title
    for keyNumber,key in enumerate(keys.split(",")):
        name,structFormat=key.strip().split("_")
        byteLocation=76+keyNumber*16
        text+=('self.%s = readStruct(fb, "%s", %d)\n'%(name,structFormat,byteLocation))
    print(text)
    return text

def keysMult(keys,title):
    text="\n### %s ###\n"%title
    for keyNumber,key in enumerate(keys.split(",")):
        name,structFormat=key.strip().split("_")
        text+=('self.%s = [None]*entryCount\n'%(name))
    for keyNumber,key in enumerate(keys.split(",")):
        name,structFormat=key.strip().split("_")
        text+=('self.%s[i] = readStruct(fb, "%s")\n'%(name,structFormat))
    print(text)
    return text
    

if __name__=="__main__":
    out=""

    # start with flat things
    out+=keysFlat(HEADER,"ABF2Header")
    out+=keysFlat2(HEADERV1,"ABF1Header")

    # then read the map
    out+=keysMap(SECTIONS,"SectionMap")

    # then read mapped flat things
    out+=keysFlat(PROTO,"ProtocolSection")

    # then read mapped multidimensional things
    out+=keysMult(ADC,"ADCSection")
    out+=keysMult(DAC,"DACSection")
    out+=keysMult(EPPERDAC,"EpochPerDACSection")
    out+=keysMult(EPSEC,"EpochSection")
    out+=keysMult(TAGS,"TagSection")


    ### MULTI DIMENSIONAL THINGS ###
    #ADCSection = [2, 128, 4]
    #DACSection = [3, 256, 4]
    #EpochPerDACSection = [5, 48, 3]
    #EpochSection = [6, 32, 3]
    #TagSection = [0, 0, 0]
    #StringsSection = [9, 240, 19]
    #SynchArraySection = [12593, 8, 13]

    ### FLAT THINGS ###
    #ProtocolSection = [1, 512, 1]

    ### DATA ###
    #DataSection = [12, 2, 3220568]

    fOut = os.path.dirname(__file__)+"/keysToCode.txt"
    with open(fOut,'w') as f:
        f.write(out)
        print("wrote",fOut)

    print("DONE")