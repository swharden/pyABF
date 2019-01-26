# 171116sh_0015-ATFwaveform.abf

## ABF Class Methods

* abf.launchInClampFit()
* abf.saveABF1()
* abf.setSweep()
* abf.sweepD()

## ABF Class Variables

* abfDateTime = `2017-11-16 14:06:28.730000`
* abfDateTimeString = `2017-11-16T14:06:28.730`
* abfFileComment = `SWHLab5[0102]`
* abfFilePath = `C:/some/path/to/171116sh_0015-ATFwaveform.abf`
* abfID = `171116sh_0015-ATFwaveform`
* abfVersion = `{'major': 2, 'minor': 6, 'bugfix': 0, 'build': 0}`
* abfVersionString = `2.6.0.0`
* adcNames = `['IN 0']`
* adcUnits = `['pA']`
* channelCount = `1`
* channelList = `[0]`
* creatorVersion = `{'major': 10, 'minor': 7, 'bugfix': 0, 'build': 3}`
* creatorVersionString = `10.7.0.3`
* dacNames = `['Cmd 0']`
* dacUnits = `['mV']`
* data = `array (2d) with values like: -119.38476, -118.16405, -117.06542, ..., -101.80663, -104.85839, -103.27148`
* dataByteStart = `6656`
* dataLengthMin = `0.6666666666666666`
* dataLengthSec = `40.0`
* dataPointByteSize = `2`
* dataPointCount = `300000`
* dataPointsPerMs = `10`
* dataRate = `10000`
* dataSecPerPoint = `0.0001`
* fileGUID = `{6820CD72-752A-410F-8E09-121CF9BAFAFA}`
* holdingCommand = `[-70.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]`
* protocol = `0221 VC sine sweep 70 +- 5 mV`
* protocolPath = `L:\Protocols\permanent\0221 VC sine sweep 70 +- 5 mV.pro`
* stimulusByChannel = `[Stimulus(abf, 0)]`
* stimulusFileFolder = `C:/some/alternate/path`
* sweepC = `array (1d) with values like: 0.00000, 0.00000, 0.00001, ..., 15.83390, 16.07410, 16.31030`
* sweepChannel = `0`
* sweepCount = `3`
* sweepEpochs = `Sweep epoch waveform: Step -70.00 [0:1562], Step 0.00 [1562:2562], Step -10.00 [2562:7562], Step -70.00 [7562:100000]`
* sweepIntervalSec = `10.0`
* sweepLabelC = `Membrane Potential (mV)`
* sweepLabelX = `time (seconds)`
* sweepLabelY = `Clamp Current (pA)`
* sweepLengthSec = `10.0`
* sweepList = `[0, 1, 2]`
* sweepNumber = `0`
* sweepPointCount = `100000`
* sweepTimesMin = `array (1d) with values like: 0.00000, 0.16667, 0.33333`
* sweepTimesSec = `array (1d) with values like: 0.00000, 10.00000, 20.00000`
* sweepUnitsC = `mV`
* sweepUnitsX = `sec`
* sweepUnitsY = `pA`
* sweepX = `array (1d) with values like: 0.00000, 0.00010, 0.00020, ..., 9.99970, 9.99980, 9.99990`
* sweepY = `array (1d) with values like: -119.38476, -118.16405, -117.06542, ..., -104.85839, -107.78808, -107.78808`
* tagComments = `[]`
* tagSweeps = `[]`
* tagTimesMin = `[]`
* tagTimesSec = `[]`

## Epochs for Channel 0


```
DAC waveform is controlled by custom file
```

## ABF2 Header

> The first several bytes of an ABF2 file contain variables     located at specific byte positions from the start of the file. 

* abfDateTime = `2017-11-16 14:06:28.730000`
* abfDateTimeString = `2017-11-16T14:06:28.730`
* abfVersionDict = `{'major': 2, 'minor': 6, 'bugfix': 0, 'build': 0}`
* abfVersionFloat = `2.6`
* abfVersionString = `2.6.0.0`
* creatorVersionDict = `{'major': 10, 'minor': 7, 'bugfix': 0, 'build': 3}`
* creatorVersionFloat = `10.703`
* creatorVersionString = `10.7.0.3`
* fFileSignature = `ABF2`
* fFileVersionNumber = `[0, 0, 6, 2]`
* lActualEpisodes = `3`
* nCRCEnable = `0`
* nDataFormat = `0`
* nFileType = `1`
* nSimultaneousScan = `1`
* sFileGUID = `{6820CD72-752A-410F-8E09-121CF9BAFAFA}`
* uCreatorNameIndex = `1`
* uCreatorVersion = `[3, 0, 7, 10]`
* uFileCRC = `0`
* uFileGUID = `[114, 205, 32, 104, 42, 117, 15, 65, 142, 9, 18, 28, 249, 186, 24, 250]`
* uFileInfoSize = `512`
* uFileStartDate = `20171116`
* uFileStartTimeMS = `50788730`
* uModifierNameIndex = `0`
* uModifierVersion = `0`
* uProtocolPathIndex = `2`
* uStopwatchTime = `2696`

## SectionMap

> Reading three numbers (int, int, long) at specific byte locations     yields the block position, byte size, and item count of specific     data stored in sections. Note that a block is 512 bytes. Some of     these sections are not read by this class because they are either     not useful for my applications, typically unused, or have an     unknown memory structure. 

* ADCPerDACSection = `[0, 0, 0]`
* ADCSection = `[2, 128, 1]`
* AnnotationSection = `[0, 0, 0]`
* DACSection = `[3, 256, 8]`
* DataSection = `[13, 2, 300000]`
* DeltaSection = `[0, 0, 0]`
* EpochPerDACSection = `[7, 48, 2]`
* EpochSection = `[8, 32, 2]`
* MathSection = `[0, 0, 0]`
* ProtocolSection = `[1, 512, 1]`
* ScopeSection = `[11, 769, 1]`
* StatsRegionSection = `[9, 128, 1]`
* StatsSection = `[0, 0, 0]`
* StringsSection = `[10, 272, 22]`
* SynchArraySection = `[1185, 8, 3]`
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
* fSecondsPerRun = `7200.0`
* fStatisticsPeriod = `1.0`
* fSynchTimeUnit = `20.0`
* fTrialStartToStart = `0.0`
* fTriggerThreshold = `0.0`
* lADCResolution = `32768`
* lAverageCount = `1`
* lDACResolution = `32768`
* lEpisodesPerRun = `3`
* lFileCommentIndex = `3`
* lFinishDisplayNum = `100000`
* lNumSamplesPerEpisode = `100000`
* lNumberOfTrials = `1`
* lPreTriggerSamples = `10`
* lRunsPerTrial = `1`
* lSamplesPerTrace = `40000`
* lStartDisplayNum = `0`
* lStatisticsMeasurements = `5`
* lTimeHysteresis = `1`
* nActiveDACChannel = `0`
* nAllowExternalTags = `0`
* nAlternateDACOutputState = `0`
* nAlternateDigitalOutputState = `0`
* nAutoAnalyseEnable = `1`
* nAutoTriggerStrategy = `1`
* nAverageAlgorithm = `0`
* nAveragingMode = `0`
* nChannelStatsStrategy = `0`
* nCommentsEnable = `1`
* nDigitalDACChannel = `0`
* nDigitalEnable = `0`
* nDigitalHolding = `0`
* nDigitalInterEpisode = `0`
* nDigitalTrainActiveLogic = `1`
* nDigitizerADCs = `16`
* nDigitizerDACs = `4`
* nDigitizerSynchDigitalOuts = `8`
* nDigitizerTotalDigitalOuts = `16`
* nDigitizerType = `6`
* nExperimentType = `2`
* nExternalTagType = `2`
* nFirstEpisodeInRun = `0`
* nLTPType = `0`
* nLevelHysteresis = `64`
* nManualInfoStrategy = `1`
* nOperationMode = `5`
* nScopeTriggerOut = `0`
* nShowPNRawData = `0`
* nSignalType = `0`
* nStatisticsClearStrategy = `1`
* nStatisticsDisplayStrategy = `0`
* nStatisticsSaveStrategy = `1`
* nStatsEnable = `0`
* nTrialTriggerSource = `-1`
* nTriggerAction = `0`
* nTriggerPolarity = `0`
* nTriggerSource = `-3`
* nUndoPromptStrategy = `0`
* nUndoRunCount = `0`
* sDigitizerType = `Digidata 1440`
* sUnused = `['\x00', '\x00', '\x00']`
* uFileCompressionRatio = `1`

## ADCSection

> Information about the ADC (what gets recorded).     There is 1 item per ADC. 

* bEnabledDuringPN = `[0]`
* fADCDisplayAmplification = `[39.999385833740234]`
* fADCDisplayOffset = `[-140.0]`
* fADCProgrammableGain = `[1.0]`
* fInstrumentOffset = `[0.0]`
* fInstrumentScaleFactor = `[0.0005000000237487257]`
* fPostProcessLowpassFilter = `[100000.0]`
* fSignalGain = `[1.0]`
* fSignalHighpassFilter = `[1.0]`
* fSignalLowpassFilter = `[5000.0]`
* fSignalOffset = `[0.0]`
* fTelegraphAccessResistance = `[0.0]`
* fTelegraphAdditGain = `[5.0]`
* fTelegraphFilter = `[2000.0]`
* fTelegraphMembraneCap = `[0.0]`
* lADCChannelNameIndex = `[4]`
* lADCUnitsIndex = `[5]`
* nADCNum = `[0]`
* nADCPtoLChannelMap = `[0]`
* nADCSamplingSeq = `[0]`
* nHighpassFilterType = `[0]`
* nLowpassFilterType = `[0]`
* nPostProcessLowpassFilterType = `['\x00']`
* nStatsChannelPolarity = `[0]`
* nTelegraphEnable = `[1]`
* nTelegraphInstrument = `[24]`
* nTelegraphMode = `[0]`
* sTelegraphInstrument = `['MultiClamp 700']`

## DACSection

> Information about the DAC (what gets clamped).     There is 1 item per DAC. 

* fBaselineDuration = `[1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0]`
* fBaselineLevel = `[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]`
* fDACCalibrationFactor = `[1.001173496246338, 1.0012290477752686, 1.001173496246338, 1.001173496246338, 1.0, 1.0, 1.0, 1.0]`
* fDACCalibrationOffset = `[-4.0, -4.0, -7.0, -6.0, 0.0, 0.0, 0.0, 0.0]`
* fDACFileOffset = `[-70.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]`
* fDACFileScale = `[0.25, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]`
* fDACHoldingLevel = `[-70.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]`
* fDACScaleFactor = `[20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0]`
* fInstrumentHoldingLevel = `[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]`
* fMembTestPostSettlingTimeMS = `[100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0]`
* fMembTestPreSettlingTimeMS = `[100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0]`
* fPNHoldingLevel = `[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]`
* fPNInterpulse = `[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]`
* fPNSettlingTime = `[100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0]`
* fPostTrainLevel = `[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]`
* fPostTrainPeriod = `[10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0]`
* fStepDuration = `[1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0]`
* fStepLevel = `[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]`
* lConditNumPulses = `[1, 0, 0, 0, 0, 0, 0, 0]`
* lDACChannelNameIndex = `[6, 9, 11, 13, 15, 17, 19, 21]`
* lDACChannelUnitsIndex = `[7, 10, 12, 14, 16, 18, 20, 22]`
* lDACFileEpisodeNum = `[0, 0, 0, 0, 0, 0, 0, 0]`
* lDACFileNumEpisodes = `[1, 0, 0, 0, 0, 0, 0, 0]`
* lDACFilePathIndex = `[8, 0, 0, 0, 0, 0, 0, 0]`
* lDACFilePtr = `[1186, 0, 0, 0, 0, 0, 0, 0]`
* nConditEnable = `[0, 0, 0, 0, 0, 0, 0, 0]`
* nDACFileADCNum = `[0, 0, 0, 0, 0, 0, 0, 0]`
* nDACNum = `[0, 1, 2, 3, 4, 5, 6, 7]`
* nInterEpisodeLevel = `[0, 0, 0, 0, 0, 0, 0, 0]`
* nLTPPresynapticPulses = `[0, 0, 0, 0, 0, 0, 0, 0]`
* nLTPUsageOfDAC = `[0, 0, 0, 0, 0, 0, 0, 0]`
* nLeakSubtractADCIndex = `[0, 0, 0, 0, 0, 0, 0, 0]`
* nLeakSubtractType = `[0, 0, 0, 0, 0, 0, 0, 0]`
* nMembTestEnable = `[0, 0, 0, 0, 0, 0, 0, 0]`
* nPNNumADCChannels = `[0, 0, 0, 0, 0, 0, 0, 0]`
* nPNNumPulses = `[4, 4, 4, 4, 4, 4, 4, 4]`
* nPNPolarity = `[1, 1, 1, 1, 1, 1, 1, 1]`
* nPNPosition = `[0, 0, 0, 0, 0, 0, 0, 0]`
* nTelegraphDACScaleFactorEnable = `[1, 0, 0, 0, 0, 0, 0, 0]`
* nWaveformEnable = `[1, 0, 0, 0, 0, 0, 0, 0]`
* nWaveformSource = `[2, 1, 1, 1, 0, 0, 0, 0]`

## EpochPerDACSection

> This section contains waveform protocol information. These are most of     the values set when using the epoch the waveform editor. Note that digital     output signals are not stored here, but are in EpochSection. 

* fEpochInitLevel = `[0.0, -10.0]`
* fEpochLevelInc = `[0.0, 0.0]`
* lEpochDurationInc = `[0, 0]`
* lEpochInitDuration = `[1000, 5000]`
* lEpochPulsePeriod = `[0, 0]`
* lEpochPulseWidth = `[0, 0]`
* nDACNum = `[0, 0]`
* nEpochNum = `[0, 1]`
* nEpochType = `[1, 1]`

## EpochSection

> This section contains the digital output signals for each epoch. This     section has been overlooked by some previous open-source ABF-reading     projects. Note that the digital output is a single byte, but represents     8 bits corresponding to 8 outputs (7->0). When working with these bits,     I convert it to a string like "10011101" for easy eyeballing. 

* nEpochDigitalOutput = `[0, 0]`
* nEpochNum = `[0, 1]`

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

* lADCChannelName = `['IN 0']`
* lADCUnits = `['pA']`
* lDACChannelName = `['Cmd 0', 'Cmd 1', 'Cmd 2', 'Cmd 3', 'AO #4', 'AO #5', 'AO #6', 'AO #7']`
* lDACChannelUnits = `['mV', 'mV', 'mV', 'mV', 'mV', 'mV', 'mV', 'mV']`
* lDACFilePath = `['L:\\Protocols\\permanent\\waveform stimulus\\sine sweep magnitude 20.atf', '', '', '', '', '', '', '']`
* lFileComment = `SWHLab5[0102]`
* nLeakSubtractADC = `['', '', '', '', '', '', '', '']`
* uCreatorName = `Clampex`
* uModifierName = ``
* uProtocolPath = `L:\Protocols\permanent\0221 VC sine sweep 70 +- 5 mV.pro`
