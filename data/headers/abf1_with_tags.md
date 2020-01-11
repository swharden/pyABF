# abf1_with_tags.abf

## ABF Class Methods

* abf.launchInClampFit()
* abf.saveABF1()
* abf.setSweep()
* abf.sweepD()

## ABF Class Variables

* abfDateTime = `2012-01-11 13:46:18.078000`
* abfDateTimeString = `2012-01-11T13:46:18.078`
* abfFileComment = ``
* abfFilePath = `C:/some/path/to/abf1_with_tags.abf`
* abfFolderPath = `C:/some/path`
* abfID = `abf1_with_tags`
* abfVersion = `{'major': 1, 'minor': 8, 'bugfix': 3, 'build': 0}`
* abfVersionString = `1.8.3.0`
* adcNames = `['IN 0']`
* adcUnits = `['pA']`
* channelCount = `1`
* channelList = `[0]`
* creator = `Clampex 9.2.0.11`
* creatorVersion = `{'major': 9, 'minor': 2, 'bugfix': 0, 'build': 11}`
* creatorVersionString = `9.2.0.11`
* dacNames = `['Cmd 0', 'Cmd 1', 'AO #2', 'AO #3']`
* dacUnits = `['mV', 'mV', 'mV', 'mV']`
* data = `array (2d) with values like: -34.54589, -34.36279, -34.91211, ..., -82.33642, -81.29882, -80.74950`
* dataByteStart = `8192`
* dataLengthMin = `15.0`
* dataLengthSec = `900.0`
* dataPointByteSize = `2`
* dataPointCount = `18000000`
* dataPointsPerMs = `20`
* dataRate = `20000`
* dataSecPerPoint = `5e-05`
* fileGUID = `FE9574DE-DF80-4B8F-A1E3-45EE5F243B92`
* holdingCommand = `[112.0, 0.0, 0.0, ..., 0.0, 0.0, 0.0]`
* protocol = `15minGapfree`
* protocolPath = `X:\Protocols\DP\15minGapfree.pro`
* stimulusByChannel = `[Stimulus(abf, 0)]`
* stimulusFileFolder = `C:/some/path/to/abf1_with_tags.abf`
* sweepC = `array (1d) with values like: 112.00000, 112.00000, 112.00000, ..., 112.00000, 112.00000, 112.00000`
* sweepChannel = `0`
* sweepCount = `1`
* sweepDerivative = `array (1d) with values like: 3662.10938, -10986.32812, -13427.73438, ..., 20751.95312, 10986.32812, 10986.32812`
* sweepEpochs = `Sweep epoch waveform: Step 112.00 [0:281250], Step 112.00 [281250:282250], Step 112.00 [282250:18000000]`
* sweepIntervalSec = `900.0`
* sweepLabelC = `Membrane Potential (mV)`
* sweepLabelD = `Digital Output (V)`
* sweepLabelX = `Time (seconds)`
* sweepLabelY = `Clamp Current (pA)`
* sweepLengthSec = `900.0`
* sweepList = `[0]`
* sweepNumber = `0`
* sweepPointCount = `18000000`
* sweepTimesMin = `array (1d) with values like: 0.00000`
* sweepTimesSec = `array (1d) with values like: 0.00000`
* sweepUnitsC = `mV`
* sweepUnitsX = `sec`
* sweepUnitsY = `pA`
* sweepX = `array (1d) with values like: 0.00000, 0.00005, 0.00010, ..., 899.99985, 899.99990, 899.99995`
* sweepY = `array (1d) with values like: -34.54589, -34.36279, -34.91211, ..., -82.33642, -81.29882, -80.74950`
* tagComments = `['APV+CGP+DNQX+ON@6']`
* tagSweeps = `[0.41661111111111115]`
* tagTimesMin = `[6.249166666666667]`
* tagTimesSec = `[374.95000000000005]`

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

> The first several bytes of an ABF1 file contain variables     located at specific byte positions from the start of the file.     All ABF1 header values are read in this single block.     Arrays which reference ADC entries are shown as read, no physical <-> logical     channel mapping and interpretation of the sampling sequence is done. 

* abfDateTime = `2012-01-11 13:46:18.078000`
* abfDateTimeString = `2012-01-11T13:46:18.078`
* abfVersionDict = `{'major': 1, 'minor': 8, 'bugfix': 3, 'build': 0}`
* abfVersionFloat = `1.83`
* abfVersionString = `1.8.3.0`
* creatorVersionDict = `{'major': 9, 'minor': 2, 'bugfix': 0, 'build': 11}`
* creatorVersionString = `9.2.0.11`
* fADCProgrammableGain = `[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]`
* fADCRange = `10.0`
* fADCSampleInterval = `50.0`
* fDACCalibrationFactor = `[1.094730019569397, 1.0859400033950806, 1.0, 1.0]`
* fDACCalibrationOffset = `[5.0, -177.0, 0.0, 0.0]`
* fDACFileOffset = `[0.0, 0.0]`
* fDACFileScale = `[1.0, 1.0]`
* fDACRange = `10.0`
* fEpochInitLevel = `[112.0, 0.0, 0.0, ..., 0.0, 0.0, 0.0]`
* fEpochLevelInc = `[-20.0, 0.0, 0.0, ..., 0.0, 0.0, 0.0]`
* fFileVersionNumber = `1.8300000429153442`
* fHeaderVersionNumber = `1.8300000429153442`
* fInstrumentHoldingLevel = `[0.0, 0.0, 0.0, 0.0]`
* fInstrumentOffset = `[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]`
* fInstrumentScaleFactor = `[0.0005000000237487257, 0.0005000000237487257, 0.10000000149011612, 0.10000000149011612, 0.10000000149011612, 0.10000000149011612, 0.10000000149011612, 0.10000000149011612, 0.10000000149011612, 0.10000000149011612, 0.10000000149011612, 0.10000000149011612, 0.10000000149011612, 0.10000000149011612, 0.10000000149011612, 0.10000000149011612]`
* fSignalGain = `[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]`
* fSignalOffset = `[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]`
* fSynchTimeUnit = `0.0`
* fTelegraphAdditGain = `[10.0, 1.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0]`
* fTelegraphFilter = `[2000.0, 10000.0, 2000.0, 2000.0, 2000.0, 2000.0, 2000.0, 2000.0, 2000.0, 2000.0, 2000.0, 2000.0, 2000.0, 2000.0, 2000.0, 2000.0]`
* fTelegraphMembraneCap = `[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]`
* lADCResolution = `32768`
* lActualAcqLength = `18000000`
* lActualEpisodes = `8721`
* lDACFileEpisodeNum = `[0, 0]`
* lDACFileNumEpisodes = `[0, 0]`
* lDACFilePtr = `[0, 0]`
* lDACResolution = `32768`
* lDataSectionPtr = `16`
* lEpisodesPerRun = `1`
* lEpochDurationInc = `[0, 0, 0, ..., 0, 0, 0]`
* lEpochInitDuration = `[1000, 0, 0, ..., 0, 0, 0]`
* lFileSignature = `1072315761`
* lFileStartDate = `20120111`
* lFileStartTime = `49578`
* lNumSamplesPerEpisode = `2064`
* lNumTagEntries = `1`
* lPreTriggerSamples = `16`
* lStopwatchTime = `8007`
* lSynchArrayPtr = `0`
* lSynchArraySize = `0`
* lTagSectionPtr = `70329`
* lTagTime = `[7499000]`
* nADCNumChannels = `1`
* nADCPtoLChannelMap = `[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]`
* nADCSamplingSeq = `[0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]`
* nActiveDACChannel = `0`
* nCreatorBugfixVersion = `0`
* nCreatorBuildVersion = `11`
* nCreatorMajorVersion = `9`
* nCreatorMinorVersion = `2`
* nDACFileADCNum = `[0, 0]`
* nDataFormat = `0`
* nDigitalEnable = `0`
* nDigitalHolding = `17`
* nDigitalInterEpisode = `0`
* nDigitalValue = `[15, 0, 0, 0, 0, 0, 0, 0, 0, 0]`
* nEpochType = `[1, 0, 0, ..., 0, 0, 0]`
* nExperimentType = `2`
* nFileStartMillisecs = `78`
* nFileType = `1`
* nInterEpisodeLevel = `[0, 0]`
* nMSBinFormat = `0`
* nNumPointsIgnored = `0`
* nOperationMode = `3`
* nTagType = `[1]`
* nTelegraphDACScaleFactorEnable = `[1, 1, 0, 0]`
* nTelegraphEnable = `[1, 1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0]`
* nTelegraphInstrument = `[24, 24, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]`
* nTelegraphMode = `[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]`
* nWaveformEnable = `[1, 0]`
* nWaveformSource = `[1, 1]`
* sADCChannelName = `['IN 0', 'ADC1', 'ADC2', 'ADC3', 'ADC4', 'ADC5', 'ADC6', 'ADC7', 'ADC8', 'ADC9', 'ADC10', 'ADC11', 'ADC12', 'ADC13', 'ADC14', 'ADC15']`
* sADCUnits = `['pA', 'pA', 'pA', 'pA', 'pA', 'pA', 'pA', 'pA', 'pA', 'pA', 'pA', 'pA', 'pA', 'pA', 'pA', 'pA']`
* sCreatorInfo = `Clampex`
* sDACChannelName = `['Cmd 0', 'Cmd 1', 'AO #2', 'AO #3']`
* sDACChannelUnit = `['mV', 'mV', 'mV', 'mV']`
* sDACFilePath = `['', '']`
* sFileCommentNew = ``
* sFileCommentOld = ``
* sFileGUID = `FE9574DE-DF80-4B8F-A1E3-45EE5F243B92`
* sProtocolPath = `X:\Protocols\DP\15minGapfree.pro`
* sTagComment = `['APV+CGP+DNQX+ON@6']`
* uFileGUID = `[222, 116, 149, 254, 128, 223, 143, 75, 161, 227, 69, 238, 95, 36, 59, 146]`
* ulFileCRC = `2170972679`
