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
