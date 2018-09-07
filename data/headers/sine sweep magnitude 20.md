# sine sweep magnitude 20.abf

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

* abfDateTime = `2013-12-17 15:27:56.218000`
* abfDateTimeString = `2013-12-17T15:27:56.218000`
* abfFileComment = ``
* abfFilePath = `C:/some/path/to/sine sweep magnitude 20.abf`
* abfID = `sine sweep magnitude 20`
* abfVersion = `{'major': 2, 'minor': 0, 'bugfix': 0, 'build': 0}`
* abfVersionString = `2.0.0.0`
* adcNames = `['IN 0']`
* adcUnits = `['']`
* channelCount = `1`
* channelList = `[0]`
* creatorVersion = `{'major': 10, 'minor': 2, 'bugfix': 0, 'build': 14}`
* creatorVersionString = `10.2.0.14`
* dacNames = `['Cmd 0']`
* dacUnits = `['mV']`
* data = `[[ 0.      0.      0.     ... 15.8339 16.0741 16.3103]]`
* dataByteStart = `3584`
* dataPointByteSize = `4`
* dataPointCount = `100000`
* dataPointsPerMs = `10`
* dataRate = `10000`
* dataSecPerPoint = `0.0001`
* epochPoints = `[0, 1562, 100000]`
* epochValues = `[-70.0, -70.0, -70.0]`
* fileGUID = `{FA90BECA-056E-4757-9776-ADFD60958D8D}`
* holdingCommand = `[-70.0, 0.0, 0.0, 0.0]`
* protocol = `(untitled)`
* protocolPath = `(untitled)`
* stimulusByChannel = `[ChannelEpochs(ABF, 0)]`
* sweepC = `[-70. -70. -70. ... -70. -70. -70.]`
* sweepChannel = `0`
* sweepCount = `1`
* sweepLabelC = `Cmd 0 (mV)`
* sweepLabelX = `time (seconds)`
* sweepLabelY = `IN 0 ()`
* sweepLengthSec = `10.0`
* sweepList = `[0]`
* sweepNumber = `0`
* sweepPointCount = `100000`
* sweepUnitsC = `mV`
* sweepUnitsX = `sec`
* sweepUnitsY = ``
* sweepX = `[0.     0.0001 0.0002 ... 9.9997 9.9998 9.9999]`
* sweepY = `[ 0.      0.      0.     ... 15.8339 16.0741 16.3103]`
* tagComments = `[]`
* tagSweeps = `[]`
* tagTimesMin = `[]`
* tagTimesSec = `[]`

## Epochs for Channel 0


```
DAC waveform is controlled by epoch table:
                Ch0 EPOCH
                     Type
         First Level (mV)
         Delta Level (mV)
 First Duration (samples)
 Delta Duration (samples)
   Train Period (samples)
    Pulse Width (samples)
```

## ABF2 Header

> The first several bytes of an ABF2 file contain variables     located at specific byte positions from the start of the file. 

* abfDateTime = `2013-12-17 15:27:56.218000`
* abfDateTimeString = `2013-12-17T15:27:56.218000`
* abfVersionDict = `{'major': 2, 'minor': 0, 'bugfix': 0, 'build': 0}`
* abfVersionFloat = `2.0`
* abfVersionString = `2.0.0.0`
* creatorVersionDict = `{'major': 10, 'minor': 2, 'bugfix': 0, 'build': 14}`
* creatorVersionFloat = `102.014`
* creatorVersionString = `10.2.0.14`
* fFileSignature = `ABF2`
* fFileVersionNumber = `[0, 0, 0, 2]`
* lActualEpisodes = `1`
* nCRCEnable = `0`
* nDataFormat = `1`
* nFileType = `1`
* nSimultaneousScan = `1`
* sFileGUID = `{FA90BECA-056E-4757-9776-ADFD60958D8D}`
* uCreatorNameIndex = `1`
* uCreatorVersion = `[14, 0, 2, 10]`
* uFileCRC = `0`
* uFileGUID = `[202, 190, 144, 250, 110, 5, 87, 71, 151, 118, 173, 253, 96, 149, 52, 141]`
* uFileInfoSize = `512`
* uFileStartDate = `20131217`
* uFileStartTimeMS = `55676218`
* uModifierNameIndex = `2`
* uModifierVersion = `167903246`
* uProtocolPathIndex = `3`
* uStopwatchTime = `696`

## SectionMap

> Reading three numbers (int, int, long) at specific byte locations     yields the block position, byte size, and item count of specific     data stored in sections. Note that a block is 512 bytes. Some of     these sections are not read by this class because they are either     not useful for my applications, typically unused, or have an     unknown memory structure. 

* ADCPerDACSection = `[0, 0, 0]`
* ADCSection = `[2, 128, 1]`
* AnnotationSection = `[0, 0, 0]`
* DACSection = `[3, 256, 4]`
* DataSection = `[7, 4, 100000]`
* DeltaSection = `[0, 0, 0]`
* EpochPerDACSection = `[0, 0, 0]`
* EpochSection = `[0, 0, 0]`
* MathSection = `[0, 0, 0]`
* ProtocolSection = `[1, 512, 1]`
* ScopeSection = `[0, 0, 0]`
* StatsRegionSection = `[5, 128, 1]`
* StatsSection = `[0, 0, 0]`
* StringsSection = `[6, 113, 12]`
* SynchArraySection = `[789, 8, 1]`
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
* fSecondsPerRun = `10.0`
* fStatisticsPeriod = `1.0`
* fSynchTimeUnit = `20.0`
* fTrialStartToStart = `0.0`
* fTriggerThreshold = `0.0`
* lADCResolution = `32768`
* lAverageCount = `1`
* lDACResolution = `32768`
* lEpisodesPerRun = `1`
* lFileCommentIndex = `0`
* lFinishDisplayNum = `0`
* lNumSamplesPerEpisode = `100000`
* lNumberOfTrials = `1`
* lPreTriggerSamples = `20`
* lRunsPerTrial = `1`
* lSamplesPerTrace = `16384`
* lStartDisplayNum = `1`
* lStatisticsMeasurements = `5`
* lTimeHysteresis = `1`
* nActiveDACChannel = `0`
* nAllowExternalTags = `0`
* nAlternateDACOutputState = `0`
* nAlternateDigitalOutputState = `0`
* nAutoAnalyseEnable = `1`
* nAutoTriggerStrategy = `1`
* nAverageAlgorithm = `0`
* nAveragingMode = `0`
* nChannelStatsStrategy = `0`
* nCommentsEnable = `0`
* nDigitalDACChannel = `0`
* nDigitalEnable = `0`
* nDigitalHolding = `0`
* nDigitalInterEpisode = `0`
* nDigitalTrainActiveLogic = `1`
* nDigitizerADCs = `16`
* nDigitizerDACs = `4`
* nDigitizerSynchDigitalOuts = `8`
* nDigitizerTotalDigitalOuts = `16`
* nDigitizerType = `6`
* nExperimentType = `2`
* nExternalTagType = `2`
* nFirstEpisodeInRun = `0`
* nLTPType = `0`
* nLevelHysteresis = `64`
* nManualInfoStrategy = `0`
* nOperationMode = `5`
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

* bEnabledDuringPN = `[0]`
* fADCDisplayAmplification = `[1.0]`
* fADCDisplayOffset = `[0.0]`
* fADCProgrammableGain = `[1.0]`
* fInstrumentOffset = `[0.0]`
* fInstrumentScaleFactor = `[0.0005000000237487257]`
* fPostProcessLowpassFilter = `[100000.0]`
* fSignalGain = `[1.0]`
* fSignalHighpassFilter = `[1.0]`
* fSignalLowpassFilter = `[5000.0]`
* fSignalOffset = `[0.0]`
* fTelegraphAccessResistance = `[0.0]`
* fTelegraphAdditGain = `[10.0]`
* fTelegraphFilter = `[2000.0]`
* fTelegraphMembraneCap = `[0.0]`
* lADCChannelNameIndex = `[4]`
* lADCUnitsIndex = `[0]`
* nADCNum = `[0]`
* nADCPtoLChannelMap = `[0]`
* nADCSamplingSeq = `[0]`
* nHighpassFilterType = `[0]`
* nLowpassFilterType = `[0]`
* nPostProcessLowpassFilterType = `['\x00']`
* nStatsChannelPolarity = `[0]`
* nTelegraphEnable = `[1]`
* nTelegraphInstrument = `[24]`
* nTelegraphMode = `[0]`
* sTelegraphInstrument = `['MultiClamp 700']`

## DACSection

> Information about the DAC (what gets clamped).     There is 1 item per DAC. 

* fBaselineDuration = `[1.0, 1.0, 1.0, 1.0]`
* fBaselineLevel = `[0.0, 0.0, 0.0, 0.0]`
* fDACCalibrationFactor = `[1.0008957386016846, 1.001062273979187, 1.0010067224502563, 1.0009512901306152]`
* fDACCalibrationOffset = `[1.0, -1.0, -3.0, 1.0]`
* fDACFileOffset = `[0.0, 0.0, 0.0, 0.0]`
* fDACFileScale = `[1.0, 1.0, 1.0, 1.0]`
* fDACHoldingLevel = `[-70.0, 0.0, 0.0, 0.0]`
* fDACScaleFactor = `[20.0, 20.0, 20.0, 20.0]`
* fInstrumentHoldingLevel = `[0.0, 0.0, 0.0, 0.0]`
* fMembTestPostSettlingTimeMS = `[100.0, 100.0, 100.0, 100.0]`
* fMembTestPreSettlingTimeMS = `[100.0, 100.0, 100.0, 100.0]`
* fPNHoldingLevel = `[0.0, 0.0, 0.0, 0.0]`
* fPNInterpulse = `[0.0, 0.0, 0.0, 0.0]`
* fPNSettlingTime = `[100.0, 100.0, 100.0, 100.0]`
* fPostTrainLevel = `[0.0, 0.0, 0.0, 0.0]`
* fPostTrainPeriod = `[10.0, 10.0, 10.0, 10.0]`
* fStepDuration = `[1.0, 1.0, 1.0, 1.0]`
* fStepLevel = `[0.0, 0.0, 0.0, 0.0]`
* lConditNumPulses = `[0, 0, 0, 0]`
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
* nPNNumPulses = `[4, 4, 4, 4]`
* nPNPolarity = `[1, 1, 1, 1]`
* nPNPosition = `[0, 0, 0, 0]`
* nTelegraphDACScaleFactorEnable = `[1, 1, 0, 0]`
* nWaveformEnable = `[1, 0, 0, 0]`
* nWaveformSource = `[1, 1, 1, 1]`

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

* strings = `[b'SSCH\x01\x00\x00\x00\x0c\x00\x00\x00\n\x00\x00\x00E\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00clampex\x00clampfit\x00(untitled)\x00IN 0\x00Cmd 0\x00mV\x00Cmd 1\x00mV\x00Cmd 2\x00mV\x00Cmd 3\x00mV\x00', b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xbd7\x066\xbd7\x067\xb5\xfe\x967\xbd7\x068\x17\xb7Q8\xb5\xfe\x968Y\x85\xcd8\xbd7\x069\x8b\xde)9\x17\xb7Q9b\xc1}9\xb5\xfe\x969\x97', b'5\xb19Y\x85\xcd9\xfa\xed\xeb9\xbd7\x06:\xed\x84\x17:\x8b\xde):\x99D=:\x17\xb7Q:\x036g:b\xc1}:\x96\xac\x8a:\xb5\xfe\x96:\n\xd7\xa3:\x975\xb1:]\x1a\xbf:Y\x85\xcd:\x8fv\xdc:\xfa\xed\xeb:\x9d\xeb\xfb:\xbd7\x06;\xc6\xbc\x0e;\xed\x84\x17;.\x90 ;\x8b\xde);\x05p3;\x99D=;K\\G;\x17\xb7Q;\xffT', b'\\;\x036g;&Zr;b\xc1};\xdd\xb5\x84;\x96\xac\x8a;\xde\xc4\x90;\xb5\xfe\x96;\x19Z\x9d;\n\xd7\xa3;\x89u\xaa;\x975\xb1;4\x17\xb8;]\x1a\xbf;\x14?\xc6;Y\x85\xcd;,\xed\xd4;\x8fv\xdc;}!\xe4;\xfa\xed\xeb;\x04\xdc\xf3;\x9d\xeb\xfb;c\x0e\x02<\xbd7\x06<\xdeq\n<\xc6\xbc\x0e<u\x18\x13<\xed\x84\x17<*\x02\x1c', b'<-\x90 <\xf8.%<\x8a\xde)<\xe4\x9e.<\x04p3<\xebQ8<\x99D=<\rHB<J\\G<M\x81L<\x16\xb7Q<\xa9\xfdV<\xfeT\\<\x1e\xbda<\x026g<\xb0\xbfl<%Zr<]\x05x<`\xc1}<\x13\xc7\x81<\xdc\xb5\x84<\x08\xad\x87<\x95\xac\x8a<\x88\xb4\x8d<\xdd\xc4\x90<\x97\xdd\x93<\xb4\xfe\x96<3(\x9a<', b'\x17Z\x9d<]\x94\xa0<\x08\xd7\xa3<\x17"\xa7<\x88u\xaa<]\xd1\xad<\x945\xb1<1\xa2\xb4<1\x17\xb8<\x93\x94\xbb<Z\x1a\xbf<\x83\xa8\xc2<\x11?\xc6<\x03\xde\xc9<U\x85\xcd<\x0e5\xd1<(\xed\xd4<\xa7\xad\xd8<\x8bv\xdc<\xcfG\xe0<y!\xe4<\x84\x03\xe8<\xf5\xed\xeb<\xc9\xe0\xef<\xff\xdb\xf3<\x9a\xdf\xf7<\x97\xeb\xfb<\xf9\xff\xff<`', b'\x0e\x02=\xf3 \x04=\xb97\x06=\xb0R\x08=\xdaq\n=6\x95\x0c=\xc2\xbc\x0e=\x81\xe8\x10=p\x18\x13=\x93L\x15=\xe7\x84\x17=l\xc1\x19=$\x02\x1c=\x0cG\x1e=\'\x90 =t\xdd"=\xf1.%=\xa2\x84\'=\x83\xde)=\x97<,=\xdc\x9e.=R\x051=\xfbo3=\xd5\xde5=\xe1Q8= \xc9:=\x8eD==0\xc4?=\x02H', b'B=\x07\xd0D=>\\G=\xa5\xecI=@\x81L=\n\x1aO=\x08\xb7Q=8XT=\x99\xfdV=)\xa7Y=\xeeT\\=\xe5\x06_=\r\xbda=gwd=\xef5g=\xad\xf8i=\x9c\xbfl=\xbd\x8ao=\x0fZr=\x90-u=F\x05x=.\xe1z=G\xc1}=\xc9R\x80=\x06\xc7\x81=]=\x83=\xce\xb5\x84=W0\x86=\xf9\xac\x87', b'=\xb1+\x89=\x85\xac\x8a=r/\x8c=w\xb4\x8d=\x95;\x8f=\xca\xc4\x90=\x1aP\x92=\x83\xdd\x93=\x05m\x95=\x9f\xfe\x96=P\x92\x98=\x1d(\x9a=\x02\xc0\x9b=\x00Z\x9d=\x16\xf6\x9e=D\x94\xa0=\x8c4\xa2=\xee\xd6\xa3=h{\xa5=\xfb!\xa7=\xa5\xca\xa8=iu\xaa=G"\xac==\xd1\xad=M\x82\xaf=r5\xb1=\xb3\xea\xb2=\r\xa2\xb4=']`

## StringsIndexed

> This object provides easy access to strings which are scattered around     the header files. The StringsSection contains strings, but various headers     contain values which point to a certain string index. This class connects     the two, and provides direct access to those strings by their indexed name. 

* lADCChannelName = `['IN 0']`
* lADCUnits = `['']`
* lDACChannelName = `['Cmd 0', 'Cmd 1', 'Cmd 2', 'Cmd 3']`
* lDACChannelUnits = `['mV', 'mV', 'mV', 'mV']`
* lDACFilePath = `['', '', '', '']`
* lFileComment = ``
* nLeakSubtractADC = `['', '', '', '']`
* uCreatorName = `clampex`
* uModifierName = `clampfit`
* uProtocolPath = `(untitled)`
