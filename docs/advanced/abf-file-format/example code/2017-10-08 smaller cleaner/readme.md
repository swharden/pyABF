**NOTES ABOUT EXAMPLE CODE:** This folder contains a standalone collection of code created from a snapshot of a work-in-progress project. It is meant for educational purposes only, and better code which does the same things may be found elsewhere
in this project.

# Smaller and Cleaner (modularized) ABF Reader
* I'm moving toward making an ABF class. I'm working out how to best separate the files. 
* obviously I took the structure code [varfmt.py](varfmt.py) out of the abf header reading script [reader.py](reader.py)
* standardized ALL data blocks, (headers and sections) to be a list. Things which aren't normally a list (like the header) are a list of length 1. Things like epochs with an element for each epoch are a list all the same. This simplifies functions which read, add to, flatten, or display data.
* rather than have a standalone function to build the flattened header dictionary at the end, I stuck that code in the struct function so every time a variable is looked up it is added to the global.
* I also removed many of the class variables since they don't need to be stored (i.e., `self.secHeader` and `self.secMap` since their data is in `self.header`)

## Standalone Code (so small!)

```python
import struct
import varfmt

class ABFheader:
    def __init__(self,abfFileName):
        """Given an ABF2 file, parse its header and provide simple access to its settings and data."""
        self.abfFileName=abfFileName
        self.header={}
        self._fb = open(abfFileName,'rb')
        self._fileReadStructMap(varfmt.HEADER)
        self._fileReadStructMap(varfmt.SECTIONS,76,16)
        self._fileReadSection('ProtocolSection',varfmt.PROTO)
        self._fileReadSection('ADCSection',varfmt.ADC)
        self._fileReadSection('DACSection',varfmt.DAC)
        self._fileReadSection('EpochPerDACSection',varfmt.EPPERDAC)
        self._fileReadSection('EpochSection',varfmt.EPSEC)      
        self._fileReadSection('TagSection',varfmt.TAGS)        
        self._fb.close()
        for key in [key for key in self.header.keys() if len(self.header[key])==1]:
            self.header[key]=self.header[key][0]
        
    def _fileReadStructMap(self,structMap,startByte=0,fixedOffset=None):
        """Given a string of varName_varFormat structs, get the objects from the file."""
        self._fb.seek(startByte)
        for structCode in structMap.replace("\n","").split(","):
            varName,varFormat=structCode.strip().split("_")
            varVal=struct.unpack(varFormat,self._fb.read(struct.calcsize(varFormat)))
            varVal=varVal if len(varVal)>1 else varVal[0]
            if not varName in self.header: self.header[varName]=[]
            self.header[varName]=self.header[varName]+[varVal]
            if fixedOffset: self._fb.read(fixedOffset-struct.calcsize(varFormat))

    def _fileReadSection(self,sectionName,structMap):
        """Read a structure map repeatedly according to its name in the section map."""
        entryStartBlock,entryBytes,entryCount=self.header[sectionName][0]
        for entryNumber in range(entryCount):
            self._fileReadStructMap(structMap,entryStartBlock*512+entryNumber*entryBytes)
                
    def showHeader(self):
        for key in sorted(self.header.keys()):
            print("%s = %s"%(key,self.header[key]))

if __name__=="__main__":
    abf=ABFheader(R"../../../../data/17o05028_ic_steps.abf")
    abf.showHeader()
```

### Output when run
```
ADCPerDACSection = (0, 0, 0)
ADCSection = (2, 128, 1)
AnnotationSection = (0, 0, 0)
DACSection = (3, 256, 8)
DataSection = (13, 2, 960000)
DeltaSection = (0, 0, 0)
EpochPerDACSection = (7, 48, 5)
EpochSection = (8, 32, 5)
FileGUID = 813622370
MathSection = (0, 0, 0)
ProtocolSection = (1, 512, 1)
ScopeSection = (11, 769, 1)
StatsRegionSection = (9, 128, 1)
StatsSection = (0, 0, 0)
StringsSection = (10, 194, 20)
SynchArraySection = (3763, 8, 16)
TagSection = (0, 0, 0)
UserListSection = (0, 0, 0)
VoiceTagSection = (0, 0, 0)
bEnableFileCompression = 0
bEnabledDuringPN = 0
fADCDisplayAmplification = 12.307504653930664
fADCDisplayOffset = -21.75
fADCProgrammableGain = 1.0
fADCRange = 10.0
fADCSequenceInterval = 50.0
fAverageWeighting = 0.10000000149011612
fBaselineDuration = [1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0]
fBaselineLevel = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
fCellID = (0.0, 0.0, 0.0)
fDACCalibrationFactor = [1.0008957386016846, 1.0010067224502563, 1.000895619392395, 1.0008400678634644, 1.0, 1.0, 1.0, 1.0]
fDACCalibrationOffset = [0.0, -2.0, -3.0, 2.0, 0.0, 0.0, 0.0, 0.0]
fDACFileOffset = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
fDACFileScale = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
fDACHoldingLevel = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
fDACRange = 10.0
fDACScaleFactor = [400.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0]
fEpisodeStartToStart = 0.0
fEpochInitLevel = [0.0, -50.0, 0.0, -50.0, -50.0]
fEpochLevelInc = [0.0, 10.0, 0.0, 0.0, 10.0]
fFileSignature = b'ABF2'
fFileVersionNumber = (0, 0, 6, 2)
fFirstRunDelayS = 0.0
fInstrumentHoldingLevel = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
fInstrumentOffset = 0.0
fInstrumentScaleFactor = 0.009999999776482582
fMembTestPostSettlingTimeMS = [100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0]
fMembTestPreSettlingTimeMS = [100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0]
fPNHoldingLevel = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
fPNInterpulse = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
fPNSettlingTime = [100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0]
fPostProcessLowpassFilter = 100000.0
fPostTrainLevel = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
fPostTrainPeriod = [10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0]
fRunStartToStart = 0.0
fScopeOutputInterval = 0.0
fSecondsPerRun = 7200.0
fSignalGain = 1.0
fSignalHighpassFilter = 1.0
fSignalLowpassFilter = 5000.0
fSignalOffset = 0.0
fStatisticsPeriod = 1.0
fStepDuration = [1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0]
fStepLevel = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
fSynchTimeUnit = 12.5
fTelegraphAccessResistance = 0.0
fTelegraphAdditGain = 1.0
fTelegraphFilter = 10000.0
fTelegraphMembraneCap = 0.0
fTrialStartToStart = 0.0
fTriggerThreshold = 0.0
lADCChannelNameIndex = 3
lADCResolution = 32768
lADCUnitsIndex = 4
lActualEpisodes = 16
lAverageCount = 1
lConditNumPulses = [1, 0, 0, 0, 0, 0, 0, 0]
lDACChannelNameIndex = [5, 7, 9, 11, 13, 15, 17, 19]
lDACChannelUnitsIndex = [6, 8, 10, 12, 14, 16, 18, 20]
lDACFileEpisodeNum = [0, 0, 0, 0, 0, 0, 0, 0]
lDACFileNumEpisodes = [0, 0, 0, 0, 0, 0, 0, 0]
lDACFilePathIndex = [0, 0, 0, 0, 0, 0, 0, 0]
lDACFilePtr = [0, 0, 0, 0, 0, 0, 0, 0]
lDACResolution = 32768
lEpisodesPerRun = 21
lEpochDurationInc = [0, 0, 0, 0, 0]
lEpochInitDuration = [2000, 10000, 10000, 10000, 10000]
lEpochPulsePeriod = [0, 0, 0, 0, 0]
lEpochPulseWidth = [0, 0, 0, 0, 0]
lFileCommentIndex = 0
lFinishDisplayNum = 60000
lNumSamplesPerEpisode = 60000
lNumberOfTrials = 1
lPreTriggerSamples = 20
lRunsPerTrial = 1
lSamplesPerTrace = 40000
lStartDisplayNum = 0
lStatisticsMeasurements = 5
lTimeHysteresis = 1
nADCNum = 0
nADCPtoLChannelMap = 0
nADCSamplingSeq = 0
nActiveDACChannel = 0
nAllowExternalTags = 0
nAlternateDACOutputState = 0
nAlternateDigitalOutputState = 0
nAutoAnalyseEnable = 1
nAutoTriggerStrategy = 1
nAverageAlgorithm = 0
nAveragingMode = 0
nCRCEnable = 0
nChannelStatsStrategy = 0
nCommentsEnable = 0
nConditEnable = [0, 0, 0, 0, 0, 0, 0, 0]
nDACFileADCNum = [0, 0, 0, 0, 0, 0, 0, 0]
nDACNum = [0, 1, 2, 3, 4, 5, 6, 7, 0, 0, 0, 0, 0]
nDataFormat = 0
nDigitalDACChannel = 0
nDigitalEnable = 0
nDigitalHolding = 0
nDigitalInterEpisode = 0
nDigitalTrainActiveLogic = 1
nDigitizerADCs = 16
nDigitizerDACs = 4
nDigitizerSynchDigitalOuts = 8
nDigitizerTotalDigitalOuts = 16
nDigitizerType = 6
nEpochDigitalOutput = [0, 0, 0, 0, 0]
nEpochNum = [0, 1, 2, 3, 4, 0, 1, 2, 3, 4]
nEpochType = [1, 1, 1, 1, 1]
nExperimentType = 2
nExternalTagType = 2
nFileType = 1
nFirstEpisodeInRun = 0
nHighpassFilterType = 0
nInterEpisodeLevel = [0, 0, 0, 0, 0, 0, 0, 0]
nLTPPresynapticPulses = [0, 0, 0, 0, 0, 0, 0, 0]
nLTPType = 0
nLTPUsageOfDAC = [0, 0, 0, 0, 0, 0, 0, 0]
nLeakSubtractADCIndex = [0, 0, 0, 0, 0, 0, 0, 0]
nLeakSubtractType = [0, 0, 0, 0, 0, 0, 0, 0]
nLevelHysteresis = 64
nLowpassFilterType = 0
nManualInfoStrategy = 1
nMembTestEnable = [0, 0, 0, 0, 0, 0, 0, 0]
nOperationMode = 5
nPNNumADCChannels = [0, 0, 0, 0, 0, 0, 0, 0]
nPNNumPulses = [4, 4, 4, 4, 4, 4, 4, 4]
nPNPolarity = [1, 1, 1, 1, 1, 1, 1, 1]
nPNPosition = [0, 0, 0, 0, 0, 0, 0, 0]
nPostProcessLowpassFilterType = b'\x00'
nScopeTriggerOut = 0
nShowPNRawData = 0
nSignalType = 0
nSimultaneousScan = 1
nStatisticsClearStrategy = 1
nStatisticsDisplayStrategy = 0
nStatisticsSaveStrategy = 0
nStatsChannelPolarity = 1
nStatsEnable = 1
nTelegraphDACScaleFactorEnable = [1, 0, 0, 0, 0, 0, 0, 0]
nTelegraphEnable = 1
nTelegraphInstrument = 24
nTelegraphMode = 1
nTrialTriggerSource = -1
nTriggerAction = 0
nTriggerPolarity = 0
nTriggerSource = -3
nUndoPromptStrategy = 0
nUndoRunCount = 0
nWaveformEnable = [1, 0, 0, 0, 0, 0, 0, 0]
nWaveformSource = [1, 1, 1, 1, 0, 0, 0, 0]
sUnused = b'\x00\x00\x00'
uCreatorNameIndex = 1
uCreatorVersion = 168230915
uFileCRC = 0
uFileCompressionRatio = 1
uFileInfoSize = 512
uFileStartDate = 20171005
uFileStartTimeMS = 52966899
uModifierNameIndex = 0
uModifierVersion = 0
uProtocolPathIndex = 2
uStopwatchTime = 8379
unknown1 = 1101957764
unknown2 = 3041560705
unknown3 = 3819584183
```