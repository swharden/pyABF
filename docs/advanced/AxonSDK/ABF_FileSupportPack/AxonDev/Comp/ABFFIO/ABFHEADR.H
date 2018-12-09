//***********************************************************************************************
//
//    Copyright (c) 1993-2004 Molecular Devices Corporation.
//    All rights reserved.
//    Permission is granted to freely use, modify and copy the code in this file.
//
//***********************************************************************************************
// HEADER:  ABFHEADR.H.
// PURPOSE: Defines the ABFFileHeader structure, and provides prototypes for
//          functions implemented in ABFHEADR.CPP for reading and writing
//          ABFFileHeader's.
// REVISIONS:
//   2.0  - This version separates the data in the file from the struct passed around within the application.

#ifndef INC_ABFHEADR2_H
#define INC_ABFHEADR2_H

#include "ABFFIO.h"
//#include "\AxonDev\Comp\AxABFFIO32\ABFHeadr.h"

#ifdef __cplusplus
extern "C" {
#endif

//
// Constants used in defining the ABF file header
//
#define ABF_ADCCOUNT           16    // number of ADC channels supported.
#define ABF_DACCOUNT           8     // number of DAC channels supported.
#define ABF_EPOCHCOUNT         50    // number of waveform epochs supported. //ST-1 : maximum epochs updated from 10 to 50
#define ABF_ADCUNITLEN         8     // length of ADC units strings
#define ABF_ADCNAMELEN_USER    8     // length of user-entered ADC channel name strings
#define ABF_ADCNAMELEN         10    // length of actual ADC channel name strings
#define ABF_DACUNITLEN         8     // length of DAC units strings
#define ABF_DACNAMELEN         10    // length of DAC channel name strings
#define ABF_USERLISTLEN        256   // length of the user list (V1.6)
#define ABF_USERLISTCOUNT      ABF_DACCOUNT     // number of independent user lists (V1.6)
#define ABF_OLDFILECOMMENTLEN  56    // length of file comment string (pre V1.6)
#define ABF_FILECOMMENTLEN     128   // length of file comment string (V1.6)
#define ABF_PATHLEN            256   // length of full path, used for DACFile and Protocol name.
#define ABF_CREATORINFOLEN     16    // length of file creator info string
#define ABF_ARITHMETICOPLEN    2     // length of the Arithmetic operator field
#define ABF_ARITHMETICUNITSLEN 8     // length of arithmetic units string
#define ABF_TAGCOMMENTLEN      56    // length of tag comment string
#define ABF_BLOCKSIZE          512   // Size of block alignment in ABF files.
#define PCLAMP6_MAXSWEEPLENGTH 16384   // Maximum multiplexed sweep length supported by pCLAMP6 apps.
#define PCLAMP7_MAXSWEEPLEN_PERCHAN    1032258  // Maximum per channel sweep length supported by pCLAMP7 apps.
#define PCLAMP11_MAXSWEEPLEN_PERCHAN   5161290  // Maximum per channel sweep length supported by pCLAMP11 apps. //ST-1
#define ABF_MAX_SWEEPS_PER_AVERAGE 65500     // The maximum number of sweeps that can be combined into a
                                             // cumulative average (nAverageAlgorithm=ABF_INFINITEAVERAGE).
#define ABF_MAX_TRIAL_SAMPLES  0x7FFFFFFF    // Maximum length of acquisition supported (samples)
                                             // INT_MAX is used instead of UINT_MAX because of the signed 
                                             // values in the ABF header.

//
// Constants for nDigitizerType
//
#define ABF_DIGI_UNKNOWN   0
#define ABF_DIGI_DEMO      1
#define ABF_DIGI_MINIDIGI  2
#define ABF_DIGI_DD132X    3
#define ABF_DIGI_OPUS      4
#define ABF_DIGI_PATCH     5
#define ABF_DIGI_DD1440    6
#define ABF_DIGI_MINIDIGI2 7
#define ABF_DIGI_DD1550    8
#define ABF_DIGI_DD1550A   9
#define ABF_DIGI_DD1550B   10

//
// Constants for nDrawingStrategy
//
#define ABF_DRAW_NONE            0
#define ABF_DRAW_REALTIME        1
#define ABF_DRAW_FULLSCREEN      2
#define ABF_DRAW_ENDOFRUN        3

//
// Constants for nTiledDisplay
//
#define ABF_DISPLAY_SUPERIMPOSED 0
#define ABF_DISPLAY_TILED        1

//
// Constants for nDataDisplayMode
//
#define ABF_DRAW_POINTS       0
#define ABF_DRAW_LINES        1

// Constants for the ABF_ReadOpen and ABF_WriteOpen functions
#define ABF_DATAFILE          0     
#define ABF_PARAMFILE         1     
#define ABF_ALLOWOVERLAP      2     // If this flag is not set, overlapping data in fixed-length 
                                    // event-detected data will be edited out by adjustment of
                                    // the synch array. (ABF_ReadOpen only!)
#define ABF_DATAFILE_ABF1     4 
#define ABF_PARAMFILE_ABF1    8 

//
// Constants for lParameterID in the ABFDelta structure.
//
// NOTE: If any changes are made to this list, the code in ABF_UpdateHeader must
//       be updated to include the new items.
#define ABF_DELTA_HOLDING0          0
#define ABF_DELTA_HOLDING1          1
#define ABF_DELTA_HOLDING2          2
#define ABF_DELTA_HOLDING3          3
#define ABF_DELTA_DIGITALOUTS       4
#define ABF_DELTA_THRESHOLD         5
#define ABF_DELTA_PRETRIGGER        6
#define ABF_DELTA_HOLDING4          7
#define ABF_DELTA_HOLDING5          8
#define ABF_DELTA_HOLDING6          9
#define ABF_DELTA_HOLDING7          10
#define ABF_DELTA_HUMFILTER_ON      11 //FB 4611
#define ABF_DELTA_HUMFILTER_OFF     12 //FB 4611


// Because of lack of space, the Autosample Gain ID also contains the ADC number.
#define ABF_DELTA_AUTOSAMPLE_GAIN   100   // +ADC channel.

// Because of lack of space, the Signal Gain ID also contains the ADC number.
#define ABF_DELTA_SIGNAL_GAIN       200   // +ADC channel.


//
// Constants for nAveragingMode
//
#define ABF_NOAVERAGING       0
#define ABF_SAVEAVERAGEONLY   1
#define ABF_AVERAGESAVEALL    2

//
// Constants for nAverageAlgorithm
//
#define ABF_INFINITEAVERAGE   0
#define ABF_SLIDINGAVERAGE    1

//
// Constants for nUndoPromptStrategy
//
#define ABF_UNDOPROMPT_ONABORT   0
#define ABF_UNDOPROMPT_ALWAYS    1

//
// Constants for nTriggerAction
//
#define ABF_TRIGGER_STARTEPISODE 0
#define ABF_TRIGGER_STARTRUN     1
#define ABF_TRIGGER_STARTTRIAL   2    // N.B. Discontinued in favor of nTrialTriggerSource

//
// Constants for nTriggerPolarity.
//
#define ABF_TRIGGER_RISINGEDGE  0
#define ABF_TRIGGER_FALLINGEDGE 1

//
// Constants for nDACFileEpisodeNum
//
#define ABF_DACFILE_SKIPFIRSTSWEEP -1
#define ABF_DACFILE_USEALLSWEEPS    0
// >0 = The specific sweep number.

//
// Constants for nInterEpisodeLevel & nDigitalInterEpisode
//
#define ABF_INTEREPI_USEHOLDING    0
#define ABF_INTEREPI_USELASTEPOCH  1

//
// Constants for nArithmeticExpression
//
#define ABF_SIMPLE_EXPRESSION    0
#define ABF_RATIO_EXPRESSION     1

//
// Constants for nLowpassFilterType & nHighpassFilterType
//
#define ABF_FILTER_NONE          0
#define ABF_FILTER_EXTERNAL      1
#define ABF_FILTER_SIMPLE_RC     2
#define ABF_FILTER_BESSEL        3
#define ABF_FILTER_BUTTERWORTH   4

//
// Constants for post nPostprocessLowpassFilterType
//
#define ABF_POSTPROCESS_FILTER_NONE          0
#define ABF_POSTPROCESS_FILTER_ADAPTIVE      1
#define ABF_POSTPROCESS_FILTER_BESSEL        2
#define ABF_POSTPROCESS_FILTER_BOXCAR        3
#define ABF_POSTPROCESS_FILTER_BUTTERWORTH   4
#define ABF_POSTPROCESS_FILTER_CHEBYSHEV     5
#define ABF_POSTPROCESS_FILTER_GAUSSIAN      6
#define ABF_POSTPROCESS_FILTER_RC            7
#define ABF_POSTPROCESS_FILTER_RC8           8
#define ABF_POSTPROCESS_FILTER_NOTCH         9

//
// The output sampling sequence identifier for a separate digital out channel.
//
#define ABF_DIGITAL_OUT_CHANNEL -1
#define ABF_PADDING_OUT_CHANNEL -2

//
// Constants for nAutoAnalyseEnable
//
#define ABF_AUTOANALYSE_DISABLED   0
#define ABF_AUTOANALYSE_DEFAULT    1
#define ABF_AUTOANALYSE_RUNMACRO   2

//
// Constants for nAutopeakSearchMode
//
#define ABF_PEAK_SEARCH_SPECIFIED       -2
#define ABF_PEAK_SEARCH_ALL             -1
// nAutopeakSearchMode 0..9   = epoch in waveform 0's epoch table
// nAutopeakSearchMode 10..19 = epoch in waveform 1's epoch table

//
// Constants for nAutopeakBaseline
//
#define ABF_PEAK_BASELINE_SPECIFIED    -3
#define ABF_PEAK_BASELINE_NONE 	      -2
#define ABF_PEAK_BASELINE_FIRSTHOLDING -1
#define ABF_PEAK_BASELINE_LASTHOLDING  -4

// Bit flag settings for nStatsSearchRegionFlags
//
#define ABF_PEAK_SEARCH_REGION0           0x01
#define ABF_PEAK_SEARCH_REGION1           0x02
#define ABF_PEAK_SEARCH_REGION2           0x04
#define ABF_PEAK_SEARCH_REGION3           0x08
#define ABF_PEAK_SEARCH_REGION4           0x10
#define ABF_PEAK_SEARCH_REGION5           0x20
#define ABF_PEAK_SEARCH_REGION6           0x40
#define ABF_PEAK_SEARCH_REGION7           0x80
#define ABF_PEAK_SEARCH_REGIONALL         0xFF        // All of the above OR'd together.

//
// Constants for nStatsActiveChannels
//
#define ABF_PEAK_SEARCH_CHANNEL0          0x0001
#define ABF_PEAK_SEARCH_CHANNEL1          0x0002
#define ABF_PEAK_SEARCH_CHANNEL2          0x0004
#define ABF_PEAK_SEARCH_CHANNEL3          0x0008
#define ABF_PEAK_SEARCH_CHANNEL4          0x0010
#define ABF_PEAK_SEARCH_CHANNEL5          0x0020
#define ABF_PEAK_SEARCH_CHANNEL6          0x0040
#define ABF_PEAK_SEARCH_CHANNEL7          0x0080
#define ABF_PEAK_SEARCH_CHANNEL8          0x0100
#define ABF_PEAK_SEARCH_CHANNEL9          0x0200
#define ABF_PEAK_SEARCH_CHANNEL10         0x0400
#define ABF_PEAK_SEARCH_CHANNEL11         0x0800
#define ABF_PEAK_SEARCH_CHANNEL12         0x1000
#define ABF_PEAK_SEARCH_CHANNEL13         0x2000
#define ABF_PEAK_SEARCH_CHANNEL14         0x4000
#define ABF_PEAK_SEARCH_CHANNEL15         0x8000
#define ABF_PEAK_SEARCH_CHANNELSALL       0xFFFF      // All of the above OR'd together.

//
// Constants for nLeakSubtractType
//
#define ABF_LEAKSUBTRACT_NONE       0
#define ABF_LEAKSUBTRACT_PN         1
#define ABF_LEAKSUBTRACT_RESISTIVE  2

//
// Constants for nPNPolarity
//
#define ABF_PN_OPPOSITE_POLARITY -1
#define ABF_PN_SAME_POLARITY     1

//
// Constants for nPNPosition
//
#define ABF_PN_BEFORE_EPISODE    0
#define ABF_PN_AFTER_EPISODE     1

//
// Constants for nAutosampleEnable
//
#define ABF_AUTOSAMPLEDISABLED   0
#define ABF_AUTOSAMPLEAUTOMATIC  1
#define ABF_AUTOSAMPLEMANUAL     2

//
// Constants for nAutosampleInstrument
//
#define ABF_INST_UNKNOWN         0   // Unknown instrument (manual or user defined telegraph table).
#define ABF_INST_AXOPATCH1       1   // Axopatch-1 with CV-4-1/100
#define ABF_INST_AXOPATCH1_1     2   // Axopatch-1 with CV-4-0.1/100
#define ABF_INST_AXOPATCH1B      3   // Axopatch-1B(inv.) CV-4-1/100
#define ABF_INST_AXOPATCH1B_1    4   // Axopatch-1B(inv) CV-4-0.1/100
#define ABF_INST_AXOPATCH201     5   // Axopatch 200 with CV 201
#define ABF_INST_AXOPATCH202     6   // Axopatch 200 with CV 202
#define ABF_INST_GENECLAMP       7   // GeneClamp
#define ABF_INST_DAGAN3900       8   // Dagan 3900
#define ABF_INST_DAGAN3900A      9   // Dagan 3900A
#define ABF_INST_DAGANCA1_1      10  // Dagan CA-1  Im=0.1
#define ABF_INST_DAGANCA1        11  // Dagan CA-1  Im=1.0
#define ABF_INST_DAGANCA10       12  // Dagan CA-1  Im=10
#define ABF_INST_WARNER_OC725    13  // Warner OC-725
#define ABF_INST_WARNER_OC725C   14  // Warner OC-725
#define ABF_INST_AXOPATCH200B    15  // Axopatch 200B
#define ABF_INST_DAGANPCONE0_1   16  // Dagan PC-ONE  Im=0.1
#define ABF_INST_DAGANPCONE1     17  // Dagan PC-ONE  Im=1.0
#define ABF_INST_DAGANPCONE10    18  // Dagan PC-ONE  Im=10
#define ABF_INST_DAGANPCONE100   19  // Dagan PC-ONE  Im=100
#define ABF_INST_WARNER_BC525C   20  // Warner BC-525C
#define ABF_INST_WARNER_PC505    21  // Warner PC-505
#define ABF_INST_WARNER_PC501    22  // Warner PC-501
#define ABF_INST_DAGANCA1_05     23  // Dagan CA-1  Im=0.05
#define ABF_INST_MULTICLAMP700   24  // MultiClamp 700
#define ABF_INST_TURBO_TEC       25  // Turbo Tec
#define ABF_INST_OPUSXPRESS6000  26  // OpusXpress 6000A
#define ABF_INST_AXOCLAMP900     27  // Axoclamp 900

//
// Constants for nTagType in the ABFTag structure.
//
#define ABF_TIMETAG              0
#define ABF_COMMENTTAG           1
#define ABF_EXTERNALTAG          2
#define ABF_VOICETAG             3
#define ABF_NEWFILETAG           4
#define ABF_ANNOTATIONTAG        5        // Same as a comment tag except that nAnnotationIndex holds 
                                          // the index of the annotation that holds extra information.

// Comment inserted for externally acquired tags (expanded with spaces to ABF_TAGCOMMENTLEN).
#define ABF_EXTERNALTAGCOMMENT   "<External>"
#define ABF_VOICETAGCOMMENT      "<Voice Tag>"

//
// Constants for nManualInfoStrategy
//
#define ABF_ENV_DONOTWRITE      0
#define ABF_ENV_WRITEEACHTRIAL  1
#define ABF_ENV_PROMPTEACHTRIAL 2

//
// Constants for nAutopeakPolarity
//
#define ABF_PEAK_NEGATIVE       -1
#define ABF_PEAK_ABSOLUTE        0
#define ABF_PEAK_POSITIVE        1

//
// LTP Types - Reflects whether the header is used for LTP as baseline or induction.
//
#define ABF_LTP_TYPE_NONE              0
#define ABF_LTP_TYPE_BASELINE          1
#define ABF_LTP_TYPE_INDUCTION         2

//
// LTP Usage of DAC - Reflects whether the analog output will be used presynaptically or postsynaptically.
//
#define ABF_LTP_DAC_USAGE_NONE         0
#define ABF_LTP_DAC_USAGE_PRESYNAPTIC  1
#define ABF_LTP_DAC_USAGE_POSTSYNAPTIC 2

// Values for the wScopeMode field in ABFScopeConfig.
#define ABF_EPISODICMODE    0
#define ABF_CONTINUOUSMODE  1
//#define ABF_XYMODE          2

//
// Constants for nExperimentType
//
#define ABF_VOLTAGECLAMP         0
#define ABF_CURRENTCLAMP         1
#define ABF_SIMPLEACQUISITION    2

//
// Miscellaneous constants
//
#define ABF_FILTERDISABLED  100000.0F     // Large frequency to disable lowpass filters
#define ABF_UNUSED_CHANNEL  -1            // Unused ADC and DAC channels.
#define ABF_ANY_CHANNEL     (UINT)-1      // Any ADC or DAC channel.

//
// Constant definitions for nDataFormat
//
#define ABF_INTEGERDATA      0
#define ABF_FLOATDATA        1

//
// Constant definitions for nOperationMode
//
#define ABF_VARLENEVENTS     1
#define ABF_FIXLENEVENTS     2     // (ABF_FIXLENEVENTS == ABF_LOSSFREEOSC)
#define ABF_LOSSFREEOSC      2
#define ABF_GAPFREEFILE      3
#define ABF_HIGHSPEEDOSC     4
#define ABF_WAVEFORMFILE     5

//
// Constants for nEpochType
//
#define ABF_EPOCHDISABLED           0     // disabled epoch
#define ABF_EPOCHSTEPPED            1     // stepped waveform
#define ABF_EPOCHRAMPED             2     // ramp waveform
#define ABF_EPOCH_TYPE_RECTANGLE    3     // rectangular pulse train
#define ABF_EPOCH_TYPE_TRIANGLE     4     // triangular waveform
#define ABF_EPOCH_TYPE_COSINE       5     // cosinusoidal waveform
#define ABF_EPOCH_TYPE_RESISTANCE   6     // was ABF_EPOCH_TYPE_RESISTANCE
#define ABF_EPOCH_TYPE_BIPHASIC     7     // biphasic pulse train
#define ABF_EPOCHSLOPE              8     // IonWorks style ramp waveform

//
// Constants for epoch resistance
//
#define ABF_MIN_EPOCH_RESISTANCE_DURATION 8

//
// Constants for nWaveformSource
//
#define ABF_WAVEFORMDISABLED     0               // disabled waveform
#define ABF_EPOCHTABLEWAVEFORM   1
#define ABF_DACFILEWAVEFORM      2

//
// Constant definitions for nFileType
//
#define ABF_ABFFILE          1
#define ABF_FETCHEX          2
#define ABF_CLAMPEX          3

//
// maximum values for various parameters (used by ABFH1_CheckUserList).
//
#define ABF_CTPULSECOUNT_MAX           10000
#define ABF2_CTBASELINEDURATION_MAX    1000000.0F
#define ABF2_CTSTEPDURATION_MAX        1000000.0F
#define ABF2_CTPOSTTRAINDURATION_MAX   1000000.0F
#define ABF2_SWEEPSTARTTOSTARTTIME_MAX 1000000.0F 
#define ABF_PNPULSECOUNT_MAX           8
#define ABF_DIGITALVALUE_MAX           0xFF
#define ABF_EPOCHDIGITALVALUE_MAX      0xFF

//
// Constants for nTriggerSource
//
#define ABF_TRIGGERLINEINPUT           -5   // Start on line trigger (DD1320 only)
#define ABF_TRIGGERTAGINPUT            -4
#define ABF_TRIGGERFIRSTCHANNEL        -3
#define ABF_TRIGGEREXTERNAL            -2
#define ABF_TRIGGERSPACEBAR            -1
// >=0 = ADC channel to trigger off.

//
// Constants for nTrialTriggerSource
//
#define ABF_TRIALTRIGGER_SWSTARTONLY   -6   // Start on software message, end when protocol ends.
#define ABF_TRIALTRIGGER_SWSTARTSTOP   -5   // Start and end on software messages.
#define ABF_TRIALTRIGGER_LINEINPUT     -4   // Start on line trigger (DD1320 only)
#define ABF_TRIALTRIGGER_SPACEBAR      -3   // Start on spacebar press.
#define ABF_TRIALTRIGGER_EXTERNAL      -2   // Start on external trigger high
#define ABF_TRIALTRIGGER_NONE          -1   // Start immediately (default).
// >=0 = ADC channel to trigger off.    // Not implemented as yet...

//
// Constants for lStatisticsMeasurements
//
#define ABF_STATISTICS_ABOVETHRESHOLD     0x00000001
#define ABF_STATISTICS_EVENTFREQUENCY     0x00000002
#define ABF_STATISTICS_MEANOPENTIME       0x00000004
#define ABF_STATISTICS_MEANCLOSEDTIME     0x00000008
#define ABF_STATISTICS_ALL                0x0000000F     // All the above OR'd together.

//
// Constants for nStatisticsSaveStrategy
//
#define ABF_STATISTICS_NOAUTOSAVE            0
#define ABF_STATISTICS_AUTOSAVE              1
#define ABF_STATISTICS_AUTOSAVE_AUTOCLEAR    2

//
// Constants for nStatisticsDisplayStrategy
//
#define ABF_STATISTICS_DISPLAY      0
#define ABF_STATISTICS_NODISPLAY    1

//
// Constants for nStatisticsClearStrategy
// determines whether to clear statistics after saving.
//
#define ABF_STATISTICS_NOCLEAR      0
#define ABF_STATISTICS_CLEAR        1

#define ABF_STATS_REGIONS     24             // The number of independent statistics regions. // ST-91
#define ABF_BASELINE_REGIONS  1              // The number of independent baseline regions.
#define ABF_STATS_NUM_MEASUREMENTS 18        // The total number of supported statistcs measurements.

//
// Constants for lAutopeakMeasurements
//
#define ABF_PEAK_MEASURE_PEAK                0x00000001
#define ABF_PEAK_MEASURE_PEAKTIME            0x00000002
#define ABF_PEAK_MEASURE_ANTIPEAK            0x00000004
#define ABF_PEAK_MEASURE_ANTIPEAKTIME        0x00000008
#define ABF_PEAK_MEASURE_MEAN                0x00000010
#define ABF_PEAK_MEASURE_STDDEV              0x00000020
#define ABF_PEAK_MEASURE_INTEGRAL            0x00000040
#define ABF_PEAK_MEASURE_MAXRISESLOPE        0x00000080
#define ABF_PEAK_MEASURE_MAXRISESLOPETIME    0x00000100
#define ABF_PEAK_MEASURE_MAXDECAYSLOPE       0x00000200
#define ABF_PEAK_MEASURE_MAXDECAYSLOPETIME   0x00000400
#define ABF_PEAK_MEASURE_RISETIME            0x00000800
#define ABF_PEAK_MEASURE_DECAYTIME           0x00001000
#define ABF_PEAK_MEASURE_HALFWIDTH           0x00002000
#define ABF_PEAK_MEASURE_BASELINE            0x00004000
#define ABF_PEAK_MEASURE_RISESLOPE           0x00008000
#define ABF_PEAK_MEASURE_DECAYSLOPE          0x00010000
#define ABF_PEAK_MEASURE_REGIONSLOPE         0x00020000
#define ABF_PEAK_MEASURE_DURATION            0x00040000

#define ABF_PEAK_NORMAL_PEAK                 0x00100000
#define ABF_PEAK_NORMAL_ANTIPEAK             0x00400000
#define ABF_PEAK_NORMAL_MEAN                 0x01000000
#define ABF_PEAK_NORMAL_STDDEV               0x02000000
#define ABF_PEAK_NORMAL_INTEGRAL             0x04000000

#define ABF_PEAK_NORMALISABLE                0x00000075
#define ABF_PEAK_NORMALISED                  0x07500000

#define ABF_PEAK_MEASURE_ALL                 0x0752FFFF    // All of the above OR'd together.

//
// Constant definitions for nParamToVary
//
#define ABF_CONDITNUMPULSES         0
#define ABF_CONDITBASELINEDURATION  1
#define ABF_CONDITBASELINELEVEL     2
#define ABF_CONDITSTEPDURATION      3
#define ABF_CONDITSTEPLEVEL         4
#define ABF_CONDITPOSTTRAINDURATION 5
#define ABF_CONDITPOSTTRAINLEVEL    6
#define ABF_EPISODESTARTTOSTART     7
#define ABF_INACTIVEHOLDING         8
#define ABF_DIGITALHOLDING          9
#define ABF_PNNUMPULSES             10
#define ABF_PARALLELVALUE           11
#define ABF_EPOCHINITLEVEL          (ABF_PARALLELVALUE + ABF_EPOCHCOUNT)
#define ABF_EPOCHINITDURATION       (ABF_EPOCHINITLEVEL + ABF_EPOCHCOUNT)
#define ABF_EPOCHTRAINPERIOD        (ABF_EPOCHINITDURATION + ABF_EPOCHCOUNT)
#define ABF_EPOCHTRAINPULSEWIDTH    (ABF_EPOCHTRAINPERIOD + ABF_EPOCHCOUNT)
// Next value is (ABF_EPOCHINITDURATION + ABF_EPOCHCOUNT)

// Values for the nEraseStrategy field in ABFScopeConfig.
#define ABF_ERASE_EACHSWEEP   0
#define ABF_ERASE_EACHRUN     1
#define ABF_ERASE_EACHTRIAL   2
#define ABF_ERASE_DONTERASE   3

// Indexes into the rgbColor field of ABFScopeConfig.
#define ABF_BACKGROUNDCOLOR   0
#define ABF_GRIDCOLOR         1
#define ABF_THRESHOLDCOLOR    2
#define ABF_EVENTMARKERCOLOR  3
#define ABF_SEPARATORCOLOR    4
#define ABF_AVERAGECOLOR      5
#define ABF_OLDDATACOLOR      6
#define ABF_TEXTCOLOR         7
#define ABF_AXISCOLOR         8
#define ABF_ACTIVEAXISCOLOR   9
#define ABF_LASTCOLOR         ABF_ACTIVEAXISCOLOR
#define ABF_SCOPECOLORS       (ABF_LASTCOLOR+1)

// Extended colors for rgbColorEx field in ABFScopeConfig
#define ABF_STATISTICS_REGION0  0
#define ABF_STATISTICS_REGION1  1
#define ABF_STATISTICS_REGION2  2
#define ABF_STATISTICS_REGION3  3
#define ABF_STATISTICS_REGION4  4
#define ABF_STATISTICS_REGION5  5
#define ABF_STATISTICS_REGION6  6
#define ABF_STATISTICS_REGION7  7
#define ABF_STATISTICS_REGION8  8
#define ABF_STATISTICS_REGION9  9
#define ABF_STATISTICS_REGION10 10
#define ABF_STATISTICS_REGION11 11
#define ABF_STATISTICS_REGION12 12
#define ABF_STATISTICS_REGION13 13
#define ABF_STATISTICS_REGION14 14
#define ABF_STATISTICS_REGION15 15
#define ABF_STATISTICS_REGION16 16
#define ABF_STATISTICS_REGION17 17
#define ABF_STATISTICS_REGION18 18
#define ABF_STATISTICS_REGION19 19
#define ABF_STATISTICS_REGION20 20
#define ABF_STATISTICS_REGION21 21
#define ABF_STATISTICS_REGION22 22
#define ABF_STATISTICS_REGION23 23
#define ABF_BASELINE_REGION     24
#define ABF_STOREDSWEEPCOLOR    25
#define ABF_LASTCOLOR_EX        ABF_STOREDSWEEPCOLOR
#define ABF_SCOPECOLORS_EX      (ABF_LASTCOLOR+1)

//
// Constants for nCompressionType in the ABFVoiceTagInfo structure.
//
#define ABF_COMPRESSION_NONE     0
#define ABF_COMPRESSION_PKWARE   1
#define ABF_CURRENTVERSION    ABF_V209       // Current file format version number //ST-10 - Enable digital or analog output in gap free mode

//
// Header Version Numbers
//
#define ABF_V200  2.00F                       // Alpha versions of pCLAMP 10 and DataXpress 2
#define ABF_V201  2.01F                       // DataXpress 2.0.0.16 and later
                                              // pCLAMP 10.0.0.6 and later
#define ABF_V202  2.02F                       // Barracuda 1.0 and later
#define ABF_V203  2.03F                       // pCLAMP 10.4.0.7 and later
#define ABF_V204  2.04F                       // pCLAMP 10.4.1.7 and later
#define ABF_V205  2.05F                       // pCLAMP 10.5 and later
#define ABF_V206	2.06F						// pCLAMP 10.6 and later //FB 4867
#define ABF_V207	2.07F						// pCLAMP 11 and later //ST-1
#define ABF_V208	2.08F						// pCLAMP 11 and later //ST-9 -  Internal changes
#define ABF_V209	2.09F						// pCLAMP 11 and later //ST-10 - Enable digital or analog output in gap free mode //ST-91 Increased ABF_STATS_REGIONS to 24

// Retired constants.
#undef ABF_AUTOANALYSE_RUNMACRO
#undef ABF_MACRONAMELEN

//
// pack structure on byte boundaries
//
#ifndef RC_INVOKED
#pragma pack(push, 1)
#endif

//
// Definition of the ABF header structure.
//
struct ABFFileHeader
{
public:
   // GROUP #1 - File ID and size information
   float    fFileVersionNumber;
   short    nOperationMode;
   long     lActualAcqLength;
   short    nNumPointsIgnored;
   long     lActualEpisodes;
   UINT     uFileStartDate;         // YYYYMMDD
   UINT     uFileStartTimeMS;
   long     lStopwatchTime;
   float    fHeaderVersionNumber;
   short    nFileType;

   // GROUP #2 - File Structure
   long     lDataSectionPtr;
   long     lTagSectionPtr;
   long     lNumTagEntries;
   long     lScopeConfigPtr;
   long     lNumScopes;
   long     lDeltaArrayPtr;
   long     lNumDeltas;
   long     lVoiceTagPtr;
   long     lVoiceTagEntries;
   long     lSynchArrayPtr;
   long     lSynchArraySize;
   short    nDataFormat;
   short    nSimultaneousScan;
   long     lStatisticsConfigPtr;
   long     lAnnotationSectionPtr;
   long     lNumAnnotations;
   long     lDACFilePtr[ABF_DACCOUNT];
   long     lDACFileNumEpisodes[ABF_DACCOUNT];

   // GROUP #3 - Trial hierarchy information
   short    nADCNumChannels;
   float    fADCSequenceInterval;
   UINT     uFileCompressionRatio;
   bool     bEnableFileCompression;
   float    fSynchTimeUnit;
   float    fSecondsPerRun;
   long     lNumSamplesPerEpisode;
   long     lPreTriggerSamples;
   long     lEpisodesPerRun;
   long     lRunsPerTrial;
   long     lNumberOfTrials;
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
   long     lAverageCount;
   short    nAutoTriggerStrategy;
   float    fFirstRunDelayS;
   UINT		nTriggerTimeout; //FB 2296

   // GROUP #4 - Display Parameters
   short    nDataDisplayMode;
   short    nChannelStatsStrategy;
   long     lSamplesPerTrace;
   long     lStartDisplayNum;
   long     lFinishDisplayNum;
   short    nShowPNRawData;
   float    fStatisticsPeriod;
   long     lStatisticsMeasurements;
   short    nStatisticsSaveStrategy;

   // GROUP #5 - Hardware information
   float    fADCRange;
   float    fDACRange;
   long     lADCResolution;
   long     lDACResolution;
   short    nDigitizerADCs;
   short    nDigitizerDACs;
   short    nDigitizerTotalDigitalOuts;
   short    nDigitizerSynchDigitalOuts;
   short    nDigitizerType;

   // GROUP #6 Environmental Information
   short    nExperimentType;
   short    nManualInfoStrategy;
   float    fCellID1;
   float    fCellID2;
   float    fCellID3;
   char     sProtocolPath[ABF_PATHLEN];
   char     sCreatorInfo[ABF_CREATORINFOLEN];
   char     sModifierInfo[ABF_CREATORINFOLEN];
   short    nCommentsEnable;
   char     sFileComment[ABF_FILECOMMENTLEN];
   short    nTelegraphEnable[ABF_ADCCOUNT];
   short    nTelegraphInstrument[ABF_ADCCOUNT];
   float    fTelegraphAdditGain[ABF_ADCCOUNT];
   float    fTelegraphFilter[ABF_ADCCOUNT];
   float    fTelegraphMembraneCap[ABF_ADCCOUNT];
   float    fTelegraphAccessResistance[ABF_ADCCOUNT];
   short    nTelegraphMode[ABF_ADCCOUNT];
   short    nTelegraphDACScaleFactorEnable[ABF_DACCOUNT];

   short    nAutoAnalyseEnable;

   GUID     FileGUID;
   float    fInstrumentHoldingLevel[ABF_DACCOUNT];
   unsigned long ulFileCRC;
   short    nCRCEnable;

   // GROUP #7 - Multi-channel information
   short    nSignalType;                        // why is this only single channel ?
   short    nADCPtoLChannelMap[ABF_ADCCOUNT];
   short    nADCSamplingSeq[ABF_ADCCOUNT];
   float    fADCProgrammableGain[ABF_ADCCOUNT];
   float    fADCDisplayAmplification[ABF_ADCCOUNT];
   float    fADCDisplayOffset[ABF_ADCCOUNT];       
   float    fInstrumentScaleFactor[ABF_ADCCOUNT];  
   float    fInstrumentOffset[ABF_ADCCOUNT];       
   float    fSignalGain[ABF_ADCCOUNT];
   float    fSignalOffset[ABF_ADCCOUNT];
   float    fSignalLowpassFilter[ABF_ADCCOUNT];
   float    fSignalHighpassFilter[ABF_ADCCOUNT];
   char     nLowpassFilterType[ABF_ADCCOUNT];
   char     nHighpassFilterType[ABF_ADCCOUNT];
   bool     bHumFilterEnable[ABF_ADCCOUNT];

   char     sADCChannelName[ABF_ADCCOUNT][ABF_ADCNAMELEN];   // extra chars so name can be modified for P/N
   char     sADCUnits[ABF_ADCCOUNT][ABF_ADCUNITLEN];
   float    fDACScaleFactor[ABF_DACCOUNT];
   float    fDACHoldingLevel[ABF_DACCOUNT];
   float    fDACCalibrationFactor[ABF_DACCOUNT];
   float    fDACCalibrationOffset[ABF_DACCOUNT];
   char     sDACChannelName[ABF_DACCOUNT][ABF_DACNAMELEN];
   char     sDACChannelUnits[ABF_DACCOUNT][ABF_DACUNITLEN];

   // GROUP #9 - Epoch Waveform and Pulses
   short    nDigitalEnable;
   short    nActiveDACChannel;                     // should retire !
   short    nDigitalDACChannel;
   short    nDigitalHolding;
   short    nDigitalInterEpisode;
   short    nDigitalTrainActiveLogic;                                   
   short    nDigitalValue[ABF_EPOCHCOUNT];
   short    nDigitalTrainValue[ABF_EPOCHCOUNT];                         
   bool     bEpochCompression[ABF_EPOCHCOUNT];
   short    nWaveformEnable[ABF_DACCOUNT];
   short    nWaveformSource[ABF_DACCOUNT];
   short    nInterEpisodeLevel[ABF_DACCOUNT];
   short    nEpochType[ABF_DACCOUNT][ABF_EPOCHCOUNT];
   float    fEpochInitLevel[ABF_DACCOUNT][ABF_EPOCHCOUNT];
   float    fEpochFinalLevel[ABF_DACCOUNT][ABF_EPOCHCOUNT]; // Only used for ABF_EPOCHSLOPE.
   float    fEpochLevelInc[ABF_DACCOUNT][ABF_EPOCHCOUNT];
   long     lEpochInitDuration[ABF_DACCOUNT][ABF_EPOCHCOUNT];
   long     lEpochDurationInc[ABF_DACCOUNT][ABF_EPOCHCOUNT];
   short    nEpochTableRepetitions[ABF_DACCOUNT];
   float    fEpochTableStartToStartInterval[ABF_DACCOUNT];

   // GROUP #10 - DAC Output File
   float    fDACFileScale[ABF_DACCOUNT];
   float    fDACFileOffset[ABF_DACCOUNT];
   long     lDACFileEpisodeNum[ABF_DACCOUNT];
   short    nDACFileADCNum[ABF_DACCOUNT];
   char     sDACFilePath[ABF_DACCOUNT][ABF_PATHLEN];

   // GROUP #11a - Presweep (conditioning) pulse train
   short    nConditEnable[ABF_DACCOUNT];
   long     lConditNumPulses[ABF_DACCOUNT];
   float    fBaselineDuration[ABF_DACCOUNT];
   float    fBaselineLevel[ABF_DACCOUNT];
   float    fStepDuration[ABF_DACCOUNT];
   float    fStepLevel[ABF_DACCOUNT];
   float    fPostTrainPeriod[ABF_DACCOUNT];
   float    fPostTrainLevel[ABF_DACCOUNT];
   float    fCTStartLevel[ABF_DACCOUNT][ABF_EPOCHCOUNT];
   float    fCTEndLevel[ABF_DACCOUNT][ABF_EPOCHCOUNT];
   float    fCTIntervalDuration[ABF_DACCOUNT][ABF_EPOCHCOUNT];
   float    fCTStartToStartInterval[ABF_DACCOUNT];

   // GROUP #11b - Membrane Test Between Sweeps
   short    nMembTestEnable[ABF_DACCOUNT];
   float    fMembTestPreSettlingTimeMS[ABF_DACCOUNT];
   float    fMembTestPostSettlingTimeMS[ABF_DACCOUNT];

    // GROUP #11c - PreSignal test pulse
   short    nPreSignalEnable[ABF_DACCOUNT];
   float    fPreSignalPreStepDuration[ABF_DACCOUNT];
   float    fPreSignalPreStepLevel[ABF_DACCOUNT];
   float    fPreSignalStepDuration[ABF_DACCOUNT];
   float    fPreSignalStepLevel[ABF_DACCOUNT];
   float    fPreSignalPostStepDuration[ABF_DACCOUNT];
   float    fPreSignalPostStepLevel[ABF_DACCOUNT];

	//	GROUP #11d - Hum Silncer Adapt between sweeps //FB 4867
	short    nAdaptEnable;
	float		fInterSweepAdaptTimeS;

   // GROUP #12 - Variable parameter user list
   short    nULEnable[ABF_USERLISTCOUNT];
   short    nULParamToVary[ABF_USERLISTCOUNT];
   short    nULRepeat[ABF_USERLISTCOUNT];
   char     sULParamValueList[ABF_USERLISTCOUNT][ABF_USERLISTLEN];

   // GROUP #13 - Statistics measurements
   short    nStatsEnable;
   unsigned short nStatsActiveChannels;             // Active stats channel bit flag
   unsigned short nStatsSearchRegionFlags;          // Active stats region bit flag
   short    nStatsSmoothing;
   short    nStatsSmoothingEnable;
   short    nStatsBaseline;
   short    nStatsBaselineDAC;                      // If mode is epoch, then this holds the DAC
   long     lStatsBaselineStart;
   long     lStatsBaselineEnd;
   long     lStatsMeasurements[ABF_STATS_REGIONS];  // Measurement bit flag for each region
   long     lStatsStart[ABF_STATS_REGIONS];
   long     lStatsEnd[ABF_STATS_REGIONS];
   short    nRiseBottomPercentile[ABF_STATS_REGIONS];
   short    nRiseTopPercentile[ABF_STATS_REGIONS];
   short    nDecayBottomPercentile[ABF_STATS_REGIONS];
   short    nDecayTopPercentile[ABF_STATS_REGIONS];
   short    nStatsChannelPolarity[ABF_ADCCOUNT];
   short    nStatsSearchMode[ABF_STATS_REGIONS];    // Stats mode per region: mode is cursor region, epoch etc 
   short    nStatsSearchDAC[ABF_STATS_REGIONS];     // If mode is epoch, then this holds the DAC

   // GROUP #14 - Channel Arithmetic
   short    nArithmeticEnable;
   short    nArithmeticExpression;
   float    fArithmeticUpperLimit;
   float    fArithmeticLowerLimit;
   short    nArithmeticADCNumA;
   short    nArithmeticADCNumB;
   float    fArithmeticK1;
   float    fArithmeticK2;
   float    fArithmeticK3;
   float    fArithmeticK4;
   float    fArithmeticK5;
   float    fArithmeticK6;
   char     sArithmeticOperator[ABF_ARITHMETICOPLEN];
   char     sArithmeticUnits[ABF_ARITHMETICUNITSLEN];

   // GROUP #15 - Leak subtraction
   short    nPNPosition;
   short    nPNNumPulses;
   short    nPNPolarity;
   float    fPNSettlingTime;
   float    fPNInterpulse;
   short    nLeakSubtractType[ABF_DACCOUNT];
   float    fPNHoldingLevel[ABF_DACCOUNT];
   short    nLeakSubtractADCIndex[ABF_DACCOUNT];

   // GROUP #16 - Miscellaneous variables
   short    nLevelHysteresis;
   long     lTimeHysteresis;
   short    nAllowExternalTags;
   short    nAverageAlgorithm;
   float    fAverageWeighting;
   short    nUndoPromptStrategy;
   short    nTrialTriggerSource;
   short    nStatisticsDisplayStrategy;
   short    nExternalTagType;
   long     lHeaderSize;
   short    nStatisticsClearStrategy;
   short    nEnableFirstLastHolding;            // First & Last Holding are now optional.

   // GROUP #17 - Trains parameters
   long     lEpochPulsePeriod[ABF_DACCOUNT][ABF_EPOCHCOUNT];
   long     lEpochPulseWidth [ABF_DACCOUNT][ABF_EPOCHCOUNT];

   // GROUP #18 - Application version data
   short    nCreatorMajorVersion;
   short    nCreatorMinorVersion;
   short    nCreatorBugfixVersion;
   short    nCreatorBuildVersion;
   short    nModifierMajorVersion;
   short    nModifierMinorVersion;
   short    nModifierBugfixVersion;
   short    nModifierBuildVersion;

   // GROUP #19 - LTP protocol
   short    nLTPType;
   short    nLTPUsageOfDAC[ABF_DACCOUNT];
   short    nLTPPresynapticPulses[ABF_DACCOUNT];

   // GROUP #20 - Digidata 132x Trigger out flag
   short    nScopeTriggerOut;

   // GROUP #21 - Epoch resistance
   char     sEpochResistanceSignalName[ABF_DACCOUNT][ABF_ADCNAMELEN];
   short    nEpochResistanceState[ABF_DACCOUNT];
   
   // GROUP #22 - Alternating episodic mode
   short    nAlternateDACOutputState;
   short    nAlternateDigitalOutputState;
   short    nAlternateDigitalValue[ABF_EPOCHCOUNT];
   short    nAlternateDigitalTrainValue[ABF_EPOCHCOUNT];

   // GROUP #23 - Post-processing actions
   float    fPostProcessLowpassFilter[ABF_ADCCOUNT];
   char     nPostProcessLowpassFilterType[ABF_ADCCOUNT];

   // GROUP #24 - Legacy gear shift info
   float    fLegacyADCSequenceInterval;
   float    fLegacyADCSecondSequenceInterval;
   long     lLegacyClockChange;
   long     lLegacyNumSamplesPerEpisode;

	// GROUP #25 - Gap-Free Config
   short    nGapFreeEpochType[ABF_DACCOUNT][ABF_EPOCHCOUNT];
   float    fGapFreeEpochLevel[ABF_DACCOUNT][ABF_EPOCHCOUNT];   
   long     lGapFreeEpochDuration[ABF_DACCOUNT][ABF_EPOCHCOUNT];
   bool     nGapFreeDigitalValue[ABF_DACCOUNT][ABF_EPOCHCOUNT];
   short    nGapFreeEpochStart;

   ABFFileHeader();
};   

inline ABFFileHeader::ABFFileHeader()
{
   // Set everything to 0.
   memset( this, 0, sizeof(ABFFileHeader) );
   
   // Set critical parameters so we can determine the version.
   fFileVersionNumber   = ABF_CURRENTVERSION;
   fHeaderVersionNumber = ABF_CURRENTVERSION;
   lHeaderSize          = sizeof(ABFFileHeader);
}

//
// Scope descriptor format.
//
#define ABF_FACESIZE 32
struct ABFLogFont
{
   short nHeight;                // Height of the font in pixels.
//   short lWidth;               // use 0
//   short lEscapement;          // use 0
//   short lOrientation;         // use 0
   short nWeight;                // MSWindows font weight value.
//   char bItalic;               // use 0
//   char bUnderline;            // use 0
//   char bStrikeOut;            // use 0
//   char cCharSet;              // use ANSI_CHARSET (0)
//   char cOutPrecision;         // use OUT_TT_PRECIS
//   char cClipPrecision;        // use CLIP_DEFAULT_PRECIS
//   char cQuality;              // use PROOF_QUALITY
   char cPitchAndFamily;         // MSWindows pitch and family mask.
   char Unused[3];               // Unused space to maintain 4-byte packing.
   char szFaceName[ABF_FACESIZE];// Face name of the font.
};     // Size = 40

struct ABFSignal
{
   char     szName[ABF_ADCNAMELEN+2];        // ABF name length + '\0' + 1 for alignment.
   short    nMxOffset;                       // Offset of the signal in the sampling sequence.
   DWORD    rgbColor;                        // Pen color used to draw trace.
   char     nPenWidth;                       // Pen width in pixels.
   char     bDrawPoints;                     // TRUE = Draw disconnected points
   char     bHidden;                         // TRUE = Hide the trace.
   char     bFloatData;                      // TRUE = Floating point pseudo channel
   float    fVertProportion;                 // Relative proportion of client area to use
   float    fDisplayGain;                    // Display gain of trace in UserUnits
   float    fDisplayOffset;                  // Display offset of trace in UserUnits

//   float    fUUTop;                          // Top of window in UserUnits
//   float    fUUBottom;                       // Bottom of window in UserUnits
};      // Size = 34

struct ABFScopeConfig
{
   // Section 1 scope configurations
   DWORD       dwFlags;                   // Flags that are meaningful to the scope.
   DWORD       rgbColor[ABF_SCOPECOLORS]; // Colors for the components of the scope.
   float       fDisplayStart;             // Start of the display area in ms.
   float       fDisplayEnd;               // End of the display area in ms.
   WORD        wScopeMode;                // Mode that the scope is in.
   char        bMaximized;                // TRUE = Scope parent is maximized.
   char        bMinimized;                // TRUE = Scope parent is minimized.
   short       xLeft;                     // Coordinate of the left edge.
   short       yTop;                      // Coordinate of the top edge.
   short       xRight;                    // Coordinate of the right edge.
   short       yBottom;                   // Coordinate of the bottom edge.
   ABFLogFont  LogFont;                   // Description of current font.
   ABFSignal   TraceList[ABF_ADCCOUNT];   // List of traces in current use.
   short       nYAxisWidth;               // Width of the YAxis region.
   short       nTraceCount;               // Number of traces described in TraceList.
   short       nEraseStrategy;            // Erase strategy.
   short       nDockState;                // Docked position.
   // Size 656
   // * Do not insert any new members above this point! *
   // Section 2 scope configurations for file version 1.68.
   short       nSizeofOldStructure;              // Unused byte to determine the offset of the version 2 data.
   DWORD       rgbColorEx[ ABF_SCOPECOLORS_EX ]; // New color settings for stored sweep and cursors.
   short       nAutoZeroState;                   // Status of the autozero selection.
   DWORD       dwCursorsVisibleState;            // Flag for visible status of cursors.
   DWORD       dwCursorsLockedState;             // Flag for enabled status of cursors.
   DWORD			rgbHumColor;							 // New color to draw the noie cancelled signal from the HumSilencer //FB 4611
   char        sUnasigned[57 /*61*/];
   // Size 113
   ABFScopeConfig();
}; // Size = 769


inline ABFScopeConfig::ABFScopeConfig()
{
   // Set everything to 0.
   memset( this, 0, sizeof(ABFScopeConfig) );
   
   // Set critical parameters so we can determine the version.
   nSizeofOldStructure = 656;
}

//
// Definition of the ABF Tag structure
//
struct ABFTag
{
   long    lTagTime;          // Time at which the tag was entered in fSynchTimeUnit units.
   char    sComment[ABF_TAGCOMMENTLEN];   // Optional tag comment.
   short   nTagType;          // Type of tag ABF_TIMETAG, ABF_COMMENTTAG, ABF_EXTERNALTAG, ABF_VOICETAG, ABF_NEWFILETAG or ABF_ANNOTATIONTAG
   union 
   {
      short   nVoiceTagNumber;   // If nTagType=ABF_VOICETAG, this is the number of this voice tag.
      short   nAnnotationIndex;  // If nTagType=ABF_ANNOTATIONTAG, this is the index of the corresponding annotation.
   };
}; // Size = 64

//
// Definition of the ABFVoiceTagInfo structure.
//
struct ABFVoiceTagInfo
{
   long  lTagNumber;          // The tag number that corresponds to this VoiceTag
   long  lFileOffset;         // Offset to this tag within the VoiceTag block
   long  lUncompressedSize;   // Size of the voice tag expanded.
   long  lCompressedSize;     // Compressed size of the tag.
   short nCompressionType;    // Compression method used.
   short nSampleSize;         // Size of the samples acquired.
   long  lSamplesPerSecond;   // Rate at which the sound was acquired.
   DWORD dwCRC;               // CRC used to check data integrity.
   WORD  wChannels;           // Number of channels in the tag (usually 1).
   WORD  wUnused;             // Unused space.
}; // Size 32

//
// Definition of the ABF Delta structure.
//
struct ABFDelta
{
   long    lDeltaTime;        // Time at which the parameter was changed in fSynchTimeUnit units.
   long    lParameterID;      // Identifier for the parameter changed
   union
   {
      long  lNewParamValue;   // Depending on the value of lParameterID
      float fNewParamValue;   // this entry may be either a float or a long.
   };
}; // Size = 12

//
// Definition of the ABF synch array structure
//
struct ABFSynch
{
   long    lStart;            // Start of the episode/event in fSynchTimeUnit units.
   long    lLength;           // Length of the episode/event in multiplexed samples.

   ABFSynch( long p_lStart, long p_lLength )
   {
      lStart  = p_lStart;
      lLength = p_lLength;
   }

   ABFSynch()
   {
      memset( this, 0, sizeof(ABFSynch) );
   }
}; // Size = 8

#ifndef RC_INVOKED
#pragma pack(pop)                      // return to default packing
#endif

// ============================================================================================
// Function prototypes for functions in ABFHEADR.C
// ============================================================================================

void WINAPI ABFH_Initialize( ABFFileHeader *pFH );

void WINAPI ABFH_InitializeScopeConfig(const ABFFileHeader *pFH, ABFScopeConfig *pCfg);

BOOL WINAPI ABFH_CheckScopeConfig(const ABFFileHeader *pFH, ABFScopeConfig *pCfg);

void WINAPI ABFH_GetADCDisplayRange( const ABFFileHeader *pFH, int nChannel, 
                                     float *pfUUTop, float *pfUUBottom);
                                     
void WINAPI ABFH_GetADCtoUUFactors( const ABFFileHeader *pFH, int nChannel, 
                                    float *pfADCToUUFactor, float *pfADCToUUShift );
void WINAPI ABFH_ClipADCUUValue(const ABFFileHeader *pFH, int nChannel, float *pfUUValue);
                                           
void WINAPI ABFH_GetDACtoUUFactors( const ABFFileHeader *pFH, int nChannel, 
                                    float *pfDACToUUFactor, float *pfDACToUUShift );
void WINAPI ABFH_ClipDACUUValue(const ABFFileHeader *pFH, int nChannel, float *pfUUValue);

BOOL WINAPI ABFH_GetMathValue(const ABFFileHeader *pFH, float fA, float fB, float *pfRval);
int WINAPI ABFH_GetMathChannelName(LPSTR psz, UINT uLen);

BOOL WINAPI ABFH_ParamReader( HANDLE hFile, ABFFileHeader *pFH, int *pnError );
BOOL WINAPI ABFH_ParamWriter( HANDLE hFile, ABFFileHeader *pFH, int *pnError );

BOOL WINAPI ABFH_GetErrorText( int nError, char *pszBuffer, UINT nBufferSize );

BOOL WINAPI ABFH_GetCreatorInfo(const ABFFileHeader *pFH, char *pszName, UINT uNameSize, char *pszVersion, UINT uVersionSize);
BOOL WINAPI ABFH_GetModifierInfo(const ABFFileHeader *pFH, char *pszName, UINT uNameSize, char *pszVersion, UINT uVersionSize);

// ABF 1 conversion functions - use with care.
struct ABFFileHeader1;
BOOL WINAPI ABFH_ConvertFromABF1( const ABFFileHeader1 *pIn, ABFFileHeader *pOut, int *pnError );
BOOL WINAPI ABFH_ConvertABF2ToABF1Header( const ABFFileHeader *pNewFH, ABFFileHeader1 *pOldFH, int *pnError );


// ABFHWAVE.CPP

// Constants for ABFH_GetEpochLimits
#define ABFH_FIRSTHOLDING  -1
#define ABFH_LASTHOLDING   ABF_EPOCHCOUNT

// Return the bounds of a given epoch in a given episode. Values returned are ZERO relative.
BOOL WINAPI ABFH_GetEpochLimits(const ABFFileHeader *pFH, int nADCChannel, UINT uDACChannel, DWORD dwEpisode, 
                                int nEpoch, UINT *puEpochStart, UINT *puEpochEnd,
                                int *pnError);

// Get the offset in the sampling sequence for the given physical channel.
BOOL WINAPI ABFH_GetChannelOffset( const ABFFileHeader *pFH, int nChannel, UINT *puChannelOffset );

// This function forms the de-multiplexed DAC output waveform for the
// particular channel in the pfBuffer, in DAC UserUnits.
BOOL WINAPI ABFH_GetWaveform( const ABFFileHeader *pFH, UINT uDACChannel, DWORD dwEpisode, 
                                float *pfBuffer, int *pnError);

// This function forms the de-multiplexed Digital output waveform for the
// particular channel in the pdwBuffer, as a bit mask. Digital OUT 0 is in bit 0.
BOOL WINAPI ABFH_GetDigitalWaveform( const ABFFileHeader *pFH, int nChannel, DWORD dwEpisode, 
                                     DWORD *pdwBuffer, int *pnError);

// Calculates the timebase array for the file.
void WINAPI ABFH_GetTimebase(const ABFFileHeader *pFH, double dTimeOffset, double *pdBuffer, UINT uBufferSize);

// Constant for ABFH_GetHoldingDuration
#define ABFH_HOLDINGFRACTION 64

// Get the duration of the first holding period.
UINT WINAPI ABFH_GetHoldingDuration(const ABFFileHeader *pFH);

// Checks whether the waveform varies from episode to episode.
BOOL WINAPI ABFH_IsConstantWaveform(const ABFFileHeader *pFH, UINT uDACChannel);

// Get the duration in sequences of the PreSignal.
UINT WINAPI ABFH_GetPreSignalSequences(const ABFFileHeader *pFH);

// Get the duration in sequences of the Main Sweep.
UINT WINAPI ABFH_GetMainSweepSequences(const ABFFileHeader *pFH);

// Get the full sweep length given the length available to epochs or vice-versa.
int WINAPI ABFH_SweepLenFromUserLen(const  ABFFileHeader *pFH, int nUserLength, int nNumChannels);
int WINAPI ABFH_UserLenFromSweepLen(const  ABFFileHeader *pFH, int nSweepLength, int nNumChannels);

// Converts a display range to the equivalent gain and offset factors.
void WINAPI ABFH_GainOffsetToDisplayRange( const ABFFileHeader *pFH, int nChannel, 
                                           float fDisplayGain, float fDisplayOffset,
                                           float *pfUUTop, float *pfUUBottom);

// Converts a display range to the equivalent gain and offset factors.
void WINAPI ABFH_DisplayRangeToGainOffset( const ABFFileHeader *pFH, int nChannel, 
                                           float fUUTop, float fUUBottom,
                                           float *pfDisplayGain, float *pfDisplayOffset);

// Converts a time value to a synch time count or vice-versa.
void WINAPI ABFH_SynchCountToMS(const ABFFileHeader *pFH, UINT uCount, double *pdTimeMS);
UINT WINAPI ABFH_MSToSynchCount(const ABFFileHeader *pFH, double dTimeMS);

// Gets the duration of the Waveform Episode (in us), allowing for split clock etc.
void WINAPI ABFH_GetEpisodeDuration(const ABFFileHeader *pFH, double *pdEpisodeDuration);

// Returns TRUE is P/N is enabled on any output channel.
BOOL WINAPI ABFH_IsPNEnabled(const ABFFileHeader *pFH, UINT uDAC=ABF_ANY_CHANNEL);

// Returns TRUE is ADC channel is corrected during leak subtraction.
BOOL WINAPI ABFH_IsADCLeakSubtracted(const ABFFileHeader *pFH, short nADC);

// Gets the duration of a P/N sequence (in us), including settling times.
void WINAPI ABFH_GetPNDuration(const ABFFileHeader *pFH, double *pdPNDuration);

// Gets the duration of a pre-sweep train in us.
void WINAPI ABFH_GetTrainDuration (const ABFFileHeader *pFH, UINT uDAC, double *pdTrainDuration);

// Gets the duration of an inter sweep adapt interval in us.  //FB 4867
void WINAPI ABFH_GetAdaptDuration(const ABFFileHeader *pFH, double *pdAdaptDuration);

// Gets the duration of a post-train portion of the pre-sweep train in us.
void WINAPI ABFH_GetPostTrainDuration (const ABFFileHeader *pFH, UINT uDAC, UINT uEpisode, double *pdDuration);

// Gets the level of a post-train portion of the pre-sweep train.
void WINAPI ABFH_GetPostTrainLevel (const ABFFileHeader *pFH, UINT uDAC, UINT uEpisode, double *pdLevel);

// Gets the duration of a whole meta-episode (in us).
void WINAPI ABFH_GetMetaEpisodeDuration(const ABFFileHeader *pFH, double *pdMetaEpisodeDuration);

// Gets the start to start period for the episode in us.
void WINAPI ABFH_GetEpisodeStartToStart(const ABFFileHeader *pFH, double *pdEpisodeStartToStart);

// Checks that the user list contains valid entries for the protocol.
BOOL WINAPI ABFH_CheckUserList(const ABFFileHeader *pFH, UINT uListNum, int *pnError);

// Counts the number of changing sweeps.
UINT WINAPI ABFH_GetNumberOfChangingSweeps( const ABFFileHeader *pFH );

// // Checks whether the digital output varies from episode to episode.
BOOL WINAPI ABFH_IsConstantDigitalOutput(const ABFFileHeader *pFH, UINT uDACChannel);

int WINAPI ABFH_GetEpochTableDuration(const ABFFileHeader *pFH, UINT uDACChannel, UINT uEpisode);
int WINAPI ABFH_GetEpochDuration(const ABFFileHeader *pFH, UINT uDACChannel, UINT uEpisode, int nEpoch);

float WINAPI ABFH_GetEpochLevel(const ABFFileHeader *pFH, UINT uDACChannel, UINT uEpisode, int nEpoch);
BOOL WINAPI ABFH_GetEpochLevelRange(const ABFFileHeader *pFH, UINT uDACChannel, int nEpoch, float *pfMin, float *pfMax);
UINT WINAPI ABFH_GetMaxPNSubsweeps(const ABFFileHeader *pFH, UINT uDACChannel);


//
// Error return values that may be returned by the ABFH_xxx functions.
//

#define ABFH_FIRSTERRORNUMBER          2001
#define ABFH_EHEADERREAD               2001
#define ABFH_EHEADERWRITE              2002
#define ABFH_EINVALIDFILE              2003
#define ABFH_EUNKNOWNFILETYPE          2004
#define ABFH_CHANNELNOTSAMPLED         2005
#define ABFH_EPOCHNOTPRESENT           2006
#define ABFH_ENOWAVEFORM               2007
#define ABFH_EDACFILEWAVEFORM          2008
#define ABFH_ENOMEMORY                 2009
#define ABFH_BADSAMPLEINTERVAL         2010
#define ABFH_BADSECONDSAMPLEINTERVAL   2011
#define ABFH_BADSAMPLEINTERVALS        2012
#define ABFH_ENOCONDITTRAINS           2013
#define ABFH_EMETADURATION             2014
#define ABFH_ECONDITNUMPULSES          2015
#define ABFH_ECONDITBASEDUR            2016
#define ABFH_ECONDITBASELEVEL          2017
#define ABFH_ECONDITPOSTTRAINDUR       2018
#define ABFH_ECONDITPOSTTRAINLEVEL     2019
#define ABFH_ESTART2START              2020
#define ABFH_EINACTIVEHOLDING          2021
#define ABFH_EINVALIDCHARS             2022
#define ABFH_ENODIG                    2023
#define ABFH_EDIGHOLDLEVEL             2024
#define ABFH_ENOPNPULSES               2025
#define ABFH_EPNNUMPULSES              2026
#define ABFH_ENOEPOCH                  2027
#define ABFH_EEPOCHLEN                 2028
#define ABFH_EEPOCHINITLEVEL           2029
#define ABFH_EDIGLEVEL                 2030
#define ABFH_ECONDITSTEPDUR            2031
#define ABFH_ECONDITSTEPLEVEL          2032
#define ABFH_EINVALIDBINARYCHARS       2033
#define ABFH_EBADWAVEFORM              2034
#define ABFH_EEPOCHCOMP				   2035 

#ifdef __cplusplus
}
#endif

#endif   /* INC_ABFHEADR2_H */
