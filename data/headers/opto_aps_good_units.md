# opto_aps_good_units.abf

## ABF Class Methods

* abf.launchInClampFit()
* abf.saveABF1()
* abf.setSweep()
* abf.sweepD()

## ABF Class Variables

* abfDateTime = `2019-08-14 13:29:01.316000`
* abfDateTimeString = `2019-08-14T13:29:01.316`
* abfFileComment = `SWHLab5[0113]`
* abfFilePath = `C:/some/path/to/opto_aps_good_units.abf`
* abfFolderPath = `C:/some/path`
* abfID = `opto_aps_good_units`
* abfVersion = `{'major': 2, 'minor': 6, 'bugfix': 0, 'build': 0}`
* abfVersionString = `2.6.0.0`
* adcNames = `['IN 0']`
* adcUnits = `['mV']`
* channelCount = `1`
* channelList = `[0]`
* creator = `Clampex 10.7.0.3`
* creatorVersion = `{'major': 10, 'minor': 7, 'bugfix': 0, 'build': 3}`
* creatorVersionString = `10.7.0.3`
* dacNames = `['Cmd 0']`
* dacUnits = `['pA']`
* data = `array (2d) with values like: -75.98877, -76.04980, -76.11084, ..., -77.30103, -77.36206, -77.33154`
* dataByteStart = `6656`
* dataLengthMin = `1.3333333333333333`
* dataLengthSec = `80.0`
* dataPointByteSize = `2`
* dataPointCount = `1200000`
* dataPointsPerMs = `20`
* dataRate = `20000`
* dataSecPerPoint = `5e-05`
* fileGUID = `3A64A49D-2965-4F2F-89D6-48997850D179`
* holdingCommand = `[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]`
* protocol = `0504 opto [0] 10 Hz 2 ms (5s in 20s sweep)`
* protocolPath = `\\Spike\locked\Protocols\permanent\0504 opto [0] 10 Hz 2 ms (5s in 20s sweep).pro`
* stimulusByChannel = `[Stimulus(abf, 0)]`
* stimulusFileFolder = `C:\Users\scott\Documents\GitHub\pyABF\data\abfs`
* sweepC = `array (1d) with values like: 0.00000, 0.00000, 0.00000, ..., 0.00000, 0.00000, 0.00000`
* sweepChannel = `0`
* sweepCount = `3`
* sweepDerivative = `array (1d) with values like: -1220.70312, -1220.70312, 610.35156, ..., 0.00000, 610.35156, 610.35156`
* sweepEpochs = `Sweep epoch waveform: Step 0.00 [0:6250], Step 0.00 [6250:106250], Step 0.00 [106250:206250], Step 0.00 [206250:400000]`
* sweepIntervalSec = `20.0`
* sweepLabelC = `Applied Current (pA)`
* sweepLabelD = `Digital Output (V)`
* sweepLabelX = `Time (seconds)`
* sweepLabelY = `Membrane Potential (mV)`
* sweepLengthSec = `20.0`
* sweepList = `[0, 1, 2]`
* sweepNumber = `0`
* sweepPointCount = `400000`
* sweepTimesMin = `array (1d) with values like: 0.00000, 0.33333, 0.66667`
* sweepTimesSec = `array (1d) with values like: 0.00000, 20.00000, 40.00000`
* sweepUnitsC = `pA`
* sweepUnitsX = `sec`
* sweepUnitsY = `mV`
* sweepX = `array (1d) with values like: 0.00000, 0.00005, 0.00010, ..., 19.99985, 19.99990, 19.99995`
* sweepY = `array (1d) with values like: -75.98877, -76.04980, -76.11084, ..., -75.53101, -75.53101, -75.50049`
* tagComments = `[]`
* tagSweeps = `[]`
* tagTimesMin = `[]`
* tagTimesSec = `[]`

## Epochs for Channel 0


```
                    EPOCH         A         B
                     Type      Step      Step
              First Level      0.00      0.00
              Delta Level      0.00      0.00
  First Duration (points)    100000    100000
  Delta Duration (points)         0         0
     Digital Pattern #3-0      0000      0000
     Digital Pattern #7-4      0000      0000
    Train Period (points)         0      2000
     Pulse Width (points)         0        40
```

## ABF2 Header

> The first several bytes of an ABF2 file contain variables     located at specific byte positions from the start of the file. 

* abfDateTime = `2019-08-14 13:29:01.316000`
* abfDateTimeString = `2019-08-14T13:29:01.316`
* abfVersionDict = `{'major': 2, 'minor': 6, 'bugfix': 0, 'build': 0}`
* abfVersionFloat = `2.6`
* abfVersionString = `2.6.0.0`
* creatorVersionDict = `{'major': 10, 'minor': 7, 'bugfix': 0, 'build': 3}`
* creatorVersionFloat = `10.703`
* creatorVersionString = `10.7.0.3`
* fFileVersionNumber = `[0, 0, 6, 2]`
* lActualEpisodes = `3`
* nCRCEnable = `0`
* nDataFormat = `0`
* nFileType = `1`
* nSimultaneousScan = `1`
* sFileGUID = `3A64A49D-2965-4F2F-89D6-48997850D179`
* sFileSignature = `ABF2`
* uCreatorNameIndex = `1`
* uCreatorVersion = `[3, 0, 7, 10]`
* uFileCRC = `0`
* uFileGUID = `[157, 164, 100, 58, 101, 41, 47, 79, 137, 214, 72, 153, 120, 80, 209, 121]`
* uFileInfoSize = `512`
* uFileStartDate = `20190814`
* uFileStartTimeMS = `48541316`
* uModifierNameIndex = `0`
* uModifierVersion = `0`
* uProtocolPathIndex = `2`
* uStopwatchTime = `12839`

## SectionMap

> Reading three numbers (int, int, long) at specific byte locations     yields the block position, byte size, and item count of specific     data stored in sections. Note that a block is 512 bytes. Some of     these sections are not read by this class because they are either     not useful for my applications, typically unused, or have an     unknown memory structure. 

* ADCPerDACSection = `[0, 0, 0]`
* ADCSection = `[2, 128, 1]`
* AnnotationSection = `[0, 0, 0]`
* DACSection = `[3, 256, 8]`
* DataSection = `[13, 2, 1200000]`
* DeltaSection = `[0, 0, 0]`
* EpochPerDACSection = `[7, 48, 2]`
* EpochSection = `[8, 32, 2]`
* MathSection = `[0, 0, 0]`
* ProtocolSection = `[1, 512, 1]`
* ScopeSection = `[11, 769, 1]`
* StatsRegionSection = `[9, 128, 1]`
* StatsSection = `[0, 0, 0]`
* StringsSection = `[10, 228, 21]`
* SynchArraySection = `[4701, 8, 3]`
* TagSection = `[0, 0, 0]`
* UserListSection = `[0, 0, 0]`
* VoiceTagSection = `[0, 0, 0]`

## ProtocolSection

> This section contains information about the recording settings.     This is useful for determining things like sample rate and     channel scaling factors. 

* bEnableFileCompression = `0`
* fADCRange = `10.0`
* fADCSequenceInterval = `50.0`
* fAverageWeighting = `0.10000000149011612`
* fCellID = `[0.0, 0.0, 0.0]`
* fDACRange = `10.0`
* fEpisodeStartToStart = `0.0`
* fFirstRunDelayS = `0.0`
* fRunStartToStart = `0.0`
* fScopeOutputInterval = `0.0`
* fSecondsPerRun = `7200.0`
* fStatisticsPeriod = `1.0`
* fSynchTimeUnit = `12.5`
* fTrialStartToStart = `0.0`
* fTriggerThreshold = `0.0`
* lADCResolution = `32768`
* lAverageCount = `1`
* lDACResolution = `32768`
* lEpisodesPerRun = `1000`
* lFileCommentIndex = `3`
* lFinishDisplayNum = `400000`
* lNumSamplesPerEpisode = `400000`
* lNumberOfTrials = `1`
* lPreTriggerSamples = `20`
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
* nDigitalEnable = `1`
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
* nStatisticsSaveStrategy = `0`
* nStatsEnable = `1`
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
* fADCDisplayAmplification = `[8.368073463439941]`
* fADCDisplayOffset = `[5.5]`
* fADCProgrammableGain = `[1.0]`
* fInstrumentOffset = `[0.0]`
* fInstrumentScaleFactor = `[0.009999999776482582]`
* fPostProcessLowpassFilter = `[100000.0]`
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
* nADCNum = `[0]`
* nADCPtoLChannelMap = `[0]`
* nADCSamplingSeq = `[0]`
* nHighpassFilterType = `[0]`
* nLowpassFilterType = `[0]`
* nPostProcessLowpassFilterType = `['\x00']`
* nStatsChannelPolarity = `[1]`
* nTelegraphEnable = `[1]`
* nTelegraphInstrument = `[24]`
* nTelegraphMode = `[1]`
* sTelegraphInstrument = `['MultiClamp 700']`

## DACSection

> Information about the DAC (what gets clamped).     There is 1 item per DAC. 

* fBaselineDuration = `[1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0]`
* fBaselineLevel = `[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]`
* fDACCalibrationFactor = `[1.001173496246338, 1.0012290477752686, 1.001173496246338, 1.001173496246338, 1.0, 1.0, 1.0, 1.0]`
* fDACCalibrationOffset = `[-4.0, -4.0, -7.0, -6.0, 0.0, 0.0, 0.0, 0.0]`
* fDACFileOffset = `[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]`
* fDACFileScale = `[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]`
* fDACHoldingLevel = `[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]`
* fDACScaleFactor = `[400.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0]`
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
* lDACChannelNameIndex = `[6, 8, 10, 12, 14, 16, 18, 20]`
* lDACChannelUnitsIndex = `[7, 9, 11, 13, 15, 17, 19, 21]`
* lDACFileEpisodeNum = `[0, 0, 0, 0, 0, 0, 0, 0]`
* lDACFileNumEpisodes = `[0, 0, 0, 0, 0, 0, 0, 0]`
* lDACFilePathIndex = `[0, 0, 0, 0, 0, 0, 0, 0]`
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
* nPNNumPulses = `[4, 4, 4, 4, 4, 4, 4, 4]`
* nPNPolarity = `[1, 1, 1, 1, 1, 1, 1, 1]`
* nPNPosition = `[0, 0, 0, 0, 0, 0, 0, 0]`
* nTelegraphDACScaleFactorEnable = `[1, 0, 0, 0, 0, 0, 0, 0]`
* nWaveformEnable = `[1, 0, 0, 0, 0, 0, 0, 0]`
* nWaveformSource = `[1, 1, 1, 1, 0, 0, 0, 0]`

## EpochPerDACSection

> This section contains waveform protocol information. These are most of     the values set when using the epoch the waveform editor. Note that digital     output signals are not stored here, but are in EpochSection. 

* fEpochInitLevel = `[0.0, 0.0]`
* fEpochLevelInc = `[0.0, 0.0]`
* lEpochDurationInc = `[0, 0]`
* lEpochInitDuration = `[100000, 100000]`
* lEpochPulsePeriod = `[0, 2000]`
* lEpochPulseWidth = `[0, 40]`
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
* lADCUnits = `['mV']`
* lDACChannelName = `['Cmd 0', 'Cmd 1', 'Cmd 2', 'Cmd 3', 'AO #4', 'AO #5', 'AO #6', 'AO #7']`
* lDACChannelUnits = `['pA', 'mV', 'mV', 'mV', 'mV', 'mV', 'mV', 'mV']`
* lDACFilePath = `['', '', '', '', '', '', '', '']`
* lFileComment = `SWHLab5[0113]`
* nLeakSubtractADC = `['', '', '', '', '', '', '', '']`
* uCreatorName = `Clampex`
* uModifierName = ``
* uProtocolPath = `\\Spike\locked\Protocols\permanent\0504 opto [0] 10 Hz 2 ms (5s in 20s sweep).pro`
