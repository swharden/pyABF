# File_axon_2.abf

## ABF Class Methods

* abf.launchInClampFit()
* abf.saveABF1()
* abf.setSweep()
* abf.sweepD()

## ABF Class Variables

* abfDateTime = `2005-06-11 14:15:00.712000`
* abfDateTimeString = `2005-06-11T14:15:00.712`
* abfFileComment = ``
* abfFilePath = `C:/some/path/to/File_axon_2.abf`
* abfFolderPath = `C:/some/path`
* abfID = `File_axon_2`
* abfVersion = `{'major': 1, 'minor': 8, 'bugfix': 3, 'build': 0}`
* abfVersionString = `1.8.3.0`
* adcNames = `['10Vm']`
* adcUnits = `['mV']`
* channelCount = `1`
* channelList = `[0]`
* creator = `AxoScope 9.2.0.9`
* creatorVersion = `{'major': 9, 'minor': 2, 'bugfix': 0, 'build': 9}`
* creatorVersionString = `9.2.0.9`
* dacNames = `['Iimp RK01G', 'VimpRK', '', '']`
* dacUnits = `['nA', 'mV', 'mV', 'mV']`
* data = `array (2d) with values like: -55.28870, -55.25513, -55.25513, ..., -50.45471, -50.42114, -50.42114`
* dataByteStart = `8192`
* dataLengthMin = `20.0`
* dataLengthSec = `1200.0`
* dataPointByteSize = `2`
* dataPointCount = `1200000`
* dataPointsPerMs = `1`
* dataRate = `1000`
* dataSecPerPoint = `0.001`
* fileGUID = `E88FB723-FA82-4C78-865A-12FE3F667099`
* fileUUID = `E7C06015-FD26-AEF8-329A-1A0F18598935`
* holdingCommand = `[0.0, 0.0, 0.0, ..., 0.0, 0.0, 0.0]`
* md5 = `E7C06015FD26AEF8329A1A0F18598935`
* protocol = `Cc_minidigi`
* protocolPath = `C:\Axon\rk400\0.1G\minidigi\Cc_minidigi.pro`
* stimulusByChannel = `[Stimulus(abf, 0)]`
* stimulusFileFolder = `C:/some/path/to/File_axon_2.abf`
* sweepC = `array (1d) with values like: 0.00000, 0.00000, 0.00000, ..., 0.00000, 0.00000, 0.00000`
* sweepChannel = `0`
* sweepCount = `1`
* sweepDerivative = `array (1d) with values like: 33.56934, 0.00000, 33.56934, ..., 33.56934, 0.00000, 0.00000`
* sweepEpochs = `Sweep epoch waveform: Step 0.00 [0:18750], Step 0.00 [18750:1200000]`
* sweepIntervalSec = `1200.0`
* sweepLabelC = `Applied Current (pA)`
* sweepLabelD = `Digital Output (V)`
* sweepLabelX = `Time (seconds)`
* sweepLabelY = `Membrane Potential (mV)`
* sweepLengthSec = `1200.0`
* sweepList = `[0]`
* sweepNumber = `0`
* sweepPointCount = `1200000`
* sweepTimesMin = `array (1d) with values like: 0.00000`
* sweepTimesSec = `array (1d) with values like: 0.00000`
* sweepUnitsC = `nA`
* sweepUnitsX = `sec`
* sweepUnitsY = `mV`
* sweepX = `array (1d) with values like: 0.00000, 0.00100, 0.00200, ..., 1199.99700, 1199.99800, 1199.99900`
* sweepY = `array (1d) with values like: -55.28870, -55.25513, -55.25513, ..., -50.45471, -50.42114, -50.42114`
* tagComments = `['Clampex start acquisition', 'C:\\Axon\\rsultats\\06-05\\11-06-05\\05611005.abf', 'Clampex end (1)', 'Clampex start acquisition']`
* tagSweeps = `[0.022304166666666667, 0.3555841666666667, 0.3555841666666667, 0.5211441666666667]`
* tagTimesMin = `[0.44608333333333333, 7.111683333333334, 7.111683333333334, 10.422883333333335]`
* tagTimesSec = `[26.765, 426.701, 426.701, 625.373]`

## Epochs for Channel 0


```
DAC waveform is not enabled
```

## ABF1 Header

> The first several bytes of an ABF1 file contain variables     located at specific byte positions from the start of the file.     All ABF1 header values are read in this single block.     Arrays which reference ADC entries are shown as read, no physical <-> logical     channel mapping and interpretation of the sampling sequence is done. 

* abfDateTime = `2005-06-11 14:15:00.712000`
* abfDateTimeString = `2005-06-11T14:15:00.712`
* abfVersionDict = `{'major': 1, 'minor': 8, 'bugfix': 3, 'build': 0}`
* abfVersionFloat = `1.83`
* abfVersionString = `1.8.3.0`
* creatorVersionDict = `{'major': 9, 'minor': 2, 'bugfix': 0, 'build': 9}`
* creatorVersionString = `9.2.0.9`
* fADCProgrammableGain = `[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]`
* fADCRange = `11.0`
* fADCSampleInterval = `1000.0`
* fDACCalibrationFactor = `[1.0, 1.0, 1.0, 1.0]`
* fDACCalibrationOffset = `[0.0, 0.0, 0.0, 0.0]`
* fDACFileOffset = `[0.0, 0.0]`
* fDACFileScale = `[0.0, 0.0]`
* fDACRange = `1.0`
* fEpochInitLevel = `[0.0, 0.0, 0.0, ..., 0.0, 0.0, 0.0]`
* fEpochLevelInc = `[0.0, 0.0, 0.0, ..., 0.0, 0.0, 0.0]`
* fFileVersionNumber = `1.8300000429153442`
* fHeaderVersionNumber = `1.8300000429153442`
* fInstrumentHoldingLevel = `[0.0, 0.0, 0.0, 0.0]`
* fInstrumentOffset = `[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]`
* fInstrumentScaleFactor = `[0.009999999776482582, 9.999999747378752e-05, 1.0, 1.0, 1.0, 1.0, 9.999999747378752e-05, 0.009999999776482582, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]`
* fSignalGain = `[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]`
* fSignalOffset = `[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]`
* fSynchTimeUnit = `0.0`
* fTelegraphAdditGain = `[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]`
* fTelegraphFilter = `[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]`
* fTelegraphMembraneCap = `[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]`
* lADCResolution = `32768`
* lActualAcqLength = `1200000`
* lActualEpisodes = `4688`
* lDACFileEpisodeNum = `[0, 0]`
* lDACFileNumEpisodes = `[0, 0]`
* lDACFilePtr = `[0, 0]`
* lDACResolution = `1`
* lDataSectionPtr = `16`
* lEpisodesPerRun = `1`
* lEpochDurationInc = `[0, 0, 0, ..., 0, 0, 0]`
* lEpochInitDuration = `[0, 0, 0, ..., 0, 0, 0]`
* lFileSignature = `1072315761`
* lFileStartDate = `20050611`
* lFileStartTime = `51300`
* lNumSamplesPerEpisode = `256`
* lNumTagEntries = `4`
* lPreTriggerSamples = `20`
* lStopwatchTime = `5632`
* lSynchArrayPtr = `0`
* lSynchArraySize = `0`
* lTagSectionPtr = `4704`
* lTagTime = `[26765, 426701, 426701, 625373]`
* nADCNumChannels = `1`
* nADCPtoLChannelMap = `[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]`
* nADCSamplingSeq = `[0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]`
* nActiveDACChannel = `0`
* nCreatorBugfixVersion = `0`
* nCreatorBuildVersion = `9`
* nCreatorMajorVersion = `9`
* nCreatorMinorVersion = `2`
* nDACFileADCNum = `[0, 0]`
* nDataFormat = `0`
* nDigitalEnable = `0`
* nDigitalHolding = `16`
* nDigitalInterEpisode = `0`
* nDigitalValue = `[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]`
* nEpochType = `[0, 0, 0, ..., 0, 0, 0]`
* nExperimentType = `1`
* nFileStartMillisecs = `712`
* nFileType = `1`
* nInterEpisodeLevel = `[0, 0]`
* nMSBinFormat = `0`
* nNumPointsIgnored = `0`
* nOperationMode = `3`
* nTagType = `[1, 4, 1, 1]`
* nTelegraphDACScaleFactorEnable = `[0, 0, 0, 0]`
* nTelegraphEnable = `[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]`
* nTelegraphInstrument = `[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]`
* nTelegraphMode = `[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]`
* nWaveformEnable = `[0, 0]`
* nWaveformSource = `[0, 0]`
* sADCChannelName = `['10Vm', 'ImRK01G1b', 'IN 2', 'IN 3', 'IN 4', 'stim', 'ImRK01G1', 'VmRK', 'IN 8', 'IN 9', 'IN 10', 'IN 11', 'IN 12', 'IN 13', 'IN 14', 'IN 15']`
* sADCUnits = `['mV', 'pA', 'V', 'V', 'V', 'V', 'pA', 'mV', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V']`
* sCreatorInfo = `AxoScope`
* sDACChannelName = `['Iimp RK01G', 'VimpRK', '', '']`
* sDACChannelUnit = `['nA', 'mV', 'mV', 'mV']`
* sDACFilePath = `['\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00']`
* sFileCommentNew = ``
* sFileCommentOld = ``
* sFileGUID = `E88FB723-FA82-4C78-865A-12FE3F667099`
* sProtocolPath = `C:\Axon\rk400\0.1G\minidigi\Cc_minidigi.pro`
* sTagComment = `['Clampex start acquisition', 'C:\\Axon\\rsultats\\06-05\\11-06-05\\05611005.abf', 'Clampex end (1)', 'Clampex start acquisition']`
* uFileGUID = `[35, 183, 143, 232, 130, 250, 120, 76, 134, 90, 18, 254, 63, 102, 112, 153]`
* ulFileCRC = `990449324`
