# File_axon_3.abf

## ABF Class Methods

* abf.launchInClampFit()
* abf.saveABF1()
* abf.setSweep()
* abf.sweepD()

## ABF Class Variables

* abfDateTime = `2005-06-11 14:15:28.552000`
* abfDateTimeString = `2005-06-11T14:15:28.552`
* abfFileComment = ``
* abfFilePath = `C:/some/path/to/File_axon_3.abf`
* abfFolderPath = `C:/some/path`
* abfID = `File_axon_3`
* abfVersion = `{'major': 1, 'minor': 8, 'bugfix': 3, 'build': 0}`
* abfVersionString = `1.8.3.0`
* adcNames = `['stim', 'VmRK']`
* adcUnits = `['V', 'mV']`
* channelCount = `2`
* channelList = `[0, 1]`
* creator = `Clampex 9.2.0.9`
* creatorVersion = `{'major': 9, 'minor': 2, 'bugfix': 0, 'build': 9}`
* creatorVersionString = `9.2.0.9`
* dacNames = `['Iimp RK01G', 'VimpRK', '', '']`
* dacUnits = `['nA', 'mV', 'mV', 'mV']`
* data = `array (2d) with values like: -15.50000, -28.00000, -28.50000, ..., -16450.00000, -16450.00000, -16450.00000`
* dataByteStart = `8192`
* dataLengthMin = `0.10321999999999999`
* dataLengthSec = `6.193199999999999`
* dataPointByteSize = `2`
* dataPointCount = `206440`
* dataPointsPerMs = `20`
* dataRate = `20000`
* dataSecPerPoint = `5e-05`
* fileGUID = `F1AA4915-8D35-4CE7-879A-77D66DD5BFEF`
* fileUUID = `3F6D913C-85EF-0008-E26F-1400B77EF158`
* holdingCommand = `[0.0, 0.0, 0.0, ..., 0.0, 0.0, 0.0]`
* md5 = `3F6D913C85EF0008E26F1400B77EF158`
* protocol = `Cc_stim ONL`
* protocolPath = `C:\Axon\rk400\0.1G\Cc_stim ONL.pro`
* stimulusByChannel = `[Stimulus(abf, 0), Stimulus(abf, 1)]`
* stimulusFileFolder = `C:/some/path/to/File_axon_3.abf`
* sweepC = `array (1d) with values like: 0.00000, 0.00000, 0.00000, ..., 0.00000, 0.00000, 0.00000`
* sweepChannel = `0`
* sweepCount = `5`
* sweepDerivative = `array (1d) with values like: -250000.00000, -10000.00000, 0.00000, ..., 0.00000, -10000.00000, -10000.00000`
* sweepEpochs = `Sweep epoch waveform: Step 0.00 [0:322], Step 0.00 [322:347], Step 0.00 [347:357], Step 0.00 [357:382], Step 0.00 [382:20644]`
* sweepIntervalSec = `1.0322`
* sweepLabelC = `Iimp RK01G (nA)`
* sweepLabelD = `Digital Output (V)`
* sweepLabelX = `Time (seconds)`
* sweepLabelY = `stim (V)`
* sweepLengthSec = `1.0322`
* sweepList = `[0, 1, 2, 3, 4]`
* sweepNumber = `0`
* sweepPointCount = `20644`
* sweepTimesMin = `array (1d) with values like: 0.00000, 0.01720, 0.03441, 0.05161, 0.06881`
* sweepTimesSec = `array (1d) with values like: 0.00000, 1.03220, 2.06440, 3.09660, 4.12880`
* sweepUnitsC = `nA`
* sweepUnitsX = `sec`
* sweepUnitsY = `V`
* sweepX = `array (1d) with values like: 0.00000, 0.00005, 0.00010, ..., 1.03205, 1.03210, 1.03215`
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

> The first several bytes of an ABF1 file contain variables     located at specific byte positions from the start of the file.     All ABF1 header values are read in this single block.     Arrays which reference ADC entries are shown as read, no physical <-> logical     channel mapping and interpretation of the sampling sequence is done. 

* abfDateTime = `2005-06-11 14:15:28.552000`
* abfDateTimeString = `2005-06-11T14:15:28.552`
* abfVersionDict = `{'major': 1, 'minor': 8, 'bugfix': 3, 'build': 0}`
* abfVersionFloat = `1.83`
* abfVersionString = `1.8.3.0`
* creatorVersionDict = `{'major': 9, 'minor': 2, 'bugfix': 0, 'build': 9}`
* creatorVersionString = `9.2.0.9`
* fADCProgrammableGain = `[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 8.0, 4.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]`
* fADCRange = `10.239999771118164`
* fADCSampleInterval = `25.0`
* fDACCalibrationFactor = `[1.0, 1.0, 1.0, 1.0]`
* fDACCalibrationOffset = `[0.0, 0.0, 0.0, 0.0]`
* fDACFileOffset = `[0.0, 0.0]`
* fDACFileScale = `[0.0, 0.0]`
* fDACRange = `10.239999771118164`
* fEpochInitLevel = `[0.0, 0.0, 0.0, ..., 0.0, 0.0, 0.0]`
* fEpochLevelInc = `[0.0, 0.0, 0.0, ..., 0.0, 0.0, 0.0]`
* fFileVersionNumber = `1.8300000429153442`
* fHeaderVersionNumber = `1.8300000429153442`
* fInstrumentHoldingLevel = `[0.0, 0.0, 0.0, 0.0]`
* fInstrumentOffset = `[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]`
* fInstrumentScaleFactor = `[0.009999999776482582, 9.999999747378752e-05, 1.0, 1.0, 1.0, 1.0, 0.0020000000949949026, 0.009999999776482582, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]`
* fSignalGain = `[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]`
* fSignalOffset = `[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]`
* fSynchTimeUnit = `12.5`
* fTelegraphAdditGain = `[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]`
* fTelegraphFilter = `[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]`
* fTelegraphMembraneCap = `[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]`
* lADCResolution = `32768`
* lActualAcqLength = `206440`
* lActualEpisodes = `5`
* lDACFileEpisodeNum = `[0, 0]`
* lDACFileNumEpisodes = `[0, 0]`
* lDACFilePtr = `[0, 0]`
* lDACResolution = `32768`
* lDataSectionPtr = `16`
* lEpisodesPerRun = `40`
* lEpochDurationInc = `[0, 0, 0, ..., 0, 0, 0]`
* lEpochInitDuration = `[1000, 25, 10, ..., 0, 0, 0]`
* lFileSignature = `1072315761`
* lFileStartDate = `20050611`
* lFileStartTime = `51328`
* lNumSamplesPerEpisode = `41288`
* lNumTagEntries = `0`
* lPreTriggerSamples = `20`
* lStopwatchTime = `5724`
* lSynchArrayPtr = `823`
* lSynchArraySize = `5`
* lTagSectionPtr = `0`
* lTagTime = `[]`
* nADCNumChannels = `2`
* nADCPtoLChannelMap = `[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]`
* nADCSamplingSeq = `[5, 7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]`
* nActiveDACChannel = `0`
* nCreatorBugfixVersion = `0`
* nCreatorBuildVersion = `9`
* nCreatorMajorVersion = `9`
* nCreatorMinorVersion = `2`
* nDACFileADCNum = `[0, 0]`
* nDataFormat = `0`
* nDigitalEnable = `1`
* nDigitalHolding = `16`
* nDigitalInterEpisode = `0`
* nDigitalValue = `[0, 8, 0, 8, 0, 0, 0, 0, 0, 0]`
* nEpochType = `[0, 1, 1, ..., 0, 0, 0]`
* nExperimentType = `0`
* nFileStartMillisecs = `552`
* nFileType = `1`
* nInterEpisodeLevel = `[0, 0]`
* nMSBinFormat = `0`
* nNumPointsIgnored = `0`
* nOperationMode = `5`
* nTagType = `[]`
* nTelegraphDACScaleFactorEnable = `[0, 0, 0, 0]`
* nTelegraphEnable = `[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]`
* nTelegraphInstrument = `[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]`
* nTelegraphMode = `[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]`
* nWaveformEnable = `[1, 0]`
* nWaveformSource = `[1, 1]`
* sADCChannelName = `['10Vm', 'ImRK01G1b', 'IN 2', 'IN 3', 'IN 4', 'stim', 'ImRK01G20', 'VmRK', 'IN 8', 'IN 9', 'IN 10', 'IN 11', 'IN 12', 'IN 13', 'IN 14', 'IN 15']`
* sADCUnits = `['mV', 'pA', 'V', 'V', 'V', 'V', 'pA', 'mV', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V']`
* sCreatorInfo = `Clampex`
* sDACChannelName = `['Iimp RK01G', 'VimpRK', '', '']`
* sDACChannelUnit = `['nA', 'mV', 'mV', 'mV']`
* sDACFilePath = `['\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00']`
* sFileCommentNew = ``
* sFileCommentOld = ``
* sFileGUID = `F1AA4915-8D35-4CE7-879A-77D66DD5BFEF`
* sProtocolPath = `C:\Axon\rk400\0.1G\Cc_stim ONL.pro`
* sTagComment = `[]`
* uFileGUID = `[21, 73, 170, 241, 53, 141, 231, 76, 135, 154, 119, 214, 109, 213, 191, 239]`
* ulFileCRC = `3865876149`
