# abf1_with_tags.abf

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

* abfDateTime = `2018-09-06 20:04:50`
* abfDateTimeString = `2018-09-06T20:04:50.000`
* abfFileComment = ``
* abfFilePath = `C:/some/path/to/abf1_with_tags.abf`
* abfID = `abf1_with_tags`
* abfVersion = `{'major': 1, 'minor': 8, 'bugfix': 3, 'build': 0}`
* abfVersionString = `1.8.3.0`
* adcNames = `['IN 0']`
* adcUnits = `['pA']`
* channelCount = `1`
* channelList = `[0]`
* creatorVersion = `{'major': 0, 'minor': 0, 'bugfix': 0, 'build': 0}`
* creatorVersionString = `0.0.0.0`
* dacNames = `['?']`
* dacUnits = `['?']`
* data = `array (2d) with values like: -34.54589, -34.36279, -34.91211, ..., -82.33642, -81.29882, -80.74950`
* dataByteStart = `8192`
* dataPointByteSize = `2`
* dataPointCount = `18000000`
* dataPointsPerMs = `20`
* dataRate = `20000`
* dataSecPerPoint = `5e-05`
* epochPoints = `[]`
* epochValues = `[]`
* fileGUID = ``
* holdingCommand = `[112.0, 0.0, 0.0, ..., 0.0, 0.0, 0.0]`
* protocol = `15minGapfree`
* protocolPath = `X:\Protocols\DP\15minGapfree.pro`
* stimulusByChannel = `[ChannelEpochs(ABF, 0)]`
* sweepC = `array (1d) with values like: nan, nan, nan, ..., nan, nan, nan`
* sweepChannel = `0`
* sweepCount = `8721`
* sweepLabelC = `Membrane Potential (mV)`
* sweepLabelX = `time (seconds)`
* sweepLabelY = `Clamp Current (pA)`
* sweepLengthSec = `0.10315`
* sweepList = `[0, 1, 2, ..., 8718, 8719, 8720]`
* sweepNumber = `0`
* sweepPointCount = `2063`
* sweepUnitsC = `?`
* sweepUnitsX = `sec`
* sweepUnitsY = `pA`
* sweepX = `array (1d) with values like: 0.00000, 0.00005, 0.00010, ..., 0.10300, 0.10305, 0.10310`
* sweepY = `array (1d) with values like: -34.54589, -34.36279, -34.91211, ..., -37.84179, -38.57421, -38.94043`
* tagComments = `['APV+CGP+DNQX+ON@6']`
* tagSweeps = `[3634.997576345129]`
* tagTimesMin = `[6.249166666666667]`
* tagTimesSec = `[374.95000000000005]`

## Epochs for Channel 0


```
DAC data from ABF1 files is not available.
```

## ABF1 Header

> The first several bytes of an ABF1 file contain variables     located at specific byte positions from the start of the file.     All ABF1 header values are read in this single block. 

* abfDateTime = `2018-09-06 20:04:50`
* abfDateTimeString = `2018-09-06T20:04:50.000`
* abfVersionDict = `{'major': 1, 'minor': 8, 'bugfix': 3, 'build': 0}`
* abfVersionFloat = `1.83`
* abfVersionString = `1.8.3.0`
* creatorVersionDict = `{'major': 0, 'minor': 0, 'bugfix': 0, 'build': 0}`
* creatorVersionString = `0.0.0.0`
* fADCProgrammableGain = `[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]`
* fADCRange = `10.0`
* fADCSampleInterval = `50.0`
* fDACCalibrationFactor = `[1.094730019569397, 1.0859400033950806, 1.0, 1.0]`
* fDACCalibrationOffset = `[5.0, -177.0, 0.0, 0.0]`
* fEpochInitLevel = `[112.0, 0.0, 0.0, ..., 0.0, 0.0, 0.0]`
* fEpochLevelInc = `[-20.0, 0.0, 0.0, ..., 0.0, 0.0, 0.0]`
* fFileSignature = `q=?`
* fFileVersionNumber = `1.8300000429153442`
* fInstrumentOffset = `[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]`
* fInstrumentScaleFactor = `[0.0005000000237487257, 0.0005000000237487257, 0.10000000149011612, 0.10000000149011612, 0.10000000149011612, 0.10000000149011612, 0.10000000149011612, 0.10000000149011612, 0.10000000149011612, 0.10000000149011612, 0.10000000149011612, 0.10000000149011612, 0.10000000149011612, 0.10000000149011612, 0.10000000149011612, 0.10000000149011612]`
* fSignalGain = `[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]`
* fSignalOffset = `[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]`
* fSynchTimeUnit = `0.0`
* fTelegraphAdditGain = `[10.0, 1.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0]`
* lADCResolution = `32768`
* lActualAcqLength = `18000000`
* lActualEpisodes = `8721`
* lDACFileNumEpisodes = `[0, 0]`
* lDACFilePtr = `[0, 0]`
* lDataSectionPtr = `16`
* lEpisodesPerRun = `1`
* lEpochDurationInc = `[0, 0, 0, ..., 0, 0, 0]`
* lEpochInitDuration = `[1000, 0, 0, ..., 0, 0, 0]`
* lFileStartTime = `49578`
* lNumSamplesPerEpisode = `2064`
* lNumTagEntries = `1`
* lPreTriggerSamples = `16`
* lSynchArrayPtr = `0`
* lSynchArraySize = `0`
* lTagSectionPtr = `70329`
* lTagTime = `[7499000]`
* nADCNumChannels = `1`
* nADCPtoLChannelMap = `[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]`
* nADCSamplingSeq = `[0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]`
* nActiveDACChannel = `0`
* nDataFormat = `0`
* nDigitalEnable = `0`
* nDigitalHolding = `17`
* nDigitalInterEpisode = `0`
* nDigitalValue = `[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]`
* nEpochType = `[1, 0, 0, ..., 0, 0, 0]`
* nFileStartMillisecs = `78`
* nInterEpisodeLevel = `[0, 0]`
* nNumPointsIgnored = `0`
* nOperationMode = `3`
* nTagType = `[1]`
* nTelegraphEnable = `[1, 1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0]`
* nWaveformEnable = `[1, 0]`
* nWaveformSource = `[1, 1]`
* sADCChannelName = `['IN 0', 'ADC1', 'ADC2', 'ADC3', 'ADC4', 'ADC5', 'ADC6', 'ADC7', 'ADC8', 'ADC9', 'ADC10', 'ADC11', 'ADC12', 'ADC13', 'ADC14', 'ADC15']`
* sADCUnits = `['pA', 'pA', 'pA', 'pA', 'pA', 'pA', 'pA', 'pA', 'pA', 'pA', 'pA', 'pA', 'pA', 'pA', 'pA', 'pA']`
* sComment = `['APV+CGP+DNQX+ON@6']`
* sProtocolPath = `X:\Protocols\DP\15minGapfree.pro`
