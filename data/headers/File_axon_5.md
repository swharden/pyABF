# File_axon_5.abf

## ABF Class Methods

* abf.launchInClampFit()
* abf.saveABF1()
* abf.setSweep()
* abf.sweepD()

## ABF Class Variables

* abfDateTime = `2007-02-09 12:54:55.828000`
* abfDateTimeString = `2007-02-09T12:54:55.828`
* abfFileComment = ``
* abfFilePath = `C:/some/path/to/File_axon_5.abf`
* abfID = `File_axon_5`
* abfVersion = `{'major': 2, 'minor': 0, 'bugfix': 0, 'build': 0}`
* abfVersionString = `2.0.0.0`
* adcNames = `['_Ipatch']`
* adcUnits = `['mV']`
* channelCount = `1`
* channelList = `[0]`
* creatorVersion = `{'major': 10, 'minor': 1, 'bugfix': 0, 'build': 7}`
* creatorVersionString = `10.1.0.7`
* dacNames = `['Cmd 0']`
* dacUnits = `['pA']`
* data = `array (2d) with values like: -71.05103, -71.05713, -71.05103, ..., -74.92065, -74.92676, -74.93286`
* dataByteStart = `5632`
* dataLengthMin = `0.7666666666666667`
* dataLengthSec = `46.0`
* dataPointByteSize = `2`
* dataPointCount = `180000`
* dataPointsPerMs = `20`
* dataRate = `20000`
* dataSecPerPoint = `5e-05`
* fileGUID = `{8F92BF12-A392-4FCF-9C94-47C4F08FD2D2}`
* holdingCommand = `[0.0, 0.0, 0.0, 0.0]`
* protocol = `step cclamp`
* protocolPath = `C:\Axon\Params\step cclamp.pro`
* stimulusByChannel = `[Stimulus(abf, 0)]`
* stimulusFileFolder = `C:/some/alternate/path`
* sweepC = `array (1d) with values like: 0.00000, 0.00000, 0.00000, ..., 0.00000, 0.00000, 0.00000`
* sweepChannel = `0`
* sweepCount = `9`
* sweepEpochs = `Sweep epoch waveform: Step 0.00 [0:312], Step 0.00 [312:4312], Step -100.00 [4312:14312], Step 0.00 [14312:18312], Step 0.00 [18312:20000]`
* sweepIntervalSec = `5.0`
* sweepLabelC = `Applied Current (pA)`
* sweepLabelX = `time (seconds)`
* sweepLabelY = `Membrane Potential (mV)`
* sweepLengthSec = `1.0`
* sweepList = `[0, 1, 2, 3, 4, 5, 6, 7, 8]`
* sweepNumber = `0`
* sweepPointCount = `20000`
* sweepTimesMin = `array (1d) with values like: 0.00000, 0.08333, 0.16667, 0.25000, 0.33333, 0.41667, 0.50000, 0.58333, 0.66667`
* sweepTimesSec = `array (1d) with values like: 0.00000, 5.00000, 10.00000, 15.00000, 20.00000, 25.00000, 30.00000, 35.00000, 40.00000`
* sweepUnitsC = `pA`
* sweepUnitsX = `sec`
* sweepUnitsY = `mV`
* sweepX = `array (1d) with values like: 0.00000, 0.00005, 0.00010, ..., 0.99985, 0.99990, 0.99995`
* sweepY = `array (1d) with values like: -71.05103, -71.05713, -71.05103, ..., -70.17212, -70.17212, -70.19043`
* tagComments = `[]`
* tagSweeps = `[]`
* tagTimesMin = `[]`
* tagTimesSec = `[]`

## Epochs for Channel 0


```
                    EPOCH         A         B         C
                     Type      Step      Step      Step
              First Level      0.00   -100.00      0.00
              Delta Level      0.00     50.00      0.00
  First Duration (points)      4000     10000      4000
  Delta Duration (points)         0         0         0
     Digital Pattern #3-0      1111      0000      0000
     Digital Pattern #7-4      0000      0000      0000
    Train Period (points)         0         0         0
     Pulse Width (points)         0         0         0
```

## ABF2 Header

> The first several bytes of an ABF2 file contain variables     located at specific byte positions from the start of the file. 

* abfDateTime = `2007-02-09 12:54:55.828000`
* abfDateTimeString = `2007-02-09T12:54:55.828`
* abfVersionDict = `{'major': 2, 'minor': 0, 'bugfix': 0, 'build': 0}`
* abfVersionFloat = `2.0`
* abfVersionString = `2.0.0.0`
* creatorVersionDict = `{'major': 10, 'minor': 1, 'bugfix': 0, 'build': 7}`
* creatorVersionFloat = `10.107`
* creatorVersionString = `10.1.0.7`
* fFileSignature = `ABF2`
* fFileVersionNumber = `[0, 0, 0, 2]`
* lActualEpisodes = `9`
* nCRCEnable = `0`
* nDataFormat = `0`
* nFileType = `1`
* nSimultaneousScan = `1`
* sFileGUID = `{8F92BF12-A392-4FCF-9C94-47C4F08FD2D2}`
* uCreatorNameIndex = `1`
* uCreatorVersion = `[7, 0, 1, 10]`
* uFileCRC = `0`
* uFileGUID = `[18, 191, 146, 143, 146, 163, 207, 79, 156, 148, 71, 196, 240, 143, 34, 210]`
* uFileInfoSize = `512`
* uFileStartDate = `20070209`
* uFileStartTimeMS = `46495828`
* uModifierNameIndex = `0`
* uModifierVersion = `0`
* uProtocolPathIndex = `2`
* uStopwatchTime = `1550460`

## SectionMap

> Reading three numbers (int, int, long) at specific byte locations     yields the block position, byte size, and item count of specific     data stored in sections. Note that a block is 512 bytes. Some of     these sections are not read by this class because they are either     not useful for my applications, typically unused, or have an     unknown memory structure. 

* ADCPerDACSection = `[0, 0, 0]`
* ADCSection = `[2, 128, 1]`
* AnnotationSection = `[0, 0, 0]`
* DACSection = `[3, 256, 4]`
* DataSection = `[11, 2, 180000]`
* DeltaSection = `[0, 0, 0]`
* EpochPerDACSection = `[5, 48, 3]`
* EpochSection = `[6, 32, 3]`
* MathSection = `[0, 0, 0]`
* ProtocolSection = `[1, 512, 1]`
* ScopeSection = `[9, 769, 1]`
* StatsRegionSection = `[7, 128, 1]`
* StatsSection = `[0, 0, 0]`
* StringsSection = `[8, 130, 12]`
* SynchArraySection = `[715, 8, 9]`
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
* fEpisodeStartToStart = `5.0`
* fFirstRunDelayS = `0.0`
* fRunStartToStart = `0.0`
* fScopeOutputInterval = `0.0`
* fSecondsPerRun = `10.0`
* fStatisticsPeriod = `1.0`
* fSynchTimeUnit = `12.5`
* fTrialStartToStart = `0.0`
* fTriggerThreshold = `0.0`
* lADCResolution = `32768`
* lAverageCount = `1`
* lDACResolution = `32768`
* lEpisodesPerRun = `9`
* lFileCommentIndex = `0`
* lFinishDisplayNum = `20000`
* lNumSamplesPerEpisode = `20000`
* lNumberOfTrials = `1`
* lPreTriggerSamples = `40`
* lRunsPerTrial = `1`
* lSamplesPerTrace = `16384`
* lStartDisplayNum = `0`
* lStatisticsMeasurements = `5`
* lTimeHysteresis = `2`
* nActiveDACChannel = `0`
* nAllowExternalTags = `0`
* nAlternateDACOutputState = `0`
* nAlternateDigitalOutputState = `0`
* nAutoAnalyseEnable = `1`
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
* nDigitizerDACs = `4`
* nDigitizerSynchDigitalOuts = `8`
* nDigitizerTotalDigitalOuts = `16`
* nDigitizerType = `6`
* nExperimentType = `2`
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
* sDigitizerType = `Digidata 1440`
* sUnused = `['\x00', '\x00', '\x00']`
* uFileCompressionRatio = `1`

## ADCSection

> Information about the ADC (what gets recorded).     There is 1 item per ADC. 

* bEnabledDuringPN = `[1]`
* fADCDisplayAmplification = `[3.8094658851623535]`
* fADCDisplayOffset = `[-19.0]`
* fADCProgrammableGain = `[1.0]`
* fInstrumentOffset = `[0.0]`
* fInstrumentScaleFactor = `[0.009999999776482582]`
* fPostProcessLowpassFilter = `[100000.0]`
* fSignalGain = `[1.0]`
* fSignalHighpassFilter = `[1.0]`
* fSignalLowpassFilter = `[5000.0]`
* fSignalOffset = `[0.0]`
* fTelegraphAccessResistance = `[0.0]`
* fTelegraphAdditGain = `[5.0]`
* fTelegraphFilter = `[3000.0]`
* fTelegraphMembraneCap = `[0.0]`
* lADCChannelNameIndex = `[3]`
* lADCUnitsIndex = `[4]`
* nADCNum = `[0]`
* nADCPtoLChannelMap = `[0]`
* nADCSamplingSeq = `[0]`
* nHighpassFilterType = `[0]`
* nLowpassFilterType = `[0]`
* nPostProcessLowpassFilterType = `['\x00']`
* nStatsChannelPolarity = `[0]`
* nTelegraphEnable = `[1]`
* nTelegraphInstrument = `[24]`
* nTelegraphMode = `[1]`
* sTelegraphInstrument = `['MultiClamp 700']`

## DACSection

> Information about the DAC (what gets clamped).     There is 1 item per DAC. 

* fBaselineDuration = `[1.0, 1.0, 1.0, 1.0]`
* fBaselineLevel = `[0.0, 0.0, 0.0, 0.0]`
* fDACCalibrationFactor = `[0.9988833665847778, 0.9988833665847778, 0.9988833665847778, 0.9988833665847778]`
* fDACCalibrationOffset = `[0.0, 0.0, -3.0, -6.0]`
* fDACFileOffset = `[0.0, 0.0, 0.0, 0.0]`
* fDACFileScale = `[1.0, 1.0, 1.0, 1.0]`
* fDACHoldingLevel = `[0.0, 0.0, 0.0, 0.0]`
* fDACScaleFactor = `[400.0, 20.0, 20.0, 20.0]`
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
* lDACChannelNameIndex = `[5, 7, 9, 11]`
* lDACChannelUnitsIndex = `[6, 8, 10, 12]`
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
* nLeakSubtractADCIndex = `[0, 0, 0, 0]`
* nLeakSubtractType = `[0, 0, 0, 0]`
* nMembTestEnable = `[0, 0, 0, 0]`
* nPNNumADCChannels = `[0, 0, 0, 0]`
* nPNNumPulses = `[4, 4, 4, 4]`
* nPNPolarity = `[1, 1, 1, 1]`
* nPNPosition = `[0, 0, 0, 0]`
* nTelegraphDACScaleFactorEnable = `[1, 0, 0, 0]`
* nWaveformEnable = `[1, 0, 0, 0]`
* nWaveformSource = `[1, 1, 1, 1]`

## EpochPerDACSection

> This section contains waveform protocol information. These are most of     the values set when using the epoch the waveform editor. Note that digital     output signals are not stored here, but are in EpochSection. 

* fEpochInitLevel = `[0.0, -100.0, 0.0]`
* fEpochLevelInc = `[0.0, 50.0, 0.0]`
* lEpochDurationInc = `[0, 0, 0]`
* lEpochInitDuration = `[4000, 10000, 4000]`
* lEpochPulsePeriod = `[0, 0, 0]`
* lEpochPulseWidth = `[0, 0, 0]`
* nDACNum = `[0, 0, 0]`
* nEpochNum = `[0, 1, 2]`
* nEpochType = `[1, 1, 1]`

## EpochSection

> This section contains the digital output signals for each epoch. This     section has been overlooked by some previous open-source ABF-reading     projects. Note that the digital output is a single byte, but represents     8 bits corresponding to 8 outputs (7->0). When working with these bits,     I convert it to a string like "10011101" for easy eyeballing. 

* nEpochDigitalOutput = `[15, 0, 0]`
* nEpochNum = `[0, 1, 2]`

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

* lADCChannelName = `['_Ipatch']`
* lADCUnits = `['mV']`
* lDACChannelName = `['Cmd 0', 'Cmd 1', 'Cmd 2', 'Cmd 3']`
* lDACChannelUnits = `['pA', 'mV', 'mV', 'mV']`
* lDACFilePath = `['', '', '', '']`
* lFileComment = ``
* nLeakSubtractADC = `['', '', '', '']`
* uCreatorName = `clampex`
* uModifierName = ``
* uProtocolPath = `C:\Axon\Params\step cclamp.pro`
