# multichannelAbf1WithTags.abf

## ABF Class Methods

* abf.launchInClampFit()
* abf.saveABF1()
* abf.setSweep()
* abf.sweepD()

## ABF Class Variables

* abfDateTime = `2019-07-01 19:42:46`
* abfDateTimeString = `2019-07-01T19:42:46.000`
* abfFileComment = ``
* abfFilePath = `C:/some/path/to/multichannelAbf1WithTags.abf`
* abfFolderPath = `C:\Users\scott\Documents\GitHub\pyABF\data\abfs`
* abfID = `multichannelAbf1WithTags`
* abfVersion = `{'major': 1, 'minor': 8, 'bugfix': 4, 'build': 0}`
* abfVersionString = `1.8.4.0`
* adcNames = `['IN 0', 'AO #0']`
* adcUnits = `['pA', 'mV']`
* channelCount = `2`
* channelList = `[0, 1]`
* creatorVersion = `{'major': 0, 'minor': 0, 'bugfix': 0, 'build': 0}`
* creatorVersionString = `0.0.0.0`
* dacNames = `['?', '?']`
* dacUnits = `['?', '?']`
* data = `array (2d) with values like: 0.85449, 0.97656, 0.73242, ..., -59.97800, -59.97800, -59.97800`
* dataByteStart = `6144`
* dataLengthMin = `0.25897`
* dataLengthSec = `15.5382`
* dataPointByteSize = `2`
* dataPointCount = `618222`
* dataPointsPerMs = `20`
* dataRate = `20000`
* dataSecPerPoint = `5e-05`
* fileGUID = ``
* holdingCommand = `[0.0, 0.0, 0.0, ..., 0.0, 0.0, 0.0]`
* protocol = `None`
* protocolPath = `None`
* stimulusByChannel = `[Stimulus(abf, 0), Stimulus(abf, 1)]`
* stimulusFileFolder = `C:\Users\scott\Documents\GitHub\pyABF\data\abfs`
* sweepC = `array (1d) with values like: 0.00000, 0.00000, 0.00000, ..., 0.00000, 0.00000, 0.00000`
* sweepChannel = `0`
* sweepCount = `187`
* sweepEpochs = `Sweep epoch waveform: Step 0.00 [0:25], Step 0.00 [25:1653]`
* sweepIntervalSec = `0.08265`
* sweepLabelC = `Membrane Potential (mV)`
* sweepLabelX = `time (seconds)`
* sweepLabelY = `Clamp Current (pA)`
* sweepLengthSec = `0.08265`
* sweepList = `[0, 1, 2, ..., 184, 185, 186]`
* sweepNumber = `0`
* sweepPointCount = `1653`
* sweepTimesMin = `array (1d) with values like: 0.00000, 0.00138, 0.00276, ..., 0.25346, 0.25484, 0.25621`
* sweepTimesSec = `array (1d) with values like: 0.00000, 0.08265, 0.16530, ..., 15.20760, 15.29025, 15.37290`
* sweepUnitsC = `?`
* sweepUnitsX = `sec`
* sweepUnitsY = `pA`
* sweepX = `array (1d) with values like: 0.00000, 0.00005, 0.00010, ..., 0.08250, 0.08255, 0.08260`
* sweepY = `array (1d) with values like: 0.85449, 0.97656, 0.73242, ..., -61.27929, -62.25586, -62.50000`
* tagComments = `['+TGOT', '-TGOT']`
* tagSweeps = `[2104.9921355111915, 3567.583787053842]`
* tagTimesMin = `[2.899626666666667, 4.914346666666668]`
* tagTimesSec = `[173.9776, 294.86080000000004]`

## Epochs for Channel 0


```
DAC waveform is not enabled
```

## Epochs for Channel 1


```

```

## ABF1 Header

> The first several bytes of an ABF1 file contain variables     located at specific byte positions from the start of the file.     All ABF1 header values are read in this single block. 

* abfDateTime = `2019-07-01 19:42:46`
* abfDateTimeString = `2019-07-01T19:42:46.000`
* abfVersionDict = `{'major': 1, 'minor': 8, 'bugfix': 4, 'build': 0}`
* abfVersionFloat = `1.84`
* abfVersionString = `1.8.4.0`
* creatorVersionDict = `{'major': 0, 'minor': 0, 'bugfix': 0, 'build': 0}`
* creatorVersionString = `0.0.0.0`
* fADCProgrammableGain = `[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]`
* fADCRange = `10.0`
* fADCSampleInterval = `25.0`
* fDACCalibrationFactor = `[1.0008957386016846, 1.001062273979187, 1.0010067224502563, 1.0009512901306152]`
* fDACCalibrationOffset = `[1.0, -1.0, -3.0, 1.0]`
* fEpochInitLevel = `[0.0, 0.0, 0.0, ..., 0.0, 0.0, 0.0]`
* fEpochLevelInc = `[0.0, 0.0, 0.0, ..., 0.0, 0.0, 0.0]`
* fFileSignature = `?`
* fFileVersionNumber = `1.840000033378601`
* fInstrumentOffset = `[0.0, 0.006103515625, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]`
* fInstrumentScaleFactor = `[0.0005000000237487257, 0.049955252557992935, 0.10000000149011612, 0.10000000149011612, 0.10000000149011612, 0.10000000149011612, 0.10000000149011612, 0.10000000149011612, 0.10000000149011612, 0.10000000149011612, 0.10000000149011612, 0.10000000149011612, 0.10000000149011612, 0.10000000149011612, 0.10000000149011612, 0.10000000149011612]`
* fSignalGain = `[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]`
* fSignalOffset = `[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]`
* fSynchTimeUnit = `12.5`
* fTelegraphAdditGain = `[5.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]`
* lADCResolution = `32768`
* lActualAcqLength = `618222`
* lActualEpisodes = `187`
* lDACFileNumEpisodes = `[0, 0]`
* lDACFilePtr = `[0, 0]`
* lDataSectionPtr = `12`
* lEpisodesPerRun = `187`
* lEpochDurationInc = `[0, 0, 0, ..., 0, 0, 0]`
* lEpochInitDuration = `[0, 0, 0, ..., 0, 0, 0]`
* lFileStartTime = `45620`
* lNumSamplesPerEpisode = `3306`
* lNumTagEntries = `2`
* lPreTriggerSamples = `40`
* lSynchArrayPtr = `2427`
* lSynchArraySize = `187`
* lTagSectionPtr = `2430`
* lTagTime = `[13918208, 23588864]`
* nADCNumChannels = `2`
* nADCPtoLChannelMap = `[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]`
* nADCSamplingSeq = `[0, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]`
* nActiveDACChannel = `0`
* nDataFormat = `0`
* nDigitalEnable = `0`
* nDigitalHolding = `0`
* nDigitalInterEpisode = `0`
* nDigitalValue = `[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]`
* nEpochType = `[0, 0, 0, ..., 0, 0, 0]`
* nFileStartMillisecs = `701`
* nInterEpisodeLevel = `[0, 0]`
* nNumPointsIgnored = `0`
* nOperationMode = `5`
* nTagType = `[1, 1]`
* nTelegraphEnable = `[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]`
* nWaveformEnable = `[1, 0]`
* nWaveformSource = `[0, 0]`
* sADCChannelName = `['IN 0', 'AO #0', 'AI #2', 'AI #3', 'AI #4', 'AI #5', 'AI #6', 'AI #7', 'AI #8', 'AI #9', 'AI #10', 'AI #11', 'AI #12', 'AI #13', 'AI #14', 'AI #15']`
* sADCUnits = `['pA', 'mV', 'pA', 'pA', 'pA', 'pA', 'pA', 'pA', 'pA', 'pA', 'pA', 'pA', 'pA', 'pA', 'pA', 'pA']`
* sComment = `['+TGOT', '-TGOT']`
* sProtocolPath = `S:\Protocols\permanent\0402 VC 2s MT-50.pro                                                                                                                                                                                                                     SWHLab5[0402]`
