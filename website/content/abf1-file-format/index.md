---
title: The ABF1 File Format
description: Unofficial Guide to the ABF1 File Format
---

# The ABF1 File Format

ABF1 files (unlike ABF2 files) use a fixed-length header and values are always
at the same byte positions in the file. This document was created to simplify
the task of finding ABF1 byte offsets. It was created from data found in the
CHM file distributed as part of the ABF1 SDK and from
[abfheadr.h](https://github.com/dongzhenye/biosignal-tools/blob/0d0a4e7ca21774138fb1d0c2384a1f610260334d/biosig4c%2B%2B/t210/abfheadr.h).
While the byte offsets are not useful for ABF2 files, the definitions are.

> 👉 Review the [Unofficial Guide to the ABF File Format](../abf2-file-format/) for a more extensive description of the ABF1 and ABF2 file format, with code examples for how to read structured data from binary files using Python.

## Table of Contents

![](TOC)

### File ID and Size Information (Group 1, 40 bytes)

Offset | Header Entry Name    | Type  | Description                                                                                                                                                                                               |
------ | -------------------- | ----  | -----------
0      | lFileSignature       | long  | File type used for format identification. Possible values are: "ABF ", "CLPX" and "FTCX". Used to create the numbers in nFileType. (In old pCLAMP and Axotape data files, the first four bytes were a float: 1 = CLAMPEX, 10 = FETCHEX/AxoTape. This is translated on reading into either CLPX or FTCX as appropriate.)
4      | fFileVersionNumber   | float | File format version stored in the data file during acquisition. The present version is 1.65. (In old pCLAMP and Axotape data files, this parameter is in the range 2.0–5.3.)                              |
8      | nOperationMode       | short | Operation mode: 1 = Event-driven, variable length; 2 = Oscilloscope, loss free (Same as Event-driven, fixed length); 3 = Gap-free; 4 = Oscilloscope, high-speed; 5 = episodic stimulation (Clampex only). |
10     | lActualAcqLength     | long  | Actual number of ADC samples (aggregate) in data file. See lAcqLength. Averaged sweeps are included.                                                                                                      |
14     | nNumPointsIgnored    | short | Number of points ignored at data start. Normally zero, but non-zero for gap-free acquisition using AXOLAB configurations with one or more ADS boards.                                                     |
16     | lActualEpisodes      | long  | Actual number of sweeps in the file including averaged sweeps. See lEpisodesPerRun. If nOperationMode = 3 (gap-free) the value of this parameter is 1.                                                    |
20     | lFileStartDate       | long  | Date when data portion of this file was first written to. Stored as YYMMDD. If YY is in the range 80–99, prefix with "19" to get the year. If YY is in the range 00–79, prefix with "20" to get the year. |
24     | lFileStartTime       | long  | Time of day in seconds past midnight when data portion of this file was first written to.                                                                                                                 |
28     | lStopwatchTime       | long  | Time since the stopwatch was zeroed that the data portion of this file was first written to. Not supported by all programs. Default = 0.                                                                  |
32     | fHeaderVersionNumber | float | Version number of the header structure returned by the ABF_ReadOpen function. Currently 1.65. This parameter does not identify the data file format. See fFileVersionNumber above.                        |
36     | nFileType            | short | Numeric equivalent of file type. 1 = ABF file; 2 = Old FETCHEX file (FTCX); 3 = Old Clampex file (CLPX). See sFileType.                                                                                   |
38     | nMSBinFormat         | short | Storage method for real numbers in the header. Also see nDataFormat. 0 = IEEE format; 1 = Microsoft Binary format (old files only).                                                                       |

### File Structure (Group 2, 78 bytes)

Offset | Header Entry Name     | Type  | Description                                                                                                                     |
------ | --------------------  | ----  | -----------
40     | lDataSectionPtr       | long  | Block number of start of Data section.                                                                                          |
44     | lTagSectionPtr        | long  | Block number of start of Tag section.                                                                                           |
48     | lNumTagEntries        | long  | Number of Tag entries.                                                                                                          |
52     | lScopeConfigPtr       | long  | Block number of the ABF Scope Config section (was block number of start of Long Description section).                           |
56     | lNumScopes            | long  | Number of ABFScopeConfig structures in the ABF Scope Config section (was number of lines of Long Description).                  |
60     | _lDACFilePtr         | long  | Do not use: see Extended File Structure. Block number of start of DAC file section.                                             |
64     | _lDACFileNumEpisodes | long  | Do not use: see Extended File Structure. Number of sweeps in the DAC file section. Sweeps are not multiplexed.                  |
68     | sUnused68             | 4char | Unused.                                                                                                                         |
72     | lDeltaArrayPtr        | long  | Block number of start of Delta Array section.                                                                                   |
76     | lNumDeltas            | long  | Number of entries in Delta Array section.                                                                                       |
80     | lVoiceTagPtr          | long  | Block number of start of Voice Tag section.                                                                                     |
84     | lVoiceTagEntries      | long  | Number of Voice Tag entries.                                                                                                    |
88     | lUnused88             | long  | (Was number of automatic entries in Notebook section).                                                                          |
92     | lSynchArrayPtr        | long  | Block number of start of the Synch Array section.                                                                               |
96     | lSynchArraySize       | long  | Number of pairs of entries in the Synch Array section. If averaging is enabled, this includes the entry for the averaged sweep. |
100    | nDataFormat           | short | Data representation. 0 = 2-byte integer; 1 = IEEE 4 byte float.                                                                 |
102    | nSimultaneousScan     | short | ADC Channel Scanning Mode: 0=Multiplexed; 1=Simultaneous Scanning (currently unimplemented).                                    |
104    | lStatisticsConfigPtr  | long  | Block number of start of Scope Config section.                                                                                  |
108    | lAnnotationSectionPtr | long  | Block number of start of annotations section                                                                                    |
112    | lNumAnnotations       | long  | Number of annotations                                                                                                           |
116    | sUnused004            | 2char | Unused.                                                                                                                         |

### Trial hierarchy information (Group 3, 82 bytes)
```c
short    channel_count_acquired; // number of input channels acquired
short    nADCNumChannels; // number of input channels recorded

/**
*  The two sample intervals must be an integer multiple (or submultiple) of each other.
*  The documentation says these two sample intervals are the interval between multiplexed samples, but not all digitisers work like that.
*  Instead, these are the per-channel sample rate divided by the number of channels.
*  If the user chose 100uS and has two channels, this value will be 50uS.
*/
float    fADCSampleInterval;
float    fADCSecondSampleInterval;
float    fSynchTimeUnit;
float    fSecondsPerRun;

/**
* The total number of samples per episode, for the recorded channels only.
* This does not include channels which are acquired but not recorded.
* This is the number of samples per episode per channel, times the number of recorded channels.
* If you want the samples per episode for one channel, you must divide this by get_channel_count_recorded().
*/

ABFLONG     lNumSamplesPerEpisode;
ABFLONG     lPreTriggerSamples;
ABFLONG     lEpisodesPerRun;
ABFLONG     lRunsPerTrial;
ABFLONG     lNumberOfTrials;
short    nAveragingMode;
short    nUndoRunCount;
short    nFirstEpisodeInRun;
float    fTriggerThreshold;
short    nTriggerSource;
short    nTriggerAction;
short    nTriggerPolarity;
float    fScopeOutputInterval;
float    fEpisodeStartToStart;
float    fRunStartToStart;
float    fTrialStartToStart;
ABFLONG     lAverageCount;
ABFLONG     lClockChange;
short    nAutoTriggerStrategy;
```

### Display Parameters (Group 4, 44 bytes)

Offset | Header Entry Name       | Type  | Description                                                                                                                                                                        |
------ | --------------------    | ----  | -----------
200    | nDrawingStrategy        | short | Strategy for the drawing of raw data: 0 = not at all; 1 = update immediately as data is acquired; 2 = update at the end of each sweep or trace; 3 = update at the end of each run; |
202    | nTiledDisplay           | short | ADC channel display arrangement: 0 = Superimposed; 1 = Tiled.                                                                                                                      |
204    | nEraseStrategy          | short | Automatically erase screen: 0 = not at all; 1 = before each sweep; 2 = before each run.                                                                                            |
206    | nDataDisplayMode        | short | Data display mode: 0 = Points; 1 = Lines.                                                                                                                                          |
208    | lDisplayAverageUpdate   | long  | Display averaged data: -1 = at end of trial; 0 = after each pseudo-doubling; N = after N runs.                                                                                     |
212    | nChannelStatsStrategy   | short | Show channel statistics in gap-free mode: 0 = No; 1 = Yes.                                                                                                                         |
214    | lCalculationPeriod      | long  | (Superseded by fStatisticsPeriod) Length of the real-time statistics update period in samples. Conventionally a multiple of 1024. Default = 16384.                                 |
218    | lSamplesPerTrace        | long  | Number of multiplexed ADC samples in displayed trace.                                                                                                                              |
222    | lStartDisplayNum        | long  | Starting sample number for sweep display: N = starting sample number. (Use N = 1 to start from the first sample.)                                                                  |
226    | lFinishDisplayNum       | long  | Finishing sample number for sweep display: 0 = finish at end of sweep; N = finishing sample number.                                                                                |
230    | nMultiColor             | short | Color control for multi-trace displays. 0 = single color for all traces; 1 = two or more colors for traces.                                                                        |
232    | nShowPNRawData          | short | 0 = display corrected data; 1 = display raw data.                                                                                                                                  |
234    | fStatisticsPeriod       | float | Length of the real-time statistics update period in seconds.                                                                                                                       |
238    | lStatisticsMeasurements | long  | Bit mask for statistics measurements to display: Above Threshold: 1, Event Frequency: 2, Mean Open Time: 4, Mean Closed Time: 8
242    | nStatisticsSaveStrategy | short | Strategy used to save statistics: No Auto Save = 0; Auto Save = 1.                                                                                                                 |

### Hardware Information (Group 5, 16 bytes)

Offset | Header Entry Name    | Type  | Description                                                                                                          |
------ | -------------------- | ----  | -----------
244    | fADCRange            | float | ADC positive full-scale input in volts (e.g. 10.00V).                                                                |
248    | fDACRange            | float | DAC positive full-scale range in volts.                                                                              |
252    | lADCResolution       | long  | Number of ADC counts corresponding to the positive full-scale voltage in ADCRange (e.g. 2000, 2048, 32000 or 32768). |
256    | lDACResolution       | long  | Number of DAC counts corresponding to the positive full-scale voltage in DACRange.                                   |

### Environmental Information (Group 6, 118 bytes)

Offset | Header Entry Name        | Type   | Description                                                                                                                                                                                                                    |
------ | --------------------     | ----   | -----------
260    | nExperimentType          | short  | Experiment type: 0 = Voltage Clamp; 1 = Current Clamp.                                                                                                                                                                         |
262    | _nAutosampleEnable      | short  | Do not use: see Extended Environmental Information. Enable storage of autosample information: 0 = Disabled; 1 = Automatic; 2 = Manual.                                                                                         |
264    | _nAutosampleADCNum      | short  | Do not use: see Extended Environmental Information. Physical ADC channel number to which autosampled parameters apply.                                                                                                         |
266    | _nAutosampleInstrument  | short  | Do not use: see Extended Environmental Information. Note: for most programs this is an information-only field. For example, in Clampex the autosample instrument is chosen as a configuration item and copied into this field. |
268    | _fAutosampleAdditGain   | float  | Do not use: see Extended Environmental Information. Additional gain multiplier of Instrument connected to nAutosampleADCNum. (Optionally autosampled by some acquisition programs.) (Default = 1.)                             |
272    | _fAutosampleFilter      | float  | Do not use: see Extended Environmental Information. Lowpass filter cutoff frequency of Instrument connected to nAutosampleADCNum. (Optionally autosampled by some acquisition programs.) (Default = 100000.)                   |
276    | _fAutosampleMembraneCap | float  | Do not use: see Extended Environmental Information. Patch-clamp membrane capacitance compensation. (Optionally autosampled by some acquisition programs.)                                                                      |
280    | nManualInfoStrategy      | short  | Strategy for writing the manually entered information: 0 = Do not write; 1 = Write each trial; 2 = Prompt each trial.                                                                                                          |
282    | fCellID1                 | float  | Numeric identifier #1, e.g. cell identifier.                                                                                                                                                                                   |
286    | fCellID2                 | float  | Numeric identifier #2, e.g. temperature in °C.                                                                                                                                                                                 |
290    | fCellID3                 | float  | Numeric identifier #3.                                                                                                                                                                                                         |
294    | sCreatorInfo             | 16char | Name and version of program used to create the file. For example, "AxoTape 2.0" or "Clampex 6.0".                                                                                                                              |
310    | _sFileComment           | 56char | Do not use: see Extended Environmental Information. 56 byte ASCII comment string.                                                                                                                                              |
366    | nFileStartMillisecs      | short  | Milliseconds portion of lFileStartTime                                                                                                                                                                                         |
368    | nCommentsEnable          | short  | Enable comments field                                                                                                                                                                                                          |
370    | sUnused003a              | 8char  | Unused.                                                                                                                                                                                                                        |

### Multi-channel Information (Group 7, 1044 bytes)

Offset | Header Entry Name              | Type   | Description                                                                                                                                                                                                                                                                                                                                                   |
------ | --------------------           | ----   | -----------
378    | nADCPtoLChannelMap(0-15)       | short  | ADC physical-to-logical channel map. The entries are in the physical order 0, 1, 2,..., 14, 15. If there are fewer than 16 logical channels in the system, the array is padded with -1. All channels supported by the hardware are present, even if only a subset is used. For example, for the TL-2 the entries would be 7, 6, 5, 4, 3, 2, 1, 0, -1,..., -1. |
410    | nADCSamplingSeq(0-15)          | short  | ADC channel sampling sequence. This is the order in which the physical ADC channels are sampled. If fewer than the maximum number of channels are sampled, pad with -1. For example, if two channels are sampled on the TL-2, this array will contain 6, 7, -1,..., -1. If two channels are sampled on the TL-1, this array will contain 14, 15, -1,..., -1.  |
442    | sADCChannelName(0-15)          | 10char | ADC channel name in physical channel number order. Default = spaces.                                                                                                                                                                                                                                                                                          |
602    | sADCUnits(0-15)                | 8char  | The user units for ADC channels in physical channel number order. Default = spaces.                                                                                                                                                                                                                                                                           |
730    | fADCProgrammableGain(0-15)     | float  | ADC programmable gain in physical channel number order (dimensionless). Default = 1.                                                                                                                                                                                                                                                                          |
794    | fADCDisplayAmplification(0-15) | float  | ADC channel display amplification in physical channel number order (dimensionless). Default = 1.                                                                                                                                                                                                                                                              |
858    | fADCDisplayOffset(0-15)        | float  | ADC channel display offset in physical channel number order (user units). Default = 0.                                                                                                                                                                                                                                                                        |
922    | fInstrumentScaleFactor(0-15)   | float  | Instrument scale factor in physical ADC channel number order (Volts at ADC / user unit). (Programs would normally display this information to the user as user units / volt at ADC).                                                                                                                                                                          |
986    | fInstrumentOffset(0-15)        | float  | Instrument offset in physical ADC channel number order (user units corresponding to 0 V at the ADC). Default is zero.                                                                                                                                                                                                                                         |
1050   | fSignalGain(0-15)              | float  | Signal conditioner gain in physical ADC channel number order (dimensionless). Default = 1.                                                                                                                                                                                                                                                                    |
1114   | fSignalOffset(0-15)            | float  | Signal conditioner offset in physical ADC channel number order (user units). Default = 0.                                                                                                                                                                                                                                                                     |
1178   | fSignalLowpassFilter(0-15)     | float  | Signal-conditioner lowpass filter corner frequency in physical ADC channel number order (Hz). 100000 means lowpass filter is bypassed (i.e. wideband). Default = 100000.                                                                                                                                                                                      |
1242   | fSignalHighpassFilter(0-15)    | float  | Signal-conditioner highpass filter corner frequency in physical ADC channel number order (Hz). 0 means highpass filter is bypassed (i.e. DC coupled). -1 means inputs are grounded. Default = 0.                                                                                                                                                              |
1306   | sDACChannelName(0-3)           | 10char | DAC channel name. Default = spaces.                                                                                                                                                                                                                                                                                                                           |
1346   | sDACChannelUnits(0-3)          | 8char  | The user units for this DAC channel. Default = spaces.                                                                                                                                                                                                                                                                                                        |
1378   | fDACScaleFactor(0-3)           | float  | DAC channel gain (user units / V at DAC). Default = 1.                                                                                                                                                                                                                                                                                                        |
1394   | fDACHoldingLevel(0-3)          | float  | DAC channel holding level (user units). Default = 0.                                                                                                                                                                                                                                                                                                          |
1410   | nSignalType                    | short  | Type of signal conditioner that was used. 0 = None; 1 = CyberAmp 320/380.                                                                                                                                                                                                                                                                                     |
1412   | sUnused004                     | 10char | Unused.                                                                                                                                                                                                                                                                                                                                                       |

### Synchronous Timer Outputs (Group 8, 14 bytes)

_Synchronous timer outputs were dropped from pCLAMP version 6. These parameters
have been kept in the ABF 1.0 specification for compatibility when reading old
data files. New programs should write zeros to all of the parameters in this
group._

Offset | Header Entry Name    | Type  | Description                                                               |
------ | -------------------- | ----  | -----------
1422   | nOUTEnable           | short | Enable synchronous timer outputs: 0 = No; 1 = Yes.                        |
1424   | nSampleNumberOUT1    | short | Sample number for pulse on synchronous timer OUT #1.                      |
1426   | nSampleNumberOUT2    | short | Sample number for pulse on synchronous timer OUT #2.                      |
1428   | nFirstEpisodeOUT     | short | First sweep at which synchronous timer OUT #1 and #2 fire.                |
1430   | nLastEpisodeOUT      | short | Last sweep at which synchronous timer OUT #1 and #2 fire.                 |
1432   | nPulseSamplesOUT1    | short | Duration and polarity of pulse on synchronous timer OUT #1 (DAC samples). |
1434   | nPulseSamplesOUT2    | short | Duration and polarity of pulse on synchronous timer OUT #2 (DAC samples). |

### Epoch Waveform and Pulses (Group 9, 184 bytes)

Offset | Header Entry Name                      | Type  | Description                                                                                                                                                                   |
------ | --------------------                   | ----  | -----------
1436   | nDigitalEnable                         | short | Enable digital outputs: 0 = No; 1 = Yes.                                                                                                                                      |
1438   | _nWaveformSource                      | short | Do not use: see Extended Epoch Waveform and Pulses. Analog waveform source: 0 = Disable; 1 = Generate waveform from epoch definition; 2 = Generate waveform from a DAC file.  |
1440   | nActiveDACChannel                      | short | Active DAC channel, i.e. the one used for waveform generation.                                                                                                                |
1442   | _nInterEpisodeLevel                   | short | Do not use: see Extended Epoch Waveform and Pulses. Inter-sweep holding level: 0 = Use holding level; 1 = Use last epoch amplitude.                                           |
1444   | _nEpochType(0-9)                      | short | Do not use: see Extended Epoch Waveform and Pulses. Epoch type: 0 = Disabled; 1 = Step; 2 = Ramp.                                                                             |
1464   | _fEpochInitLevel(0-9)                 | float | Do not use: see Extended Epoch Waveform and Pulses. Epoch initial level (user units).                                                                                         |
1504   | _fEpochLevelInc(0-9)                  | float | Do not use: see Extended Epoch Waveform and Pulses. Epoch level increment (user units).                                                                                       |
1544   | _nEpochInitDuration(0-9)              | short | Do not use: see Extended Epoch Waveform and Pulses. Epoch initial duration (in sequence counts).                                                                              |
1564   | _nEpochDurationInc(0-9)               | short | Do not use: see Extended Epoch Waveform and Pulses. Epoch duration increment (in sequence counts).                                                                            |
1584   | nDigitalHolding                        | short | Holding value for digital output.                                                                                                                                             |
1586   | nDigitalInterEpisode                   | short | Inter-sweep digital holding value: 0 = Use holding value; 1 = Use last epoch value.                                                                                           |
1588   | nDigitalValue(0-9)                     | short | Epoch value for digital output (0...15).                                                                                                                                      |
1608   | sUnavailable1608 (was fWaveformOffset) | 4char | Do not use. This parameter was used by CLAMPFIT 6.0. Offset (in active DAC user units) in instrument command pathway, usually due to a non-zero holding potential or current. |
1612   | nDigitalDACChannel                     | short | Not used.                                                                                                                                                                     |
1614   | sUnused005                             | 6char | Unused.                                                                                                                                                                       |

### DAC Output File (Group 10, 98 bytes)
```c
float    _fDACFileScale;
float    _fDACFileOffset;
char     sUnused006[2];
short    _nDACFileEpisodeNum;
short    _nDACFileADCNum;
char     _sDACFilePath[ABF_DACFILEPATHLEN]; // ABF_DACFILEPATHLEN == 84 (old was 60)
```

### Presweep (conditioning) pulse train (Group 11, 44 bytes)
```c
short    _nConditEnable;
short    _nConditChannel;
ABFLONG     _lConditNumPulses;
float    _fBaselineDuration;
float    _fBaselineLevel;
float    _fStepDuration;
float    _fStepLevel;
float    _fPostTrainPeriod;
float    _fPostTrainLevel;
char     sUnused007[12];
```

### Variable parameter user list (Group 12, 82 bytes)
```c
short    _nParamToVary;
char     _sParamValueList[ABF_VARPARAMLISTLEN]; // ABF_VARPARAMLISTLEN == 80
```

### Autopeak measurement (Group 13, 36 bytes)
```c
short    _nAutopeakEnable;
short    _nAutopeakPolarity;
short    _nAutopeakADCNum;
short    _nAutopeakSearchMode;
ABFLONG     _lAutopeakStart;
ABFLONG     _lAutopeakEnd;
short    _nAutopeakSmoothing;
short    _nAutopeakBaseline;
short    _nAutopeakAverage;
char     sUnavailable1866[2];     // Was nAutopeakSaveStrategy, use nStatisticsSaveStrategy
ABFLONG     _lAutopeakBaselineStart;
ABFLONG     _lAutopeakBaselineEnd;
ABFLONG     _lAutopeakMeasurements;
```

### Channel Arithmetic (Group 14, 52 bytes)
```c
short    nArithmeticEnable;
float    fArithmeticUpperLimit;
float    fArithmeticLowerLimit;
short    nArithmeticADCNumA;
short    nArithmeticADCNumB;
float    fArithmeticK1;
float    fArithmeticK2;
float    fArithmeticK3;
float    fArithmeticK4;
char     sArithmeticOperator[ABF_ARITHMETICOPLEN]; // ABF_ARITHMETICOPLEN == 2
char     sArithmeticUnits[ABF_ARITHMETICUNITSLEN]; // ABF_ARITHMETICUNITSLEN == 8
float    fArithmeticK5;
float    fArithmeticK6;
short    nArithmeticExpression;
char     sUnused008[2];
```

### On-line subtraction (Group 15, 34 bytes)
```c
short    _nPNEnable;
short    nPNPosition;
short    _nPNPolarity;
short    nPNNumPulses;
short    _nPNADCNum;
float    _fPNHoldingLevel;
float    fPNSettlingTime;
float    fPNInterpulse;
char     sUnused009[12];
```

### Miscellaneous Parameters (Group 16, 82 bytes)

Offset | Header Entry Name          | Type   | Description                                                                                                                                                                                                                                                                |
------ | --------------------       | ----   | -----------
1966   | _nListEnable              | short  | Do not use: see Extended Variable Parameter User List. Parameter list activation status: 0 = Disable; 1 = Enable.                                                                                                                                                          |
1968   | nBellEnable(0-1)           | short  | Auditory tone activation status: 0 = Disable; 1 = Enable.                                                                                                                                                                                                                  |
1972   | nBellLocation(0-1)         | short  | Location of bell relative to trial: 0 = Before; 1 = After.                                                                                                                                                                                                                 |
1976   | nBellRepetitions(0-1)      | short  | Number of sounds to produce.                                                                                                                                                                                                                                               |
1980   | nLevelHysteresis           | short  | Amount of level hysteresis to use when detecting events. This is the amount that the data has to go past the trigger level before it is considered triggered. Re-arming of the trigger level is always done at the actual nominated trigger level (see fTriggerThreshold). |
1982   | lTimeHysteresis            | long   | Amount of time hysteresis to use when detecting events. This is the number of samples that have to be below the trigger point before the trigger is said to be rearmed.                                                                                                    |
1986   | nAllowExternalTags         | short  | 0 = Do not scan for external tags during acquisition. 1 = Scan for external tags.                                                                                                                                                                                          |
1988   | nLowpassFilterType(0-15)   | char   | Type of Low Pass filter for each ADC channel: 0 = None; 1 = External; 2 = Simple RC; 3 = Bessell; 4 = Butterworth.                                                                                                                                                         |
2004   | nHighpassFilterType(0-15)  | char   | Type of High Pass filter for each ADC channel: 0 = None; 1 = External; 2 = Simple RC; 3 = Bessell; 4 = Butterworth.                                                                                                                                                        |
2020   | nAverageAlgorithm          | short  | Algorithm used for calculating averages: 0 = Cumulative Averaging; 1 = Most Recent Averaging (uses fAverageWeighting below).                                                                                                                                               |
2022   | fAverageWeighting          | float  | Weighting Factor for Most Recent Averaging. This is the proportion of the incoming sweep to include in the average.                                                                                                                                                        |
2026   | nUndoPromptStrategy        | short  | Strategy for Prompting to create an Undo file: 0 = On Abort; 1 = Always.                                                                                                                                                                                                   |
2028   | nTrialTriggerSource        | short  | Trigger source for start trial: -3 = Spacebar; -2 = External Trigger; -1 = None.                                                                                                                                                                                           |
2030   | nStatisticsDisplayStrategy | short  | Strategy for displaying statistics: 0 = Display Statistics; 1 = Do Not display Statistics                                                                                                                                                                                  |
2032   | nExternalTagType           | short  | Type of External Tag: 0 = Time Tag; 1 = External Tag; 2 = External Tag (from BNC input) 3 = Voice Tag (from audio input); 4 = New File Tag                                                                                                                                 |
2034   | lHeaderSize                | long   | Total size of the header. Currently 6144 bytes.                                                                                                                                                                                                                            |
2038   | dFileDuration              | double | Not used.                                                                                                                                                                                                                                                                  |
2046   | nStatisticsDisplayStrategy | short  | Strategy for displaying statistics: 0 = Display Statistics; 1 = Do Not display Statistics.                                                                                                                                                                                 |

### Extended File Structure (Extended Group 2, 16 bytes)

Offset | Header Entry Name        | Type  | Description                                                          |
------ | --------------------     | ----  | -----------
2048   | lDACFilePtr(0-1)         | 2long | Block number of start of DAC file section.                           |
2056   | lDACFileNumEpisodes(0-1) | 2long | Number of sweeps in the DAC file section. Sweeps are not multiplexed |

```
   // EXTENDED GROUP #3 - Trial Hierarchy (10 bytes)
   // 2064
   float    fFirstRunDelay;
   char     sUnused010[6];
   // 2074 = 40 + 78 + 82 + 44 + 16 + 118 + 1044 + 14 + 184 + 98 + 44 + 84 + 36 + 52 + 34 + 82 + 16 + 10
```

### Extended Multi-channel Information (Extended Group 7, 62 bytes)

Offset | Header Entry Name           | Type   | Description                      |
------ | --------------------        | ----   | -----------
2074   | fDACCalibrationFactor (0-3) | 4float | Calibration factor for each DAC. |
2090   | fDACCalibrationOffset (0-3) | 4float | Calibration offset for each DAC. |
2106   | sUnused011                  | 30char | Unused.                          |

### Train Parameters (Group 17, 160 bytes)

Offset | Header Entry Name           | Type   | Description                                                                 |
------ | --------------------        | ----   | -----------
2136   | lEpochPulsePeriod(0-1)(0-9) | 80long | Train period in physical DAC channel order then epoch order (samples).      |
2216   | lEpochPulseWidth(0-1)(0-9)  | 80long | Train pulse width in physical DAC channel order then epoch order (samples). |

### Extended Epoch Waveform and Pulses (Extended Group 9, 412 bytes)

Offset | Header Entry Name             | Type    | Description                                                                                                                                                                       |
------ | --------------------          | ----    | -----------
2296   | nWaveformEnable(0-1)          | 2short  | Analog waveform enabled: 0 = No; 1 = Yes.                                                                                                                                         |
2300   | nWaveformSource(0-1)          | 2short  | Analog waveform source: 0 = Disable; 1 = Generate waveform from epoch definitions; 2 = Generate waveform from a DAC file.                                                         |
2304   | nInterEpisodeLevel(0-1)       | 2short  | Inter-sweep holding level: 0 = Use holding level; 1 = Use last epoch amplitude.                                                                                                   |
2308   | nEpochType(0-1) (0-9)         | 20short | Epoch type: 0 = Disabled; 1 = Step; 2 = Ramp.Indexes: analog out waveform, epoch number.                                                                                          |
2348   | fEpochInitLevel(0-1) (0-9)    | 20float | Epoch initial level (user units).                                                                                                                                                 |
2428   | fEpochLevelInc(0-1) (0-9)     | 20float | Epoch level increment (user units).                                                                                                                                               |
2508   | lEpochInitDuration(0-1) (0-9) | 20long  | Epoch initial duration (in sequence counts).                                                                                                                                      |
2588   | lEpochDurationInc(0-1) (0-9)  | 20long  | Epoch duration increment (in sequence counts).                                                                                                                                    |
2668   | nDigitalTrainValue(0-9)       | 10short | Epoch duration increment in physical DAC channel order then epoch order (in sequence counts)                                                                                      |
2688   | nDigitalTrainActiveLogic      | short   | Epoch value for digital train output in epoch order. 0000 = Disabled; 0\*000 = Generates digital train on bit 3. Train period and pulse width can be controlled by the user list. |
2690   | sUnused012                    | 18char  | Unused                                                                                                                                                                            |

```
ASCII digital train pattern
|0000  :0x00000000
|000*  :0x00000001
|00*0  :0x00000002
|0*00  :0x00000004
|*000  :0x00000008|
```

### Extended DAC Output File (Extended Group 10, 552 bytes)

Offset | Header Entry Name       | Type    | Description                                                                                                                                                     |
------ | --------------------    | ----    | -----------
2708   | fDACFileScale(0-1)      | 2float  | Scaling factor to apply to DACwaveforms.                                                                                                                        |
2716   | fDACFileOffset(0-1)     | 2float  | Offset (in user units) to apply to DAC waveforms.                                                                                                               |
2724   | lDACFileEpisodeNum(0-1) | 2long   | Sweep (or column) number to replay from waveforms: -1 = all except the first (which is skipped), repeating last if necessary; 0 = all sweeps; N = sweep number. |
2732   | nDACFileADCNum(0-1)     | 2short  | Logical ADC channel number to replay from waveform file.                                                                                                        |
2736   | sDACFilePath(0-1)       | 412char | File path and name of DAC file containing waveform data. Must be ABF or ATF format.                                                                             |
3248   | sUnused013              | 12char  | Unused.                                                                                                                                                         |

### Extended Pre-sweep (Conditioning) Pulse Train (Extended Group 11, 100 bytes)

Offset | Header Entry Name      | Type   | Description                                                                                                                        |
------ | --------------------   | ----   | -----------
3260   | nConditEnable(0-1)     | 2short | Conditioning pulse train activation status: 0 = Disable; 1 = Enable.                                                               |
3264   | lConditNumPulses(0-1)  | 2long  | Number of pulses in conditioning pulse train.                                                                                      |
3272   | fBaselineDuration(0-1) | 2float | A single pulse in the conditioning train consists of a baseline followed by a step. This parameter is the baseline duration in ms. |
3280   | fBaselineLevel(0-1)    | 2float | Baseline level (user units).                                                                                                       |
3288   | fStepDuration(0-1)     | 2float | Step duration (ms).                                                                                                                |
3296   | fStepLevel(0-1)        | 2float | Step level (user units).                                                                                                           |
3304   | fPostTrainPeriod(0-1)  | 2float | At the end of the conditioning train there is a post-train steady-state output. This parameter is the post-train duration in ms.   |
3312   | fPostTrainLevel(0-1)   | 2float | Post-train level (user units).                                                                                                     |
3320   | sUnused014             | 40char | Unused.                                                                                                                            |

### Extended Variable Parameter User List (Extended Group 12, 1096 bytes)

Offset | Header Entry Name       | Type     | Description                                                                                                                                                                                                                  |
------ | --------------------    | ----     | -----------
3360   | nULEnable (0-3)         | 4short   | Parameter list activation status: 0 = Disable; 1 = Enable.                                                                                                                                                                   |
3368   | nULParamToVary (0-3)    | 4short   | Holds the index of the parameter that varies from sweep to sweep in one run.                                                                                                                                                 |
3376   | sULParamValueList (0-3) | 1024char | List of comma-separated values. If the number of entries in the list is fewer than the requested number of sweeps, the last list value is re-used. If there are more values in the list, the excess list values are ignored. |
4400   | nULRepeat(0-3)          | 4short   | Repeat the list when the current sweep exceeds the number of entries in the list. 0 = Disable, 1 = Repeat the list.                                                                                                          |
4408   | sUnused015              | 48char   | Unused.                                                                                                                                                                                                                      |

```
nULParamToVary:
    CONDITNUMPULSES=0
    CONDITBASELINEDURATION=1
    CONDITBASELINELEVEL=2
    CONDITSTEPDURATION=3
    CONDITSTEPLEVEL=4
    CONDITPOSTTRAINDURATION=5
    CONDITPOSTTRAINLEVEL=6
    EPISODESTARTTOSTART =7
    INACTIVEHOLDING=8
    DIGITALINTEREPISODE=9
    PNNUMPULSES=10
    PARALLELVALUE(0-9)=11-20
    EPOCHINITLEVEL(0-9)=21-30
    EPOCHINITDURATION(0-9)=31-40
```

```
   // EXTENDED GROUP #15 - On-line subtraction (56 bytes)
   short    nPNEnable[ABF_WAVEFORMCOUNT];
   short    nPNPolarity[ABF_WAVEFORMCOUNT];
   short    __nPNADCNum[ABF_WAVEFORMCOUNT];
   float    fPNHoldingLevel[ABF_WAVEFORMCOUNT];
   short    nPNNumADCChannels[ABF_WAVEFORMCOUNT];
   char     nPNADCSamplingSeq[ABF_WAVEFORMCOUNT][ABF_ADCCOUNT];
   // 4512 = 40 + 78 + 82 + 44 + 16 + 118 + 1044 + 14 + 184 + 98 + 44 + 84 + 36 + 52 + 34 + 82 + 16 + 10 + 62 + 160 + 412 + 552 + 100 + 1096 + 56
```

### Extended Environmental Information (Extended Group 6, 898 bytes)

Offset | Header Entry Name                   | Type    | Description                                                                                                                                                                |
------ | --------------------                | ----    | -----------
4512   | nTelegraphEnable(0-15)              | 16short | Telegraphs enabled in ADC channels: 0 = No; 1 = Yes.Index: ADC channel                                                                                                     |
4544   | nTelegraphInstrument(0-15)          | 16short | Telegraphs instrument identifier. Index: ADC channel                                                                                                                       |
4576   | fTelegraphAdditGain(0-15)           | 16float | Additional gain multiplier of Instrument. (Default = 1.)Index: ADC channel                                                                                                 |
4640   | fTelegraphFilter(0-15)              | 16float | Lowpass filter cutoff frequency of Instrument connected to nAutosampleADCNum. (Optionally autosampled by some acquisition programs.) (Default = 100000.)Index: ADC channel |
4704   | fTelegraphMembraneCap(0-15)         | 16float | Patch-clamp membrane capacitance compensation.                                                                                                                             |
4768   | nTelegraphMode(0-15)                | 16short | I-Clamp or V-Clamp mode. Currently this field is supported only for MultiClamp                                                                                             |
4800   | nTelegraphDACScaleFactorEnable(0-3) | 16short | Determines whether fDACScaleFactor was telegraphed: 1 = telegraphed; 0 = not telegraphed                                                                                   |
4808   | sUnused016a                         | 24char  | Unused.                                                                                                                                                                    |
4832   | nAutoAnalyseEnable                  | short   | Enable auto-analyze                                                                                                                                                        |
4834   | sAutoAnalysisMacroName              | 64char  | Name of auto-analysis macro.                                                                                                                                               |
4898   | sProtocolPath                       | 256char | File path of protocol.                                                                                                                                                     |
5154   | sFileComment                        | 128char | 128 byte ASCII comment string.                                                                                                                                             |
5282   | FileGUID                            | 16char  | FileGUID struct.                                                                                                                                                           |
5298   | fInstrumentHoldingLevel             | 16float | Instrument holding level                                                                                                                                                   |
5314   | ulFileCRC                           | long    | File CRC value, probably unused for later versions.                                                                                                                        |
5318   | sModifierInfo                       | 16char  | modifier info                                                                                                                                                              |
5334   | sUnused17                           | 76char  | Unused                                                                                                                                                                     |

```
nTelegraphInstrument codes
    0 = Unknown instrument;
    1 = Axopatch-1 with CV-4-1/100;
    2 = Axopatch-1 with CV-4-0.1/100;
    3 = Axopatch-1B(inv.) CV-4-1/100;
    4 = Axopatch-1B(inv) CV-4-0.1/100;
    5 = Axopatch 200 with CV 201;
    6 = Axopatch 200 with CV 202;
    7 = GeneClamp;
    8 = Dagan 3900;
    9 = Dagan 3900A;
    10 = Dagan CA-1 Im=0.1;
    11 = Dagan CA-1 Im=1.0;
    12 = Dagan CA-1 Im=10;
    13 = Warner OC-725;
    14 = Warner OC-725C;
    15 = AxoPatch 200B;
    16 = Dagan PC-ONE Im=0.1;
    17 = Dagan PC-ONE Im=1.0;
    18 = Dagan PC-ONE Im=10;
    19 = Dagan PC-ONE Im=100;
    20 = Warner BC-525C;
    21 = Warner PC-505;
    22 = Warner PC-501;
    23 = Dagan CA-1 Im=0.05;
    24 = MultiClamp 700
    25 = Turbo Tec.
```

### Statistics measurements (Group 13, 388 bytes)
```c
   short    nStatsEnable;
   unsigned short nStatsActiveChannels;             // Active stats channel bit flag
   unsigned short nStatsSearchRegionFlags;          // Active stats region bit flag
   short    nStatsSelectedRegion;
   short    _nStatsSearchMode;
   short    nStatsSmoothing;
   short    nStatsSmoothingEnable;
   short    nStatsBaseline;
   ABFLONG     lStatsBaselineStart;
   ABFLONG     lStatsBaselineEnd;
   ABFLONG     lStatsMeasurements[ABF_STATS_REGIONS];  // Measurement bit flag for each region ABF_STATS_REGIONS == 8
   ABFLONG     lStatsStart[ABF_STATS_REGIONS];
   ABFLONG     lStatsEnd[ABF_STATS_REGIONS];
   short    nRiseBottomPercentile[ABF_STATS_REGIONS];
   short    nRiseTopPercentile[ABF_STATS_REGIONS];
   short    nDecayBottomPercentile[ABF_STATS_REGIONS];
   short    nDecayTopPercentile[ABF_STATS_REGIONS];
   short    nStatsChannelPolarity[ABF_ADCCOUNT];
   short    nStatsSearchMode[ABF_STATS_REGIONS];    // Stats mode per region: mode is cursor region, epoch etc
   char     sUnused018[156];
```

IHS-1 telegraphs are not supported. Note: for most programs this is an
information-only field. For example, in Clampex the autosample instrument is
chosen as a configuration item and copied into this field.

### Application Version Data (Group 18, 16 bytes)

Offset | Header Entry Name    | Type  | Description                              |
------ | -------------------- | ----  | -----------
5798   | nMajorVersion        | short | Major version of application:  x.0.0.0   |
5800   | nMajorVersion        | short | Minor version of application:  0.x.0.0   |
5802   | nBugfixVersion       | short | Bug fix version of application:  0.0.x.0 |
5804   | nBuildVersion        | short | Build version of application:  0.0.0.x   |
5806   | sUnused019           | 8char | Unused.                                  |
5806   | nModifierMajorVersion | short | program that last edited the file
5808   | nModifierMinorVersion | short | program that last edited the file
5810   | nModifierBugfixVersion| short | program that last edited the file
5812   | nModifierBuildVersion | short | program that last edited the file

### LTP protocol (Group 19, 14 bytes)
```c
short    nLTPType;
short    nLTPUsageOfDAC[ABF_WAVEFORMCOUNT];
short    nLTPPresynapticPulses[ABF_WAVEFORMCOUNT];
char     sUnused020[4];
```
### Digidata 132x Trigger out flag (Group 20, 8 bytes)
```c
short    nDD132xTriggerOut;
char     sUnused021[6];
```

### Epoch resistance (Group 21, 56 bytes)
```c
char     sEpochResistanceSignalName[ABF_WAVEFORMCOUNT][ABF_ADCNAMELEN];
short    nEpochResistanceState[ABF_WAVEFORMCOUNT];
char     sUnused022[16]; // TODO remove??
```

### Alternating episodic mode (Group 22, 58 bytes)
```c
short    nAlternateDACOutputState;
short    nAlternateDigitalValue[ABF_EPOCHCOUNT];
short    nAlternateDigitalTrainValue[ABF_EPOCHCOUNT];
short    nAlternateDigitalOutputState;
char     sUnused023[14];
```

### Post-processing actions (Group 23, 210 bytes)
```c
float    fPostProcessLowpassFilter[ABF_ADCCOUNT];
char     nPostProcessLowpassFilterType[ABF_ADCCOUNT];
char     sUnused2048[130];
```

### The ABF Synch Section

The ABF Synch array is an important array that stores the start time and length
of each portion of the data if the data are not part of a continuous gap-free
acquisition. The data section might contain equal length or variable length
sweeps of data. The Synch Array contains a record to indicate the start time
and length of every sweep or Event in the data file. The ABF reading routines
automatically decode the Synch Array when providing information about the data.

A Synch array is created and used in the following acquisition modes:
ABF_VARLENEVENTS, ABF_FIXLENEVENTS & ABF_HIGHSPEEDOSC. The acquisition modes
ABF_GAPFREEFILE and ABF_WAVEFORMFILE do not always use a Synch array.

Offset | Header Entry Name    | Type | Description                                  |
------ | -------------------- | ---- | -----------
0      | lStart               | long | Start time of sweep in fSynchTimeUnit units. |
4      | lLength              | long | Length of the sweep in multiplexed samples.  |

### The ABF Tag Section

During an acquisition, some programs allow the user to tag points of interest
in the input data stream. These tags are saved in the Tag Section. Each tag
consists of a time stamp, a text comment, and a tag type identifier. If the tag
is a voice tag, the data is held in an ABFVoiceTagInfo struct.

**ABFTag Structure:**

Offset | Header Entry Name    | Type   | Description                                                                                          |
------ | -------------------- | ----   | -----------
0      | lTagTime             | long   | Time at which the tag was entered in fSynchTimeUnit units.                                           |
4      | sComment             | 56char | Optional comment to describe the tag.                                                                |
60     | nTagType             | short  | Type of tag. Valid types are ABF_TIMETAG=0, ABF_COMMENTTAG=1, ABF_EXTERNALTAG=2, ABF_VOICETAG=3. |
62     | nVoiceTagNumber      | short  | If nTagType=ABF_VOICETAG, this is the number of this voice tag.                                     |

**ABFVoiceTagInfo structure:**

Offset | Header Entry Name    | Type  | Description                                       |
------ | -------------------- | ----  | -----------
0      | lTagNumber           | long  | The tag number that corresponds to this VoiceTag. |
4      | lFileOffset          | long  | Offset to this tag within the VoiceTag block.     |
8      | lUncompressedSize    | long  | Size of the voice tag expanded.                   |
12     | lCompressedSize      | long  | Compressed size of the tag.                       |
16     | nCompressionType     | short | Compression method used.                          |
18     | nSampleSize          | short | Size of the samples acquired.                     |
20     | lSamplesPerSecond    | long  | Rate at which the sound was acquired.             |
24     | dwCRC                | DWORD | CRC used to check data integrity.                 |
28     | wChannels            | WORD  | Number of channels in the tag (usually 1).        |
30     | wUnused              | WORD  | Unused space.                                     |

### The ABF Deltas Section

When acquisition parameters are changed during an acquisition, the changes are
tracked and entered in the ABF deltas section. Each entry is time stamped in
fSynchTimeUnit units, so that the value of the parameter can be determined at
any point during the acquisition.

Offset | Header Entry Name             | Type       | Description                                                                             |
------ | --------------------          | ----       | -----------
0      | lDeltaTime                    | long       | Time at which the parameter was changed in fSynchTimeUnit units.                        |
4      | lParameterID                  | long       | Identifier for the parameter changed. Legal parameter values are: ABF_DELTA_XXXXXXXX. |
8      | lNewParamValue fNewParamValue | long float | Depending on the value of lParameterID this entry may be either a float or a long.      |