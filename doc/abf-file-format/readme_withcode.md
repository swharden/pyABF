# SWHarden's Unofficial ABF File Format Guide
Electrophysiology data acquired with pCLAMP (clampEx and clampFit, developed by Molecular Devices) is saved in a proprietary ABF format. The internal structure of these ABF (Axon Binary Format) files is intentionally undocumented (since 2006 when pCLAMP 10 featured the ABF2 file format), as its users are encouraged to interact with the data exclusively through a DLL they provide (without source code).

>According to the [official documentation](https://mdc.custhelp.com/euf/assets/content/ABFHelp.pdf): "_One of the goals of the ABF reading routines is to isolate the applications programmer from the need to know anything other than the most basic information about the file format. ABF 2.0 now uses a header of variable length.  This means that it is now essential to use the ABFFIO.DLL library to access the data._"

The purpose of this page is to document how to extract meaningful information directly from ABF files encoded in the ABF2 file format without relying on a DLL or any external libraries. Although the concepts here are presented in Python, effort has been invested to ensure these concepts can be easily ported to other languages (with personal interest in Visual Studio / C# and PHP).

This document contains a blend of code and insights provided by various developers in the past (see  [References](#references)) supplemented with additional code and insights added by the author. Discovery of previously-undocumented features (e.g., extracting digital output command signals from the waveform protocol) was primarially achieved by comparing ABFs in a hex editor (comparing files byte-by-byte, modifying individual bits, and viewing modified files in ClampEx).

Documentation and development is biased toward the use-cases of the author: Analysis of 1-2 channel ABF2 fixed-length episodic files (voltage clamp and current clamp) recorded using whole-cell patch-clamp technique in brain slices. No effort will be invested into documenting features I don't use (e.g., variable-length sweeps, gap-free mode, or voice tags).


# Is a new ABF reader really necessary?
The best available Python code to read ABF headers (axonio.py, part of Neo-IO) is a line-by-line translation of a MatLab script, and is not very Pythonic. It makes them difficult to read. Consider this part of the header reading code which turns the bytes corresponding into the file recording time into a python datetime object. These two snippets perform the identical task.

#### Neo-IO Code:
```python
YY = int(header['uFileStartDate'] / 10000)
MM = int((header['uFileStartDate'] - YY * 10000) / 100)
DD = int(header['uFileStartDate'] - YY * 10000 - MM * 100)
hh = int(header['uFileStartTimeMS'] / 1000. / 3600.)
mm = int((header['uFileStartTimeMS'] / 1000. - hh * 3600) / 60)
ss = header['uFileStartTimeMS'] / 1000. - hh * 3600 - mm * 60
ms = int((ss%1)*1e6)
ss = int(ss)
dt = datetime.datetime(YY, MM, DD, hh, mm, ss, ms) 
```
#### My Code:
```python
dt=datetime.datetime.strptime(str(self.header['uFileStartDate']), "%Y%M%d")
dt=dt+datetime.timedelta(seconds=self.header['uFileStartTimeMS']/1000)
```

Multiply findings like this times a hundred, and this is why I think creating a pure-python ABF reading solution from scratch may be worthwhile. In addition to being useful in learning and documenting the ABF2 file format, the finished class can be rapidly implemented into dependency-free projects.


# Reading an ABF
The overall process of reading ABF file occurs in a series of steps in this order. Each step has its own section further down in this document.

* Read the **ABF header** and confirm it is an ABF2 file
* Create **section map** noting byte locations of all sections
* Pull strings from **StringsSection**
* Pull ABF acquisition information from **ProtocolSection**
* Pull comment tags from **TagSection**
* Recreate the epoch chart using **EpochSection** and **EpochPerDACSection**
* Add to the epoch chart using **ADCSection** and **DACSection**
* Load sweep data as desired from the **DataSection**

# Reading the ABF Header
The header always starts ate byte position zero. It can be read into a fixed sequence of variables, but they all have different formats. I created a list of variable names which also include the [struct character format](https://docs.python.org/2/library/struct.html#format-characters) (separated by an underscore). Other sources use a list of tuples, but I prefer this 1d list. Portability is easy too.

```python
HEADER_KEYS=["fFileSignature_4s","fFileVersionNumber_4b","uFileInfoSize_I","lActualEpisodes_I",
  "uFileStartDate_I","uFileStartTimeMS_I","uStopwatchTime_I","nFileType_H","nDataFormat_H",
  "nSimultaneousScan_H","nCRCEnable_H","uFileCRC_I","FileGUID_I","unknown1_I","unknown2_I",
  "unknown3_I","uCreatorVersion_I","uCreatorNameIndex_I","uModifierVersion_I",
  "uModifierNameIndex_I","uProtocolPathIndex_I"]
```

**note about version number:** The ABF file version is encoded in byte position 4-8. Each is an uint, but they are in reverse order. Byte values `[0,0,6,2]` represent version `2.6`.


### Example ABF Header Output
```
### HEADER ###
fFileSignature = ABF2
fFileVersionNumber = 2.6
uFileInfoSize = 512
lActualEpisodes = 16
uFileStartDate = 20171005
uFileStartTimeMS = 52966899
uStopwatchTime = 8379
nFileType = 1
nDataFormat = 0
nSimultaneousScan = 1
nCRCEnable = 0
uFileCRC = 0
FileGUID = 813622370
unknown1 = 1101957764
unknown2 = 3041560705
unknown3 = 3819584183
uCreatorVersion = 168230915
uCreatorNameIndex = 1
uModifierVersion = 0
uModifierNameIndex = 0
uProtocolPathIndex = 2
```

# Notes on Sections

Data in ABF2 files is grouped into _sections_ which contain arbitrary numbers of _entries_ of arbitrary sizes. Information about the byte positions of where sections start, how many bytes elements in sections are, and how many elements search section has are defined in a _section map_ in the beginning of the ABF file.

## List of Sections (in order)
To read waveform position data, you have to know the list of sections. They are in a specific order. They can be found in everyone's project, but easy to review in StimFit's [ProtocolStructs.h](https://github.com/neurodroid/stimfit/blob/master/src/libstfio/abf/axon2/ProtocolStructs.h#L109). Although data from all sections is accessible, I typically only utilize data from a few sections (in bold)

* **ProtocolSection** - the protocol
* **ADCSection** - one for each ADC channel
* **DACSection** - one for each DAC channel
* **EpochSection** - one for each epoch
* ADCPerDACSection - one for each ADC for each DAC
* **EpochPerDACSection** - one for each epoch for each DAC
* UserListSection - one for each user list
* StatsRegionSection - one for each stats region
* MathSection - Math
* **StringsSection** - ABF comments and protocol
* **DataSection** - Data
* **TagSection** - Tags
* ScopeSection - Scope config
* DeltaSection - Deltas
* VoiceTagSection - Voice Tags
* SynchArraySection - Synch Array
* AnnotationSection - Annotations
* StatsSection - Stats config

# Section Map (ABFheader.sectionMap)
For each section (in the order shown) the section information can be found (as  int16, int16, long32) starting at byte 76 (shifted 16 bytes per section). Here's a snip of Python which should be enough to paint the point.
```Python
BLOCKSIZE=512
for each sectionNumber,sectionName in enumerate(listOfSections):
  bytePosition=76+sectionNumber*16
  blockNumber, entrySize, entryCount = fileReadStruct(fb,bytePosition,"IIl")
  sectionByteLocation = blockNumber*BLOCKSIZE
```

## Example Section Map
This section map was created from 17o05028.abf. Sections with empty data are listed but their byte locations are not shown (e.g., `TagSection` is blank because this ABF has no tags). Byte locations for the various sections will be different for every ABF file!

```
    ADCPerDACSection (empty in my example)
   AnnotationSection (empty in my example)
        DeltaSection (empty in my example)
         MathSection (empty in my example)
        StatsSection (empty in my example)
          TagSection (empty in my example)
     UserListSection (empty in my example)
     VoiceTagSection (empty in my example)
     ProtocolSection 1 x 512 bytes (0.50 kb) [bytes 512-1024] [blocks 1-2.00]
          ADCSection 1 x 128 bytes (0.12 kb) [bytes 1024-1152] [blocks 2-2.25]
          DACSection 8 x 256 bytes (2.00 kb) [bytes 1536-3584] [blocks 3-7.00]
  EpochPerDACSection 5 x 48 bytes (0.23 kb) [bytes 3584-3824] [blocks 7-7.47]
        EpochSection 5 x 32 bytes (0.16 kb) [bytes 4096-4256] [blocks 8-8.31]
  StatsRegionSection 1 x 128 bytes (0.12 kb) [bytes 4608-4736] [blocks 9-9.25]
      StringsSection 20 x 194 bytes (3.79 kb) [bytes 5120-9000] [blocks 10-17.58]
        ScopeSection 1 x 769 bytes (0.75 kb) [bytes 5632-6401] [blocks 11-12.50]
         DataSection 960000 x 2 bytes (1875.00 kb) [bytes 6656-1926656] [blocks 13-3763.00]
   SynchArraySection 16 x 8 bytes (0.12 kb) [bytes 1926656-1926784] [blocks 3763-3763.25] 
```

**Epoch waveform:** Consider the custom waveform tab when you design a protocol. The values from epochs A-J (10 of them) are stored in the ABF. According to the section map, the `EpochPerDACSection` section contains 10 entries (one per epoch, A-J). The section map also tells us each entry is 48 bytes, and this section starts at file byte position 3584. My software trims-off unused epochs so it only displays 5 here (because my ABF had 5 active epochs)

**Data section:** The largest section of an ABF file is typically `DataSection` because it contains all that electrophysiology data. It contains 960,000 entries each 2 bytes in size (int16). At 20kHz sample rate, this means 24 seconds of data can be read directly from the ABF file starting at byte 6,656.


# Reading Mapped Sections
Most sections have a pre-defined list of values (which can be loaded as a structure using name / vartype (byte length) loading scheme). These sections can be easily loaded assuming you have the list of variable names / variable types for that section. Sections loaded this way are: `ProtocolSection`, `ADCSection`, `DACSection*`, `EpochPerDACSection*`, `EpochSection*`, and `StringsSection*`. Sections marked with asterisks may have more than 1 entry, so the data structure is repeatedly loaded at each entry start byte (this is most useful for repeating elements, like values per epoch or values per DAC channel). Note that some sections (like `StringsSection`) have a very simple data structure (repeated 194-byte strings) and do not require a value/structure key set to load. The following code snippets are how I read values from a binary file buffer with a minimum of code duplication.

### Read a _byte string_ directly from the ABF (returns a string)

```python
def fileRead(self,bytePosition,nBytes):
	"""Return bytestring from a specific position in the open file."""
	self.fb.seek(bytePosition)
	return self.fb.read(nBytes)
```

### Read a _formatted character structure_ directly from the ABF (returns a string)
After reviewing the [structure format characters](https://docs.python.org/3/library/struct.html#format-characters) you'll start to get an idea of how to turn byte strings into meaningful data. This function will read your custom `structFormat` starting at `bytePosition`. The cool thing here is that if your format is a single value (e.g., `i`) it will return the single value (an integer, 4 bytes) but if you give it multiples (e.g., `iii` or `3i`) it will return a _list_ of what you requested (here resulting in 3 integers spanning 12 bytes). You can also mix and match, such as `iiL`.

```python
def fileReadStruct(self,bytePosition,structFormat,allowByteString=False):
	"""Given a file position and a struct code, return the object(s)."""
	self.fb.seek(bytePosition)
	val = struct.unpack(structFormat, self.fb.read(struct.calcsize(structFormat)))
	val = val[0] if len(val)==1 else list(val)
	return val
```

### Example keyed structure (for ProtocolSection)
Here I carry around keyed structures as a list of strings, where each string maintains the format "variableName_structFormat". Since splitting each string at the underscore yields a key/struct pair, it seems much easier than to maintain (and port to other languages) than a list of tuples like matLab and Neo-IO source code tries to do. It's also a little shorter. I almost made it a space-separated multi-line string, but thought this would be easier to copy/paste into PHP later exactly as it is.

```python
KEYS_HEADER=['fFileSignature_4s','fFileVersionNumber_4b','uFileInfoSize_I','lActualEpisodes_I',
    'uFileStartDate_I','uFileStartTimeMS_I','uStopwatchTime_I','nFileType_H','nDataFormat_H',
    'nSimultaneousScan_H','nCRCEnable_H','uFileCRC_I','FileGUID_I','unknown1_I','unknown2_I',
    'unknown3_I','uCreatorVersion_I','uCreatorNameIndex_I','uModifierVersion_I',
    'uModifierNameIndex_I','uProtocolPathIndex_I']
```

### Read keyed structure value directly from the ABF (returns a dict)
Since we already have tools to get character-formatted structures from a file position, iterating this process over a series of key/struct pairs becomes easy. This function absorbs a list strings (formatted as `varName_structCharacters`) and builds a dictionary of all items. Note that this is essentially a 1d dictionary, as its contents will all be single values or short lists. This is useful for `ProtocolSection` and `ADCSection` since (according to their map) the number of elements is always 1. 

```python
def fileReadSectionKeys(self,bytePosition,sectionKeys,fixedOffsetBytes=False,allowByteString=False):
	"""Given a list of "name_struct"-formatted keys, create and return the list of objects."""
	self.fb.seek(bytePosition)
	items={}
	for key in sectionKeys:
		varName,structFormat=key.split("_")
		items[varName]=self.fileReadStruct(bytePosition,structFormat,allowByteString)
		if fixedOffsetBytes:
			bytePosition+=fixedOffsetBytes
		else:
			bytePosition+=struct.calcsize(structFormat)
	return items  
```



### Read repeated keyed structures directly from the ABF (returns a list of dicts)
For more advanced structured datasets (i.e., `EpochPerDACSection` which has the same structure but repeats once per epoch) it becomes useful to iterate over the building of key/struct-based dictionaries. Unlike previous functions which require a start position, we just give this the `sectionName` (which should be a key in `ABFheader.sectionMap`) and it knows how to look up the start position and number of iterations required. This function is useful for `DACSection`, `EpochPerDACSection`, `EpochSection` (or any other repeating keyed structure which has a top-level designation in the section map) and returns a list of dictionaries.

```python
def fileReadMappedSection(self,sectionName,sectionKeys):
	"""Given the name of a mapped section (in self.sectionMap) return a list of all its elements."""
	entries=[]
	if not sectionName in self.sectionMap.keys():
		print("ERROR:",sectionName,"is not in the section map!")
		return
	else:
		entryFirstPosition=self.sectionMap[sectionName]['byteStart']
		entrySize=self.sectionMap[sectionName]['entrySize']
		entryCount=self.sectionMap[sectionName]['entryCount']
		for entryNumber in range(entryCount):
			bytePosition=entryFirstPosition+entrySize*entryNumber
			entries.append(self.fileReadSectionKeys(bytePosition,sectionKeys))
	return entries
```

# What's in the data?
Once you've loaded all your header data, you're probably overwhelmed in crazy-looking values. Most likely you only need to extract a handfull of numbers from the ABF header, so I'll comment on a few of the important items.

## ProtocolSection (ABFHeader.protocol, dictionary)
One advantage of this data block is that it can be read from any file (since it doesn't require creation of the section map). If you accidentally load a JPEG, you'll find out pretty quickly that something is wrong.

* bytes 0-4 of the ABF file contain the file signature. It may be worth assuring this reads  `ABF2`
* convert to date using `dt=datetime.datetime.strptime(str(self.header['uFileStartDate']), "%Y%M%d")`
* add time with `dt=dt+datetime.timedelta(seconds=self.header['uFileStartTimeMS']/1000)`

```python
FileGUID = 813622370 # in theory this is an identifier unique to this file
fFileSignature = ABF2 # first 4 bytes of the file
fFileVersionNumber = [0, 0, 6, 2] # version number in REVERSE order. This means version 2.6.0.0
lActualEpisodes = 16 # number of sweeps
nCRCEnable = 0
nDataFormat = 0
nFileType = 1
nSimultaneousScan = 1
uCreatorNameIndex = 1
uCreatorVersion = 168230915
uFileCRC = 0
uFileInfoSize = 512
uFileStartDate = 20171005 # file recording date
uFileStartTimeMS = 52966899 # file recording time
uModifierNameIndex = 0
uModifierVersion = 0
uProtocolPathIndex = 2
uStopwatchTime = 8379
unknown1 = 1101957764
unknown2 = 3041560705
unknown3 = 3819584183
```

## ADCSection (ABFHeader.adc, list of dictionaries)
There is a list of these, 1 per DAC. I don't get anythig from this currently...

```python
bEnabledDuringPN = 0
fADCDisplayAmplification = 12.307504653930664
fADCDisplayOffset = -21.75
fADCProgrammableGain = 1.0
fInstrumentOffset = 0.0
fInstrumentScaleFactor = 0.009999999776482582
fPostProcessLowpassFilter = 100000.0
fSignalGain = 1.0
fSignalHighpassFilter = 1.0
fSignalLowpassFilter = 5000.0
fSignalOffset = 0.0
fTelegraphAccessResistance = 0.0
fTelegraphAdditGain = 1.0
fTelegraphFilter = 10000.0
fTelegraphMembraneCap = 0.0
lADCChannelNameIndex = 3
lADCUnitsIndex = 4
nADCNum = 0
nADCPtoLChannelMap = 0
nADCSamplingSeq = 0
nHighpassFilterType = 0
nLowpassFilterType = 0
nPostProcessLowpassFilterType = b'\x00'
nStatsChannelPolarity = 1
nTelegraphEnable = 1
nTelegraphInstrument = 24
nTelegraphMode = 1
```

## DACSection (ABFHeader.dac)
There is a list of these, 1 per DAC.
* I extract the holding current (not defined in the epoch waveform tab) as `fDACHoldingLevel`.

```python
fBaselineDuration = 1.0
fBaselineLevel = 0.0
fDACCalibrationFactor = 1.0008957386016846
fDACCalibrationOffset = 0.0
fDACFileOffset = 0.0
fDACFileScale = 1.0
fDACHoldingLevel = 0.0
fDACScaleFactor = 400.0
fInstrumentHoldingLevel = 0.0
fMembTestPostSettlingTimeMS = 100.0
fMembTestPreSettlingTimeMS = 100.0
fPNHoldingLevel = 0.0
fPNInterpulse = 0.0
fPNSettlingTime = 100.0
fPostTrainLevel = 0.0
fPostTrainPeriod = 10.0
fStepDuration = 1.0
fStepLevel = 0.0
lConditNumPulses = 1
lDACChannelNameIndex = 5
lDACChannelUnitsIndex = 6
lDACFileEpisodeNum = 0
lDACFileNumEpisodes = 0
lDACFilePathIndex = 0
lDACFilePtr = 0
nConditEnable = 0
nDACFileADCNum = 0
nDACNum = 0
nInterEpisodeLevel = 0
nLTPPresynapticPulses = 0
nLTPUsageOfDAC = 0
nLeakSubtractADCIndex = 0
nLeakSubtractType = 0
nMembTestEnable = 0
nPNNumADCChannels = 0
nPNNumPulses = 4
nPNPolarity = 1
nPNPosition = 0
nTelegraphDACScaleFactorEnable = 1
nWaveformEnable = 1
nWaveformSource = 1
```

## EpochSection (ABFHeader.epochSection)
* I use this to capture the digital output signal for each epoch. I get it from `nEpochDigitalOutput`. Rather than handle it as a separate dictionary or array or something, I read it then insert "sDigitalOutput" into the regular epoch object (a list of dictionaries).
* The digital output is a single byte, but represents 8 bits corresponding to 8 outputs (7->0). I convert it to a string like "10011101" for easy eyeballing.
* Convert a byte (int) to an 8-character binary string of 1s and 0s with `format(byteInteger,'b').rjust(8,'0')`

## EpochPerDACSection (ABFHeader.epochPerDac)
This is what you probably think of when you visualize the _waveform editor_ tab in ClampEx. Aside from the digital outputs, most of the stuff is here. After adding manually inserting the digital output onto the epoch dictionaries, a sample epoch (4) is shown here.

* Epoch types: 1=step, 4=ramp

```
fEpochInitLevel = -50.0 # command current or voltage
fEpochLevelInc = 10.0 # delta command
lEpochDurationInc = 0 # delta duration
lEpochInitDuration = 10000 # duration (MS)
lEpochPulsePeriod = 0 # pulse period
lEpochPulseWidth = 0 # pulse width
nDACNum = 0 # this epoch entry goes with DAC0
nEpochNum = 4 # epoch 4 corresponds to epoch D.
nEpochType = 1 # this epoch is a "step"
sDigitalOutput = 00000000 # digital output codes (added from EpochSection)
```

## StringsSection (ABFHeader.strings and ABFHeader.stringsAll)
This is a mess and information is clearly missing. Briefly, some quasi-useful information can be pulled from the strings parsing these keys can produce. First, throw away any keys that don't contain key words (AXENGN, clampex, Clampex, CLAMPEX, or axoscope). If a keyword is found, split the string at the key word and take the last part. Finally, split the string at 0x00. What's left are ~20 strings. These seem to be the ABF comment (if it exists), the protocol used to make the recording, and signal labels.

* The first string is always the protocol file (if it exists) but I get mixed results on the second line. If a comment doesn't eixst, that line is just gone
* You probably should not rely on capturing unit information from these strings because they seem unreliable...

```
0000: S:\Protocols\permanent\0402 VC 2s MT-50.pro
0001: SWHLab5[0402]
0002: IN 0
0003: pA
0004: Cmd 0
0005: mV
0006: Cmd 1
0007: mV
0008: Cmd 2
0009: mV
0010: Cmd 3
0011: mV
```

## DataSection
The data section is where the electrical recordings are stored. To see how to retrieve this data, navigate to the "Reading Sweep data" section of this document.

## TagSection (ABFHeader.tags)
At the end of the file are the tags (time-encoded text comments).

* I'm still working out the tag time units (are they microseconds?)

```
### TAG 0 ###
lTagTime = 13918208
nTagType = 1
nVoiceTagNumberorAnnotationIndex = 0
sComment = +TGOT

### TAG 1 ###
lTagTime = 23588864
nTagType = 1
nVoiceTagNumberorAnnotationIndex = 0
sComment = -TGOT
```

# Reading Sweep Data
**I WILL REVISIT THIS LATER!** - There is a lot or room to discuss memory mapping, file opening/closing, and speed optimization. For now, here's how you extract a sweep of ephys data which is probably why you came here:

```python
def getSweep(self,sweepNumber=0):
	"""Returns data values for a given channel and sweep. Numpy memmap should be considered for this."""
	sweepNumber=max(0,min((sweepNumber,self.header['lActualEpisodes']-1))) # make sure it's a real sweep
	dataPos0=self.sectionMap['DataSection']['byteStart']
	sweepPointCount=self.protocol[0]['lNumSamplesPerEpisode']
	sweepByteCount=sweepPointCount*2 # assuming 16-bit (2-byte) data points
	sweepByteStart=int(dataPos0+sweepNumber*sweepByteCount)
	dataScale=header.protocol[0]['lADCResolution']/1e6 # multiply this by the data
	with open(self.abfFileName,'rb') as f:
		f.seek(sweepByteStart)
		data=f.read(sweepByteCount)
	f.close()
	sweepData=struct.unpack('%dh'%(sweepByteCount/2),data)
	sweepData=[x*dataScale for x in data]
	return(sweepData)
```

# References

* [Python struct format characters](https://docs.python.org/2/library/struct.html#format-characters)

## ABF File Format
* [Official ABF Format PDF](https://mdc.custhelp.com/euf/assets/content/ABFHelp.pdf) - It's interesting, but they ONLY want you to use their DLL to access ABF data, so this document doesn't help much when learning how to access information directly from the binary file.
* [Official Axon pCLAMP ABF SDK](http://mdc.custhelp.com/app/answers/detail/a_id/18881/~/axon™-pclamp®-abf-file-support-pack-download-page)
  * [abfheader.h](https://github.com/dongzhenye/biosignal-tools/blob/master/biosig4c%2B%2B/t210/abfheadr.h) is on github
  * Most code elsewhere mimics these variable names.
  * Comments are useful in defining variable names.
  * Variables are not in the same order they are in the structs which build the file itself.
* MatLab ABF Readers
  * [MatLab ABF Loader (sbf2load.m)](https://github.com/voyn/transalyzer/blob/master/Functions/abf2load.m)
  * [official](https://www.mathworks.com/matlabcentral/fileexchange/45667-apanalysis?focused=6744051&tab=function) - This code floats on the internet in several places. I think it was line-by-line ported to Python for the Neo-IO project
* StimFit
  * [abflib.cpp](https://github.com/neurodroid/stimfit/blob/master/src/libstfio/abf/abflib.cpp) - another implementation of an ABF reader.
  *  Header structures are define is in [ProtocolStructs.h](https://github.com/neurodroid/stimfit/blob/master/src/libstfio/abf/axon2/ProtocolStructs.h)
* Neo-IO
  * [axonrawio.py](https://github.com/NeuralEnsemble/python-neo/blob/master/neo/rawio/axonrawio.py)
* QUB Express
  * Python 2 code written to interact with abffio.dll contains interesting content in its [python code](https://qub.mandelics.com/src/qub-express/qubx/data_abf.py)