# sample trace_0054.abf

## ABF Class Methods

* abf.launchInClampFit()
* abf.saveABF1()
* abf.setSweep()
* abf.sweepD()

## ABF Class Variables

* abfDateTime = `2018-11-20 07:41:29`
* abfDateTimeString = `2018-11-20T07:41:29.000`
* abfFileComment = ``
* abfFilePath = `C:/some/path/to/sample trace_0054.abf`
* abfID = `sample trace_0054`
* abfVersion = `{'major': 1, 'minor': 6, 'bugfix': 4, 'build': 9}`
* abfVersionString = `1.6.4.9`
* adcNames = `['IN 0']`
* adcUnits = `['nA']`
* channelCount = `1`
* channelList = `[0]`
* creatorVersion = `{'major': 0, 'minor': 0, 'bugfix': 0, 'build': 0}`
* creatorVersionString = `0.0.0.0`
* dacNames = `['?']`
* dacUnits = `['?']`
* data = `array (2d) with values like: 0.00931, 0.01373, 0.03296, ..., 0.01694, 0.02716, 0.02365`
* dataByteStart = `8192`
* dataLengthMin = `0.7433333333333334`
* dataLengthSec = `44.6`
* dataPointByteSize = `2`
* dataPointCount = `2230000`
* dataPointsPerMs = `50`
* dataRate = `50000`
* dataSecPerPoint = `2e-05`
* fileGUID = ``
* holdingCommand = `[112.0, 0.0, 0.0, ..., 0.0, 0.0, 0.0]`
* protocol = `slaven-Ch1-gapfree`
* protocolPath = `C:\Axon\Params\slaven-Ch1-gapfree.pro`
* stimulusByChannel = `[Stimulus(abf, 0)]`
* stimulusFileFolder = `C:/some/alternate/path`
* sweepC = `array (1d) with values like: 112.00000, 112.00000, 112.00000, ..., 112.00000, 112.00000, 112.00000`
* sweepChannel = `0`
* sweepCount = `1`
* sweepEpochs = `Sweep epoch waveform: Step 112.00 [0:34843], Step 112.00 [34843:35843], Step 112.00 [35843:2230000]`
* sweepIntervalSec = `44.6`
* sweepLabelC = `? (?)`
* sweepLabelX = `time (seconds)`
* sweepLabelY = `IN 0 (nA)`
* sweepLengthSec = `44.6`
* sweepList = `[0]`
* sweepNumber = `0`
* sweepPointCount = `2230000`
* sweepTimesMin = `array (1d) with values like: 0.00000`
* sweepTimesSec = `array (1d) with values like: 0.00000`
* sweepUnitsC = `?`
* sweepUnitsX = `sec`
* sweepUnitsY = `nA`
* sweepX = `array (1d) with values like: 0.00000, 0.00002, 0.00004, ..., 44.59994, 44.59996, 44.59998`
* sweepY = `array (1d) with values like: 0.00931, 0.01373, 0.03296, ..., 0.01694, 0.02716, 0.02365`
* tagComments = `[]`
* tagSweeps = `[]`
* tagTimesMin = `[]`
* tagTimesSec = `[]`

## Epochs for Channel 0


```
                    EPOCH         A
                     Type      Step
              First Level    112.00
              Delta Level    -20.00
  First Duration (points)      1000
  Delta Duration (points)         0
     Digital Pattern #3-0      0000
     Digital Pattern #7-4      0000
    Train Period (points)         0
     Pulse Width (points)         0
```

## ABF1 Header

> The first several bytes of an ABF1 file contain variables     located at specific byte positions from the start of the file.     All ABF1 header values are read in this single block. 

* abfDateTime = `2018-11-20 07:41:29`
* abfDateTimeString = `2018-11-20T07:41:29.000`
* abfVersionDict = `{'major': 1, 'minor': 6, 'bugfix': 4, 'build': 9}`
* abfVersionFloat = `1.649`
* abfVersionString = `1.6.4.9`
* creatorVersionDict = `{'major': 0, 'minor': 0, 'bugfix': 0, 'build': 0}`
* creatorVersionString = `0.0.0.0`
* fADCProgrammableGain = `[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]`
* fADCRange = `10.0`
* fADCSampleInterval = `20.0`
* fDACCalibrationFactor = `[1.092650055885315, 1.096560001373291, 1.0, 1.0]`
* fDACCalibrationOffset = `[-192.0, -143.0, 0.0, 0.0]`
* fEpochInitLevel = `[112.0, 0.0, 0.0, ..., 0.0, 0.0, 0.0]`
* fEpochLevelInc = `[-20.0, 0.0, 0.0, ..., 0.0, 0.0, 0.0]`
* fFileSignature = `33?`
* fFileVersionNumber = `1.649999976158142`
* fInstrumentOffset = `[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]`
* fInstrumentScaleFactor = `[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]`
* fSignalGain = `[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]`
* fSignalOffset = `[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]`
* fSynchTimeUnit = `0.0`
* fTelegraphAdditGain = `[2.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]`
* lADCResolution = `32768`
* lActualAcqLength = `2230000`
* lActualEpisodes = `1081`
* lDACFileNumEpisodes = `[0, 0]`
* lDACFilePtr = `[0, 0]`
* lDataSectionPtr = `16`
* lEpisodesPerRun = `1`
* lEpochDurationInc = `[0, 0, 0, ..., 0, 0, 0]`
* lEpochInitDuration = `[1000, 0, 0, ..., 0, 0, 0]`
* lFileStartTime = `57783`
* lNumSamplesPerEpisode = `2064`
* lNumTagEntries = `0`
* lPreTriggerSamples = `16`
* lSynchArrayPtr = `0`
* lSynchArraySize = `0`
* lTagSectionPtr = `0`
* lTagTime = `[]`
* nADCNumChannels = `1`
* nADCPtoLChannelMap = `[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]`
* nADCSamplingSeq = `[0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]`
* nActiveDACChannel = `0`
* nDataFormat = `0`
* nDigitalEnable = `0`
* nDigitalHolding = `16`
* nDigitalInterEpisode = `0`
* nDigitalValue = `[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]`
* nEpochType = `[1, 0, 0, ..., 0, 0, 0]`
* nFileStartMillisecs = `566`
* nInterEpisodeLevel = `[0, 0]`
* nNumPointsIgnored = `0`
* nOperationMode = `3`
* nTagType = `[]`
* nTelegraphEnable = `[1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]`
* nWaveformEnable = `[1, 0]`
* nWaveformSource = `[1, 1]`
* sADCChannelName = `['IN 0', 'IN 1', 'IN 2', 'IN 3', 'IN 4', 'IN 5', 'IN 6', 'IN 7', 'IN 8', 'IN 9', 'IN 10', 'IN 11', 'IN 12', 'IN 13', 'IN 14', 'IN 15']`
* sADCUnits = `['nA', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V']`
* sComment = `[]`
* sProtocolPath = `C:\Axon\Params\slaven-Ch1-gapfree.pro`
