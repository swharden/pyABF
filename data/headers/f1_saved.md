# f1_saved.abf

## ABF Class Methods

* abf.launchInClampFit()
* abf.saveABF1()
* abf.setSweep()
* abf.sweepD()

## ABF Class Variables

* abfDateTime = `2018-12-03 05:44:39`
* abfDateTimeString = `2018-12-03T05:44:39.000`
* abfFileComment = ``
* abfFilePath = `C:/some/path/to/f1_saved.abf`
* abfID = `f1_saved`
* abfVersion = `{'major': 1, 'minor': 2, 'bugfix': 9, 'build': 9}`
* abfVersionString = `1.2.9.9`
* adcNames = `['\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00']`
* adcUnits = `['pA']`
* channelCount = `1`
* channelList = `[0]`
* creatorVersion = `{'major': 0, 'minor': 0, 'bugfix': 0, 'build': 0}`
* creatorVersionString = `0.0.0.0`
* dacNames = `['?']`
* dacUnits = `['?']`
* data = `array (2d) with values like: -30.51758, -41.50391, -32.34863, ..., -37.84180, -36.62109, -25.63477`
* dataByteStart = `2048`
* dataLengthMin = `0.4583333333333333`
* dataLengthSec = `27.5`
* dataPointByteSize = `2`
* dataPointCount = `500000`
* dataPointsPerMs = `20`
* dataRate = `20000`
* dataSecPerPoint = `5e-05`
* fileGUID = ``
* holdingCommand = `[nan, nan, nan, ..., nan, nan, nan]`
* protocol = `None`
* protocolPath = `None`
* stimulusByChannel = `[Stimulus(abf, 0)]`
* stimulusFileFolder = `C:/some/alternate/path`
* sweepC = `array (1d) with values like: nan, nan, nan, ..., nan, nan, nan`
* sweepChannel = `0`
* sweepCount = `10`
* sweepEpochs = `Sweep epoch waveform: Step nan [0:781], Unknown nan [781:-8060257], Unknown nan [-8060257:-14679509], Unknown nan [-14679509:-23395909], Unknown nan [-23395909:-29753007], Unknown nan [-29753007:-38469385], Unknown nan [-38469385:-46923625], Unknown nan [-46923625:-54853579], Unknown nan [-54853579:-61341741], Unknown nan [-61341741:-69271695], Unknown nan [-69271695:-76284159], Step nan [-76284159:50000]`
* sweepIntervalSec = `2.5`
* sweepLabelC = `Membrane Potential (mV)`
* sweepLabelX = `time (seconds)`
* sweepLabelY = `Clamp Current (pA)`
* sweepLengthSec = `2.5`
* sweepList = `[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]`
* sweepNumber = `0`
* sweepPointCount = `50000`
* sweepTimesMin = `array (1d) with values like: 0.00000, 0.04167, 0.08333, ..., 0.29167, 0.33333, 0.37500`
* sweepTimesSec = `array (1d) with values like: 0.00000, 2.50000, 5.00000, ..., 17.50000, 20.00000, 22.50000`
* sweepUnitsC = `?`
* sweepUnitsX = `sec`
* sweepUnitsY = `pA`
* sweepX = `array (1d) with values like: 0.00000, 0.00005, 0.00010, ..., 2.49985, 2.49990, 2.49995`
* sweepY = `array (1d) with values like: -30.51758, -41.50391, -32.34863, ..., -57.37305, -49.43848, -55.54199`
* tagComments = `[]`
* tagSweeps = `[]`
* tagTimesMin = `[]`
* tagTimesSec = `[]`

## Epochs for Channel 0


```
unknown nWaveformSource (-120)
```

## ABF1 Header

> The first several bytes of an ABF1 file contain variables     located at specific byte positions from the start of the file.     All ABF1 header values are read in this single block. 

* abfDateTime = `2018-12-03 05:44:39`
* abfDateTimeString = `2018-12-03T05:44:39.000`
* abfVersionDict = `{'major': 1, 'minor': 2, 'bugfix': 9, 'build': 9}`
* abfVersionFloat = `1.299`
* abfVersionString = `1.2.9.9`
* creatorVersionDict = `{'major': 0, 'minor': 0, 'bugfix': 0, 'build': 0}`
* creatorVersionString = `0.0.0.0`
* fADCProgrammableGain = `[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]`
* fADCRange = `10.0`
* fADCSampleInterval = `50.0`
* fDACCalibrationFactor = `[-3.3894989373961696e+38, -3.176826514552504e+38, nan, nan]`
* fDACCalibrationOffset = `[nan, nan, nan, nan]`
* fEpochInitLevel = `[nan, nan, nan, ..., nan, nan, nan]`
* fEpochLevelInc = `[nan, -3.3363379305286145e+38, nan, ..., nan, nan, nan]`
* fFileSignature = `ff?`
* fFileVersionNumber = `1.2999999523162842`
* fInstrumentOffset = `[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]`
* fInstrumentScaleFactor = `[0.0010000000474974513, 0.0010000000474974513, 0.0010000000474974513, 0.0010000000474974513, 0.0010000000474974513, 0.0010000000474974513, 0.0010000000474974513, 0.0010000000474974513, 0.0010000000474974513, 0.0010000000474974513, 0.0010000000474974513, 0.0010000000474974513, 0.0010000000474974513, 0.0010000000474974513, 0.0010000000474974513, 0.0010000000474974513]`
* fSignalGain = `[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]`
* fSignalOffset = `[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]`
* fSynchTimeUnit = `0.0`
* fTelegraphAdditGain = `[-3.3895078616563952e+38, -3.203411074468202e+38, nan, -3.362923707388889e+38, -3.0704931426680154e+38, nan, nan, nan, nan, -3.389511512490124e+38, nan, -3.3363391474731907e+38, nan, nan, nan, nan]`
* lADCResolution = `32768`
* lActualAcqLength = `500000`
* lActualEpisodes = `10`
* lDACFileNumEpisodes = `[-9240692, -8716426]`
* lDACFilePtr = `[-8847460, -9896042]`
* lDataSectionPtr = `4`
* lEpisodesPerRun = `0`
* lEpochDurationInc = `[-7405670, -7012490, -8192094, ..., -6488180, -8847462, -7536776]`
* lEpochInitDuration = `[-8061038, -6619252, -8716400, ..., -7536756, -7798916, -8978554]`
* lFileStartTime = `0`
* lNumSamplesPerEpisode = `50000`
* lNumTagEntries = `0`
* lPreTriggerSamples = `0`
* lSynchArrayPtr = `0`
* lSynchArraySize = `0`
* lTagSectionPtr = `0`
* lTagTime = `[]`
* nADCNumChannels = `1`
* nADCPtoLChannelMap = `[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]`
* nADCSamplingSeq = `[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]`
* nActiveDACChannel = `0`
* nDataFormat = `0`
* nDigitalEnable = `0`
* nDigitalHolding = `0`
* nDigitalInterEpisode = `0`
* nDigitalValue = `[-102, -114, -138, -108, -94, -126, -124, -112, -110, -102]`
* nEpochType = `[-116, -98, -114, ..., -156, -106, -122]`
* nFileStartMillisecs = `0`
* nInterEpisodeLevel = `[-138, -116]`
* nNumPointsIgnored = `0`
* nOperationMode = `5`
* nTagType = `[]`
* nTelegraphEnable = `[-126, -102, -144, -120, -104, -126, -126, -114, -136, -124, -96, -126, -112, -104, -136, -126]`
* nWaveformEnable = `[-102, -116]`
* nWaveformSource = `[-120, -110]`
* sADCChannelName = `['\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00']`
* sADCUnits = `['pA', 'pA', 'pA', 'pA', 'pA', 'pA', 'pA', 'pA', 'pA', 'pA', 'pA', 'pA', 'pA', 'pA', 'pA', 'pA']`
* sComment = `[]`
* sProtocolPath = `||^tx|rn|~zp|tpndzrzxpzjzzrt~|~ztjvtrphtnlv|lzvvX`
