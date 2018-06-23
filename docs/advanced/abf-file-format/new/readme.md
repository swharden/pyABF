> ## WARNING: INCOMPLETE CONTENT
This document is a work in progress. Until it is complete, refer to the [old version](../) of this document.

---

# Unofficial Guide to the ABF File Format

***by [Scott Harden](http://www.SWHarden.com)***

### Introduction

The field of cellular electrophysiology uses highly-sensitive voltage and current measurement devices to gain insights into the electrical properties of biological membranes. Voltage-clamp and current-clamp circuits are used to measure the flow of ions through ion channels embedded in small patches of cell membranes. This technique is called _patch-clamp electrophysiology_, and Axon Instruments (now a division of Molecular Devices) sells patch-clamp systems (including amplifiers, digitizers, and software) which are commonly used by electrophysiologists in scientific research environments. Electrophysiological data produced by theses systems is saved in Axon Binary Format (ABF) files. Their patch-clamp analysis software suite (pCLAMP) includes acquisition software (Clampex) and analysis software (ClampFit) which can read and write ABF files.

### Reading ABF Files

Axon Binary Format (ABF) files are encoded in a proprietary format. In the late 90s and early 2000s the internal file structure of ABF files was widely understood and custom software could be easily written to read data from these files. In 2006 pCLAMP 10 was released, featuring a new file format (ABF2) which was intentionally undocumented. Programmers seeking to write software to analyze ABF files were told by Molecular Devices that they had to interact with ABF files exclusively through a 32-bit Windows-only DLL (abffio.dll) they provide (without source code) as part of the Axon pCLAMP SDK.

> "_One of the goals of the ABF reading routines is to isolate the applications programmer from the need to know anything other than the most basic information about the file format. ABF 2.0 now uses a header of variable length.  This means that it is now essential to use the ABFFIO.DLL library to access the data._" 
 -[ABF User Guide](http://mdc.custhelp.com/euf/assets/software/FSP_ABFHelp_2.03.pdf) (page 9)

The purpose of the pyABF project is to document how to extract meaningful information directly from ABF files (including those encoded in the ABF2 file format) without relying on a DLL or any external libraries, and to provide a Pythonic API to provide simple and intuitive access to ABF header and data values. Efforts were taken to maximize portability of these findings so that similar ABF-reading APIs can be developed for other programming languages in the future.

### Development of this Guide

This document contains a blend of information I learned by inspecting the work of previous designers, supplemented with code examples and insights I discovered myself. A lot of my understanding initially came from reviewing what open-source ABF-reading projects were available, and I have tried to credit all of these developers by listing their projects at the bottom of this document. Characterization of previously-undocumented features (e.g., extracting digital output command waveforms from the ABF header) was primarily achieved by comparing ABFs in a hex editor, comparing files byte-by-byte, and modifying individual bits in ABF files to see how they changed when viewed in ClampFit.

Documentation and development is biased toward my personal use-cases for ABF files: Analysis of 1-2 channel ABF2 fixed-length episodic files (voltage clamp and current clamp) recorded using whole-cell patch-clamp technique in brain slices. Little effort has been invested into documenting features I don't personally use (such as variable-length sweeps and voice tags). If you benefit from the information provided in this document and figure out how to achieve additional functionality or implement your own improvements into this basic framework, please contact me so I can add your contributions to this growing collection of source code examples and documentation!

# Reading the ABF Header
For the following examples we will be inspecting the content of ABF files in the [/data/](/data/) folder.

## Reading Structured Data
Text files are usually UTF-8 encoded ASCII characters, where every 8-bit byte corresponds to a single character. On the other hand, binary files can contain variables which span multiple bytes, and they're not always directly mappable to ASCII characters. 

Since ABF files are binary, we need to open them with the `'rb'` mode. We can then read a certain number of bytes with `read(numBytes)`:

```python
f = open("14o08011_ic_pair.abf", 'rb')
byteString = f.read(16)
f.close()
```

Now let's display the 16 bytes we read:

```python
b'ABF2\x00\x00\x00\x02\x00\x02\x00\x00\x03\x00\x00\x00'
```

Notice the message starts with `b` - that means this is a _bytestring_ object, not a string! If a byte corresponds to an ASCII character ([on the chart](https://www.asciitable.com)), it is displayed by that character. If the character isn't ASCII, it's displayed in [hexadecimal](https://en.wikipedia.org/wiki/Hexadecimal) format. If you count the number of bytes visually, you'll identify 16: 4 characters (`'ABF2'`) and 12 hexadecimal codes (each starting with `\x`).

Let's display the same message as a list of integers. Calling `list()` on a bytestring does this conversion:

```python
byteList = list(byteString)
print(byteList)
```

We then observe a list of 16 integers, each representing one of the bytes in the bytestring:

```
[65, 66, 70, 50, 0, 0, 0, 2, 0, 2, 0, 0, 3, 0, 0, 0]
```

As we would predict from the [ASCII table](https://www.asciitable.com), `'A'`, `'B'`, `'F'`, and `'2'`, correspond to integers `65`, `66`, `70`, and `50`.

## Determine if a file is ABF1 or ABF2
Notice the first 4 characters are `'ABF2'`. This is how you know this is an ABF2 format ABF file. ABF1 files start with `'ABF '` where the 4th character is a space (ASCII 32). Therefore the fastest way to determine if a file is ABF1 or ABF2 is to determine if the 4th byte of the file is `50` or `32`.

## Reading multi-byte integers from bytestrings

I happen to know that the number of sweeps in an episodic ABF2 file is a four-byte unsigned integer formed from bytes 13, 14, 15, and 16. One way to read just these 4 bytes is to use the `seek()` method of the file object to go to byte 13, then just read-out 4 bytes. Note that to read byte 1 you'd `seek(0)`, so to read byte 13 you'd `seek(12)`.

```python
f.seek(12)
byteString = f.read(4)
byteList = list(byteString)
print(byteList)
```

The output is then 4 bytes:

```
[3, 0, 0, 0]
```

The [struct](https://docs.python.org/2/library/struct.html) package lets us convert bytestrings into python objects as long as we know what format they are in (e.g., this value is a 4-byte, 32-bit, unsigned integer). According to the [list of struct format characters](https://docs.python.org/2/library/struct.html#format-characters), this data type corresponds to the C `unsigned int` and has the format `I`. 

This program uses `struct.unpack()` to pull an `I`-formatted value from the 4 bytes starting at the 13th byte of the file.

```python
import struct

f = open("14o08011_ic_pair.abf", 'rb')
f.seek(12)
byteString = f.read(4)
f.close()

numSweeps = struct.unpack("I", byteString)
print(numSweeps)
```

The output is what you'd expect:
```
(3,)
```

Notice it's a [tuple](https://www.w3schools.com/python/python_tuples.asp). It doesn't really matter, just expect `struct.unpack()` to always return tuples. In my code I often convert them to lists right away because I frequently change the content of items in the returned data, and tuples are immutable.

## Writing a Function to read Structured Data

Since we will be reading lots of structured data, our lives get easier if we can write a function to simplify it. Notice that I use `struct.calcsize()` to determine how many bytes we must `read()`.

```python
def readStruct(f, structFormat, seekTo=-1):
  if seekTo>=0:
    f.seek(seekTo)
  byteCount = struct.calcsize(structFormat)
  byteString = f.read(byteCount)
  value = struct.unpack(structFormat, byteString)
  return list(value)
```

I can now call it multiple times easily. Also note that to retrieve multiple values of the same type, send a string format with a number before the character. A struct format of `'5I'` will return a tuple of 5 integers, `'4b'` will return a list of 4 bytes, and `'4s'` will a list of 4 characters.

```python
f = open("14o08011_ic_pair.abf", 'rb')
print(readStruct(f, "4s", 0))
print(readStruct(f, "I", 12))
f.close()
```

Now we can tell this is an ABF2 file with 3 sweeps:

```
[b'ABF2']
[3]
```

To convert a character-containing bytestring to a string object, use `.decode()`. I usually add extra arguments to ensure it decodes ASCII and doesn't crash if it encounters a non-character code.

```python
value1 = readStruct(f, "4s", 0)[0]
print(value1)
value2 = value1[0].decode("ascii", errors="ignore")
print(value2)
```

You can recognize the bytestring from the `b`, and the second line is a true string:

```
b'ABF2'
ABF2
```

## Byte Maps and Structs

How did I know that the 4 bytes starting at byte position 13 contained an unsigned integer indicating the number of sweeps in the ABF? It's because I have a _byte map_ for the ABF2 header, and the same data values are always at the same positions. There is another byte map for ABF1 files. You can find these byte maps (derived from _structs_ found in C headers and other source code) in the [structures.py](/src/pyabf/structures.py) file of the pyABF source code.

## ABF1 Header

Reading the ABF1 header is very simple. The same variables are always found at the same byte positions. This code can be used to read the entire ABF1 header. 

```python
fFileSignature = readStruct(f, "4s", 0)
fFileVersionNumber = readStruct(f, "f", 4)
nOperationMode = readStruct(f, "h", 8)
lActualAcqLength = readStruct(f, "i", 10)
nNumPointsIgnored = readStruct(f, "h", 14)
lActualEpisodes = readStruct(f, "i", 16)
lFileStartTime = readStruct(f, "i", 24)
lDataSectionPtr = readStruct(f, "i", 40)
lTagSectionPtr = readStruct(f, "i", 44)
lNumTagEntries = readStruct(f, "i", 48)
lSynchArrayPtr = readStruct(f, "i", 92)
lSynchArraySize = readStruct(f, "i", 96)
nDataFormat = readStruct(f, "h", 100)
nADCNumChannels = readStruct(f, "h", 120)
fADCSampleInterval = readStruct(f, "f", 122)
fSynchTimeUnit = readStruct(f, "f", 130)
lNumSamplesPerEpisode = readStruct(f, "i", 138)
lPreTriggerSamples = readStruct(f, "i", 142)
lEpisodesPerRun = readStruct(f, "i", 146)
fADCRange = readStruct(f, "f", 244)
lADCResolution = readStruct(f, "i", 252)
nFileStartMillisecs = readStruct(f, "h", 366)
nADCPtoLChannelMap = readStruct(f, "16h", 378)
nADCSamplingSeq = readStruct(f, "16h", 410)
sADCChannelName = readStruct(f, "10s"*16, 442)
sADCUnits = readStruct(f, "8s"*16, 602)
fADCProgrammableGain = readStruct(f, "16f", 730)
fInstrumentScaleFactor = readStruct(f, "16f", 922)
fInstrumentOffset = readStruct(f, "16f", 986)
fSignalGain = readStruct(f, "16f", 1050)
fSignalOffset = readStruct(f, "16f", 1114)
nDigitalEnable = readStruct(f, "h", 1436)
nActiveDACChannel = readStruct(f, "h", 1440)
nDigitalHolding = readStruct(f, "h", 1584)
nDigitalInterEpisode = readStruct(f, "h", 1586)
nDigitalValue = readStruct(f, "10h", 2588)
lDACFilePtr = readStruct(f, "2i", 2048)
lDACFileNumEpisodes = readStruct(f, "2i", 2056)
fDACCalibrationFactor = readStruct(f, "4f", 2074)
fDACCalibrationOffset = readStruct(f, "4f", 2090)
nWaveformEnable = readStruct(f, "2h", 2296)
nWaveformSource = readStruct(f, "2h", 2300)
nInterEpisodeLevel = readStruct(f, "2h", 2304)
nEpochType = readStruct(f, "20h", 2308)
fEpochInitLevel = readStruct(f, "20f", 2348)
fEpochLevelInc = readStruct(f, "20f", 2428)
lEpochInitDuration = readStruct(f, "20i", 2508)
lEpochDurationInc = readStruct(f, "20i", 2588)
nTelegraphEnable = readStruct(f, "16h", 4512)
fTelegraphAdditGain = readStruct(f, "16f", 4576)
sProtocolPath = readStruct(f, "384s", 4898)
```

A detailed description of which variables are useful is in the [ABF File Reading Sequence](#ABF%20File%20Reading%20Sequence) section. 

## ABF2 Header

Reading the ABF2 header is similarly simple, as those variables are always found at the same byte positions too. This code can read the ABF2 header, but it's important to note that ABF2 files have many more additional variables stored throughout the file. These data values are stored in _sections_, which we will review later. For now, you can use the code we've already written to read all these variables from the ABF2 header.

Notice that we only `seek()` once. This is because after reading a struct, the position of the file read buffer has been moved by the size of the struct. Unlike ABF1 headers which have irregularly-spaced data values, almost all ABF2 variable lists can be read consecutively without having to `seek()` from byte to byte.

```python
fb.seek(0)
fFileSignature = readStruct(f, "4s")
fFileVersionNumber = readStruct(f, "4b")
uFileInfoSize = readStruct(f, "I")
lActualEpisodes = readStruct(f, "I")
uFileStartDate = readStruct(f, "I")
uFileStartTimeMS = readStruct(f, "I")
uStopwatchTime = readStruct(f, "I")
nFileType = readStruct(f, "H")
nDataFormat = readStruct(f, "H")
nSimultaneousScan = readStruct(f, "H")
nCRCEnable = readStruct(f, "H")
uFileCRC = readStruct(f, "I")
FileGUID = readStruct(f, "I")
unknown1 = readStruct(f, "I")
unknown2 = readStruct(f, "I")
unknown3 = readStruct(f, "I")
uCreatorVersion = readStruct(f, "I")
uCreatorNameIndex = readStruct(f, "I")
uModifierVersion = readStruct(f, "I")
uModifierNameIndex = readStruct(f, "I")
uProtocolPathIndex = readStruct(f, "I")
```

A detailed description of which variables are useful is in the [ABF File Reading Sequence](#ABF%20File%20Reading%20Sequence) section. 

# Reading ABF Sections
You'll notice the ABF2 header itself contains many fewer values than the ABF1 header. That's because its header values are split into _sections_. There's a DACSection, ADCsection, ProtocolSection, etc.
Some sections (like ProtocolSection) are always "flat" and their corresponding struct of variables only gets read a single time. Other sections can be multidimensional, and their struct variables are read over and over to build an array of values (e.g., the structs for ADCsection get read once per ADC channel).

This is a list of _sections_ contained in ABF2 headers along with a brief description of what they're for:

* **ProtocolSection** - 
This section contains information about the recording settings.
This is useful for determining things like sample rate and
channel scaling factors.

* **ADCSection** - 
Information about the ADC (what gets recorded). 
There is 1 item per ADC.

* **DACSection** - 
Information about the DAC (what gets clamped). 
There is 1 item per DAC.

* **EpochPerDACSection** - 
This section contains waveform protocol information. These are most of
the values set when using the epoch the waveform editor. Note that digital
output signals are not stored here, but are in EpochSection.

* **EpochSection** - 
This section contains the digital output signals for each epoch. This
section has been overlooked by some previous open-source ABF-reading
projects. Note that the digital output is a single byte, but represents 
8 bits corresponding to 8 outputs (7->0). When working with these bits,
I convert it to a string like "10011101" for easy eyeballing.

* **TagSection** - 
Tags are comments placed in ABF files during the recording. Physically
they are located at the end of the file (after the data).
Later we will populate the times and sweeps (human-understandable units)
by multiplying the lTagTime by fSynchTimeUnit from the protocol section.

* **StringsSection** - 
Part of the ABF file contains long strings. Some of these can be broken
apart into indexed strings. 
The first string is the only one which seems to contain useful information.
This contains information like channel names, channel units, and abf 
protocol path and comments. The other strings are very large and I do not 
know what they do.
Strings which contain indexed substrings are separated by \\x00 characters.

* **DataSection** - 
This is the exciting part. It contains the electrophysiological data itself!

_**A note about other sections:** I only read data from the sections listed here.
Other sections are either not useful for my applications, are typically unused,
or have an undocumented struct format and cannot be deciphered._

## Obtaining the Section Map

Each section starts at a different byte position and its values can be read with its own list of structs. Unfortunately, the sections aren't at the same byte location in every ABF file. To discover where each section starts, how big it is, and how many replicates it has, we need to read from the Section Map. Thankfully, the section map is always at the same byte locations:

```python
# Sections I find useful
ProtocolSection = readStruct(f, "IIl", 76)
ADCSection = readStruct(f, "IIl", 92)
DACSection = readStruct(f, "IIl", 108)
EpochSection = readStruct(f, "IIl", 124)
ADCPerDACSection = readStruct(f, "IIl", 140)
EpochPerDACSection = readStruct(f, "IIl", 156)
StringsSection = readStruct(f, "IIl", 220)
DataSection = readStruct(f, "IIl", 236)
TagSection = readStruct(f, "IIl", 252)

# Sections I don't find useful
UserListSection = readStruct(f, "IIl", 172)
StatsRegionSection = readStruct(f, "IIl", 188)
MathSection = readStruct(f, "IIl", 204)
ScopeSection = readStruct(f, "IIl", 268)
DeltaSection = readStruct(f, "IIl", 284)
VoiceTagSection = readStruct(f, "IIl", 300)
SynchArraySection = readStruct(f, "IIl", 316)
AnnotationSection = readStruct(f, "IIl", 332)
StatsSection = readStruct(f, "IIl", 348)

```

Notice that we read a struct format `IIl` for each section, corresponding to `int`, `int`, `long`. This causes all returned values to be a list of 3 numbers which reveals information for each section: 
`[blockNumber, byteCount, itemCount]`.

* `blockNumber` is the byte location where the section starts (each block is 512 bytes)
* `byteCount` is the number of bytes each "read" of the section produces
* `itemCount` is how many times consecutively the section should be read

## Iteratively Reading Data from Sections
If you know how to read structured data at specific byte positions, you'll be able to figure out how
to build arrays of section data by reading the same struct over and over for a given section once you've built the Section Map. The ideal strategy for this will vary depending on programming language.

In Python I found it useful to create classes for each section, and make every variable
a list that gets appended with new values every time the struct is re-read.
These classes (and struct formats) can be found in pyABF's [structures.py](https://github.com/swharden/pyABF/blob/master/src/pyabf/structures.py) file, 
which gets read by the ABFcore class in [core.py](https://github.com/swharden/pyABF/blob/master/src/pyabf/core.py).

## Reading Data from DataSection
Interestingly, reading data is no different than reading any other series of numbers from a binary file. We could even use the `readStruct()` function we wrote earlier to pull data from the file!

To read sweep data from an ABF, learn about the data section:

```python
f = open("14o08011_ic_pair.abf", 'rb')
DataSection = readStruct(f, "IIl", 236)
print(DataSection)
f.close()
```

This will reveal the blockNumber, byteCount, and itemCount:

```
[9, 2, 3600000]
```

This result tells us the following:
  * ABF data starts at byte 4608 (9*512)
  * Each data point is 2 bytes (probably 16-bit integers)
  * There are 3,600,000 data points in this file

Reviewing the [struct format characters](https://docs.python.org/2/library/struct.html#format-characters) you'll notice that 2-byte integers correspond to the `short` C type and are struct format `h`. 

Lets read the first 10 data values from our ABF file using our `readStruct()` function:

```python
f = open("14o08011_ic_pair.abf", 'rb')
DataSection = readStruct(f, "IIl", 236)
data = readStruct(f, "10h", DataSection[0]*512)
f.close()
print(data)
```

The output is some seriously huge numbers. That's okay, because they're not properly scaled yet. We will tackle that issue later.

```
[-2147, -1839, -2147, -1838, -2147, -1838, -2147, -1837, -2147, -1838]
```

Something to consider is that the `readStruct()` function we wrote is simple and easy to use, but slow for massive amounts of data. [Numpy](http://www.numpy.org) is a Python package which is optimized for working with large amounts of multidimensional numerical data, and it has a function to read structured data directly from binary files into numpy arrays. We will use numpy for handling all ABF data from now on:

```python
import numpy as np
f = open("14o08011_ic_pair.abf", 'rb')
DataSection = readStruct(f, "IIl", 236)
f.seek(DataSection[0]*512)
data = np.fromfile(f, dtype=np.int16, count=DataSection[2])
f.close()
print(data)
```

The output is the same as before, it's just a numpy array, and it contains ALL data in the ABF file.

```
[-2147 -1839 -2147 ..., -1416 -1972 -1417]
```

If you have a single-channel ABF file, you're done! You can plot this data right away.

If you have a multi-channel ABF file, data from each channel is _interleaved_. This means for a 2-channel ABF, to plot one channel you'd need to plot every other data point.

How do you determine how many channels an ABF has? For ABF1 files it's the `nADCNumChannels` value in the header. For ABF2 files I take the third value (itemCount) from the `ADCsection` of the section map.

Let's assume the number of channels is in a `channelCount` variable. The easiest way to _deinterleave_ a numpy array is to reshape it.

After reshaping it, it forms 2 columns. I'd rather have two _rows_ so I can plot my two channels as data[0] and data[1], so it's necessary to use `np.rotate()`. Interestingly this places the channels in opposite order (the last channel is data[0]), so I reverse the order by slapping `[::-1]` at the end.

```python
f = open("14o08011_ic_pair.abf", 'rb')
DataSection = readStruct(f, "IIl", 236)
ADCSection = readStruct(f, "IIl", 92)
channelCount = ADCSection[2]
f.seek(DataSection[0]*512)
data = np.fromfile(f, dtype=np.int16, count=DataSection[2])
data = np.reshape(data, (int(len(data)/channelCount), channelCount))
data = np.rot90(data)[::-1]
f.close()
print(data)
```

The final result is an n-dimensional numpy array where every row is an ADC channel.

```
[[-2147 -2147 -2147 ..., -1971 -1971 -1972]
 [-1839 -1838 -1838 ..., -1417 -1416 -1417]]
```

Take a moment to appreciate we have a header-parsing multi-channel data reading ABF2 file reader in ten lines! Nice.

```python
import matplotlib.pyplot as plt
plt.figure(figsize=(12,3))
for channel in range(channelCount):
    plt.plot(data[channel], label=f"channel {channel}", alpha=.7)
plt.margins(0,0)
plt.tight_layout()
plt.axis([250_000, 425_000, -2300, 1700])
plt.legend()
plt.show()
```

A few lines of [matplotlib](https://matplotlib.org) is all it takes to graph this ABF data by channel:

![](code/01.png)

Horizontal units can be converted to seconds by dividing by the sample rate. How to determine the sample rate is discussed later in this document.

Vertical units can be converted to true units by multiplying the data by a _scaling factor_ which has to be calculated from a variety of header values. Since the data originated as int16, the output of the ADC will span 2^16 units centered at 0 (-32,768 to 32,768), and hence this data is much larger vertically than expected. How to determine the scaling factor is discussed later in this document.


# ABF File Reading Sequence

When pyABF loads an ABF file, the [ABFcore class](/src/pyabf/core.py) reads the contents of the entire ABF header, all sections, and all data, then does all the operations necessary to determine the number of channels, sweeps, sample rate, scaling factor, etc. It is written in such a way that it is agnostic as to whether it loads an ABF1 or ABF2 file. Any software written to analyze ABF files will benefit from reading ABF files in this same sequence. 

In this section I will walk through every step pyABF uses to load ABF files, and mention some of the tricks and surprises I learned along the way. To benefit from advice in these sections it is assumed you have a full understanding of how to read ABF header and data values using the structures outlined in [structures.py](/src/pyabf/structures.py).

To see specific examples code for any of the following sections, simply navigate to that function in the [ABFcore class](/src/pyabf/core.py).

```python
# This is what pyABF does to fully load an ABF file
self._fileOpen()
self._determineAbfFormat()
self._readHeaders()
self._formatVersion()
self._determineCreationDateTime()
self._determineDataProperties()
self._determineDataUnits()
self._determineDataScaling()
self._determineHoldingValues()
self._determineProtocolPath()
self._determineProtocolComment()
self._makeTagTimesHumanReadable()
self._makeUsefulObjects()
self._digitalWaveformEpochs()
self._loadAndScaleData()
self._fileClose()
```


## fileOpen()
_TODO_

## determineAbfFormat()
_TODO_

## readHeaders()
_TODO_

## formatVersion()
_TODO_

## determineCreationDateTime()
_TODO_

## determineDataProperties()
_TODO_

## determineDataUnits()
_TODO_

## determineDataScaling()
_TODO_

## determineHoldingValues()
_TODO_

## determineProtocolPath()
_TODO_

## determineProtocolComment()
_TODO_

## makeTagTimesHumanReadable()
_TODO_

## makeUsefulObjects()
_TODO_

## digitalWaveformEpochs()
_TODO_

## loadAndScaleData()
_TODO_

## fileClose()
_TODO_



# References

### Official ABF Documents and Software
* Official [Axon Binary Format (ABF) User Guide](http://mdc.custhelp.com/euf/assets/software/FSP_ABFHelp_2.03.pdf) (3rd party cache)
* [pCLAMP 10 download page](http://mdc.custhelp.com/app/answers/detail/a_id/18779/~/axon™-pclamp™-10-electrophysiology-data-acquisition-%26-analysis-software) for pCLAMP, ClampFit, and AxoScope
* [Historical pCLAMP User Guides](http://mdc.custhelp.com/app/answers/detail/a_id/18747/session/L2F2LzEvdGltZS8xNTI5Nzc5MDQ2L3NpZC9TdEZxa1hQbg%3D%3D)
* [pCLAMP ABF File Support Pack](http://mdc.custhelp.com/app/answers/detail/a_id/18881/~/axon™-pclamp®-abf-file-support-pack-download-page) (contains abffio.dll)   

### Other ABF-reading Projects
* [BioSig](https://github.com/dongzhenye/biosignal-tools/tree/master/biosig4c%2B%2B/t210) uses modified Axon Library Files
  * [abfheader.h](https://github.com/dongzhenye/biosignal-tools/blob/master/biosig4c%2B%2B/t210/abfheadr.h) - 
_Defines the ABFFileHeader structure and provides prototypes for functions implemented in ABFHEADR.CPP for reading and writing ABFFileHeaders_
  * [axon_structs.h](https://github.com/dongzhenye/biosignal-tools/blob/master/biosig4c%2B%2B/t210/axon_structs.h) - _brief header containing all structures of ABF_
  * [sopen_abf_read.c](https://github.com/dongzhenye/biosignal-tools/blob/master/biosig4c%2B%2B/t210/sopen_abf_read.c) - _reads data from ABF files_
* MatLab - [abf2load.m](https://www.mathworks.com/matlabcentral/fileexchange/45667-apanalysis?focused=6744051&tab=function) - reads ABF files in MatLab
* StimFit - [abflib.cpp](https://github.com/neurodroid/stimfit/blob/master/src/libstfio/abf/abflib.cpp) - C++ implementation of an ABF reader
* Neo-IO - [axonrawio.py](https://github.com/NeuralEnsemble/python-neo/blob/master/neo/rawio/axonrawio.py)
* QUB Express - [Python 2 code](https://qub.mandelics.com/src/qub-express/qubx/data_abf.py) interacts with abffio.dll 

### Electrophysiology Equipment and Theory
* [Axoclamp-2B theory and operation](https://neurophysics.ucsd.edu/Manuals/Axon%20Instruments/Axoclamp-2B_Manual.pdf)
* [pCLAMP 10 User Guide](https://neurophysics.ucsd.edu/Manuals/Axon%20Instruments/pCLAMP10-User-Guide-RevA.pdf)

### Programming Concepts
* [Python struct format characters](https://docs.python.org/2/library/struct.html#format-characters)
* [Numpy.fromfile()](https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.fromfile.html)
* [Numpy's built-in dataypes](https://docs.scipy.org/doc/numpy-1.13.0/reference/arrays.scalars.html#arrays-scalars-built-in)

---



