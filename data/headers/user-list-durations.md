# user-list-durations.abf

## ABF Class Methods

* abf.launchInClampFit()
* abf.saveABF1()
* abf.setSweep()
* abf.sweepD()

## ABF Class Variables

* abfDateTime = `2020-12-03 14:13:03.760000`
* abfDateTimeString = `2020-12-03T14:13:03.760`
* abfFileComment = ``
* abfFilePath = `C:/some/path/to/user-list-durations.abf`
* abfFolderPath = `C:/some/path`
* abfID = `user-list-durations`
* abfVersion = `{'major': 2, 'minor': 0, 'bugfix': 0, 'build': 0}`
* abfVersionString = `2.0.0.0`
* adcNames = `['IN 0', 'AO #0']`
* adcUnits = `['pA', 'mV']`
* channelCount = `2`
* channelList = `[0, 1]`
* creator = `AXENGN 2.0.1.69 0.0.0.0`
* creatorVersion = `{'major': 0, 'minor': 0, 'bugfix': 0, 'build': 0}`
* creatorVersionString = `0.0.0.0`
* dacNames = `['Cmd 0', 'Cmd 1']`
* dacUnits = `['mV', 'mV']`
* data = `array (2d) with values like: -69.68749, -44.68750, -54.68750, ..., -35.00000, -35.00000, -35.00000`
* dataByteStart = `5120`
* dataLengthMin = `2.1801000000000004`
* dataLengthSec = `130.806`
* dataPointByteSize = `4`
* dataPointCount = `309672`
* dataPointsPerMs = `2`
* dataRate = `2000`
* dataSecPerPoint = `0.0005`
* fileGUID = `8AD87A5D-AD26-4C0E-86CC-BDD1AFAA8A3C`
* fileUUID = `9B6F89BD-92E4-AB44-2D1F-4921627117CA`
* holdingCommand = `[-35.0, -35.0, 0.0, 0.0]`
* md5 = `9B6F89BD92E4AB442D1F4921627117CA`
* nOperationMode = `5`
* protocol = `WT_act with ramp_reversed_env`
* protocolPath = `C:\Delbert\Protocols\HCN2\WT_mHCN2\new_staggered\WT_act with ramp_reversed_env.pro`
* stimulusByChannel = `[Stimulus(abf, 0), Stimulus(abf, 1)]`
* stimulusFileFolder = `C:/some/path/to/user-list-durations.abf`
* sweepC = `array (1d) with values like: -35.00000, -35.00000, -35.00000, ..., -35.00000, -35.00000, -35.00000`
* sweepChannel = `0`
* sweepCount = `3`
* sweepDerivative = `array (1d) with values like: 49999.99219, -20000.00000, 0.00000, ..., -29999.99219, 19999.99219, 19999.99219`
* sweepEpochs = `Sweep epoch waveform: Step -35.00 [0:806], Step -35.00 [806:1806], Ramp 30.00 [1806:2806], Ramp -35.00 [2806:3806], Step -35.00 [3806:4806], Step -145.00 [4806:7306], Step -145.00 [7306:8506], Step 0.00 [8506:14506], Step -35.00 [14506:15506], Ramp 30.00 [15506:16506], Ramp -35.00 [16506:17506], Step -35.00 [17506:51612]`
* sweepIntervalSec = `35.0`
* sweepLabelC = `Membrane Potential (mV)`
* sweepLabelD = `Digital Output (V)`
* sweepLabelX = `Time (seconds)`
* sweepLabelY = `Clamp Current (pA)`
* sweepLengthSec = `25.806`
* sweepList = `[0, 1, 2]`
* sweepNumber = `0`
* sweepPointCount = `51612`
* sweepTimesMin = `array (1d) with values like: 0.00000, 0.58333, 1.16667`
* sweepTimesSec = `array (1d) with values like: 0.00000, 35.00000, 70.00000`
* sweepUnitsC = `mV`
* sweepUnitsX = `sec`
* sweepUnitsY = `pA`
* sweepX = `array (1d) with values like: 0.00000, 0.00050, 0.00100, ..., 25.80450, 25.80500, 25.80550`
* sweepY = `array (1d) with values like: -69.68749, -44.68750, -54.68750, ..., -49.68750, -64.68749, -54.68750`
* tagComments = `[]`
* tagSweeps = `[]`
* tagTimesMin = `[]`
* tagTimesSec = `[]`
* userList = `[4000.0, 6000.0, 6000.0, 10000.0, 20000.0, 30000.0, 30000.0, 30000.0, 30000.0]`
* userListEnable = `[1]`
* userListParamToVary = `[35]`
* userListParamToVaryName = `['EPOCHINITLEVEL']`
* userListRepeat = `[0]`

## Epochs for Channel 0


```
                    EPOCH         A         B         C         D         E         F         G         H         I         J
                     Type      Step      Ramp      Ramp      Step      Step      Step      Step      Step      Ramp      Ramp
              First Level    -35.00     30.00    -35.00    -35.00   -145.00   -145.00      0.00    -35.00     30.00    -35.00
              Delta Level      0.00      0.00      0.00      0.00     15.00      0.00      0.00      0.00      0.00      0.00
  First Duration (points)      1000      1000      1000      1000      2500      1200      6000      1000      1000      1000
  Delta Duration (points)         0         0         0         0         0         0         0         0         0         0
     Digital Pattern #3-0      1111      1000      0000      0000      0000      0000      0000      0000      0000      0000
     Digital Pattern #7-4      0000      0000      0000      0000      0000      0000      0000      0000      0000      0000
    Train Period (points)         0         0         0         0         0         0         0         0         0         0
     Pulse Width (points)         0         0         0         0         0         0         0         0         0         0
```

## Epochs for Channel 1


```

```

## ABF2 Header

> The first several bytes of an ABF2 file contain variables     located at specific byte positions from the start of the file. 

* abfDateTime = `2020-12-03 14:13:03.760000`
* abfDateTimeString = `2020-12-03T14:13:03.760`
* abfVersionDict = `{'major': 2, 'minor': 0, 'bugfix': 0, 'build': 0}`
* abfVersionFloat = `2.0`
* abfVersionString = `2.0.0.0`
* creatorVersionDict = `{'major': 0, 'minor': 0, 'bugfix': 0, 'build': 0}`
* creatorVersionFloat = `0.0`
* creatorVersionString = `0.0.0.0`
* fFileVersionNumber = `[0, 0, 0, 2]`
* lActualEpisodes = `3`
* nCRCEnable = `0`
* nDataFormat = `1`
* nFileType = `1`
* nSimultaneousScan = `0`
* sFileGUID = `8AD87A5D-AD26-4C0E-86CC-BDD1AFAA8A3C`
* sFileSignature = `ABF2`
* uCreatorNameIndex = `1`
* uCreatorVersion = `[0, 0, 0, 0]`
* uFileCRC = `0`
* uFileGUID = `[93, 122, 216, 138, 38, 173, 14, 76, 134, 204, 189, 209, 175, 170, 138, 60]`
* uFileInfoSize = `512`
* uFileStartDate = `20201203`
* uFileStartTimeMS = `51183760`
* uModifierNameIndex = `2`
* uModifierVersion = `167903250`
* uProtocolPathIndex = `3`
* uStopwatchTime = `5299`

## SectionMap

> Reading three numbers (int, int, long) at specific byte locations     yields the block position, byte size, and item count of specific     data stored in sections. Note that a block is 512 bytes. Some of     these sections are not read by this class because they are either     not useful for my applications, typically unused, or have an     unknown memory structure. 

* ADCPerDACSection = `[0, 0, 0]`
* ADCSection = `[2, 128, 2]`
* AnnotationSection = `[0, 0, 0]`
* DACSection = `[3, 256, 4]`
* DataSection = `[10, 4, 309672]`
* DeltaSection = `[0, 0, 0]`
* EpochPerDACSection = `[5, 48, 10]`
* EpochSection = `[6, 32, 10]`
* MathSection = `[0, 0, 0]`
* ProtocolSection = `[1, 512, 1]`
* ScopeSection = `[0, 0, 0]`
* StatsRegionSection = `[7, 128, 1]`
* StatsSection = `[0, 0, 0]`
* StringsSection = `[9, 264, 16]`
* SynchArraySection = `[2430, 8, 3]`
* TagSection = `[0, 0, 0]`
* UserListSection = `[8, 64, 1]`
* VoiceTagSection = `[0, 0, 0]`

## ProtocolSection

> This section contains information about the recording settings.     This is useful for determining things like sample rate and     channel scaling factors. 

* bEnableFileCompression = `0`
* fADCRange = `10.239999771118164`
* fADCSequenceInterval = `500.0`
* fAverageWeighting = `0.10000000149011612`
* fCellID = `[0.0, 0.0, 0.0]`
* fDACRange = `10.239999771118164`
* fEpisodeStartToStart = `35.0`
* fFirstRunDelayS = `0.0`
* fRunStartToStart = `0.0`
* fScopeOutputInterval = `0.0`
* fSecondsPerRun = `0.0`
* fStatisticsPeriod = `1.0`
* fSynchTimeUnit = `25.0`
* fTrialStartToStart = `0.0`
* fTriggerThreshold = `0.0`
* lADCResolution = `32768`
* lAverageCount = `1`
* lDACResolution = `32768`
* lEpisodesPerRun = `3`
* lFileCommentIndex = `0`
* lFinishDisplayNum = `0`
* lNumSamplesPerEpisode = `103224`
* lNumberOfTrials = `1`
* lPreTriggerSamples = `32`
* lRunsPerTrial = `1`
* lSamplesPerTrace = `16384`
* lStartDisplayNum = `1`
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
* nCommentsEnable = `0`
* nDigitalDACChannel = `0`
* nDigitalEnable = `0`
* nDigitalHolding = `0`
* nDigitalInterEpisode = `0`
* nDigitalTrainActiveLogic = `0`
* nDigitizerADCs = `16`
* nDigitizerDACs = `2`
* nDigitizerSynchDigitalOuts = `4`
* nDigitizerTotalDigitalOuts = `8`
* nDigitizerType = `1`
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
* sDigitizerType = `Demo`
* uFileCompressionRatio = `1`

## ADCSection

> Information about the ADC (what gets recorded).     There is 1 item per ADC. 

* bEnabledDuringPN = `[0, 0]`
* fADCDisplayAmplification = `[5.251201629638672, 1.0]`
* fADCDisplayOffset = `[-1050.0, 0.0]`
* fADCProgrammableGain = `[1.0, 1.0]`
* fInstrumentOffset = `[0.0, 0.0]`
* fInstrumentScaleFactor = `[0.0010000000474974513, 0.05000000074505806]`
* fPostProcessLowpassFilter = `[100000.0, 100000.0]`
* fSignalGain = `[1.0, 1.0]`
* fSignalHighpassFilter = `[1.0, 1.0]`
* fSignalLowpassFilter = `[1000.0, 10000.0]`
* fSignalOffset = `[0.0, 0.0]`
* fTelegraphAccessResistance = `[0.0, 0.0]`
* fTelegraphAdditGain = `[1.0, 0.0]`
* fTelegraphFilter = `[10000.0, 0.0]`
* fTelegraphMembraneCap = `[11.60312557220459, 0.0]`
* lADCChannelNameIndex = `[4, 6]`
* lADCUnitsIndex = `[5, 7]`
* nADCNum = `[0, 1]`
* nADCPtoLChannelMap = `[0, 1]`
* nADCSamplingSeq = `[0, 0]`
* nHighpassFilterType = `[0, 0]`
* nLowpassFilterType = `[0, 0]`
* nPostProcessLowpassFilterType = `['\x00', '\x00']`
* nStatsChannelPolarity = `[0, 0]`
* nTelegraphEnable = `[1, 0]`
* nTelegraphInstrument = `[15, 0]`
* nTelegraphMode = `[0, 0]`
* sTelegraphInstrument = `['Axopatch 200B', 'Unknown instrument (manual or user defined telegraph table).']`

## DACSection

> Information about the DAC (what gets clamped).     There is 1 item per DAC. 

* fBaselineDuration = `[0.009999999776482582, 0.0, 0.0, 0.0]`
* fBaselineLevel = `[0.0, 0.0, 0.0, 0.0]`
* fDACCalibrationFactor = `[1.0, 1.0, 1.0, 1.0]`
* fDACCalibrationOffset = `[0.0, 0.0, 0.0, 0.0]`
* fDACFileOffset = `[0.0, 0.0, 0.0, 0.0]`
* fDACFileScale = `[1.0, 0.0, 1.0, 1.0]`
* fDACHoldingLevel = `[-35.0, -35.0, 0.0, 0.0]`
* fDACScaleFactor = `[20.0, 20.0, 20.0, 20.0]`
* fInstrumentHoldingLevel = `[0.0, 0.0, 0.0, 0.0]`
* fMembTestPostSettlingTimeMS = `[100.0, 100.0, 100.0, 100.0]`
* fMembTestPreSettlingTimeMS = `[100.0, 100.0, 100.0, 100.0]`
* fPNHoldingLevel = `[0.0, 0.0, 0.0, 0.0]`
* fPNInterpulse = `[0.0, 0.0, 0.0, 0.0]`
* fPNSettlingTime = `[0.0, 0.0, 0.0, 0.0]`
* fPostTrainLevel = `[0.0, 0.0, 0.0, 0.0]`
* fPostTrainPeriod = `[0.0, 0.0, 10.0, 10.0]`
* fStepDuration = `[0.009999999776482582, 0.0, 0.0, 0.0]`
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
* nPNNumPulses = `[2, 2, 2, 2]`
* nPNPolarity = `[1, 1, 1, 1]`
* nPNPosition = `[0, 0, 0, 0]`
* nTelegraphDACScaleFactorEnable = `[0, 0, 0, 0]`
* nWaveformEnable = `[1, 0, 0, 0]`
* nWaveformSource = `[1, 1, 0, 0]`

## EpochPerDACSection

> This section contains waveform protocol information. These are most of     the values set when using the epoch the waveform editor. Note that digital     output signals are not stored here, but are in EpochSection. 

* fEpochInitLevel = `[-35.0, 30.0, -35.0, -35.0, -145.0, -145.0, 0.0, -35.0, 30.0, -35.0]`
* fEpochLevelInc = `[0.0, 0.0, 0.0, 0.0, 15.0, 0.0, 0.0, 0.0, 0.0, 0.0]`
* lEpochDurationInc = `[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]`
* lEpochInitDuration = `[1000, 1000, 1000, 1000, 2500, 1200, 6000, 1000, 1000, 1000]`
* lEpochPulsePeriod = `[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]`
* lEpochPulseWidth = `[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]`
* nDACNum = `[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]`
* nEpochNum = `[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]`
* nEpochType = `[1, 2, 2, 1, 1, 1, 1, 1, 2, 2]`

## EpochSection

> This section contains the digital output signals for each epoch. This     section has been overlooked by some previous open-source ABF-reading     projects. Note that the digital output is a single byte, but represents     8 bits corresponding to 8 outputs (7->0). When working with these bits,     I convert it to a string like "10011101" for easy eyeballing. 

* nEpochDigitalOutput = `[15, 1, 0, 0, 0, 0, 0, 0, 0, 0]`
* nEpochNum = `[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]`

## TagSection

> Tags are comments placed in ABF files during the recording. Physically     they are located at the end of the file (after the data).      Later we will populate the times and sweeps (human-understandable units)     by multiplying the lTagTime by fSynchTimeUnit from the protocol section. 

* lTagTime = `[]`
* nTagType = `[]`
* nVoiceTagNumberorAnnotationIndex = `[]`
* sComment = `[]`
* sweeps = `[]`
* timesMin = `[]`
* timesSec = `[]`

## SynchArraySection

> Contains start time (in fSynchTimeUnit units) and length (in      multiplexed samples) of each portion of the data if the data      are not part of a continuous gap-free acquisition. 

* lLength = `[103224, 103224, 103224]`
* lStart = `[0, 1400000, 2800000]`

## StringsSection

> Part of the ABF file contains long strings. Some of these can be broken     apart into indexed strings.      The first string is the only one which seems to contain useful information.     This contains information like channel names, channel units, and abf     protocol path and comments. The other strings are very large and I do not     know what they do.      Strings which contain indexed substrings are separated by \x00 characters. 

* strings = `not shown due to non-ASCII characters`
