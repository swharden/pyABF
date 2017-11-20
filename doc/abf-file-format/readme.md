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

**Scale in multi-channel ABFs:** I haven't tested this extensively, but for some reason I got a weird behavior where the scale in 2-channel ABFs needed to be multiplied by 2. I don't understand it well enough to say this with confidence, but I suspect this is what should be done:
```
dataScale=lADCResolution/1e6*numberOfChannels
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

# Using a Byte Map To Extract Single Header Values
Let's say we aren't interested in tags and amplifier settings and epochs and all that stuff. We just want to capture a couple values out of an ABF header. In this case, even the 300 line ABFheader class is overkill, as we can get these values in about ten lines. This bytemap indicates which variables have fixed vs dynamic byte locations in the ABF file, and walks you through how to capture a value even if it's in a dynamically-located section.

**Example Problem:** _How can I read just `lADCResolution` from an ABF header?_
* Ensure the first 4 bytes of the file are `b'ABF2'`
* Notice `lADCResolution` is in `ProtocolSection` so find that section's byte position
* byte 76 of the section map (fixed byte positions) indicates the `ProtocolSection` start block.
* We know from the section key that `ProtocolSection` has a structure format of `IIl`. These are 3 variables (blockNumber, entrySize, entryCount) and we only want the first one.
* We know from the byte map below (ABFheader._byteMap) that the byte idicating where ProtocolSection starts is at byte 76.
* To get `blockNumber` just read the `I` (a 4-byte unsigned integer) at byte position 76
* `bytePosition = blockNumber * 512` (ABF2 blocks are a fixed 512 bytes)
* We know from the section key that `lADCResolution` has struct format `i` (a 4-byte signed integer)
* Therefore, just read the struct format `i` at position `bytePosition` and you have your `lADCResolution`

**Example Code:** This STANDALONE script reads all sweep data and scales it using lADCResolution
```python
import struct
import numpy as np

def getSectionValue(fb,byteOfSectionBlock,sectionOffset=0,fmt="h"):
    """Return an arbitrary value from an arbitrary section in an ABF2 header."""
    fb.seek(byteOfSectionBlock)
    sectionBlock,entryByteSize,entryCount=struct.unpack("IIl",fb.read(struct.calcsize("IIl")))
    fmt=str(entryCount)+fmt
    fb.seek(sectionBlock*512+sectionOffset)
    val=struct.unpack(fmt,fb.read(struct.calcsize(fmt)))
    val=val[0] if len(val)==1 else val
    return val

def getScaledSignalData(abfFileName):
    """Return a numpy array of the scaled signal data for a recording."""
    fb=open(abfFileName,'rb')
    if not fb.read(4)==b'ABF2':
        raise ValueError("only ABF2 files are supported by this example")
    scalingFactor = getSectionValue(fb,76,118,"i") # ProtocolSection [76] (just want lADCResolution [118])
    data = getSectionValue(fb,236) # DataSection [236] (we want all of it)
    fb.close()    
    return np.array(data)*scalingFactor/1e6

signalData = getScaledSignalData("../../../../data/17o05027_ic_ramp.abf")
print(signalData)    
```

**Output:** `[-51.544064 -51.6096   -51.675136 ..., -42.074112 -42.074112 -42.041344]`

## Byte Map
_this data is accessible via `ABFHeader._byteMap`_

```
### Header (fixed byte positions) ###
fFileSignature: [0]
fFileVersionNumber: [4]
uFileInfoSize: [8]
lActualEpisodes: [12]
uFileStartDate: [16]
uFileStartTimeMS: [20]
uStopwatchTime: [24]
nFileType: [28]
nDataFormat: [30]
nSimultaneousScan: [32]
nCRCEnable: [34]
uFileCRC: [36]
FileGUID: [40]
unknown1: [44]
unknown2: [48]
unknown3: [52]
uCreatorVersion: [56]
uCreatorNameIndex: [60]
uModifierVersion: [64]
uModifierNameIndex: [68]
uProtocolPathIndex: [72]

### Section Map (fixed byte positions) ###
ProtocolSection: [76]
ADCSection: [92]
DACSection: [108]
EpochSection: [124]
ADCPerDACSection: [140]
EpochPerDACSection: [156]
UserListSection: [172]
StatsRegionSection: [188]
MathSection: [204]
StringsSection: [220]
DataSection: [236]
TagSection: [252]
ScopeSection: [268]
DeltaSection: [284]
VoiceTagSection: [300]
SynchArraySection: [316]
AnnotationSection: [332]
StatsSection: [348]

### ProtocolSection (section byte offsets) ###
nOperationMode: [+0]
fADCSequenceInterval: [+2]
bEnableFileCompression: [+6]
sUnused: [+7]
uFileCompressionRatio: [+10]
fSynchTimeUnit: [+14]
fSecondsPerRun: [+18]
lNumSamplesPerEpisode: [+22]
lPreTriggerSamples: [+26]
lEpisodesPerRun: [+30]
lRunsPerTrial: [+34]
lNumberOfTrials: [+38]
nAveragingMode: [+42]
nUndoRunCount: [+44]
nFirstEpisodeInRun: [+46]
fTriggerThreshold: [+48]
nTriggerSource: [+52]
nTriggerAction: [+54]
nTriggerPolarity: [+56]
fScopeOutputInterval: [+58]
fEpisodeStartToStart: [+62]
fRunStartToStart: [+66]
lAverageCount: [+70]
fTrialStartToStart: [+74]
nAutoTriggerStrategy: [+78]
fFirstRunDelayS: [+80]
nChannelStatsStrategy: [+84]
lSamplesPerTrace: [+86]
lStartDisplayNum: [+90]
lFinishDisplayNum: [+94]
nShowPNRawData: [+98]
fStatisticsPeriod: [+100]
lStatisticsMeasurements: [+104]
nStatisticsSaveStrategy: [+108]
fADCRange: [+110]
fDACRange: [+114]
lADCResolution: [+118]
lDACResolution: [+122]
nExperimentType: [+126]
nManualInfoStrategy: [+128]
nCommentsEnable: [+130]
lFileCommentIndex: [+132]
nAutoAnalyseEnable: [+136]
nSignalType: [+138]
nDigitalEnable: [+140]
nActiveDACChannel: [+142]
nDigitalHolding: [+144]
nDigitalInterEpisode: [+146]
nDigitalDACChannel: [+148]
nDigitalTrainActiveLogic: [+150]
nStatsEnable: [+152]
nStatisticsClearStrategy: [+154]
nLevelHysteresis: [+156]
lTimeHysteresis: [+158]
nAllowExternalTags: [+162]
nAverageAlgorithm: [+164]
fAverageWeighting: [+166]
nUndoPromptStrategy: [+170]
nTrialTriggerSource: [+172]
nStatisticsDisplayStrategy: [+174]
nExternalTagType: [+176]
nScopeTriggerOut: [+178]
nLTPType: [+180]
nAlternateDACOutputState: [+182]
nAlternateDigitalOutputState: [+184]
fCellID: [+186]
nDigitizerADCs: [+198]
nDigitizerDACs: [+200]
nDigitizerTotalDigitalOuts: [+202]
nDigitizerSynchDigitalOuts: [+204]
nDigitizerType: [+206]

### ADCSection (section byte offsets) ###
nADCNum: [+0]
nTelegraphEnable: [+2]
nTelegraphInstrument: [+4]
fTelegraphAdditGain: [+6]
fTelegraphFilter: [+10]
fTelegraphMembraneCap: [+14]
nTelegraphMode: [+18]
fTelegraphAccessResistance: [+20]
nADCPtoLChannelMap: [+24]
nADCSamplingSeq: [+26]
fADCProgrammableGain: [+28]
fADCDisplayAmplification: [+32]
fADCDisplayOffset: [+36]
fInstrumentScaleFactor: [+40]
fInstrumentOffset: [+44]
fSignalGain: [+48]
fSignalOffset: [+52]
fSignalLowpassFilter: [+56]
fSignalHighpassFilter: [+60]
nLowpassFilterType: [+64]
nHighpassFilterType: [+65]
fPostProcessLowpassFilter: [+66]
nPostProcessLowpassFilterType: [+70]
bEnabledDuringPN: [+71]
nStatsChannelPolarity: [+72]
lADCChannelNameIndex: [+74]
lADCUnitsIndex: [+78]

### DACSection (section byte offsets) ###
nDACNum: [+0]
nTelegraphDACScaleFactorEnable: [+2]
fInstrumentHoldingLevel: [+4]
fDACScaleFactor: [+8]
fDACHoldingLevel: [+12]
fDACCalibrationFactor: [+16]
fDACCalibrationOffset: [+20]
lDACChannelNameIndex: [+24]
lDACChannelUnitsIndex: [+28]
lDACFilePtr: [+32]
lDACFileNumEpisodes: [+36]
nWaveformEnable: [+40]
nWaveformSource: [+42]
nInterEpisodeLevel: [+44]
fDACFileScale: [+46]
fDACFileOffset: [+50]
lDACFileEpisodeNum: [+54]
nDACFileADCNum: [+58]
nConditEnable: [+60]
lConditNumPulses: [+62]
fBaselineDuration: [+66]
fBaselineLevel: [+70]
fStepDuration: [+74]
fStepLevel: [+78]
fPostTrainPeriod: [+82]
fPostTrainLevel: [+86]
nMembTestEnable: [+90]
nLeakSubtractType: [+92]
nPNPolarity: [+94]
fPNHoldingLevel: [+96]
nPNNumADCChannels: [+100]
nPNPosition: [+102]
nPNNumPulses: [+104]
fPNSettlingTime: [+106]
fPNInterpulse: [+110]
nLTPUsageOfDAC: [+114]
nLTPPresynapticPulses: [+116]
lDACFilePathIndex: [+118]
fMembTestPreSettlingTimeMS: [+122]
fMembTestPostSettlingTimeMS: [+126]
nLeakSubtractADCIndex: [+130]

### EpochPerDACSection (section byte offsets) ###
nEpochNum: [+0]
nEpochType: [+4]
fEpochInitLevel: [+6]
fEpochLevelInc: [+10]
lEpochInitDuration: [+14]
lEpochDurationInc: [+18]
lEpochPulsePeriod: [+22]
lEpochPulseWidth: [+26]

### EpochSection (section byte offsets) ###
nEpochDigitalOutput: [+2]

### TagSection (section byte offsets) ###
lTagTime: [+0]
sComment: [+4]
nTagType: [+60]
nVoiceTagNumberorAnnotationIndex: [+62]
```

# Reading Multichannel ABFs
Raw data is interleaved by the number of channels. That's it! The number of channels is the number of entries (the third value of `ADCSection`).

**Python tips:** 
* Get every 7th number from a python list: use `data=someList[::7]`. 
* Get every 7th number starting from the third point: `data=someList[2::7]`. 
* Get an ABF signal:  `data=abfData[channel::numberOfChannels]`.

**Example: plot multi-channel ABF data**
```python
import matplotlib.pyplot as plt
import numpy as np
abf=ABFheader(abfFileName)
for i in range(abf.header['dataChannels']):
	Ys=abf.data[i::abf.header['dataChannels']]
	Xs=np.arange(len(Ys))*abf.header['timeSecPerPoint']
	plt.plot(Xs,Ys)
```

![](/doc/graphics/2017-11-18-multichannel.png)


# Reading ABF1 Files
Although I created this entire project with the intent of only working with ABF2 files (all of my personal data is ABF2, and Clampex has been creating ABF2 files since 2006), reading ABF1 files is so easy I might as well just document it. Forget everything you know about byte maps and sections. ABF1 has a fixed header structure. 

**Fixed header structure of the ABF1 header.** _(Each item expresses variableName, byteLocation, and structFormat)_

```python
HEADERV1 = [('fFileSignature',0,'4s'),('fFileVersionNumber',4,'f'),('nOperationMode',8,'h'),
('lActualAcqLength',10,'i'),('nNumPointsIgnored',14,'h'),('lActualEpisodes',16,'i'),('lFileStartTime',24,'i'),
('lDataSectionPtr',40,'i'),('lTagSectionPtr',44,'i'),('lNumTagEntries',48,'i'),('lSynchArrayPtr',92,'i'),
('lSynchArraySize',96,'i'),('nDataFormat',100,'h'),('nADCNumChannels',120,'h'),('fADCSampleInterval',122,'f'),
('fSynchTimeUnit',130,'f'),('lNumSamplesPerEpisode',138,'i'),('lPreTriggerSamples',142,'i'),
('lEpisodesPerRun',146,'i'),('fADCRange',244,'f'),('lADCResolution',252,'i'),('nFileStartMillisecs',366,'h'),
('nADCPtoLChannelMap',378,'16h'),('nADCSamplingSeq',410,'16h'),('sADCChannelName',442,'10s'*16),
('sADCUnits',602,'8s'*16),('fADCProgrammableGain',730,'16f'),('fInstrumentScaleFactor',922,'16f'),
('fInstrumentOffset',986,'16f'),('fSignalGain',1050,'16f'),('fSignalOffset',1114,'16f'),
('nDigitalEnable',1436,'h'),('nActiveDACChannel',1440,'h'),('nDigitalHolding',1584,'h'),
('nDigitalInterEpisode',1586,'h'),('nDigitalValue',2588,'10h'),('lDACFilePtr',2048,'2i'),
('lDACFileNumEpisodes',2056,'2i'),('fDACCalibrationFactor',2074,'4f'),('fDACCalibrationOffset',2090,'4f'),
('nWaveformEnable',2296,'2h'),('nWaveformSource',2300,'2h'),('nInterEpisodeLevel',2304,'2h'),
('nEpochType',2308,'20h'),('fEpochInitLevel',2348,'20f'),('fEpochLevelInc',2428,'20f'),
('lEpochInitDuration',2508,'20i'),('lEpochDurationInc',2588,'20i'),('nTelegraphEnable',4512,'16h'),
('fTelegraphAdditGain',4576,'16f'),('sProtocolPath',4898,'384s')]
```

**Example ABF1 header values from an old file I found:**
```
fFileSignature = ['ABF']
fFileVersionNumber = [1.8300000429153442]
nOperationMode = [5]
lActualAcqLength = [720000]
nNumPointsIgnored = [0]
lActualEpisodes = [6]
lFileStartTime = [57175]
lDataSectionPtr = [16]
lTagSectionPtr = [0]
lNumTagEntries = [0]
lSynchArrayPtr = [2829]
lSynchArraySize = [6]
nDataFormat = [0]
nADCNumChannels = [2]
fADCSampleInterval = [25.0]
fSynchTimeUnit = [12.5]
lNumSamplesPerEpisode = [120000]
lPreTriggerSamples = [32]
lEpisodesPerRun = [6]
fADCRange = [10.0]
lADCResolution = [32768]
nFileStartMillisecs = [328]
nADCPtoLChannelMap = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
nADCSamplingSeq = [0, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
sADCChannelName = ['Voltage 0', 'Current 1', 'IN 2', 'Ext Cmd', 'IN 4', 'IN 5', 'I_Steps', 'IN 7', 'IN 8', 'IN 9', 'IN 10', 'IN 11', 'IN 12', 'IN 13', 'readout', 'exposure']
sADCUnits = ['pA', 'pA', 'V', 'mV', 'V', 'V', 'pA', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V']
fADCProgrammableGain = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
fInstrumentScaleFactor = [0.0005000000237487257, 0.0005000000237487257, 1.0, 0.05000000074505806, 1.0, 1.0, 0.002469999948516488, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
fInstrumentOffset = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
fSignalGain = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
fSignalOffset = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
nDigitalEnable = [1]
nActiveDACChannel = [0]
nDigitalHolding = [16]
nDigitalInterEpisode = [0]
nDigitalValue = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
lDACFilePtr = [0, 0]
lDACFileNumEpisodes = [0, 0]
fDACCalibrationFactor = [1.0842299461364746, 1.0852099657058716, 1.0, 1.0]
fDACCalibrationOffset = [-253.0, -260.0, 0.0, 0.0]
nWaveformEnable = [1, 0]
nWaveformSource = [1, 1]
nInterEpisodeLevel = [0, 0]
nEpochType = [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
fEpochInitLevel = [-70.0, -80.0, -70.0, -70.0, -70.0, -70.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
fEpochLevelInc = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
lEpochInitDuration = [100, 1000, 20, 10000, 100, 30000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
lEpochDurationInc = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
nTelegraphEnable = [1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
fTelegraphAdditGain = [20.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
sProtocolPath = ['D:\\Data\\Protocols\\noMovies).pro']
```

# Porting to C#

_**ADDITIONAL CODE:** Full source code, more programs, and downloadable Visual Studio project files are in the [/dev/](/dev/) folder_

I whipped up a function for C# which reads sweeps of scaled data right out of ABF2 files. It's a little thin on the error checking, but it gets the job done. Don't forget to add `using System.IO;` to the top so we have access to BinaryReader. By the way, my SweepReader.exe is 6kb.

### Example Standalone Sweep Reading Function

```C#
/* Return an array of scaled data from a given sweep (sweep numbers start at 1) */
public static float[] GetSweepData(string abfFileName, int sweepNumber=1)
{
	// open the file in binary mode
	BinaryReader fb = new BinaryReader(File.Open(abfFileName, FileMode.Open));

	// verify this is an ABF2 file
	if (new string(fb.ReadChars(4)) != "ABF2")
		throw new System.ArgumentException("The file is not a valid ABF2 file.");

	// pull everything we need from the header information (using our byte map cheat sheet)
	int BLOCKSIZE = 512; // blocks are a fixed size in ABF1 and ABF2 files
	fb.BaseStream.Seek(12, SeekOrigin.Begin); // this byte stores the number of sweeps
	long sweepCount = fb.ReadUInt32();
	fb.BaseStream.Seek(76, SeekOrigin.Begin); // this byte stores the ProtocolSection block number
	long posProtocolSection = fb.ReadUInt32()*BLOCKSIZE;
	long poslADCResolution = posProtocolSection + 118; // figure out where lADCResolution lives
	fb.BaseStream.Seek(poslADCResolution, SeekOrigin.Begin); // then go there
	long lADCResolution = fb.ReadInt32();
	float scaleFactor = lADCResolution / (float)1e6;
	fb.BaseStream.Seek(236, SeekOrigin.Begin); // this byte stores the DataSection block number
	long posDataSection = fb.ReadUInt32() * BLOCKSIZE;
	long dataPointByteSize = fb.ReadUInt32(); // this will always be 2 for a 16-bit DAC
	long dataPointCount = fb.ReadInt64();
	long sweepPointCount = dataPointCount / sweepCount;

	// make sure our requested sweep is valid
	if ((sweepNumber > sweepCount) ||(sweepNumber < 1))
		throw new System.ArgumentException("Invalid sweep requested.");

	// figure out what data positions we want to read (modify these lines to get ALL data)
	long dataByteStart = posDataSection + (sweepNumber-1) * sweepPointCount * dataPointByteSize;
	long pointsToRead = sweepPointCount;

	// fill the float array by reading raw data out of the ABF, scaling as we go
	fb.BaseStream.Seek(dataByteStart, SeekOrigin.Begin);
	float[] data = new float[pointsToRead];
	for (long i=0; i < pointsToRead; i++)
		data[i] = fb.ReadInt16() * scaleFactor;
	fb.Close(); // close and unlock the file ASAP

	// display the data
	System.Console.Write("DATA FOR SWEEP {0}: ",sweepNumber);
	for (int i =0; i<3; i++)
		System.Console.Write("{0}, ", data[i]);
	System.Console.Write("...");
	for (int i = 3; i > 0; i--)
		System.Console.Write(", {0}", data[pointsToRead - i]);
	System.Console.Write(" ({0} points in total)\n",data.Length);

	return data;
}
```

### Output
`DATA FOR SWEEP 1: -4.325376, -4.292608, -4.096, ..., -6.651904, -6.684672, -6.848512 (200000 points in total)`


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
