**NOTES ABOUT EXAMPLE CODE:** This folder contains a standalone collection of code created from a snapshot of a work-in-progress project. It is meant for educational purposes only, and better code which does the same things may be found elsewhere
in this project.

## Notable Changes
* The header format is now an [ordered dictionary](https://docs.python.org/2/library/collections.html)
  * This retains the order of all the sections and variables rather than mashing them up into a huge crazy list which can only be organized alphabetically.
  * I add section names as header dictionary entries so we know down the road which variables go to which section. It also greatly helps the display of the header (or its formatting when saved as HTML or markdown)
  * I added an "extras" section to the collection of ABF header variable sections. The extras section contains things I think are useful, given common sense and intuitive variable names.
* I started an `ABF` class which is the only thing the user will interact with
  * end users never interact with the `ABFheader` class.
  * the first line of the `ABF` class is just `self.header=ABFheader(abfFile).header`. This provides excellent separation between work related to the ABFheader (which is a work in progress) and work related to _using_ data from ABFs (graphing, measuring, etc).
  * abf header tools ([abfHeaderTools.py](abfHeaderTools.py)) can be used to display the header or save it as HTML ([demo.html](demo.html)) or markdown ([demo.md](demo.md)). The markdown below was generated with this code.
  * this will contain functions like `getSweepData(sweepNumber)`
  
# ABF Header Contents

## Header
* fFileSignature = `b'ABF2'`
* fFileVersionNumber = `(0, 0, 6, 2)`
* uFileInfoSize = `512`
* lActualEpisodes = `16`
* uFileStartDate = `20171005`
* uFileStartTimeMS = `52966899`
* uStopwatchTime = `8379`
* nFileType = `1`
* nDataFormat = `0`
* nSimultaneousScan = `1`
* nCRCEnable = `0`
* uFileCRC = `0`
* FileGUID = `813622370`
* unknown1 = `1101957764`
* unknown2 = `3041560705`
* unknown3 = `3819584183`
* uCreatorVersion = `168230915`
* uCreatorNameIndex = `1`
* uModifierVersion = `0`
* uModifierNameIndex = `0`
* uProtocolPathIndex = `2`

## Section Map
* ProtocolSection = `(1, 512, 1)`
* ADCSection = `(2, 128, 1)`
* DACSection = `(3, 256, 8)`
* EpochSection = `(8, 32, 5)`
* ADCPerDACSection = `(0, 0, 0)`
* EpochPerDACSection = `(7, 48, 5)`
* UserListSection = `(0, 0, 0)`
* StatsRegionSection = `(9, 128, 1)`
* MathSection = `(0, 0, 0)`
* StringsSection = `(10, 194, 20)`
* DataSection = `(13, 2, 960000)`
* TagSection = `(0, 0, 0)`
* ScopeSection = `(11, 769, 1)`
* DeltaSection = `(0, 0, 0)`
* VoiceTagSection = `(0, 0, 0)`
* SynchArraySection = `(3763, 8, 16)`
* AnnotationSection = `(0, 0, 0)`
* StatsSection = `(0, 0, 0)`

## ProtocolSection
* nOperationMode = `5`
* fADCSequenceInterval = `50.0`
* bEnableFileCompression = `0`
* sUnused = `b'\x00\x00\x00'`
* uFileCompressionRatio = `1`
* fSynchTimeUnit = `12.5`
* fSecondsPerRun = `7200.0`
* lNumSamplesPerEpisode = `60000`
* lPreTriggerSamples = `20`
* lEpisodesPerRun = `21`
* lRunsPerTrial = `1`
* lNumberOfTrials = `1`
* nAveragingMode = `0`
* nUndoRunCount = `0`
* nFirstEpisodeInRun = `0`
* fTriggerThreshold = `0.0`
* nTriggerSource = `-3`
* nTriggerAction = `0`
* nTriggerPolarity = `0`
* fScopeOutputInterval = `0.0`
* fEpisodeStartToStart = `0.0`
* fRunStartToStart = `0.0`
* lAverageCount = `1`
* fTrialStartToStart = `0.0`
* nAutoTriggerStrategy = `1`
* fFirstRunDelayS = `0.0`
* nChannelStatsStrategy = `0`
* lSamplesPerTrace = `40000`
* lStartDisplayNum = `0`
* lFinishDisplayNum = `60000`
* nShowPNRawData = `0`
* fStatisticsPeriod = `1.0`
* lStatisticsMeasurements = `5`
* nStatisticsSaveStrategy = `0`
* fADCRange = `10.0`
* fDACRange = `10.0`
* lADCResolution = `32768`
* lDACResolution = `32768`
* nExperimentType = `2`
* nManualInfoStrategy = `1`
* nCommentsEnable = `0`
* lFileCommentIndex = `0`
* nAutoAnalyseEnable = `1`
* nSignalType = `0`
* nDigitalEnable = `0`
* nActiveDACChannel = `0`
* nDigitalHolding = `0`
* nDigitalInterEpisode = `0`
* nDigitalDACChannel = `0`
* nDigitalTrainActiveLogic = `1`
* nStatsEnable = `1`
* nStatisticsClearStrategy = `1`
* nLevelHysteresis = `64`
* lTimeHysteresis = `1`
* nAllowExternalTags = `0`
* nAverageAlgorithm = `0`
* fAverageWeighting = `0.10000000149011612`
* nUndoPromptStrategy = `0`
* nTrialTriggerSource = `-1`
* nStatisticsDisplayStrategy = `0`
* nExternalTagType = `2`
* nScopeTriggerOut = `0`
* nLTPType = `0`
* nAlternateDACOutputState = `0`
* nAlternateDigitalOutputState = `0`
* fCellID = `(0.0, 0.0, 0.0)`
* nDigitizerADCs = `16`
* nDigitizerDACs = `4`
* nDigitizerTotalDigitalOuts = `16`
* nDigitizerSynchDigitalOuts = `8`
* nDigitizerType = `6`

## ADCSection
* nADCNum = `0`
* nTelegraphEnable = `1`
* nTelegraphInstrument = `24`
* fTelegraphAdditGain = `1.0`
* fTelegraphFilter = `10000.0`
* fTelegraphMembraneCap = `0.0`
* nTelegraphMode = `1`
* fTelegraphAccessResistance = `0.0`
* nADCPtoLChannelMap = `0`
* nADCSamplingSeq = `0`
* fADCProgrammableGain = `1.0`
* fADCDisplayAmplification = `12.307504653930664`
* fADCDisplayOffset = `-21.75`
* fInstrumentScaleFactor = `0.009999999776482582`
* fInstrumentOffset = `0.0`
* fSignalGain = `1.0`
* fSignalOffset = `0.0`
* fSignalLowpassFilter = `5000.0`
* fSignalHighpassFilter = `1.0`
* nLowpassFilterType = `0`
* nHighpassFilterType = `0`
* fPostProcessLowpassFilter = `100000.0`
* nPostProcessLowpassFilterType = `b'\x00'`
* bEnabledDuringPN = `0`
* nStatsChannelPolarity = `1`
* lADCChannelNameIndex = `3`
* lADCUnitsIndex = `4`

## DACSection
* nDACNum = `[0, 1, 2, 3, 4, 5, 6, 7, 0, 0, 0, 0, 0]`
* nTelegraphDACScaleFactorEnable = `[1, 0, 0, 0, 0, 0, 0, 0]`
* fInstrumentHoldingLevel = `[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]`
* fDACScaleFactor = `[400.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0]`
* fDACHoldingLevel = `[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]`
* fDACCalibrationFactor = `[1.0008957386016846, 1.0010067224502563, 1.000895619392395, 1.0008400678634644, 1.0, 1.0, 1.0, 1.0]`
* fDACCalibrationOffset = `[0.0, -2.0, -3.0, 2.0, 0.0, 0.0, 0.0, 0.0]`
* lDACChannelNameIndex = `[5, 7, 9, 11, 13, 15, 17, 19]`
* lDACChannelUnitsIndex = `[6, 8, 10, 12, 14, 16, 18, 20]`
* lDACFilePtr = `[0, 0, 0, 0, 0, 0, 0, 0]`
* lDACFileNumEpisodes = `[0, 0, 0, 0, 0, 0, 0, 0]`
* nWaveformEnable = `[1, 0, 0, 0, 0, 0, 0, 0]`
* nWaveformSource = `[1, 1, 1, 1, 0, 0, 0, 0]`
* nInterEpisodeLevel = `[0, 0, 0, 0, 0, 0, 0, 0]`
* fDACFileScale = `[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]`
* fDACFileOffset = `[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]`
* lDACFileEpisodeNum = `[0, 0, 0, 0, 0, 0, 0, 0]`
* nDACFileADCNum = `[0, 0, 0, 0, 0, 0, 0, 0]`
* nConditEnable = `[0, 0, 0, 0, 0, 0, 0, 0]`
* lConditNumPulses = `[1, 0, 0, 0, 0, 0, 0, 0]`
* fBaselineDuration = `[1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0]`
* fBaselineLevel = `[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]`
* fStepDuration = `[1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0]`
* fStepLevel = `[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]`
* fPostTrainPeriod = `[10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0]`
* fPostTrainLevel = `[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]`
* nMembTestEnable = `[0, 0, 0, 0, 0, 0, 0, 0]`
* nLeakSubtractType = `[0, 0, 0, 0, 0, 0, 0, 0]`
* nPNPolarity = `[1, 1, 1, 1, 1, 1, 1, 1]`
* fPNHoldingLevel = `[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]`
* nPNNumADCChannels = `[0, 0, 0, 0, 0, 0, 0, 0]`
* nPNPosition = `[0, 0, 0, 0, 0, 0, 0, 0]`
* nPNNumPulses = `[4, 4, 4, 4, 4, 4, 4, 4]`
* fPNSettlingTime = `[100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0]`
* fPNInterpulse = `[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]`
* nLTPUsageOfDAC = `[0, 0, 0, 0, 0, 0, 0, 0]`
* nLTPPresynapticPulses = `[0, 0, 0, 0, 0, 0, 0, 0]`
* lDACFilePathIndex = `[0, 0, 0, 0, 0, 0, 0, 0]`
* fMembTestPreSettlingTimeMS = `[100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0]`
* fMembTestPostSettlingTimeMS = `[100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0]`
* nLeakSubtractADCIndex = `[0, 0, 0, 0, 0, 0, 0, 0]`

## EpochPerDACSection
* nEpochNum = `[0, 1, 2, 3, 4, 0, 1, 2, 3, 4]`
* nEpochType = `[1, 1, 1, 1, 1]`
* fEpochInitLevel = `[0.0, -50.0, 0.0, -50.0, -50.0]`
* fEpochLevelInc = `[0.0, 10.0, 0.0, 0.0, 10.0]`
* lEpochInitDuration = `[2000, 10000, 10000, 10000, 10000]`
* lEpochDurationInc = `[0, 0, 0, 0, 0]`
* lEpochPulsePeriod = `[0, 0, 0, 0, 0]`
* lEpochPulseWidth = `[0, 0, 0, 0, 0]`

## EpochSection
* nEpochDigitalOutput = `[0, 0, 0, 0, 0]`

## TagSection

## Extras
* abfFilePath = `C:\Users\scott\Documents\GitHub\pyABF\data\17o05028_ic_steps.abf`
* abfFileName = `17o05028_ic_steps.abf`
* abfID = `17o05028_ic_steps`
* abfDatetime = `2017-01-05 14:52:46.899000`
* sweepFirstByte = `6656`
* sweepPointCount = `60000`
* sweepCount = `16`
* signalScale = `0.032768`
