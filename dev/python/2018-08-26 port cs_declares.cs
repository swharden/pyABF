
//HeaderV1
public string fFileSignature;
public float fFileVersionNumber;
public short nOperationMode;
public int lActualAcqLength;
public short nNumPointsIgnored;
public int lActualEpisodes;
public int lFileStartTime;
public int lDataSectionPtr;
public int lTagSectionPtr;
public int lNumTagEntries;
public int lSynchArrayPtr;
public int lSynchArraySize;
public short nDataFormat;
public short nADCNumChannels;
public float fADCSampleInterval;
public float fSynchTimeUnit;
public int lNumSamplesPerEpisode;
public int lPreTriggerSamples;
public int lEpisodesPerRun;
public float fADCRange;
public int lADCResolution;
public short nFileStartMillisecs;
public short[] nADCPtoLChannelMap;
public short[] nADCSamplingSeq;
public string sADCChannelName;
public string sADCUnits;
public float[] fADCProgrammableGain;
public float[] fInstrumentScaleFactor;
public float[] fInstrumentOffset;
public float[] fSignalGain;
public float[] fSignalOffset;
public short nDigitalEnable;
public short nActiveDACChannel;
public short nDigitalHolding;
public short nDigitalInterEpisode;
public short[] nDigitalValue;
public int[] lDACFilePtr;
public int[] lDACFileNumEpisodes;
public float[] fDACCalibrationFactor;
public float[] fDACCalibrationOffset;
public short[] nWaveformEnable;
public short[] nWaveformSource;
public short[] nInterEpisodeLevel;
public short[] nEpochType;
public float[] fEpochInitLevel;
public float[] fEpochLevelInc;
public int[] lEpochInitDuration;
public int[] lEpochDurationInc;
public short[] nTelegraphEnable;
public float[] fTelegraphAdditGain;
public string sProtocolPath;

//HeaderV2
public string fFileSignature;
public char[] fFileVersionNumber;
public uint uFileInfoSize;
public uint lActualEpisodes;
public uint uFileStartDate;
public uint uFileStartTimeMS;
public uint uStopwatchTime;
public ushort nFileType;
public ushort nDataFormat;
public ushort nSimultaneousScan;
public ushort nCRCEnable;
public uint uFileCRC;
public uchar[] uFileGUID;
public uchar[] uCreatorVersion;
public uint uCreatorNameIndex;
public uint uModifierVersion;
public uint uModifierNameIndex;
public uint uProtocolPathIndex;

//SectionMap
public uint ProtocolSection_byteStart;
public uint ADCSection_byteStart;
public uint DACSection_byteStart;
public uint EpochSection_byteStart;
public uint ADCPerDACSection_byteStart;
public uint EpochPerDACSection_byteStart;
public uint UserListSection_byteStart;
public uint StatsRegionSection_byteStart;
public uint MathSection_byteStart;
public uint StringsSection_byteStart;
public uint DataSection_byteStart;
public uint TagSection_byteStart;
public uint ScopeSection_byteStart;
public uint DeltaSection_byteStart;
public uint VoiceTagSection_byteStart;
public uint SynchArraySection_byteStart;
public uint AnnotationSection_byteStart;
public uint StatsSection_byteStart;

//ProtocolSection
public short nOperationMode;
public float fADCSequenceInterval;
public char bEnableFileCompression;
public char[] sUnused;
public uint uFileCompressionRatio;
public float fSynchTimeUnit;
public float fSecondsPerRun;
public int lNumSamplesPerEpisode;
public int lPreTriggerSamples;
public int lEpisodesPerRun;
public int lRunsPerTrial;
public int lNumberOfTrials;
public short nAveragingMode;
public short nUndoRunCount;
public short nFirstEpisodeInRun;
public float fTriggerThreshold;
public short nTriggerSource;
public short nTriggerAction;
public short nTriggerPolarity;
public float fScopeOutputInterval;
public float fEpisodeStartToStart;
public float fRunStartToStart;
public int lAverageCount;
public float fTrialStartToStart;
public short nAutoTriggerStrategy;
public float fFirstRunDelayS;
public short nChannelStatsStrategy;
public int lSamplesPerTrace;
public int lStartDisplayNum;
public int lFinishDisplayNum;
public short nShowPNRawData;
public float fStatisticsPeriod;
public int lStatisticsMeasurements;
public short nStatisticsSaveStrategy;
public float fADCRange;
public float fDACRange;
public int lADCResolution;
public int lDACResolution;
public short nExperimentType;
public short nManualInfoStrategy;
public short nCommentsEnable;
public int lFileCommentIndex;
public short nAutoAnalyseEnable;
public short nSignalType;
public short nDigitalEnable;
public short nActiveDACChannel;
public short nDigitalHolding;
public short nDigitalInterEpisode;
public short nDigitalDACChannel;
public short nDigitalTrainActiveLogic;
public short nStatsEnable;
public short nStatisticsClearStrategy;
public short nLevelHysteresis;
public int lTimeHysteresis;
public short nAllowExternalTags;
public short nAverageAlgorithm;
public float fAverageWeighting;
public short nUndoPromptStrategy;
public short nTrialTriggerSource;
public short nStatisticsDisplayStrategy;
public short nExternalTagType;
public short nScopeTriggerOut;
public short nLTPType;
public short nAlternateDACOutputState;
public short nAlternateDigitalOutputState;
public float[] fCellID;
public short nDigitizerADCs;
public short nDigitizerDACs;
public short nDigitizerTotalDigitalOuts;
public short nDigitizerSynchDigitalOuts;
public short nDigitizerType;

//ADCSection

//DACSection

//EpochPerDACSection

//EpochSection

//TagSection

//StringsSection

//StringsIndexed
