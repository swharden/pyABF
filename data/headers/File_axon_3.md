# File_axon_3.abf

## ABF Class Methods

* abf.launchInClampFit()
* abf.saveABF1()
* abf.setSweep()
* abf.sweepD()

## ABF Class Variables

* abfDateTime = `2018-09-05 02:02:35`
* abfDateTimeString = `2018-09-05T02:02:35.000`
* abfFileComment = ``
* abfFilePath = `C:/some/path/to/File_axon_3.abf`
* abfID = `File_axon_3`
* abfVersion = `{'major': 1, 'minor': 8, 'bugfix': 3, 'build': 0}`
* abfVersionString = `1.8.3.0`
* adcNames = `['10Vm', 'ImRK01G1b']`
* adcUnits = `['mV', 'pA']`
* channelCount = `2`
* channelList = `[0, 1]`
* creatorVersion = `{'major': 0, 'minor': 0, 'bugfix': 0, 'build': 0}`
* creatorVersionString = `0.0.0.0`
* dacNames = `['?', '?']`
* dacUnits = `['?', '?']`
* data = `array (2d) with values like: -15.50000, -28.00000, -28.50000, ..., -16450.00000, -16450.00000, -16450.00000`
* dataByteStart = `8192`
* dataLengthMin = `0.051609999999999996`
* dataLengthSec = `3.0965999999999996`
* dataPointByteSize = `2`
* dataPointCount = `206440`
* dataPointsPerMs = `40`
* dataRate = `40000`
* dataSecPerPoint = `2.5e-05`
* fileGUID = ``
* holdingCommand = `[0.0, 0.0, 0.0, ..., 0.0, 0.0, 0.0]`
* protocol = `Cc_stim ONL`
* protocolPath = `C:\Axon\rk400\0.1G\Cc_stim ONL.pro`
* stimulusByChannel = `[Stimulus(abf, 0), Stimulus(abf, 1)]`
* stimulusFileFolder = `C:/some/alternate/path`
* sweepC = `array (1d) with values like: 0.00000, 0.00000, 0.00000, ..., 0.00000, 0.00000, 0.00000`
* sweepChannel = `0`
* sweepCount = `5`
* sweepEpochs = `Sweep epoch waveform: Step 0.00 [0:322], Step 0.00 [322:347], Step 0.00 [347:357], Step 0.00 [357:382], Step 0.00 [382:20644]`
* sweepIntervalSec = `0.5161`
* sweepLabelC = `Applied Current (pA)`
* sweepLabelX = `time (seconds)`
* sweepLabelY = `Membrane Potential (mV)`
* sweepLengthSec = `0.5161`
* sweepList = `[0, 1, 2, 3, 4]`
* sweepNumber = `0`
* sweepPointCount = `20644`
* sweepTimesMin = `array (1d) with values like: 0.00000, 0.00860, 0.01720, 0.02581, 0.03441`
* sweepTimesSec = `array (1d) with values like: 0.00000, 0.51610, 1.03220, 1.54830, 2.06440`
* sweepUnitsC = `?`
* sweepUnitsX = `sec`
* sweepUnitsY = `mV`
* sweepX = `array (1d) with values like: 0.00000, 0.00003, 0.00005, ..., 0.51603, 0.51605, 0.51608`
* sweepY = `array (1d) with values like: -15.50000, -28.00000, -28.50000, ..., -28.00000, -28.00000, -28.50000`
* tagComments = `[]`
* tagSweeps = `[]`
* tagTimesMin = `[]`
* tagTimesSec = `[]`

## Epochs for Channel 0


```
                    EPOCH         B         C         D
                     Type      Step      Step      Step
              First Level      0.00      0.00      0.00
              Delta Level      0.00      0.00      0.00
  First Duration (points)        25        10        25
  Delta Duration (points)         0         0         0
     Digital Pattern #3-0      0000      0000      0000
     Digital Pattern #7-4      0000      0000      0000
    Train Period (points)         0         0         0
     Pulse Width (points)         0         0         0
```

## Epochs for Channel 1


```

```

## ABF1 Header

> The first several bytes of an ABF1 file contain variables     located at specific byte positions from the start of the file.     All ABF1 header values are read in this single block. 

* abfDateTime = `2018-09-05 02:02:35`
* abfDateTimeString = `2018-09-05T02:02:35.000`
* abfVersionDict = `{'major': 1, 'minor': 8, 'bugfix': 3, 'build': 0}`
* abfVersionFloat = `1.83`
* abfVersionString = `1.8.3.0`
* creatorVersionDict = `{'major': 0, 'minor': 0, 'bugfix': 0, 'build': 0}`
* creatorVersionString = `0.0.0.0`
* fADCProgrammableGain = `[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 8.0, 4.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]`
* fADCRange = `10.239999771118164`
* fADCSampleInterval = `25.0`
* fDACCalibrationFactor = `[1.0, 1.0, 1.0, 1.0]`
* fDACCalibrationOffset = `[0.0, 0.0, 0.0, 0.0]`
* fEpochInitLevel = `[0.0, 0.0, 0.0, ..., 0.0, 0.0, 0.0]`
* fEpochLevelInc = `[0.0, 0.0, 0.0, ..., 0.0, 0.0, 0.0]`
* fFileSignature = `q=?`
* fFileVersionNumber = `1.8300000429153442`
* fInstrumentOffset = `[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]`
* fInstrumentScaleFactor = `[0.009999999776482582, 9.999999747378752e-05, 1.0, 1.0, 1.0, 1.0, 0.0020000000949949026, 0.009999999776482582, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]`
* fSignalGain = `[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]`
* fSignalOffset = `[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]`
* fSynchTimeUnit = `12.5`
* fTelegraphAdditGain = `[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]`
* lADCResolution = `32768`
* lActualAcqLength = `206440`
* lActualEpisodes = `5`
* lDACFileNumEpisodes = `[0, 0]`
* lDACFilePtr = `[0, 0]`
* lDataSectionPtr = `16`
* lEpisodesPerRun = `40`
* lEpochDurationInc = `[0, 0, 0, ..., 0, 0, 0]`
* lEpochInitDuration = `[1000, 25, 10, ..., 0, 0, 0]`
* lFileStartTime = `51328`
* lNumSamplesPerEpisode = `41288`
* lNumTagEntries = `0`
* lPreTriggerSamples = `20`
* lSynchArrayPtr = `823`
* lSynchArraySize = `5`
* lTagSectionPtr = `0`
* lTagTime = `[]`
* nADCNumChannels = `2`
* nADCPtoLChannelMap = `[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]`
* nADCSamplingSeq = `[5, 7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]`
* nActiveDACChannel = `0`
* nDataFormat = `0`
* nDigitalEnable = `1`
* nDigitalHolding = `16`
* nDigitalInterEpisode = `0`
* nDigitalValue = `[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]`
* nEpochType = `[0, 1, 1, ..., 0, 0, 0]`
* nFileStartMillisecs = `552`
* nInterEpisodeLevel = `[0, 0]`
* nNumPointsIgnored = `0`
* nOperationMode = `5`
* nTagType = `[]`
* nTelegraphEnable = `[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]`
* nWaveformEnable = `[1, 0]`
* nWaveformSource = `[1, 1]`
* sADCChannelName = `['10Vm', 'ImRK01G1b', 'IN 2', 'IN 3', 'IN 4', 'stim', 'ImRK01G20', 'VmRK', 'IN 8', 'IN 9', 'IN 10', 'IN 11', 'IN 12', 'IN 13', 'IN 14', 'IN 15']`
* sADCUnits = `['mV', 'pA', 'V', 'V', 'V', 'V', 'pA', 'mV', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V']`
* sComment = `[]`
* sProtocolPath = `C:\Axon\rk400\0.1G\Cc_stim ONL.pro`
