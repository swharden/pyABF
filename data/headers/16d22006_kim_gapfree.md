# 16d22006_kim_gapfree.abf

## ABF Class Methods

* abf.launchInClampFit()
* abf.saveABF1()
* abf.setSweep()
* abf.sweepD()

## ABF Class Variables

* abfDateTime = `2016-12-22 14:39:47.945000`
* abfDateTimeString = `2016-12-22T14:39:47.945`
* abfFileComment = ``
* abfFilePath = `C:/some/path/to/16d22006_kim_gapfree.abf`
* abfID = `16d22006_kim_gapfree`
* abfVersion = `{'major': 2, 'minor': 0, 'bugfix': 0, 'build': 0}`
* abfVersionString = `2.0.0.0`
* adcNames = `['IN 2', 'IN 3']`
* adcUnits = `['dB', 'mV']`
* channelCount = `2`
* channelList = `[0, 1]`
* creatorVersion = `{'major': 10, 'minor': 3, 'bugfix': 2, 'build': 1}`
* creatorVersionString = `10.3.2.1`
* dacNames = `['Cmd 0', 'Cmd 1']`
* dacUnits = `['mV', 'mV']`
* data = `array (2d) with values like: 0.01007, 0.01251, 0.01343, ..., 0.10376, 0.10345, 0.10376`
* dataByteStart = `4608`
* dataLengthMin = `0.8049999999999999`
* dataLengthSec = `48.3`
* dataPointByteSize = `2`
* dataPointCount = `966000`
* dataPointsPerMs = `10`
* dataRate = `10000`
* dataSecPerPoint = `0.0001`
* fileGUID = `{7125B685-4F50-474D-B53F-AF2D1E9D3434}`
* holdingCommand = `[0.0, 0.0, 0.0, 0.0]`
* protocol = `mapping`
* protocolPath = `C:\Users\kim\Documents\Molecular Devices\pCLAMP\Params\mapping.pro`
* stimulusByChannel = `[Stimulus(abf, 0), Stimulus(abf, 1)]`
* stimulusFileFolder = `C:/some/alternate/path`
* sweepC = `array (1d) with values like: 0.00000, 0.00000, 0.00000, ..., 0.00000, 0.00000, 0.00000`
* sweepChannel = `0`
* sweepCount = `1`
* sweepEpochs = `Sweep epoch waveform: Step 0.00 [0:7546], Step 0.00 [7546:483000]`
* sweepIntervalSec = `48.3`
* sweepLabelC = `Cmd 0 (mV)`
* sweepLabelX = `time (seconds)`
* sweepLabelY = `IN 2 (dB)`
* sweepLengthSec = `48.3`
* sweepList = `[0]`
* sweepNumber = `0`
* sweepPointCount = `483000`
* sweepTimesMin = `array (1d) with values like: 0.00000`
* sweepTimesSec = `array (1d) with values like: 0.00000`
* sweepUnitsC = `mV`
* sweepUnitsX = `sec`
* sweepUnitsY = `dB`
* sweepX = `array (1d) with values like: 0.00000, 0.00010, 0.00020, ..., 48.29970, 48.29980, 48.29990`
* sweepY = `array (1d) with values like: 0.01007, 0.01251, 0.01343, ..., 0.01129, 0.01038, 0.01099`
* tagComments = `[]`
* tagSweeps = `[]`
* tagTimesMin = `[]`
* tagTimesSec = `[]`

## Epochs for Channel 0


```
DAC waveform is not enabled
```

## Epochs for Channel 1


```

```

## ABF2 Header

> The first several bytes of an ABF2 file contain variables     located at specific byte positions from the start of the file. 

* abfDateTime = `2016-12-22 14:39:47.945000`
* abfDateTimeString = `2016-12-22T14:39:47.945`
* abfVersionDict = `{'major': 2, 'minor': 0, 'bugfix': 0, 'build': 0}`
* abfVersionFloat = `2.0`
* abfVersionString = `2.0.0.0`
* creatorVersionDict = `{'major': 10, 'minor': 3, 'bugfix': 2, 'build': 1}`
* creatorVersionFloat = `10.321`
* creatorVersionString = `10.3.2.1`
* fFileSignature = `ABF2`
* fFileVersionNumber = `[0, 0, 0, 2]`
* lActualEpisodes = `0`
* nCRCEnable = `0`
* nDataFormat = `0`
* nFileType = `1`
* nSimultaneousScan = `0`
* sFileGUID = `{7125B685-4F50-474D-B53F-AF2D1E9D3434}`
* uCreatorNameIndex = `1`
* uCreatorVersion = `[1, 2, 3, 10]`
* uFileCRC = `0`
* uFileGUID = `[133, 182, 37, 113, 80, 79, 77, 71, 181, 63, 175, 45, 30, 157, 215, 52]`
* uFileInfoSize = `512`
* uFileStartDate = `20161222`
* uFileStartTimeMS = `52787945`
* uModifierNameIndex = `0`
* uModifierVersion = `0`
* uProtocolPathIndex = `2`
* uStopwatchTime = `2088`

## SectionMap

> Reading three numbers (int, int, long) at specific byte locations     yields the block position, byte size, and item count of specific     data stored in sections. Note that a block is 512 bytes. Some of     these sections are not read by this class because they are either     not useful for my applications, typically unused, or have an     unknown memory structure. 

* ADCPerDACSection = `[0, 0, 0]`
* ADCSection = `[2, 128, 2]`
* AnnotationSection = `[0, 0, 0]`
* DACSection = `[3, 256, 4]`
* DataSection = `[9, 2, 966000]`
* DeltaSection = `[0, 0, 0]`
* EpochPerDACSection = `[0, 0, 0]`
* EpochSection = `[0, 0, 0]`
* MathSection = `[0, 0, 0]`
* ProtocolSection = `[1, 512, 1]`
* ScopeSection = `[7, 769, 1]`
* StatsRegionSection = `[5, 128, 1]`
* StatsSection = `[0, 0, 0]`
* StringsSection = `[6, 172, 14]`
* SynchArraySection = `[0, 0, 0]`
* TagSection = `[0, 0, 0]`
* UserListSection = `[0, 0, 0]`
* VoiceTagSection = `[0, 0, 0]`

## ProtocolSection

> This section contains information about the recording settings.     This is useful for determining things like sample rate and     channel scaling factors. 

* bEnableFileCompression = `0`
* fADCRange = `10.0`
* fADCSequenceInterval = `100.0`
* fAverageWeighting = `0.10000000149011612`
* fCellID = `[0.0, 0.0, 0.0]`
* fDACRange = `10.0`
* fEpisodeStartToStart = `0.0`
* fFirstRunDelayS = `0.0`
* fRunStartToStart = `0.0`
* fScopeOutputInterval = `0.0`
* fSecondsPerRun = `0.0`
* fStatisticsPeriod = `1.0`
* fSynchTimeUnit = `0.0`
* fTrialStartToStart = `0.0`
* fTriggerThreshold = `0.0`
* lADCResolution = `32768`
* lAverageCount = `0`
* lDACResolution = `32768`
* lEpisodesPerRun = `1`
* lFileCommentIndex = `0`
* lFinishDisplayNum = `0`
* lNumSamplesPerEpisode = `4000`
* lNumberOfTrials = `1`
* lPreTriggerSamples = `40`
* lRunsPerTrial = `1`
* lSamplesPerTrace = `20000`
* lStartDisplayNum = `0`
* lStatisticsMeasurements = `5`
* lTimeHysteresis = `1`
* nActiveDACChannel = `0`
* nAllowExternalTags = `0`
* nAlternateDACOutputState = `0`
* nAlternateDigitalOutputState = `0`
* nAutoAnalyseEnable = `0`
* nAutoTriggerStrategy = `1`
* nAverageAlgorithm = `0`
* nAveragingMode = `0`
* nChannelStatsStrategy = `0`
* nCommentsEnable = `0`
* nDigitalDACChannel = `0`
* nDigitalEnable = `0`
* nDigitalHolding = `0`
* nDigitalInterEpisode = `0`
* nDigitalTrainActiveLogic = `1`
* nDigitizerADCs = `16`
* nDigitizerDACs = `2`
* nDigitizerSynchDigitalOuts = `8`
* nDigitizerTotalDigitalOuts = `16`
* nDigitizerType = `3`
* nExperimentType = `2`
* nExternalTagType = `2`
* nFirstEpisodeInRun = `0`
* nLTPType = `0`
* nLevelHysteresis = `64`
* nManualInfoStrategy = `0`
* nOperationMode = `3`
* nScopeTriggerOut = `0`
* nShowPNRawData = `0`
* nSignalType = `1`
* nStatisticsClearStrategy = `0`
* nStatisticsDisplayStrategy = `0`
* nStatisticsSaveStrategy = `0`
* nStatsEnable = `0`
* nTrialTriggerSource = `-1`
* nTriggerAction = `0`
* nTriggerPolarity = `0`
* nTriggerSource = `-3`
* nUndoPromptStrategy = `0`
* nUndoRunCount = `0`
* sDigitizerType = `DD132X`
* sUnused = `['\x00', '\x00', '\x00']`
* uFileCompressionRatio = `1`

## ADCSection

> Information about the ADC (what gets recorded).     There is 1 item per ADC. 

* bEnabledDuringPN = `[0, 0]`
* fADCDisplayAmplification = `[1.0, 1.0]`
* fADCDisplayOffset = `[0.0, 0.0]`
* fADCProgrammableGain = `[1.0, 1.0]`
* fInstrumentOffset = `[0.0, 0.0]`
* fInstrumentScaleFactor = `[1.0, 1.0]`
* fPostProcessLowpassFilter = `[100000.0, 100000.0]`
* fSignalGain = `[1.0, 1.0]`
* fSignalHighpassFilter = `[1.0, 0.0]`
* fSignalLowpassFilter = `[5000.0, 4000.0]`
* fSignalOffset = `[0.0, 0.0]`
* fTelegraphAccessResistance = `[0.0, 0.0]`
* fTelegraphAdditGain = `[1.0, 1.0]`
* fTelegraphFilter = `[0.0, 0.0]`
* fTelegraphMembraneCap = `[0.0, 0.0]`
* lADCChannelNameIndex = `[3, 5]`
* lADCUnitsIndex = `[4, 6]`
* nADCNum = `[2, 3]`
* nADCPtoLChannelMap = `[2, 3]`
* nADCSamplingSeq = `[0, 0]`
* nHighpassFilterType = `[0, 1]`
* nLowpassFilterType = `[0, 1]`
* nPostProcessLowpassFilterType = `['\x00', '\x00']`
* nStatsChannelPolarity = `[0, 0]`
* nTelegraphEnable = `[0, 0]`
* nTelegraphInstrument = `[0, 0]`
* nTelegraphMode = `[0, 0]`
* sTelegraphInstrument = `['Unknown instrument (manual or user defined telegraph table).', 'Unknown instrument (manual or user defined telegraph table).']`

## DACSection

> Information about the DAC (what gets clamped).     There is 1 item per DAC. 

* fBaselineDuration = `[1.0, 1.0, 1.0, 1.0]`
* fBaselineLevel = `[0.0, 0.0, 0.0, 0.0]`
* fDACCalibrationFactor = `[1.0930800437927246, 1.094059944152832, 1.0, 1.0]`
* fDACCalibrationOffset = `[-31.0, -28.0, 0.0, 0.0]`
* fDACFileOffset = `[0.0, 0.0, 0.0, 0.0]`
* fDACFileScale = `[1.0, 1.0, 1.0, 1.0]`
* fDACHoldingLevel = `[0.0, 0.0, 0.0, 0.0]`
* fDACScaleFactor = `[20.0, 20.0, 20.0, 20.0]`
* fInstrumentHoldingLevel = `[0.0, 0.0, 0.0, 0.0]`
* fMembTestPostSettlingTimeMS = `[100.0, 100.0, 100.0, 100.0]`
* fMembTestPreSettlingTimeMS = `[100.0, 100.0, 100.0, 100.0]`
* fPNHoldingLevel = `[0.0, 0.0, 0.0, 0.0]`
* fPNInterpulse = `[0.0, 0.0, 0.0, 0.0]`
* fPNSettlingTime = `[100.0, 100.0, 100.0, 100.0]`
* fPostTrainLevel = `[0.0, 0.0, 0.0, 0.0]`
* fPostTrainPeriod = `[10.0, 10.0, 10.0, 10.0]`
* fStepDuration = `[1.0, 1.0, 1.0, 1.0]`
* fStepLevel = `[0.0, 0.0, 0.0, 0.0]`
* lConditNumPulses = `[1, 0, 0, 0]`
* lDACChannelNameIndex = `[7, 9, 11, 13]`
* lDACChannelUnitsIndex = `[8, 10, 12, 14]`
* lDACFileEpisodeNum = `[0, 0, 0, 0]`
* lDACFileNumEpisodes = `[0, 0, 0, 0]`
* lDACFilePathIndex = `[0, 0, 0, 0]`
* lDACFilePtr = `[0, 0, 0, 0]`
* nConditEnable = `[0, 0, 0, 0]`
* nDACFileADCNum = `[0, 0, 0, 0]`
* nDACNum = `[0, 1, 2, 3]`
* nInterEpisodeLevel = `[0, 0, 0, 0]`
* nLTPPresynapticPulses = `[0, 0, 0, 0]`
* nLTPUsageOfDAC = `[0, 0, 0, 0]`
* nLeakSubtractADCIndex = `[3, 0, 0, 0]`
* nLeakSubtractType = `[0, 0, 0, 0]`
* nMembTestEnable = `[0, 0, 0, 0]`
* nPNNumADCChannels = `[0, 0, 0, 0]`
* nPNNumPulses = `[4, 4, 4, 4]`
* nPNPolarity = `[1, 1, 1, 1]`
* nPNPosition = `[0, 0, 0, 0]`
* nTelegraphDACScaleFactorEnable = `[0, 0, 0, 0]`
* nWaveformEnable = `[1, 0, 0, 0]`
* nWaveformSource = `[0, 0, 0, 0]`

## EpochPerDACSection

> This section contains waveform protocol information. These are most of     the values set when using the epoch the waveform editor. Note that digital     output signals are not stored here, but are in EpochSection. 

* fEpochInitLevel = `[]`
* fEpochLevelInc = `[]`
* lEpochDurationInc = `[]`
* lEpochInitDuration = `[]`
* lEpochPulsePeriod = `[]`
* lEpochPulseWidth = `[]`
* nDACNum = `[]`
* nEpochNum = `[]`
* nEpochType = `[]`

## EpochSection

> This section contains the digital output signals for each epoch. This     section has been overlooked by some previous open-source ABF-reading     projects. Note that the digital output is a single byte, but represents     8 bits corresponding to 8 outputs (7->0). When working with these bits,     I convert it to a string like "10011101" for easy eyeballing. 

* nEpochDigitalOutput = `[]`
* nEpochNum = `[]`

## TagSection

> Tags are comments placed in ABF files during the recording. Physically     they are located at the end of the file (after the data).      Later we will populate the times and sweeps (human-understandable units)     by multiplying the lTagTime by fSynchTimeUnit from the protocol section. 

* lTagTime = `[]`
* nTagType = `[]`
* nVoiceTagNumberorAnnotationIndex = `[]`
* sComment = `[]`
* sweeps = `[]`
* timesMin = `[]`
* timesSec = `[]`

## StringsSection

> Part of the ABF file contains long strings. Some of these can be broken     apart into indexed strings.      The first string is the only one which seems to contain useful information.     This contains information like channel names, channel units, and abf     protocol path and comments. The other strings are very large and I do not     know what they do.      Strings which contain indexed substrings are separated by \x00 characters. 

* strings = `not shown due to non-ASCII characters`

## StringsIndexed

> This object provides easy access to strings which are scattered around     the header files. The StringsSection contains strings, but various headers     contain values which point to a certain string index. This class connects     the two, and provides direct access to those strings by their indexed name. 

* lADCChannelName = `['IN 2', 'IN 3']`
* lADCUnits = `['dB', 'mV']`
* lDACChannelName = `['Cmd 0', 'Cmd 1', 'Cmd 2', 'Cmd 3']`
* lDACChannelUnits = `['mV', 'mV', 'mV', 'mV']`
* lDACFilePath = `['', '', '', '']`
* lFileComment = ``
* nLeakSubtractADC = `['IN 2', '', '', '']`
* uCreatorName = `AxoScope`
* uModifierName = ``
* uProtocolPath = `C:\Users\kim\Documents\Molecular Devices\pCLAMP\Params\mapping.pro`
