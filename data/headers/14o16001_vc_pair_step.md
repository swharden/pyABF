# 14o16001_vc_pair_step.abf

## ABF Class Methods

* abf.launchInClampFit()
* abf.saveABF1()
* abf.setSweep()
* abf.sweepD()

## ABF Class Variables

* abfDateTime = `2014-10-16 10:01:35.078000`
* abfDateTimeString = `2014-10-16T10:01:35.078`
* abfFileComment = `SWH[MTIV]`
* abfFilePath = `C:/some/path/to/14o16001_vc_pair_step.abf`
* abfID = `14o16001_vc_pair_step`
* abfVersion = `{'major': 2, 'minor': 0, 'bugfix': 0, 'build': 0}`
* abfVersionString = `2.0.0.0`
* adcNames = `['IN 0', 'IN 1']`
* adcUnits = `['pA', 'pA']`
* channelCount = `2`
* channelList = `[0, 1]`
* creatorVersion = `{'major': 10, 'minor': 3, 'bugfix': 0, 'build': 2}`
* creatorVersionString = `10.3.0.2`
* dacNames = `['Cmd 0', 'Cmd 1']`
* dacUnits = `['mV', 'mV']`
* data = `array (2d) with values like: -25.87890, -27.09961, -26.73340, ..., -31.37207, -31.49414, -31.49414`
* dataByteStart = `6144`
* dataLengthMin = `0.9333333333333333`
* dataLengthSec = `56.0`
* dataPointByteSize = `2`
* dataPointCount = `1040000`
* dataPointsPerMs = `10`
* dataRate = `10000`
* dataSecPerPoint = `0.0001`
* fileGUID = `{7468FC35-C797-4101-8212-7E5BF83BF9F9}`
* holdingCommand = `[-70.0, -70.0, 0.0, 0.0]`
* protocol = `pair-MTIV`
* protocolPath = `X:\Protocols\Scott\SWHlab\paired\pair-MTIV.pro`
* stimulusByChannel = `[Stimulus(abf, 0), Stimulus(abf, 1)]`
* stimulusFileFolder = `C:/some/alternate/path`
* sweepC = `array (1d) with values like: -70.00000, -70.00000, -70.00000, ..., -70.00000, -70.00000, -70.00000`
* sweepChannel = `0`
* sweepCount = `13`
* sweepEpochs = `Sweep epoch waveform: Step -70.00 [0:625], Step -70.00 [625:2625], Step -80.00 [2625:4625], Step -70.00 [4625:9625], Step -110.00 [9625:14625], Step -70.00 [14625:19625], Step -50.00 [19625:24625], Step -110.00 [24625:29625], Step -50.00 [29625:34625], Step -70.00 [34625:40000]`
* sweepIntervalSec = `4.0`
* sweepLabelC = `Membrane Potential (mV)`
* sweepLabelX = `time (seconds)`
* sweepLabelY = `Clamp Current (pA)`
* sweepLengthSec = `4.0`
* sweepList = `[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]`
* sweepNumber = `0`
* sweepPointCount = `40000`
* sweepTimesMin = `array (1d) with values like: 0.00000, 0.06667, 0.13333, ..., 0.66667, 0.73333, 0.80000`
* sweepTimesSec = `array (1d) with values like: 0.00000, 4.00000, 8.00000, ..., 40.00000, 44.00000, 48.00000`
* sweepUnitsC = `mV`
* sweepUnitsX = `sec`
* sweepUnitsY = `pA`
* sweepX = `array (1d) with values like: 0.00000, 0.00010, 0.00020, ..., 3.99970, 3.99980, 3.99990`
* sweepY = `array (1d) with values like: -25.87890, -27.09961, -26.73340, ..., -30.27344, -33.44726, -34.54589`
* tagComments = `[]`
* tagSweeps = `[]`
* tagTimesMin = `[]`
* tagTimesSec = `[]`

## Epochs for Channel 0


```
                    EPOCH         A         B         C         D         E         F         G         H
                     Type      Step      Step      Step      Step      Step      Step      Step      Step
              First Level    -70.00    -80.00    -70.00   -110.00    -70.00    -50.00   -110.00    -50.00
              Delta Level      0.00      0.00      0.00      5.00      0.00      0.00      5.00      0.00
  First Duration (points)      2000      2000      5000      5000      5000      5000      5000      5000
  Delta Duration (points)         0         0         0         0         0         0         0         0
     Digital Pattern #3-0      1111      0000      0000      0000      0000      0000      0000      0000
     Digital Pattern #7-4      0000      0000      0000      0000      0000      0000      0000      0000
    Train Period (points)         0         0         0         0         0         0         0         0
     Pulse Width (points)         0         0         0         0         0         0         0         0
```

## Epochs for Channel 1


```

```

## ABF2 Header

> The first several bytes of an ABF2 file contain variables     located at specific byte positions from the start of the file. 

* abfDateTime = `2014-10-16 10:01:35.078000`
* abfDateTimeString = `2014-10-16T10:01:35.078`
* abfVersionDict = `{'major': 2, 'minor': 0, 'bugfix': 0, 'build': 0}`
* abfVersionFloat = `2.0`
* abfVersionString = `2.0.0.0`
* creatorVersionDict = `{'major': 10, 'minor': 3, 'bugfix': 0, 'build': 2}`
* creatorVersionFloat = `10.302`
* creatorVersionString = `10.3.0.2`
* fFileSignature = `ABF2`
* fFileVersionNumber = `[0, 0, 0, 2]`
* lActualEpisodes = `13`
* nCRCEnable = `0`
* nDataFormat = `0`
* nFileType = `1`
* nSimultaneousScan = `1`
* sFileGUID = `{7468FC35-C797-4101-8212-7E5BF83BF9F9}`
* uCreatorNameIndex = `1`
* uCreatorVersion = `[2, 0, 3, 10]`
* uFileCRC = `0`
* uFileGUID = `[53, 252, 104, 116, 151, 199, 1, 65, 130, 18, 126, 91, 248, 59, 63, 249]`
* uFileInfoSize = `512`
* uFileStartDate = `20141016`
* uFileStartTimeMS = `36095078`
* uModifierNameIndex = `0`
* uModifierVersion = `0`
* uProtocolPathIndex = `2`
* uStopwatchTime = `5561`

## SectionMap

> Reading three numbers (int, int, long) at specific byte locations     yields the block position, byte size, and item count of specific     data stored in sections. Note that a block is 512 bytes. Some of     these sections are not read by this class because they are either     not useful for my applications, typically unused, or have an     unknown memory structure. 

* ADCPerDACSection = `[0, 0, 0]`
* ADCSection = `[2, 128, 2]`
* AnnotationSection = `[0, 0, 0]`
* DACSection = `[3, 256, 4]`
* DataSection = `[12, 2, 1040000]`
* DeltaSection = `[0, 0, 0]`
* EpochPerDACSection = `[5, 48, 16]`
* EpochSection = `[7, 32, 8]`
* MathSection = `[0, 0, 0]`
* ProtocolSection = `[1, 512, 1]`
* ScopeSection = `[10, 769, 1]`
* StatsRegionSection = `[8, 128, 1]`
* StatsSection = `[0, 0, 0]`
* StringsSection = `[9, 161, 15]`
* SynchArraySection = `[4075, 8, 13]`
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
* fSecondsPerRun = `10.0`
* fStatisticsPeriod = `1.0`
* fSynchTimeUnit = `10.0`
* fTrialStartToStart = `0.0`
* fTriggerThreshold = `0.0`
* lADCResolution = `32768`
* lAverageCount = `1`
* lDACResolution = `32768`
* lEpisodesPerRun = `13`
* lFileCommentIndex = `3`
* lFinishDisplayNum = `40000`
* lNumSamplesPerEpisode = `80000`
* lNumberOfTrials = `1`
* lPreTriggerSamples = `40`
* lRunsPerTrial = `1`
* lSamplesPerTrace = `16384`
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

* bEnabledDuringPN = `[0, 0]`
* fADCDisplayAmplification = `[3.5555009841918945, 1.0]`
* fADCDisplayOffset = `[-75.0, 0.0]`
* fADCProgrammableGain = `[1.0, 1.0]`
* fInstrumentOffset = `[0.0, 0.0]`
* fInstrumentScaleFactor = `[0.0005000000237487257, 0.0005000000237487257]`
* fPostProcessLowpassFilter = `[100000.0, 100000.0]`
* fSignalGain = `[1.0, 1.0]`
* fSignalHighpassFilter = `[1.0, 1.0]`
* fSignalLowpassFilter = `[5000.0, 5000.0]`
* fSignalOffset = `[0.0, 0.0]`
* fTelegraphAccessResistance = `[0.0, 0.0]`
* fTelegraphAdditGain = `[5.0, 5.0]`
* fTelegraphFilter = `[2000.0, 2000.0]`
* fTelegraphMembraneCap = `[0.0, 0.0]`
* lADCChannelNameIndex = `[4, 6]`
* lADCUnitsIndex = `[5, 7]`
* nADCNum = `[0, 1]`
* nADCPtoLChannelMap = `[0, 1]`
* nADCSamplingSeq = `[0, 0]`
* nHighpassFilterType = `[0, 0]`
* nLowpassFilterType = `[0, 0]`
* nPostProcessLowpassFilterType = `['\x00', '\x00']`
* nStatsChannelPolarity = `[0, 0]`
* nTelegraphEnable = `[1, 1]`
* nTelegraphInstrument = `[24, 24]`
* nTelegraphMode = `[0, 0]`
* sTelegraphInstrument = `['MultiClamp 700', 'MultiClamp 700']`

## DACSection

> Information about the DAC (what gets clamped).     There is 1 item per DAC. 

* fBaselineDuration = `[1.0, 1.0, 1.0, 1.0]`
* fBaselineLevel = `[0.0, 0.0, 0.0, 0.0]`
* fDACCalibrationFactor = `[1.0008957386016846, 1.0010067224502563, 1.000895619392395, 1.0008400678634644]`
* fDACCalibrationOffset = `[0.0, -2.0, -3.0, 2.0]`
* fDACFileOffset = `[0.0, 0.0, 0.0, 0.0]`
* fDACFileScale = `[1.0, 1.0, 1.0, 1.0]`
* fDACHoldingLevel = `[-70.0, -70.0, 0.0, 0.0]`
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
* lDACChannelNameIndex = `[8, 10, 12, 14]`
* lDACChannelUnitsIndex = `[9, 11, 13, 15]`
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
* nTelegraphDACScaleFactorEnable = `[1, 1, 0, 0]`
* nWaveformEnable = `[1, 1, 0, 0]`
* nWaveformSource = `[1, 1, 1, 1]`

## EpochPerDACSection

> This section contains waveform protocol information. These are most of     the values set when using the epoch the waveform editor. Note that digital     output signals are not stored here, but are in EpochSection. 

* fEpochInitLevel = `[-70.0, -80.0, -70.0, -110.0, -70.0, -50.0, -110.0, -50.0, -70.0, -80.0, -70.0, -110.0, -70.0, -50.0, -110.0, -50.0]`
* fEpochLevelInc = `[0.0, 0.0, 0.0, 5.0, 0.0, 0.0, 5.0, 0.0, 0.0, 0.0, 0.0, 5.0, 0.0, 0.0, 5.0, 0.0]`
* lEpochDurationInc = `[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]`
* lEpochInitDuration = `[2000, 2000, 5000, 5000, 5000, 5000, 5000, 5000, 2000, 2000, 5000, 5000, 5000, 5000, 5000, 5000]`
* lEpochPulsePeriod = `[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]`
* lEpochPulseWidth = `[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]`
* nDACNum = `[0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1]`
* nEpochNum = `[0, 1, 2, 3, 4, 5, 6, 7, 0, 1, 2, 3, 4, 5, 6, 7]`
* nEpochType = `[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]`

## EpochSection

> This section contains the digital output signals for each epoch. This     section has been overlooked by some previous open-source ABF-reading     projects. Note that the digital output is a single byte, but represents     8 bits corresponding to 8 outputs (7->0). When working with these bits,     I convert it to a string like "10011101" for easy eyeballing. 

* nEpochDigitalOutput = `[15, 0, 0, 0, 0, 0, 0, 0]`
* nEpochNum = `[0, 1, 2, 3, 4, 5, 6, 7]`

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

* lADCChannelName = `['IN 0', 'IN 1']`
* lADCUnits = `['pA', 'pA']`
* lDACChannelName = `['Cmd 0', 'Cmd 1', 'Cmd 2', 'Cmd 3']`
* lDACChannelUnits = `['mV', 'mV', 'mV', 'mV']`
* lDACFilePath = `['', '', '', '']`
* lFileComment = `SWH[MTIV]`
* nLeakSubtractADC = `['', '', '', '']`
* uCreatorName = `Clampex`
* uModifierName = ``
* uProtocolPath = `X:\Protocols\Scott\SWHlab\paired\pair-MTIV.pro`
