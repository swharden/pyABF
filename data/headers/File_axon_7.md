# File_axon_7.abf

## ABF Class Methods

* abf.launchInClampFit()
* abf.saveABF1()
* abf.setSweep()
* abf.sweepD()

## ABF Class Variables

* abfDateTime = `2016-08-02 21:39:10.343000`
* abfDateTimeString = `2016-08-02T21:39:10.343`
* abfFileComment = ``
* abfFilePath = `C:/some/path/to/File_axon_7.abf`
* abfID = `File_axon_7`
* abfVersion = `{'major': 2, 'minor': 6, 'bugfix': 0, 'build': 0}`
* abfVersionString = `2.6.0.0`
* adcNames = `['IN 1']`
* adcUnits = `['pA']`
* channelCount = `1`
* channelList = `[0]`
* creatorVersion = `{'major': 0, 'minor': 0, 'bugfix': 0, 'build': 0}`
* creatorVersionString = `0.0.0.0`
* dacNames = `['Cmd 0']`
* dacUnits = `['mV']`
* data = `array (2d) with values like: -1.48067, -0.80929, -0.13112, ..., -1.18700, -1.01261, -0.69290`
* dataByteStart = `4608`
* dataLengthMin = `2.066790736145575`
* dataLengthSec = `124.0074441687345`
* dataPointByteSize = `4`
* dataPointCount = `19380`
* dataPointsPerMs = `0`
* dataRate = `403`
* dataSecPerPoint = `0.0024813895781637717`
* fileGUID = `{F0257BE6-17F2-419A-AFE1-AF009E85FAFA}`
* holdingCommand = `[-80.0, -80.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]`
* protocol = `Apl NMDA 2 s -80mV cada 2ms esp 10 2480us`
* protocolPath = `C:\Axon\Params\neuromodulacion\Gustavo\Ach\Apl NMDA 2 s -80mV cada 2ms esp 10 2480us.pro`
* stimulusByChannel = `[Stimulus(abf, 0)]`
* stimulusFileFolder = `C:/some/alternate/path`
* sweepC = `array (1d) with values like: -80.00000, -80.00000, -80.00000, ..., -80.00000, -80.00000, -80.00000`
* sweepChannel = `0`
* sweepCount = `12`
* sweepEpochs = `Sweep epoch waveform: Step -80.00 [0:25], Step -80.00 [25:1615]`
* sweepIntervalSec = `10.0`
* sweepLabelC = `Membrane Potential (mV)`
* sweepLabelX = `time (seconds)`
* sweepLabelY = `Clamp Current (pA)`
* sweepLengthSec = `4.007444168734492`
* sweepList = `[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]`
* sweepNumber = `0`
* sweepPointCount = `1615`
* sweepTimesMin = `array (1d) with values like: 0.00000, 0.16667, 0.33333, ..., 1.50000, 1.66667, 1.83333`
* sweepTimesSec = `array (1d) with values like: 0.00000, 10.00000, 20.00000, ..., 90.00000, 100.00000, 110.00000`
* sweepUnitsC = `mV`
* sweepUnitsX = `sec`
* sweepUnitsY = `pA`
* sweepX = `array (1d) with values like: 0.00000, 0.00248, 0.00496, ..., 4.00000, 4.00248, 4.00496`
* sweepY = `array (1d) with values like: -1.48067, -0.80929, -0.13112, ..., 0.60808, 0.20118, 0.12658`
* tagComments = `[]`
* tagSweeps = `[]`
* tagTimesMin = `[]`
* tagTimesSec = `[]`

## Epochs for Channel 0


```
DAC waveform is not enabled
```

## ABF2 Header

> The first several bytes of an ABF2 file contain variables     located at specific byte positions from the start of the file. 

* abfDateTime = `2016-08-02 21:39:10.343000`
* abfDateTimeString = `2016-08-02T21:39:10.343`
* abfVersionDict = `{'major': 2, 'minor': 6, 'bugfix': 0, 'build': 0}`
* abfVersionFloat = `2.6`
* abfVersionString = `2.6.0.0`
* creatorVersionDict = `{'major': 0, 'minor': 0, 'bugfix': 0, 'build': 0}`
* creatorVersionFloat = `0.0`
* creatorVersionString = `0.0.0.0`
* fFileSignature = `ABF2`
* fFileVersionNumber = `[0, 0, 6, 2]`
* lActualEpisodes = `12`
* nCRCEnable = `0`
* nDataFormat = `1`
* nFileType = `1`
* nSimultaneousScan = `0`
* sFileGUID = `{F0257BE6-17F2-419A-AFE1-AF009E85FAFA}`
* uCreatorNameIndex = `1`
* uCreatorVersion = `[0, 0, 0, 0]`
* uFileCRC = `0`
* uFileGUID = `[230, 123, 37, 240, 242, 23, 154, 65, 175, 225, 175, 0, 158, 133, 61, 250]`
* uFileInfoSize = `512`
* uFileStartDate = `20160802`
* uFileStartTimeMS = `77950343`
* uModifierNameIndex = `2`
* uModifierVersion = `168165890`
* uProtocolPathIndex = `3`
* uStopwatchTime = `83`

## SectionMap

> Reading three numbers (int, int, long) at specific byte locations     yields the block position, byte size, and item count of specific     data stored in sections. Note that a block is 512 bytes. Some of     these sections are not read by this class because they are either     not useful for my applications, typically unused, or have an     unknown memory structure. 

* ADCPerDACSection = `[0, 0, 0]`
* ADCSection = `[2, 128, 1]`
* AnnotationSection = `[0, 0, 0]`
* DACSection = `[3, 256, 8]`
* DataSection = `[9, 4, 19380]`
* DeltaSection = `[0, 0, 0]`
* EpochPerDACSection = `[0, 0, 0]`
* EpochSection = `[0, 0, 0]`
* MathSection = `[0, 0, 0]`
* ProtocolSection = `[1, 512, 1]`
* ScopeSection = `[0, 0, 0]`
* StatsRegionSection = `[7, 128, 1]`
* StatsSection = `[0, 0, 0]`
* StringsSection = `[8, 319, 22]`
* SynchArraySection = `[161, 8, 12]`
* TagSection = `[0, 0, 0]`
* UserListSection = `[0, 0, 0]`
* VoiceTagSection = `[0, 0, 0]`

## ProtocolSection

> This section contains information about the recording settings.     This is useful for determining things like sample rate and     channel scaling factors. 

* bEnableFileCompression = `0`
* fADCRange = `10.0`
* fADCSequenceInterval = `2480.0`
* fAverageWeighting = `0.10000000149011612`
* fCellID = `[0.0, 0.0, 0.0]`
* fDACRange = `10.0`
* fEpisodeStartToStart = `10.0`
* fFirstRunDelayS = `0.0`
* fRunStartToStart = `0.0`
* fScopeOutputInterval = `0.0`
* fSecondsPerRun = `10.0`
* fStatisticsPeriod = `1.0`
* fSynchTimeUnit = `62.0`
* fTrialStartToStart = `0.0`
* fTriggerThreshold = `0.0`
* lADCResolution = `32768`
* lAverageCount = `1`
* lDACResolution = `32768`
* lEpisodesPerRun = `12`
* lFileCommentIndex = `0`
* lFinishDisplayNum = `0`
* lNumSamplesPerEpisode = `1615`
* lNumberOfTrials = `1`
* lPreTriggerSamples = `0`
* lRunsPerTrial = `1`
* lSamplesPerTrace = `16384`
* lStartDisplayNum = `1`
* lStatisticsMeasurements = `5`
* lTimeHysteresis = `1`
* nActiveDACChannel = `1`
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
* nDigitalHolding = `17`
* nDigitalInterEpisode = `0`
* nDigitalTrainActiveLogic = `0`
* nDigitizerADCs = `16`
* nDigitizerDACs = `2`
* nDigitizerSynchDigitalOuts = `4`
* nDigitizerTotalDigitalOuts = `8`
* nDigitizerType = `1`
* nExperimentType = `0`
* nExternalTagType = `2`
* nFirstEpisodeInRun = `0`
* nLTPType = `0`
* nLevelHysteresis = `64`
* nManualInfoStrategy = `0`
* nOperationMode = `5`
* nScopeTriggerOut = `0`
* nShowPNRawData = `0`
* nSignalType = `0`
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
* sDigitizerType = `Demo`
* sUnused = `['\x00', '\x00', '\x00']`
* uFileCompressionRatio = `1`

## ADCSection

> Information about the ADC (what gets recorded).     There is 1 item per ADC. 

* bEnabledDuringPN = `[0]`
* fADCDisplayAmplification = `[12.738659858703613]`
* fADCDisplayOffset = `[-755.0]`
* fADCProgrammableGain = `[1.0]`
* fInstrumentOffset = `[0.0]`
* fInstrumentScaleFactor = `[0.0010000000474974513]`
* fPostProcessLowpassFilter = `[40.0]`
* fSignalGain = `[1.0]`
* fSignalHighpassFilter = `[1.0]`
* fSignalLowpassFilter = `[5000.0]`
* fSignalOffset = `[0.0]`
* fTelegraphAccessResistance = `[0.0]`
* fTelegraphAdditGain = `[1.0]`
* fTelegraphFilter = `[10000.0]`
* fTelegraphMembraneCap = `[0.0]`
* lADCChannelNameIndex = `[4]`
* lADCUnitsIndex = `[5]`
* nADCNum = `[1]`
* nADCPtoLChannelMap = `[1]`
* nADCSamplingSeq = `[0]`
* nHighpassFilterType = `[0]`
* nLowpassFilterType = `[0]`
* nPostProcessLowpassFilterType = `['\x03']`
* nStatsChannelPolarity = `[0]`
* nTelegraphEnable = `[1]`
* nTelegraphInstrument = `[1]`
* nTelegraphMode = `[0]`
* sTelegraphInstrument = `['Axopatch-1 with CV-4-1/100']`

## DACSection

> Information about the DAC (what gets clamped).     There is 1 item per DAC. 

* fBaselineDuration = `[1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]`
* fBaselineLevel = `[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]`
* fDACCalibrationFactor = `[1.0828900337219238, 1.088070034980774, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]`
* fDACCalibrationOffset = `[1.0, -147.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]`
* fDACFileOffset = `[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]`
* fDACFileScale = `[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]`
* fDACHoldingLevel = `[-80.0, -80.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]`
* fDACScaleFactor = `[20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0]`
* fInstrumentHoldingLevel = `[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]`
* fMembTestPostSettlingTimeMS = `[100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0]`
* fMembTestPreSettlingTimeMS = `[100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0]`
* fPNHoldingLevel = `[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]`
* fPNInterpulse = `[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]`
* fPNSettlingTime = `[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]`
* fPostTrainLevel = `[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]`
* fPostTrainPeriod = `[0.0, 0.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0]`
* fStepDuration = `[1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]`
* fStepLevel = `[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]`
* lConditNumPulses = `[1, 1, 0, 0, 0, 0, 0, 0]`
* lDACChannelNameIndex = `[6, 8, 11, 13, 15, 17, 19, 21]`
* lDACChannelUnitsIndex = `[7, 9, 12, 14, 16, 18, 20, 22]`
* lDACFileEpisodeNum = `[0, 0, 0, 0, 0, 0, 0, 0]`
* lDACFileNumEpisodes = `[0, 0, 0, 0, 0, 0, 0, 0]`
* lDACFilePathIndex = `[0, 10, 0, 0, 0, 0, 0, 0]`
* lDACFilePtr = `[0, 0, 0, 0, 0, 0, 0, 0]`
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
* nPNNumPulses = `[2, 2, 2, 2, 2, 2, 2, 2]`
* nPNPolarity = `[1, 1, 1, 1, 1, 1, 1, 1]`
* nPNPosition = `[0, 0, 0, 0, 0, 0, 0, 0]`
* nTelegraphDACScaleFactorEnable = `[0, 0, 0, 0, 0, 0, 0, 0]`
* nWaveformEnable = `[0, 1, 0, 0, 0, 0, 0, 0]`
* nWaveformSource = `[0, 0, 0, 0, 0, 0, 0, 0]`

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

* lADCChannelName = `['IN 1']`
* lADCUnits = `['pA']`
* lDACChannelName = `['Cmd 0', 'Cmd 1', 'AO #2', 'AO #3', 'AO #4', 'AO #5', 'AO #6', 'AO #7']`
* lDACChannelUnits = `['mV', 'mV', 'mV', 'mV', 'mV', 'mV', 'mV', 'mV']`
* lDACFilePath = `['', 'C:\\Documents and Settings\\Equipo2\\Escritorio\\ruidos\\ruidoDrBraniff\\puroruido1.abf', '', '', '', '', '', '']`
* lFileComment = ``
* nLeakSubtractADC = `['', '', '', '', '', '', '', '']`
* uCreatorName = `AXENGN 2.0.2.2`
* uModifierName = `Clampfit`
* uProtocolPath = `C:\Axon\Params\neuromodulacion\Gustavo\Ach\Apl NMDA 2 s -80mV cada 2ms esp 10 2480us.pro`
