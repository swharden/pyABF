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

## Reading Structured Data

## ABF1 Header

## ABF2 Header

# Reading ABF Sections

## Obtaining the Section Map
Reading three numbers (int, int, long) at specific byte locations
yields the block position, byte size, and item count of specific
data stored in sections. Note that a block is 512 bytes. 

Some of these sections are not read by this class because they are either
not useful for my applications, typically unused, or have an
unknown memory structure.

## Section Descriptions

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
yahs

## How to Read Sections
about sequential file access

# Putting it All Together
Document this, step by step
```python
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



