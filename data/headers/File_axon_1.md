# File_axon_1.abf

## ABF Class Methods

* abf.getInfoPage()
* abf.setSweep()
* abf.sweepArea()
* abf.sweepAvg()
* abf.sweepBaseline()
* abf.sweepD()
* abf.sweepMax()
* abf.sweepMin()
* abf.sweepStdev()

## ABF Class Variables

* abfDateTime = `2008-04-28 14:47:33.262000`
* abfDateTimeString = `2008-04-28T14:47:33.262000`
* abfFileComment = ``
* abfFilePath = `c:\Users\scott\Documents\GitHub\pyABF\data\abfs\File_axon_1.abf`
* abfID = `File_axon_1`
* abfVersion = `{'major': 2, 'minor': 0, 'bugfix': 0, 'build': 0}`
* abfVersionString = `2.0.0.0`
* adcNames = `['ImRK01G20']`
* adcUnits = `['pA']`
* channelCount = `1`
* channelList = `[0]`
* creatorVersion = `{'major': 10, 'minor': 0, 'bugfix': 0, 'build': 61}`
* creatorVersionString = `10.0.0.61`
* dacNames = `['Iimp RK01']`
* dacUnits = `['nA']`
* data = `[[ 2.18811035  2.19726562  2.21252441 ...,  1.33056641  1.3458252    1.3671875 ]]`
* dataByteStart = `4608`
* dataPointByteSize = `2`
* dataPointCount = `1912832`
* dataPointsPerMs = `10`
* dataRate = `10000`
* dataSecPerPoint = `0.0001`
* epochPoints = `[0, 29888, 1912832]`
* epochValues = `[0.0, 0.0, 0.0]`
* fileGUID = `{F182D298-AB6D-4149-970B-AE3BCB5EEDED}`
* holdingCommand = `[0.0, 0.0, 0.0, 0.0]`
* protocol = `VC_cour01G20`
* protocolPath = `C:\MANIPS\PROTOCOLES AMPLI\rk400\0.1 G Brigitte\AS\VC_cour01G20.pro`
* stimulusByChannel = `[ChannelEpochs(ABF, 0)]`
* sweepC = `[ nan  nan  nan ...,  nan  nan  nan]`
* sweepChannel = `0`
* sweepCount = `1`
* sweepLabelC = `Membrane Potential (mV)`
* sweepLabelX = `time (seconds)`
* sweepLabelY = `Clamp Current (pA)`
* sweepLengthSec = `191.2832`
* sweepList = `[0]`
* sweepNumber = `0`
* sweepPointCount = `1912832`
* sweepUnitsC = `nA`
* sweepUnitsX = `sec`
* sweepUnitsY = `pA`
* sweepX = `[  0.00000000e+00   1.00000000e-04   2.00000000e-04 ...,   1.91282900e+02    1.91283000e+02   1.91283100e+02]`
* sweepY = `[ 2.18811035  2.19726562  2.21252441 ...,  1.33056641  1.3458252   1.3671875 ]`
* tagComments = `[]`
* tagSweeps = `[]`
* tagTimesMin = `[]`
* tagTimesSec = `[]`

## Epochs for Channel 0


```
DAC waveform is not enabled.
```

## ABF2 Header

> The first several bytes of an ABF2 file contain variables     located at specific byte positions from the start of the file. 

* abfDateTime = `2008-04-28 14:47:33.262000`
* abfDateTimeString = `2008-04-28T14:47:33.262000`
* abfVersionDict = `{'major': 2, 'minor': 0, 'bugfix': 0, 'build': 0}`
* abfVersionFloat = `2.0`
* abfVersionString = `2.0.0.0`
* creatorVersionDict = `{'major': 10, 'minor': 0, 'bugfix': 0, 'build': 61}`
* creatorVersionFloat = `100.061`
* creatorVersionString = `10.0.0.61`
* fFileSignature = `ABF2`
* fFileVersionNumber = `[0, 0, 0, 2]`
* lActualEpisodes = `0`
* nCRCEnable = `0`
* nDataFormat = `0`
* nFileType = `1`
* nSimultaneousScan = `1`
* sFileGUID = `{F182D298-AB6D-4149-970B-AE3BCB5EEDED}`
* uCreatorNameIndex = `1`
* uCreatorVersion = `[61, 0, 0, 10]`
* uFileCRC = `0`
* uFileGUID = `[152, 210, 130, 241, 109, 171, 73, 65, 151, 11, 174, 59, 203, 94, 172, 237]`
* uFileInfoSize = `512`
* uFileStartDate = `20080428`
* uFileStartTimeMS = `53253262`
* uModifierNameIndex = `0`
* uModifierVersion = `0`
* uProtocolPathIndex = `2`
* uStopwatchTime = `1903`

## SectionMap

> Reading three numbers (int, int, long) at specific byte locations     yields the block position, byte size, and item count of specific     data stored in sections. Note that a block is 512 bytes. Some of     these sections are not read by this class because they are either     not useful for my applications, typically unused, or have an     unknown memory structure. 

* ADCPerDACSection = `[0, 0, 0]`
* ADCSection = `[2, 128, 1]`
* AnnotationSection = `[0, 0, 0]`
* DACSection = `[3, 256, 4]`
* DataSection = `[9, 2, 1912832]`
* DeltaSection = `[0, 0, 0]`
* EpochPerDACSection = `[0, 0, 0]`
* EpochSection = `[0, 0, 0]`
* MathSection = `[0, 0, 0]`
* ProtocolSection = `[1, 512, 1]`
* ScopeSection = `[7, 769, 1]`
* StatsRegionSection = `[5, 128, 1]`
* StatsSection = `[0, 0, 0]`
* StringsSection = `[6, 176, 12]`
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
* fSecondsPerRun = `1200.0`
* fStatisticsPeriod = `0.5`
* fSynchTimeUnit = `0.0`
* fTrialStartToStart = `0.0`
* fTriggerThreshold = `255.99200439453125`
* lADCResolution = `32768`
* lAverageCount = `0`
* lDACResolution = `32768`
* lEpisodesPerRun = `1`
* lFileCommentIndex = `0`
* lFinishDisplayNum = `0`
* lNumSamplesPerEpisode = `256`
* lNumberOfTrials = `1`
* lPreTriggerSamples = `1000`
* lRunsPerTrial = `1`
* lSamplesPerTrace = `328192`
* lStartDisplayNum = `0`
* lStatisticsMeasurements = `2`
* lTimeHysteresis = `1`
* nActiveDACChannel = `0`
* nAllowExternalTags = `0`
* nAlternateDACOutputState = `0`
* nAlternateDigitalOutputState = `0`
* nAutoAnalyseEnable = `1`
* nAutoTriggerStrategy = `0`
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
* nDigitizerDACs = `4`
* nDigitizerSynchDigitalOuts = `8`
* nDigitizerTotalDigitalOuts = `16`
* nDigitizerType = `6`
* nExperimentType = `1`
* nExternalTagType = `2`
* nFirstEpisodeInRun = `1`
* nLTPType = `0`
* nLevelHysteresis = `64`
* nManualInfoStrategy = `0`
* nOperationMode = `3`
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
* fADCDisplayAmplification = `[15.691628456115723]`
* fADCDisplayOffset = `[-31.300003051757812]`
* fADCProgrammableGain = `[1.0]`
* fInstrumentOffset = `[0.0]`
* fInstrumentScaleFactor = `[-0.10000000149011612]`
* fPostProcessLowpassFilter = `[100000.0]`
* fSignalGain = `[1.0]`
* fSignalHighpassFilter = `[1.0]`
* fSignalLowpassFilter = `[5000.0]`
* fSignalOffset = `[0.0]`
* fTelegraphAccessResistance = `[0.0]`
* fTelegraphAdditGain = `[1.0]`
* fTelegraphFilter = `[0.0]`
* fTelegraphMembraneCap = `[0.0]`
* lADCChannelNameIndex = `[3]`
* lADCUnitsIndex = `[4]`
* nADCNum = `[6]`
* nADCPtoLChannelMap = `[0]`
* nADCSamplingSeq = `[0]`
* nHighpassFilterType = `[0]`
* nLowpassFilterType = `[0]`
* nPostProcessLowpassFilterType = `['\x00']`
* nStatsChannelPolarity = `[0]`
* nTelegraphEnable = `[0]`
* nTelegraphInstrument = `[0]`
* nTelegraphMode = `[0]`
* sTelegraphInstrument = `['Unknown instrument (manual or user defined telegraph table).']`

## DACSection

> Information about the DAC (what gets clamped).     There is 1 item per DAC. 

* fBaselineDuration = `[0.009999999776482582, 0.009999999776482582, 0.0, 0.0]`
* fBaselineLevel = `[0.0, 0.0, 0.0, 0.0]`
* fDACCalibrationFactor = `[0.9992715120315552, 0.9992160797119141, 0.9992160797119141, 0.9992715120315552]`
* fDACCalibrationOffset = `[4.0, -3.0, 1.0, -1.0]`
* fDACFileOffset = `[0.0, 0.0, 0.0, 0.0]`
* fDACFileScale = `[0.0, 0.0, 1.0, 1.0]`
* fDACHoldingLevel = `[0.0, 0.0, 0.0, 0.0]`
* fDACScaleFactor = `[10.0, 20.0, 20.0, 20.0]`
* fInstrumentHoldingLevel = `[0.0, 0.0, 0.0, 0.0]`
* fMembTestPostSettlingTimeMS = `[100.0, 100.0, 100.0, 100.0]`
* fMembTestPreSettlingTimeMS = `[100.0, 100.0, 100.0, 100.0]`
* fPNHoldingLevel = `[0.0, 0.0, 0.0, 0.0]`
* fPNInterpulse = `[0.0, 0.0, 0.0, 0.0]`
* fPNSettlingTime = `[0.0, 0.0, 0.0, 0.0]`
* fPostTrainLevel = `[0.0, 0.0, 0.0, 0.0]`
* fPostTrainPeriod = `[0.0, 0.0, 10.0, 10.0]`
* fStepDuration = `[0.009999999776482582, 0.009999999776482582, 0.0, 0.0]`
* fStepLevel = `[0.0, 0.0, 0.0, 0.0]`
* lConditNumPulses = `[1, 1, 0, 0]`
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
* nPNNumPulses = `[1, 1, 1, 1]`
* nPNPolarity = `[1, 1, 1, 1]`
* nPNPosition = `[0, 0, 0, 0]`
* nTelegraphDACScaleFactorEnable = `[0, 0, 0, 0]`
* nWaveformEnable = `[0, 0, 0, 0]`
* nWaveformSource = `[1, 1, 0, 0]`

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

* strings = `[b'SSCH\x01\x00\x00\x00\x0c\x00\x00\x00C\x00\x00\x00\x84\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00Clampex\x00C:\\MANIPS\\PROTOCOLES AMPLI\\rk400\\0.1 G Brigitte\\AS\\VC_cour01G20.pro\x00ImRK01G20\x00pA\x00Iimp RK01\x00nA\x00VimpRK\x00mV\x00OUT #2\x00mV\x00OUT #3\x00mV\x00', b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x00\x00\x00\xff\xff\xff\x00\xc0\xc0\xc0\x00\x80\x00\x00\x00', b'\xff\x00\x00\x00\x00\x00\x00\x00\xff\x00\x00\x00\xc0\xc0\xc0\x00\x00\x00\x00\x00\xec\xe9\xd8\x00\xac\xa8\x99\x00\x00\x00\x00\x00\x00@ H\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xf5\xff\x90\x01 \x00\x00\x00Arial\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00ImRK01G20\x00\x00\x00\x00\x00\x00\x00\xff\x00\x01\x00\x00\x00\x00\x00\x80?bV\x1b@\x00\x80\x9d\xc4\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00>\x00\x01\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x00\x00\x00\x00\x80\x00\x00\x80\x80\x00\x00\x00\x00\x80\x00\x80\x00\x80\x00\x00\x80\x80\x00\x80\x80\x80\x00\xff\x00\x00\x00\x00\x80\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x003\xfd0\xfd+\xfd*\xfd*\xfd(\xfd$\xfd$\xfd&\xfd(\xfd(\xfd'\xfd&\xfd(\xfd/\xfd3\xfd3\xfd6\xfd8\xfd9\xfd;\xfd>\xfd@\xfd>\xfd", b'<\xfd;\xfd5\xfd-\xfd)\xfd(\xfd(\xfd(\xfd%\xfd\x1e\xfd\x17\xfd\x19\xfd$\xfd+\xfd-\xfd)\xfd\x1f\xfd\x13\xfd\r\xfd\x0e\xfd\x11\xfd\x13\xfd\x14\xfd\x16\xfd\x12\xfd\x0b\xfd\x00\xfd\xf4\xfc\xef\xfc\xef\xfc\xf2\xfc\xf7\xfc\xf7\xfc\xf6\xfc\xf9\xfc\xf9\xfc\xfc\xfc\x05\xfd\x10\xfd\x1f\xfd+\xfd2\xfd8\xfd<\xfd<\xfd9\xfd6\xfd5\xfd2\xfd,\xfd\'\xfd$\xfd"\xfd\x1f\xfd\x16\xfd\x10\xfd\x0e\xfd\x15\xfd\x19\xfd\x11\xfd\t\xfd\x06\xfd\x0b\xfd\x14\xfd\x1b\xfd\x1b\xfd\x1b\xfd\x1d\xfd!\xfd&\xfd\'\xfd%\xfd$\xfd%\xfd(\xfd.\xfd4\xfd;\xfd?\xfdA\xfd<\xfd6\xfd/\xfd.\xfd,\xfd*\xfd+\xfd(\xfd', b'#\xfd\x19\xfd\x17\xfd\x17\xfd\x1c\xfd\x1f\xfd#\xfd%\xfd)\xfd0\xfd3\xfd6\xfd8\xfd8\xfd2\xfd+\xfd)\xfd-\xfd2\xfd5\xfd3\xfd5\xfd<\xfd?\xfd@\xfdD\xfdA\xfd9\xfd-\xfd\x1e\xfd\x14\xfd\x15\xfd\x1b\xfd\x1f\xfd \xfd\x1f\xfd\x19\xfd\x15\xfd\x19\xfd#\xfd.\xfd5\xfd7\xfd5\xfd3\xfd/\xfd/\xfd/\xfd1\xfd3\xfd9\xfd@\xfdB\xfd?\xfd>\xfd9\xfd3\xfd.\xfd\'\xfd!\xfd\x1d\xfd\x1c\xfd\x19\xfd\x19\xfd \xfd+\xfd7\xfd>\xfd>\xfd7\xfd/\xfd.\xfd2\xfd2\xfd-\xfd"\xfd\x1e\xfd \xfd%\xfd)\xfd)\xfd(\xfd(\xfd\'\xfd#\xfd\x1b\xfd\x14\xfd\x11\xfd', b'\x11\xfd\x13\xfd\x18\xfd\x1a\xfd\x1b\xfd\x1d\xfd!\xfd%\xfd)\xfd,\xfd/\xfd0\xfd-\xfd,\xfd-\xfd0\xfd5\xfd6\xfd5\xfd5\xfd9\xfd;\xfd;\xfd9\xfd7\xfd5\xfd5\xfd9\xfd8\xfd5\xfd/\xfd\'\xfd\x1e\xfd\x19\xfd\x17\xfd\x1a\xfd\x1e\xfd\x1a\xfd\x13\xfd\x11\xfd\x11\xfd\x15\xfd\x1a\xfd\x1e\xfd \xfd\x1f\xfd\x1e\xfd \xfd$\xfd&\xfd#\xfd\x1e\xfd\x1b\xfd\x17\xfd\x13\xfd\x13\xfd\x15\xfd\x19\xfd\x1d\xfd!\xfd"\xfd \xfd\x1e\xfd\x1b\xfd\x15\xfd\x0e\xfd\n\xfd\x06\xfd\t\xfd\r\xfd\x0f\xfd\x0e\xfd\x0e\xfd\x10\xfd\x15\xfd\x1c\xfd#\xfd!\xfd\x1d\xfd\x1a\xfd\x1c\xfd"\xfd#\xfd#\xfd&\xfd,\xfd5\xfd>\xfd']`

## StringsIndexed

> This object provides easy access to strings which are scattered around     the header files. The StringsSection contains strings, but various headers     contain values which point to a certain string index. This class connects     the two, and provides direct access to those strings by their indexed name. 

* lADCChannelName = `['ImRK01G20']`
* lADCUnits = `['pA']`
* lDACChannelName = `['Iimp RK01', 'VimpRK', 'OUT #2', 'OUT #3']`
* lDACChannelUnits = `['nA', 'mV', 'mV', 'mV']`
* lDACFilePath = `['', '', '', '']`
* lFileComment = ``
* nLeakSubtractADC = `['', '', '', '']`
* uCreatorName = `Clampex`
* uModifierName = ``
* uProtocolPath = `C:\MANIPS\PROTOCOLES AMPLI\rk400\0.1 G Brigitte\AS\VC_cour01G20.pro`
