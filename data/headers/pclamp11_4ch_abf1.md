# pclamp11_4ch_abf1.abf

## ABF Class Methods

* abf.launchInClampFit()
* abf.saveABF1()
* abf.setSweep()
* abf.sweepD()

## ABF Class Variables

* abfDateTime = `2018-12-14 20:42:15`
* abfDateTimeString = `2018-12-14T20:42:15.000`
* abfFileComment = ``
* abfFilePath = `C:/some/path/to/pclamp11_4ch_abf1.abf`
* abfID = `pclamp11_4ch_abf1`
* abfVersion = `{'major': 1, 'minor': 8, 'bugfix': 4, 'build': 0}`
* abfVersionString = `1.8.4.0`
* adcNames = `['IN 0', 'IN 1', 'IN 2', 'IN 3']`
* adcUnits = `['pA', 'pA', 'pA', 'pA']`
* channelCount = `4`
* channelList = `[0, 1, 2, 3]`
* creatorVersion = `{'major': 0, 'minor': 0, 'bugfix': 0, 'build': 0}`
* creatorVersionString = `0.0.0.0`
* dacNames = `['?', '?', '?', '?']`
* dacUnits = `['?', '?', '?', '?']`
* data = `array (2d) with values like: -0.23987, -0.02472, -0.36377, ..., -0.02563, 0.19806, 0.38391`
* dataByteStart = `6144`
* dataLengthMin = `0.009166666666666667`
* dataLengthSec = `0.55`
* dataPointByteSize = `2`
* dataPointCount = `160000`
* dataPointsPerMs = `80`
* dataRate = `80000`
* dataSecPerPoint = `1.25e-05`
* fileGUID = ``
* holdingCommand = `[10.0, 0.0, 0.0, ..., 0.0, 0.0, 0.0]`
* protocol = `None`
* protocolPath = `None`
* stimulusByChannel = `[Stimulus(abf, 0), Stimulus(abf, 1), Stimulus(abf, 2), Stimulus(abf, 3)]`
* stimulusFileFolder = `C:/some/alternate/path`
* sweepC = `array (1d) with values like: 10.00000, 10.00000, 10.00000, ..., 10.00000, 10.00000, 10.00000`
* sweepChannel = `0`
* sweepCount = `10`
* sweepEpochs = `Sweep epoch waveform: Step 10.00 [0:62], Step 10.00 [62:2062], Step 10.00 [2062:4000]`
* sweepIntervalSec = `0.05`
* sweepLabelC = `Membrane Potential (mV)`
* sweepLabelX = `time (seconds)`
* sweepLabelY = `Clamp Current (pA)`
* sweepLengthSec = `0.05`
* sweepList = `[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]`
* sweepNumber = `0`
* sweepPointCount = `4000`
* sweepTimesMin = `array (1d) with values like: 0.00000, 0.00083, 0.00167, ..., 0.00583, 0.00667, 0.00750`
* sweepTimesSec = `array (1d) with values like: 0.00000, 0.05000, 0.10000, ..., 0.35000, 0.40000, 0.45000`
* sweepUnitsC = `?`
* sweepUnitsX = `sec`
* sweepUnitsY = `pA`
* sweepX = `array (1d) with values like: 0.00000, 0.00001, 0.00003, ..., 0.04996, 0.04998, 0.04999`
* sweepY = `array (1d) with values like: -0.23987, -0.02472, -0.36377, ..., -0.32227, -0.41077, -0.51056`
* tagComments = `[]`
* tagSweeps = `[]`
* tagTimesMin = `[]`
* tagTimesSec = `[]`

## Epochs for Channel 0


```
                    EPOCH         A
                     Type      Step
              First Level     10.00
              Delta Level      0.00
  First Duration (points)      2000
  Delta Duration (points)         0
     Digital Pattern #3-0      0000
     Digital Pattern #7-4      0000
    Train Period (points)         0
     Pulse Width (points)         0
```

## Epochs for Channel 1


```

```

## Epochs for Channel 2


```

```

## Epochs for Channel 3


```

```

## ABF1 Header

> The first several bytes of an ABF1 file contain variables     located at specific byte positions from the start of the file.     All ABF1 header values are read in this single block. 

* abfDateTime = `2018-12-14 20:42:15`
* abfDateTimeString = `2018-12-14T20:42:15.000`
* abfVersionDict = `{'major': 1, 'minor': 8, 'bugfix': 4, 'build': 0}`
* abfVersionFloat = `1.84`
* abfVersionString = `1.8.4.0`
* creatorVersionDict = `{'major': 0, 'minor': 0, 'bugfix': 0, 'build': 0}`
* creatorVersionString = `0.0.0.0`
* fADCProgrammableGain = `[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]`
* fADCRange = `10.0`
* fADCSampleInterval = `12.5`
* fDACCalibrationFactor = `[1.0, 1.0, 1.0, 1.0]`
* fDACCalibrationOffset = `[0.0, 0.0, 0.0, 0.0]`
* fEpochInitLevel = `[10.0, 0.0, 0.0, ..., 0.0, 0.0, 0.0]`
* fEpochLevelInc = `[0.0, 0.0, 0.0, ..., 0.0, 0.0, 0.0]`
* fFileSignature = `?`
* fFileVersionNumber = `1.840000033378601`
* fInstrumentOffset = `[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]`
* fInstrumentScaleFactor = `[1.0, 1.0, 1.0, 1.0, 0.10000000149011612, 0.10000000149011612, 0.10000000149011612, 0.10000000149011612, 0.10000000149011612, 0.10000000149011612, 0.10000000149011612, 0.10000000149011612, 0.10000000149011612, 0.10000000149011612, 0.10000000149011612, 0.10000000149011612]`
* fSignalGain = `[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]`
* fSignalOffset = `[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]`
* fSynchTimeUnit = `3.125`
* fTelegraphAdditGain = `[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]`
* lADCResolution = `32768`
* lActualAcqLength = `160000`
* lActualEpisodes = `10`
* lDACFileNumEpisodes = `[0, 0]`
* lDACFilePtr = `[0, 0]`
* lDataSectionPtr = `12`
* lEpisodesPerRun = `10`
* lEpochDurationInc = `[0, 0, 0, ..., 0, 0, 0]`
* lEpochInitDuration = `[2000, 0, 0, ..., 0, 0, 0]`
* lFileStartTime = `74172`
* lNumSamplesPerEpisode = `16000`
* lNumTagEntries = `0`
* lPreTriggerSamples = `80`
* lSynchArrayPtr = `637`
* lSynchArraySize = `10`
* lTagSectionPtr = `0`
* lTagTime = `[]`
* nADCNumChannels = `4`
* nADCPtoLChannelMap = `[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]`
* nADCSamplingSeq = `[0, 1, 2, 3, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]`
* nActiveDACChannel = `0`
* nDataFormat = `0`
* nDigitalEnable = `0`
* nDigitalHolding = `0`
* nDigitalInterEpisode = `0`
* nDigitalValue = `[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]`
* nEpochType = `[1, 0, 0, ..., 0, 0, 0]`
* nFileStartMillisecs = `308`
* nInterEpisodeLevel = `[0, 0]`
* nNumPointsIgnored = `0`
* nOperationMode = `5`
* nTagType = `[]`
* nTelegraphEnable = `[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]`
* nWaveformEnable = `[1, 1]`
* nWaveformSource = `[1, 1]`
* sADCChannelName = `['IN 0', 'IN 1', 'IN 2', 'IN 3', 'AI #4', 'AI #5', 'AI #6', 'AI #7', 'AI #8', 'AI #9', 'AI #10', 'AI #11', 'AI #12', 'AI #13', 'AI #14', 'AI #15']`
* sADCUnits = `['pA', 'pA', 'pA', 'pA', 'pA', 'pA', 'pA', 'pA', 'pA', 'pA', 'pA', 'pA', 'pA', 'pA', 'pA', 'pA']`
* sComment = `[]`
* sProtocolPath = `(untitled)`
