# SWHarden's Unofficial ABF File Format Guide
Electrophysiology data acquired with pCLAMP (clampEx and clampFit, developed by Molecular Devices) is saved in a proprietary format. The internal structure of these ABF (Axon Binary Format) files is intentionally undocumented (since 2006 when pCLAMP 10 featured the ABF2 file format), as its users are encouraged to interact with the data exclusively through a 32-bit DLL they provide (without source code).

>According to the [official documentation](https://mdc.custhelp.com/euf/assets/content/ABFHelp.pdf): "_One of the goals of the ABF reading routines is to isolate the applications programmer from the need to know anything other than the most basic information about the file format. ABF 2.0 now uses a header of variable length.  This means that it is now essential to use the ABFFIO.DLL library to access the data._"

The purpose of this page is to document how to extract meaningful information directly from ABF files encoded in the ABF2 file format without relying on a DLL or any external libraries. Although this pages displays a few examples of code using Python, effort has been invested to ensure these concepts can be easily ported to other languages (with personal interest in writing an ABF reader for C# (Visual Studio) and PHP.

This document is a blend of code and insights provided by the work of previous developers (see  [References](#references)) supplemented with additional code and insights added by the author. Discovery of previously-undocumented features (e.g., extracting digital output command signals from the waveform protocol) was primarially achieved by comparing ABFs in a hex editor (comparing files byte-by-byte, modifying individual bits and viewing modified files in ClampEx).

Documentation and development is biased toward the use-cases of the author: Analysis of 1-2 channel ABF2 fixed-length episodic files (voltage clamp and current clamp) recorded using whole-cell patch-clamp technique in brain slices. No effort will be invested into documenting features I don't use (e.g., variable-length sweeps, gap-free mode, or voice tags). If you benefit from the information provided on this document and figure out how to achieve additional functionality or implement your own improvements into this basic framework, please contact me so I can add your contributions to this growing collection of source code examples and documentation!

# Reading an ABF
The overall process of reading ABF file occurs in a series of steps in this order. Each step has its own section described in detail further down in this document.

* Read the **ABF header** and confirm it is an ABF2 file
* Create **section map** noting byte locations of all sections
* Pull strings from **StringsSection**
* Pull ABF acquisition information from **ProtocolSection**
* Pull comment tags from **TagSection**
* Recreate the epoch chart using **EpochSection** and **EpochPerDACSection**
* Add to the epoch chart using **ADCSection** and **DACSection**
* Load sweep data as desired from the **DataSection**

## Extracting Structured Data from Binary Files
Core to the ability to extract data from ABF files is an understanding of bytestrings and structs. Consider a bytestring of 16 bytes which is 128 bits in a row (128 1s or 0s). This byte string could represent 16 one-byte `char`s, 8 two-byte `short`s, 4 four-byte `int`s, 2 8-byte `long`s. The [_structure character format_](https://docs.python.org/2/library/struct.html#format-characters) for each variable type is standard across most programming languages and helps turn a continuous a series of bytes into separate variables. For example an int is an `i` (4 bytes) and a double is a `d` (8 bytes). Our 16-byte bytestring could be interpreted as `iiii` (4 `int`s) or `dd` (2 `long`s) or even a mix like `iid`.

If I know a bytestring contains a certain list of variables, I know the order of the list, and I know the type of each variable, I can load the data into the variables one by one. In Python I can run `varName = struct.unpack(format, byteString)` where format is the character code for the variable type.

I can simplify things in Python with dictionaries (or keyed arrays in other languages) by storing a list of variables and their respective struct characters (separated with an underscore) as a 1d array of strings. Consider this example:

```python
SAMPLE_KEYS=["myAge_i","myWage_f"]
info={}
for key in SAMPLE_KEYS:
    varName,varFormat=key.split("_")
    info[varName]=struct.unpack(varFormat, byteString)
```

This is how _ALL_ data is read from the ABF file. It gets fancier due to iterations (i.e., the same set of keys is used to read all keys from an epoch, but is looped over every epoch).

# Reading the ABF Header
The first thing to read when visiting a new ABF file is the header. The header has a bunch of values in a pre-defined sequence and always starts at byte position zero. This code demonstrates how to display all information in the header and uses the variable key method described earlier. 

### Standalone code to read an ABF header

```python
KEYS_HEADER=["fFileSignature_4s","fFileVersionNumber_4b","uFileInfoSize_I","lActualEpisodes_I",
  "uFileStartDate_I","uFileStartTimeMS_I","uStopwatchTime_I","nFileType_H","nDataFormat_H",
  "nSimultaneousScan_H","nCRCEnable_H","uFileCRC_I","FileGUID_I","unknown1_I","unknown2_I",
  "unknown3_I","uCreatorVersion_I","uCreatorNameIndex_I","uModifierVersion_I",
  "uModifierNameIndex_I","uProtocolPathIndex_I"]

import struct
f=open(R"C:\data\17n06003.abf",'rb') # note1
f.seek(0) # note2
for key in KEYS_HEADER:
    varName,varFormat=key.split("_")
    varSize=struct.calcsize(varFormat)
    byteString=f.read(varSize)
    var=struct.unpack(varFormat,byteString)
    if len(var)==1: var=var[0] # note3
    print("%s (%s, %d bytes) = %s"%(varName,varFormat,varSize,var))
f.close()
```
* note1: the file must be opened in read binary mode (not ascii mode).
* note2: by default a newly opened file seeks to byte 0, but you can start reading data anywhere with `seek(bytePosition)`. Also note that every time a read occurs the position is automatically advanced. This is why you don't have to call `seek()` after every read.
* note3: `struct.unpack()` always returns a tuple. If it has just 1 element, just return that element. `(7,)` becomes just `7`, but if the varFormat is multiple items (notice `fFileVersionNumber_4b`) the returned result is a tuple with multiple items. Noe that `4b` is the same as `bbbb`.

### Example Output
```
fFileSignature (4s, 4 bytes) = b'ABF2'
fFileVersionNumber (4b, 4 bytes) = (0, 0, 6, 2)
uFileInfoSize (I, 4 bytes) = 512
lActualEpisodes (I, 4 bytes) = 7
uFileStartDate (I, 4 bytes) = 20171106
uFileStartTimeMS (I, 4 bytes) = 44884136
uStopwatchTime (I, 4 bytes) = 4128
nFileType (H, 2 bytes) = 1
nDataFormat (H, 2 bytes) = 0
nSimultaneousScan (H, 2 bytes) = 1
nCRCEnable (H, 2 bytes) = 0
uFileCRC (I, 4 bytes) = 0
FileGUID (I, 4 bytes) = 3595561293
unknown1 (I, 4 bytes) = 1202434462
unknown2 (I, 4 bytes) = 2861915294
unknown3 (I, 4 bytes) = 4153321813
uCreatorVersion (I, 4 bytes) = 168230915
uCreatorNameIndex (I, 4 bytes) = 1
uModifierVersion (I, 4 bytes) = 0
uModifierNameIndex (I, 4 bytes) = 0
uProtocolPathIndex (I, 4 bytes) = 2
```

# Sections and the Section Map

The header was easy to read because we know its sequence of variables and their structures (`KEYS_HEADER`) and know to start reading at byte 0. Other secions have similar variable sequences (e.g., variables for digital-to-analog converter configuration) but as of ABF2 their first byte is different from file to file. Further, some sections have multiple _entries_ (e.g., the epoch section has one entry for each epoch). In addition to the byte position varying from file to file, the number of entries each section has may vary as well! To make sense of it we create a _section map_ which contains three details about every section: the first byte of a section, the number of bytes each entry has in that section, and the number of entries that section has. With these 3 values for each section we know where all data is in the ABF!

Just like we extracted variables from the header with `KEYS_HEADER` (always starting at byte 0), we can get details about all sections with `KEYS_SECTIONS`. Conveniently the data about each section (`blockStart`, `entrySize`, `entryCount`) uses the same struct format `IIl` for every section (unsigned int, unsigned int, long). Note that a block always represents 512 bytes.

Data for sections starts at byte 72 and shifts 16-bytes for every section (even though `IIl` is only 4+4+4=12 bytes).

### Standalone Code to Create the ABF Section Map

```python
BLOCKSIZE=512
KEYS_SECTIONS=['ProtocolSection_IIl','ADCSection_IIl','DACSection_IIl',
    'EpochSection_IIl','ADCPerDACSection_IIl','EpochPerDACSection_IIl','UserListSection_IIl',
    'StatsRegionSection_IIl','MathSection_IIl','StringsSection_IIl','DataSection_IIl',
    'TagSection_IIl','ScopeSection_IIl','DeltaSection_IIl','VoiceTagSection_IIl',
    'SynchArraySection_IIl','AnnotationSection_IIl','StatsSection_IIl']

import struct
f=open(R"C:\data\17n06003.abf",'rb')
for keyNumber,key in enumerate(KEYS_SECTIONS):
    f.seek(76+keyNumber*16)
    varName,varFormat=key.split("_")
    varSize=struct.calcsize(varFormat)
    byteString=f.read(varSize)
    blockStart,entrySize,entryCount=struct.unpack(varFormat,byteString)
    firstByte=blockStart*BLOCKSIZE
    print("%s @ byte %d (%d x %d byte entries)"%(varName,firstByte,entryCount,entrySize))
f.close()
```

### Example Output

```python
ProtocolSection @ byte 512 (1 x 512 byte entries)
ADCSection @ byte 1024 (1 x 128 byte entries)
DACSection @ byte 1536 (8 x 256 byte entries)
EpochSection @ byte 4096 (6 x 32 byte entries)
ADCPerDACSection @ byte 0 (0 x 0 byte entries)
EpochPerDACSection @ byte 3584 (6 x 48 byte entries)
UserListSection @ byte 0 (0 x 0 byte entries)
StatsRegionSection @ byte 4608 (1 x 128 byte entries)
MathSection @ byte 0 (0 x 0 byte entries)
StringsSection @ byte 5120 (20 x 172 byte entries)
DataSection @ byte 6656 (490000 x 2 byte entries)
TagSection @ byte 0 (0 x 0 byte entries)
ScopeSection @ byte 5632 (1 x 769 byte entries)
DeltaSection @ byte 0 (0 x 0 byte entries)
VoiceTagSection @ byte 0 (0 x 0 byte entries)
SynchArraySection @ byte 987136 (7 x 8 byte entries)
AnnotationSection @ byte 0 (0 x 0 byte entries)
StatsSection @ byte 0 (0 x 0 byte entries)
```

### Shortcut Method for Getting a Section's Byte Position
If you are only interested in getting the `blockStart`, `entrySize`, and `entryCount` of a single section, you can use this shortcut table. If you read an `IIl` struct from each of these byte positions, you will get these three values.

```
byte 076: ProtocolSection
byte 092: ADCSection
byte 108: DACSection
byte 124: EpochSection
byte 140: ADCPerDACSection
byte 156: EpochPerDACSection
byte 172: UserListSection
byte 188: StatsRegionSection
byte 204: MathSection
byte 220: StringsSection
byte 236: DataSection
byte 252: TagSection
byte 268: ScopeSection
byte 284: DeltaSection
byte 300: VoiceTagSection
byte 316: SynchArraySection
byte 332: AnnotationSection
byte 348: StatsSection
```

## List of Sections
Although I read byte information for all sections, I typically don't _use_ data from every section. Only those in bold contain information I think is useful. Note that other ABF reading platforms (such as the MatLab code and the Neo-IO scripts) ignore some sections too. One such ignored section is `EpochSection`, which I discovered contains the digital output codes typically displayed in the waveform editor tab (note that all the other epoch settings are in `EpochPerDACSection`).

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

# Reading theData
This section is largely redacted. The best way to see how data is read is to view the source code provided in this folder. It all boils down to the extraction of binary data into objects using variable lists and structure codes. Some complex sections (i.e., `EpochPerDACSection`) have a structure for each DAC and need to be iterated several times (according to the `entryCount` found when creating the section map).

# What information is available in an ABF?
ABF files contain a _lot_ of structured variables. Most likely are only interested in a handfull of them. I'll list all of the variables here and add comments to the ones I think are important or noteworthy. Note that there are plenty of variables for which I have no clue what they do.

## ProtocolSection (ABFHeader.protocol, dictionary)
This is the abf header we practiced reading from earlier in this document.
One advantage of this data block is that it can be read from any file (since it doesn't require creation of the section map). If you accidentally load a JPEG, you'll find out pretty quickly that something is wrong.

#### Example
```
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

#### Notes
* bytes 0-4 of the ABF file contain the file signature. It may be worth assuring this reads  `ABF2`
* convert to date using `dt=datetime.datetime.strptime(str(self.header['uFileStartDate']), "%Y%M%d")`
* add time with `dt=dt+datetime.timedelta(seconds=self.header['uFileStartTimeMS']/1000)`


## ADCSection (ABFHeader.adc, list of dictionaries)
There is a list of these, 1 per DAC. I don't use anythig from this currently.

#### Example

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

#### Example

```python
fBaselineDuration = 1.0
fBaselineLevel = 0.0
fDACCalibrationFactor = 1.0008957386016846
fDACCalibrationOffset = 0.0
fDACFileOffset = 0.0
fDACFileScale = 1.0
fDACHoldingLevel = 0.0 # this is the holding current
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

#### Example

```python
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

#### Notes
* Epoch types: 1=step, 4=ramp
  * One way to figure out the rest is to modify this byte in a hex editor then view the protocol!

## StringsSection (ABFHeader.strings and ABFHeader.stringsAll)
This section is very poorly documented, hwoever some quasi-useful information can be pulled from the strings parsing these keys can produce. First, throw away any keys that don't contain key words (AXENGN, clampex, Clampex, CLAMPEX, or axoscope). If a keyword is found, split the string at the key word and take the last part. Finally, split the string at 0x00. What's left are ~20 strings. These seem to be the ABF comment (if it exists), the protocol used to make the recording, and signal labels.


#### Example
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

#### Notes

* The first string is always the protocol file (if it exists) but I get mixed results on the second line. If a comment doesn't eixst, that line is just gone
* You probably should not rely on capturing unit information from these strings because they seem unreliable...

## DataSection
The data section is where the electrical recordings are stored. To see how to retrieve this data, navigate to the "Reading Sweep data" section of this document.

## TagSection (ABFHeader.tags)
At the end of the file are the tags (time-encoded text comments).

* I'm still working out the tag time units (are they microseconds?)

```python
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
When designing an application to read ABF sweep data, much attention should be paid to optomizing speed. For example, [Numpy's memmap feature](https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.memmap.html) seems like an excellent way to access sweep data directly from the file buffer! In this example, however, simplicity is desired over speed.

### Standalone Code to Read All Data in an ABF

```python
BLOCKSIZE=512
import struct
f=open(R"C:\data\17n06003.abf",'rb')
f.seek(236) # byte position (shortcut) for DataSection map information
blockStart,entrySize,entryCount=struct.unpack("IIl",f.read(struct.calcsize("IIl")))
f.seek(blockStart*BLOCKSIZE) # go to the byte position of the first data point
byteString=f.read(entrySize*entryCount) # read the data into a byte string
sweepData=struct.unpack('%dh'%(entryCount),byteString) # unpack it to a list
f.close()
```

That's it, really! If you want to test it out, try graphing what you got with matplotlib:

```python
import matplotlib.pyplot as plt
plt.plot(sweepData)
plt.show()
```
![](/doc/graphics/2017-11-06-raw.png)

Okay let's get fancier. This is the code I use to create an image of nice wide dimensions, high resolution, without a frame:

```python
import matplotlib.pyplot as plt
plt.figure(figsize=(10,2)) # figure dimensions
plt.plot(sweepData) # plot the data
plt.margins(0,0) # stretch the data to the window
plt.gca().axis('off') # remove square around edges
plt.xticks([]) # remove x labels
plt.yticks([]) # remove y labels
plt.tight_layout() # fill the frame space
plt.savefig(R"C:\data\2017-11-06-aps.png",dpi=200)
```
![](/doc/graphics/2017-11-06-aps.png)

### Notes

**Sweeps:** If you want to know where the bounds of individual sweeps are, look closer at the header. It contains a variable `lNumSamplesPerEpisode` which helps you determine data for each episode (sweep) starts. You could use something like:
```
sweepByteStart=int(byteDataStart+sweepNumber*(lNumSamplesPerEpisode*2))
```

**Scale:** Data coming out of the file is a signed integer. It needs to be convered to a float by dividing it by a scaling factor. The scaling factor also exists in the header variable as `lADCResolution`. To scale a list of sweep data, use something like:
```
dataScale=lADCResolution/1e6
sweepData=[x*dataScale for x in data]
```

# ABF1 Support
Eventually I'll get around to adding ABF1 support to the `ABFClass`. I think I can recycle almost all my code. The difference in ABF1 is that it doesn't require a section map, as the sections are all at pre-defined byte locations for every file. This should be trivial to implement... when I get around to it.


# File access, locking, and storing data in memory
Every ABF reading API probably has something like a `getSweepData(sweepNumber)` function which returns the data for that sweep. My goal is to design an ABF class which provides access to sweep data in the best way. I there are a few ways I can think of to go about this, each with different pros and cons.

* *ClampFit uses option 1.* - Pain in the butt becausae you can't view an ABF on a network drive if it's open on someone elses's computer.
* *abffio.dll uses option 2* - but I'm not 100% on this
* *I'm leaning toward option 3* - because I hate file blocking and I hate initiating the reading bytes over network drives

**OPTION 1 - Keep the ABF file open:** Open the ABF file for buffered reading when the header reading class is instantiated and leave it open. It's already open when we request a sweep's data, so just seek() to that position and return the file's contents.
  * **PRO:** opening the file takes a little bit of time (more on network drives) and so we save time by calling it once.
  * **CON:** The file is locked open until the user manually destroys the class or calls file.close(). Open ABF files can not be viewed by ClampFit or abffio.dll (orly?)

**OPTION 2 - Open the ABF when reading a sweep:** The goal here is to only have the ABF open when it's needed (once to read the header, then every time a sweep is requested). 
  * **PRO:** only blocks file when sweeps are requested
  * **PRO:** the user never has to manually close the file
  * **CON:** the small amount of time it takes to open/close a file is multiplied by the number of times a a sweep is requested. This becomes much slower on network drives.
  
**OPTION 3 - Load all sweep data in memory:** We could open the file just once to read the header then load ALL the signal data into memory and close the file forever. It isn't _that_ much memory. A 16-bit 20khz signal only takes up 40kB/sec (2.4 MB/min). A whole hour of recording is 144 MB. ***Attention should be paid to the format of storage!*** The data loaded from the ABF is `int16`, so mindlessly converting it to floats could easily double (`float16` half precision) or quadruple (`float32` single precision) memory requirements. However, since we know data will be converted to a float eventually (when multiplied by its scaling factor), maybe we can save time by doing the conversion when the data is loaded. Doubling the memory requirement (288 MB / hr of recording) would prevent the need for integer-to-float conversion and data scaling (float multiplication) later, improving performance.

  * **PRO:** no file blocking
  * **PRO:** file opening/closing time is eliminated (big pro for network drives)
  * **PRO:** on-demand file _reading_ time is eliminated (big pro for network drives)
  * **CON:** class instantiation time is increased, but this could be disabled with an argument
  

# Faster data extraction with Numpy
The slowest part about working with ABFs is reading their signal data (tens to hundreds of MB) and scaling it. Data is stored as signed 16-bit integers and must be scaled by a scaling factor and provided to the end user as an array of floats. While there are many ways we could read data from ABFs, if one is not careful they will write code that runs slowly. This is an easy trap for young players.

## Python's integers are bigger than your ABF's

```python
fileBuffer = open("flename.abf", 'rb')
fileBuffer.seek(someBytePosition)
byteString = fileBuffer.read(numberOfPoints*2)
dataValues = struct.unpack("%dh"%(numberOfPoints), byteString)
fileBuffer.close()
```

This code works, but there's a problem. We use `struct.unpack()` and request to decode the bytestring in `h` format (16-bit signed integer) from the bytestring. Consider our signal is just 100 data points. A 16-bit (2-byte) format means 100 points occupies 200 bytes of memory. However, `dataValues` is a tuple of integers _in your Python platform's default integer size_. For me that's 64-bit integers. This means that one line of code quadrupled the size of data in memory from 200 bytes to 800 bytes. For this reason, it is a bad idea to store ABF signal data in Python's default integer size.

## Numpy's highly structured arrays support Int16

```python
fileBuffer = open("flename.abf", 'rb')
fileBuffer.seek(someBytePosition)
dataValues = numpy.fromfile(fileBuffer, dtype=np.int16, count=numberOfPoints)
fileBuffer.close()
```

This code is faster and four times smaller in memory. It also eliminates the need to _convert_ to a numpy array later for scaling. If numpy is available, use this method! using `sys.getsizeof(dataValues)` you will learn that the entire numpy object is about 100 bytes larger than the data itself.

## Scaling signal data (and floating point conversion)
As we saw earlier when we tried to plot the raw data (unsigned integers), values right out of the ABF are crazy-large numbers and need to be scaled down before they are meaningful. The scaling factor is a float, and the fastest way to do what we want is to let numpy handle the integer/float multiplication and return the result as a numpy float datatype. Be sure to set the dtype! If your system's default float is a 64-bit float, we quadrupled our memory requirement again.

```python
scaleFactor = lADCResolution / 1e6
scaledData=np.multiply(dataValues,scaleFactor,dtype='float32')
```

**Should we use 16-, 32-, or 64-bit floats for representing signals?** Although float16 _might_ be okay, it distorts the trace a wee little bit due to floating point errors counfounded by the division and multiplication operations. In my recording conditions (whole-cell patch-clamp in brain slices) I calculated that the average floating point error in 16-bit floats (compared to 64-bit precision) is only 0.0023 pA. This seems acceptable (and well below the RMS noise floor), but also consider that the _peak_ floating point error in these conditions is 0.329632 pA. Also future operations (like low-pass filtering and baseline subtraction) would aplify this error and introduce additional error. That's not acceptable to me so I'll double my memory usage and go with a 32-bit floating point precision. 0.3 pA seems like a lot of error to me, but I think it comes from _two_ floating point math operations: one for the scale factor (int16 / float) and applying the scale factor (int16 * float). With 32-bit floats our peak deviation (compared to 64-bit precision) is 0.0000160469 pA. If I reach a point where that is not enough precision, I will want to find a new job. For now I'm satisfied with float-32 because we know it's accurate and at 20kHz recording rate (40 kB raw data / sec) we produce 80 kB of scaled floating-point data per second (or 288 MB per hour of recording).


# Designing for Numpy as an option (not a requirement)
I want my ABFHeader class to be dependency-free. Buuuuuuut if numpy is around, let's use it. For all the reasons listed above, using numpy will massively improve performance. This is what I did to make Numpy optional:

### Optional import of Numpy

When importing the abf header module, try to import numpy. If it fails, that's fine!

```python
try:
    import numpy as np # use Numpy if we have it
except:
    np=False
```

### Optional use of Numpy

When sweeps are requested, use Numpy if we have it, and don't if we don't! Functionality is exactly the same if numpy is available or not. The difference is numpy is faster and will return a `ndarray` object if it's used. Otherwise you'll get a traditional python list. The values are the same!

```python
fb=open("someFile.abf",'rb')
fb.seek(firstBytePosition)
scaleFactor = self.header['lADCResolution'] / 1e6
if np:
	data = np.fromfile(fb, dtype=np.int16, count=pointCount)
	data = np.multiply(data,scaleFactor,dtype='float32')
else:
	print("WARNING: data is being retrieved without numpy (this is slow). See docs.")
	data = struct.unpack("%dh"%(pointCount), fb.read(pointCount*2)) # 64-bit int
	data = [point*scaleFactor for point in data] # 64-bit int * 64-bit floating point
fb.close()
```

# Performance Testing

## Numpy vs. Python: Sweep Hopping

I wrote a stress test that opens a 15 MB ABF file (about 6 minutes of data) and reads every sweep, and repeats this ten times. It then reports the total number of sweeps read, how long it took, and the average read time per sweep.

```
Without Numpy
read 1870 sweeps in 4.38152 sec (2.343 ms/sweep)
read 1870 sweeps in 4.37068 sec (2.337 ms/sweep)
read 1870 sweeps in 4.37608 sec (2.340 ms/sweep)
read 1870 sweeps in 4.37229 sec (2.338 ms/sweep)
read 1870 sweeps in 4.47250 sec (2.392 ms/sweep)
total 21.97307 sec

With Numpy
read 1870 sweeps in 0.34502 sec (0.185 ms/sweep)
read 1870 sweeps in 0.32036 sec (0.171 ms/sweep)
read 1870 sweeps in 0.31698 sec (0.170 ms/sweep)
read 1870 sweeps in 0.31709 sec (0.170 ms/sweep)
read 1870 sweeps in 0.32123 sec (0.172 ms/sweep)
total 1.62068 sec
```

**Conclusion:** Numpy is 13.56 times faster than pure python when loading sweeps

## Numpy vs. Python: Full File Reading

I was surprised to see performance goes in opposite directions when I load the full file in one block as compared to sweep by sweep. I think the weak point here is the `[x for x in y]` python code, and numpy shines. The performance _increase_ for numpy is probably the decrease in the need to `seek()` 1870 times.

```
without Numpy
read 1870 full file 10 times in 7.35235 sec (3.932 ms/load)
read 1870 full file 10 times in 7.30406 sec (3.906 ms/load)
read 1870 full file 10 times in 7.43636 sec (3.977 ms/load)
read 1870 full file 10 times in 7.32984 sec (3.920 ms/load)
read 1870 full file 10 times in 7.39116 sec (3.952 ms/load)
total 36.81377 sec

with Numpy
read full file 10 times in 0.23099 sec (0.124 ms/load)
read full file 10 times in 0.21806 sec (0.117 ms/load)
read full file 10 times in 0.21913 sec (0.117 ms/load)
read full file 10 times in 0.21845 sec (0.117 ms/load)
read full file 10 times in 0.21978 sec (0.118 ms/load)
total 1.10641 sec
```

**Conclusion:** Numpy is 33.27 times faster than pure python when loading a full file

## Loading Full Files into Memory: do this!
These data demonstrate that reading a full file into memory (and scaling it) is extremely fast and doesn't take-up much memory. I vote we do this automatically without even asking. A one-hour-long ABF would take one second to load into memory (incluidng scaling) and only occupy 288 MB of memory. Open a file, grab its header, pull its data, and close it. File locking issues gone forever.

# Epoch/signal misalignment and pre-padding offset
For some reason I still don't understand, some data gets recorded _before_ epoch A begins in each sweep. More confusingly, it's not a fixed amount of pre-epoch time for each sweep. Instead, ***Exactly 1/64'th of the sweep length exists in the pre-epoch area at the beginning each sweep.*** This must be taken into account if you intend to synthesize the protocol waveform from just the epoch table. This is what I've done, and these are my results.

# Byte Map (fixed & dynamic)
I read an ABF file and noted the byte position(s) for every value. Some byte positions may change, but some don't. It's on you to look up which are fixed. I added this functionality to the ABFheader class as `ABFheader._byteMap`. This map is useful when answering questions like, "_What byte position would I look at to find `lADCResolution`?_" (which assumes you know that `lADCResolution` is part of the header structure and is not part of a section with a dynamic location)

```
fFileSignature [0]
fFileVersionNumber [4]
uFileInfoSize [8]
lActualEpisodes [12]
uFileStartDate [16]
uFileStartTimeMS [20]
uStopwatchTime [24]
nFileType [28]
nDataFormat [30]
nSimultaneousScan [32]
nCRCEnable [34]
uFileCRC [36]
FileGUID [40]
unknown1 [44]
unknown2 [48]
unknown3 [52]
uCreatorVersion [56]
uCreatorNameIndex [60]
uModifierVersion [64]
uModifierNameIndex [68]
uProtocolPathIndex [72]
ProtocolSection [76]
ADCSection [92]
DACSection [108]
EpochSection [124]
ADCPerDACSection [140]
EpochPerDACSection [156]
UserListSection [172]
StatsRegionSection [188]
MathSection [204]
StringsSection [220]
DataSection [236]
TagSection [252]
ScopeSection [268]
DeltaSection [284]
VoiceTagSection [300]
SynchArraySection [316]
AnnotationSection [332]
StatsSection [348]
nOperationMode [512]
fADCSequenceInterval [514]
bEnableFileCompression [518]
sUnused [519]
uFileCompressionRatio [522]
fSynchTimeUnit [526]
fSecondsPerRun [530]
lNumSamplesPerEpisode [534]
lPreTriggerSamples [538]
lEpisodesPerRun [542]
lRunsPerTrial [546]
lNumberOfTrials [550]
nAveragingMode [554]
nUndoRunCount [556]
nFirstEpisodeInRun [558]
fTriggerThreshold [560]
nTriggerSource [564]
nTriggerAction [566]
nTriggerPolarity [568]
fScopeOutputInterval [570]
fEpisodeStartToStart [574]
fRunStartToStart [578]
lAverageCount [582]
fTrialStartToStart [586]
nAutoTriggerStrategy [590]
fFirstRunDelayS [592]
nChannelStatsStrategy [596]
lSamplesPerTrace [598]
lStartDisplayNum [602]
lFinishDisplayNum [606]
nShowPNRawData [610]
fStatisticsPeriod [612]
lStatisticsMeasurements [616]
nStatisticsSaveStrategy [620]
fADCRange [622]
fDACRange [626]
lADCResolution [630]
lDACResolution [634]
nExperimentType [638]
nManualInfoStrategy [640]
nCommentsEnable [642]
lFileCommentIndex [644]
nAutoAnalyseEnable [648]
nSignalType [650]
nDigitalEnable [652]
nActiveDACChannel [654]
nDigitalHolding [656]
nDigitalInterEpisode [658]
nDigitalDACChannel [660]
nDigitalTrainActiveLogic [662]
nStatsEnable [664]
nStatisticsClearStrategy [666]
nLevelHysteresis [668]
lTimeHysteresis [670]
nAllowExternalTags [674]
nAverageAlgorithm [676]
fAverageWeighting [678]
nUndoPromptStrategy [682]
nTrialTriggerSource [684]
nStatisticsDisplayStrategy [686]
nExternalTagType [688]
nScopeTriggerOut [690]
nLTPType [692]
nAlternateDACOutputState [694]
nAlternateDigitalOutputState [696]
fCellID [698]
nDigitizerADCs [710]
nDigitizerDACs [712]
nDigitizerTotalDigitalOuts [714]
nDigitizerSynchDigitalOuts [716]
nDigitizerType [718]
nADCNum [1024]
nTelegraphEnable [1026]
nTelegraphInstrument [1028]
fTelegraphAdditGain [1030]
fTelegraphFilter [1034]
fTelegraphMembraneCap [1038]
nTelegraphMode [1042]
fTelegraphAccessResistance [1044]
nADCPtoLChannelMap [1048]
nADCSamplingSeq [1050]
fADCProgrammableGain [1052]
fADCDisplayAmplification [1056]
fADCDisplayOffset [1060]
fInstrumentScaleFactor [1064]
fInstrumentOffset [1068]
fSignalGain [1072]
fSignalOffset [1076]
fSignalLowpassFilter [1080]
fSignalHighpassFilter [1084]
nLowpassFilterType [1088]
nHighpassFilterType [1089]
fPostProcessLowpassFilter [1090]
nPostProcessLowpassFilterType [1094]
bEnabledDuringPN [1095]
nStatsChannelPolarity [1096]
lADCChannelNameIndex [1098]
lADCUnitsIndex [1102]
nDACNum [1536, 1792, 2048, 2304, 2560, 2816, 3072, 3328, 3586, 3634, 3682, 3730, 3778]
nTelegraphDACScaleFactorEnable [1538, 1794, 2050, 2306, 2562, 2818, 3074, 3330]
fInstrumentHoldingLevel [1540, 1796, 2052, 2308, 2564, 2820, 3076, 3332]
fDACScaleFactor [1544, 1800, 2056, 2312, 2568, 2824, 3080, 3336]
fDACHoldingLevel [1548, 1804, 2060, 2316, 2572, 2828, 3084, 3340]
fDACCalibrationFactor [1552, 1808, 2064, 2320, 2576, 2832, 3088, 3344]
fDACCalibrationOffset [1556, 1812, 2068, 2324, 2580, 2836, 3092, 3348]
lDACChannelNameIndex [1560, 1816, 2072, 2328, 2584, 2840, 3096, 3352]
lDACChannelUnitsIndex [1564, 1820, 2076, 2332, 2588, 2844, 3100, 3356]
lDACFilePtr [1568, 1824, 2080, 2336, 2592, 2848, 3104, 3360]
lDACFileNumEpisodes [1572, 1828, 2084, 2340, 2596, 2852, 3108, 3364]
nWaveformEnable [1576, 1832, 2088, 2344, 2600, 2856, 3112, 3368]
nWaveformSource [1578, 1834, 2090, 2346, 2602, 2858, 3114, 3370]
nInterEpisodeLevel [1580, 1836, 2092, 2348, 2604, 2860, 3116, 3372]
fDACFileScale [1582, 1838, 2094, 2350, 2606, 2862, 3118, 3374]
fDACFileOffset [1586, 1842, 2098, 2354, 2610, 2866, 3122, 3378]
lDACFileEpisodeNum [1590, 1846, 2102, 2358, 2614, 2870, 3126, 3382]
nDACFileADCNum [1594, 1850, 2106, 2362, 2618, 2874, 3130, 3386]
nConditEnable [1596, 1852, 2108, 2364, 2620, 2876, 3132, 3388]
lConditNumPulses [1598, 1854, 2110, 2366, 2622, 2878, 3134, 3390]
fBaselineDuration [1602, 1858, 2114, 2370, 2626, 2882, 3138, 3394]
fBaselineLevel [1606, 1862, 2118, 2374, 2630, 2886, 3142, 3398]
fStepDuration [1610, 1866, 2122, 2378, 2634, 2890, 3146, 3402]
fStepLevel [1614, 1870, 2126, 2382, 2638, 2894, 3150, 3406]
fPostTrainPeriod [1618, 1874, 2130, 2386, 2642, 2898, 3154, 3410]
fPostTrainLevel [1622, 1878, 2134, 2390, 2646, 2902, 3158, 3414]
nMembTestEnable [1626, 1882, 2138, 2394, 2650, 2906, 3162, 3418]
nLeakSubtractType [1628, 1884, 2140, 2396, 2652, 2908, 3164, 3420]
nPNPolarity [1630, 1886, 2142, 2398, 2654, 2910, 3166, 3422]
fPNHoldingLevel [1632, 1888, 2144, 2400, 2656, 2912, 3168, 3424]
nPNNumADCChannels [1636, 1892, 2148, 2404, 2660, 2916, 3172, 3428]
nPNPosition [1638, 1894, 2150, 2406, 2662, 2918, 3174, 3430]
nPNNumPulses [1640, 1896, 2152, 2408, 2664, 2920, 3176, 3432]
fPNSettlingTime [1642, 1898, 2154, 2410, 2666, 2922, 3178, 3434]
fPNInterpulse [1646, 1902, 2158, 2414, 2670, 2926, 3182, 3438]
nLTPUsageOfDAC [1650, 1906, 2162, 2418, 2674, 2930, 3186, 3442]
nLTPPresynapticPulses [1652, 1908, 2164, 2420, 2676, 2932, 3188, 3444]
lDACFilePathIndex [1654, 1910, 2166, 2422, 2678, 2934, 3190, 3446]
fMembTestPreSettlingTimeMS [1658, 1914, 2170, 2426, 2682, 2938, 3194, 3450]
fMembTestPostSettlingTimeMS [1662, 1918, 2174, 2430, 2686, 2942, 3198, 3454]
nLeakSubtractADCIndex [1666, 1922, 2178, 2434, 2690, 2946, 3202, 3458]
nEpochNum [3584, 3632, 3680, 3728, 3776, 4096, 4128, 4160, 4192, 4224]
nEpochType [3588, 3636, 3684, 3732, 3780]
fEpochInitLevel [3590, 3638, 3686, 3734, 3782]
fEpochLevelInc [3594, 3642, 3690, 3738, 3786]
lEpochInitDuration [3598, 3646, 3694, 3742, 3790]
lEpochDurationInc [3602, 3650, 3698, 3746, 3794]
lEpochPulsePeriod [3606, 3654, 3702, 3750, 3798]
lEpochPulseWidth [3610, 3658, 3706, 3754, 3802]
nEpochDigitalOutput [4098, 4130, 4162, 4194, 4226]
```

# References

* [Python struct format characters](https://docs.python.org/2/library/struct.html#format-characters)
* [Numpy.fromfile()](https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.fromfile.html)
* [Numpy's built-in dataypes](https://docs.scipy.org/doc/numpy-1.13.0/reference/arrays.scalars.html#arrays-scalars-built-in)

## Equipment and Theory
* [Axoclamp-2B theory and operation](https://neurophysics.ucsd.edu/Manuals/Axon%20Instruments/Axoclamp-2B_Manual.pdf)
* [pCLAMP 10 User Guide](https://neurophysics.ucsd.edu/Manuals/Axon%20Instruments/pCLAMP10-User-Guide-RevA.pdf)

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
