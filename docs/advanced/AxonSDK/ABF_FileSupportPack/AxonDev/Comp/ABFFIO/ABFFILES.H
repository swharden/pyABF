 //***********************************************************************************************
//
//    Copyright (c) 1993-2004 Molecular Devices Corporation.
//    All rights reserved.
//    Permission is granted to freely to use, modify and copy the code in this file.
//
//***********************************************************************************************

#ifndef INC_ABFFILES2_H
#define INC_ABFFILES2_H

#include "ABFFIO.h"

// Include the description of the ABFFileHeader structure
#ifndef RC_INVOKED
#include "abfheadr.h"
#endif

#ifdef __cplusplus
extern "C" {
#endif  /* __cplusplus */

   
// This is ABFFILES.H; a companion file to ABFFILES.C

#define ABF_INVALID_HANDLE    -1

// Error numbers for routines in this module. 
// Only positive numbers are used.

#define ABF_SUCCESS                 0
#define ABF_EUNKNOWNFILETYPE        1001
#define ABF_EBADFILEINDEX           1002
#define ABF_TOOMANYFILESOPEN        1003
#define ABF_EOPENFILE               1004
#define ABF_EBADPARAMETERS          1005
#define ABF_EREADDATA               1006
#define ABF_OUTOFMEMORY             1008
#define ABF_EREADSYNCH              1009
#define ABF_EBADSYNCH               1010
#define ABF_EEPISODERANGE           1011
#define ABF_EINVALIDCHANNEL         1012
#define ABF_EEPISODESIZE            1013
#define ABF_EREADONLYFILE           1014
#define ABF_EDISKFULL               1015
#define ABF_ENOTAGS                 1016
#define ABF_EREADTAG                1017
#define ABF_ENOSYNCHPRESENT         1018
#define ABF_EREADDACEPISODE         1019
#define ABF_ENOWAVEFORM             1020
#define ABF_EBADWAVEFORM            1021
#define ABF_BADMATHCHANNEL          1022
#define ABF_BADTEMPFILE             1023
#define ABF_NODOSFILEHANDLES        1025
#define ABF_ENOSCOPESPRESENT        1026
#define ABF_EREADSCOPECONFIG        1027
#define ABF_EBADCRC                 1028
#define ABF_ENOCOMPRESSION          1029
#define ABF_EREADDELTA              1030
#define ABF_ENODELTAS               1031
#define ABF_EBADDELTAID             1032
#define ABF_EWRITEONLYFILE          1033
#define ABF_ENOSTATISTICSCONFIG     1034
#define ABF_EREADSTATISTICSCONFIG   1035
#define ABF_EWRITERAWDATAFILE       1036
#define ABF_EWRITEMATHCHANNEL       1037
#define ABF_EWRITEANNOTATION        1038
#define ABF_EREADANNOTATION         1039
#define ABF_ENOANNOTATIONS          1040
#define ABF_ECRCVALIDATIONFAILED    1041
#define ABF_EWRITESTRING            1042
#define ABF_ENOSTRINGS              1043
#define ABF_EFILECORRUPT			1044

// Notifications that can be passed to the registered callback function.
#define ABF_NVOICETAGSTART    2000
#define ABF_NWRITEVOICETAG    2001
#define ABF_NVOICETAGEND      2002

// Constants for ABF_MultiplexWrite
#define ABF_APPEND            2     // Episodes may be appended to the current
                                    // episode when writing ABF_VARLNEEVENTS files

// Constant for ABF_FormatTag
#define ABF_MAXTAGFORMATLEN   84

// Start time saved in the synch array for the oscilloscope mode average sweep
#define ABF_AVERAGESWEEPSTART DWORD(-1)

// CRC switch
#define ABF_CRC_DISABLED 0
#define ABF_CRC_ENABLED  1

//---------------------- Exported Function Definitions -------------------------

// Definitions of the functions in ABFFiles.cpp

BOOL ABF_Initialize(HINSTANCE hDLL);
void ABF_Cleanup(void);

BOOL WINAPI ABF_ReadOpen( LPCSTR szFileName, int *phFile, UINT fFlags, ABFFileHeader *pFH, 
                          UINT *puMaxSamples, DWORD *pdwMaxEpi, int *pnError );

BOOL WINAPI ABF_WriteOpen( LPCSTR szFileName, int *phFile, UINT fFlags, ABFFileHeader *pFH, int *pnError );

BOOL WINAPI ABF_UpdateHeader(int nFile, ABFFileHeader *pFH, int *pnError);

BOOL WINAPI ABF_IsABFFile(const char *szFileName, int *pnDataFormat, int *pnError);

BOOL WINAPI ABF_ParamReader( int nFile, ABFFileHeader *pFH, int *pnError);

BOOL WINAPI ABF_ParamWriter(const char *pszFilename, ABFFileHeader *pFH, int *pnError);

BOOL WINAPI ABF_HasData(int nFile, const ABFFileHeader *pFH);

BOOL WINAPI ABF_Close(int nFile, int *pnError);

BOOL WINAPI ABF_MultiplexRead(int nFile, const ABFFileHeader *pFH, DWORD dwEpisode, 
                              void *pvBuffer, UINT *puSizeInSamples, int *pnError);

BOOL WINAPI ABF_MultiplexWrite(int nFile, const ABFFileHeader *pFH, UINT uFlags, const void *pvBuffer, 
                               DWORD dwEpiStart, UINT uSizeInSamples, int *pnError);

BOOL WINAPI ABF_WriteRawData(int nFile, const void *pvBuffer, DWORD dwSizeInBytes, int *pnError);

BOOL WINAPI ABF_ReadChannel(int nFile, const ABFFileHeader *pFH, int nChannel, DWORD dwEpisode, 
                            float *pfBuffer, UINT *puNumSamples, int *pnError);
                                   
BOOL WINAPI ABF_ReadRawChannel(int nFile, const ABFFileHeader *pFH, int nChannel, DWORD dwEpisode, 
                               void *pvBuffer, UINT *puNumSamples, int *pnError);
                                   
BOOL WINAPI ABF_ReadDACFileEpi(int nFile, const ABFFileHeader *pFH, short *pnDACArray,
                               UINT nChannel, DWORD dwEpisode, int *pnError);

BOOL WINAPI ABF_WriteDACFileEpi(int nFile, ABFFileHeader *pFH, UINT uDACChannel, const short *pnDACArray, int *pnError);

BOOL WINAPI ABF_GetWaveform(int nFile, const ABFFileHeader *pFH, UINT uDACChannel, DWORD dwEpisode, 
                              float *pfBuffer, int *pnError);
                            
BOOL WINAPI ABF_WriteTag(int nFile, ABFFileHeader *pFH, const ABFTag *pTag, int *pnError);

BOOL WINAPI ABF_UpdateTag(int nFile, UINT uTag, const ABFTag *pTag, int *pnError);

BOOL WINAPI ABF_ReadTags(int nFile, const ABFFileHeader *pFH, DWORD dwFirstTag, ABFTag *pTagArray, 
                         UINT uNumTags, int *pnError);

BOOL WINAPI ABF_FormatTag(int nFile, const ABFFileHeader *pFH, long lTagNumber, 
                          char *pszBuffer, UINT uSize, int *pnError);

BOOL WINAPI ABF_EpisodeFromSynchCount(int nFile, const ABFFileHeader *pFH, DWORD *pdwSynchCount, 
                                      DWORD *pdwEpisode, int *pnError);

BOOL WINAPI ABF_SynchCountFromEpisode(int nFile, const ABFFileHeader *pFH, DWORD dwEpisode, 
                                      DWORD *pdwSynchCount, int *pnError);

BOOL WINAPI ABF_GetEpisodeFileOffset(int nFile, const ABFFileHeader *pFH, DWORD dwEpisode, 
                                     DWORD *pdwFileOffset, int *pnError);

BOOL WINAPI ABF_GetMissingSynchCount(int nFile, const ABFFileHeader *pFH, DWORD dwEpisode, 
                                     DWORD *pdwMissingSynchCount, int *pnError);

BOOL WINAPI ABF_HasOverlappedData(int nFile, BOOL *pbHasOverlapped, int *pnError);

BOOL WINAPI ABF_GetNumSamples(int nFile, const ABFFileHeader *pFH, DWORD dwEpisode, 
                              UINT *puNumSamples, int *pnError);

BOOL WINAPI ABF_GetStartTime(int nFile, const ABFFileHeader *pFH, int nChannel, DWORD dwEpisode, 
                             double *pdStartTime, int *pnError);

BOOL WINAPI ABF_GetEpisodeDuration(int nFile, const ABFFileHeader *pFH, DWORD dwEpisode, 
                                   double *pdDuration, int *pnError);

BOOL WINAPI ABF_GetTrialDuration(int nFile, const ABFFileHeader *pFH, 
                                   double *pdDuration, int *pnError);

BOOL WINAPI ABF_WriteScopeConfig( int nFile, ABFFileHeader *pFH, int nScopes, 
                                  /*const*/ ABFScopeConfig *pCfg, int *pnError);
                                        
BOOL WINAPI ABF_ReadScopeConfig( int nFile, ABFFileHeader *pFH, ABFScopeConfig *pCfg, 
                                 UINT uMaxScopes, int *pnError);

BOOL WINAPI ABF_WriteStatisticsConfig( int nFile, ABFFileHeader *pFH, 
                                       const ABFScopeConfig *pCfg, int *pnError);
                                        
BOOL WINAPI ABF_ReadStatisticsConfig( int nFile, const ABFFileHeader *pFH, ABFScopeConfig *pCfg, int *pnError);

BOOL WINAPI ABF_SaveVoiceTag( int nFile, LPCSTR pszFileName, long lDataOffset,
                              ABFVoiceTagInfo *pVTI, int *pnError);
                              
BOOL WINAPI ABF_GetVoiceTag( int nFile, const ABFFileHeader *pFH, UINT uTag, LPCSTR pszFileName, 
                             long lDataOffset, ABFVoiceTagInfo *pVTI, int *pnError);
                              
BOOL WINAPI ABF_PlayVoiceTag( int nFile, const ABFFileHeader *pFH, UINT uTag, int *pnError);

BOOL WINAPI ABF_WriteDelta(int nFile, ABFFileHeader *pFH, const ABFDelta *pDelta, int *pnError);
BOOL WINAPI ABF_ReadDeltas(int nFile, const ABFFileHeader *pFH, DWORD dwFirstDelta, 
                           ABFDelta *pDeltaArray, UINT uNumDeltas, int *pnError);
BOOL WINAPI ABF_FormatDelta(const ABFFileHeader *pFH, const ABFDelta *pDelta, 
                            char *pszText, UINT uTextLen, int *pnError);

BOOL WINAPI ABF_GetFileHandle(int nFile, HANDLE *phHandle, int *pnError);

BOOL WINAPI ABF_GetFileName( int nFile, LPSTR pszFilename, UINT uTextLen, int *pnError );

BOOL WINAPI ABF_BuildErrorText(int nErrorNum, const char *szFileName, char *sTxtBuf, UINT uMaxLen);

typedef BOOL (CALLBACK *ABFCallback)(void *pvThisPointer, int nError);
BOOL WINAPI ABF_SetErrorCallback(int nFile, ABFCallback fnCallback, void *pvThisPointer, int *pnError);

// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

BOOL WINAPI ABF_AppendOpen(LPCSTR szFileName, int *phFile, ABFFileHeader *pFH, 
                           UINT *puMaxSamples, DWORD *pdwMaxEpi, int *pnError);

BOOL WINAPI ABF_UpdateEpisodeSamples(int nFile, const ABFFileHeader *pFH, int nChannel, UINT uEpisode, 
                                     UINT uStartSample, UINT uNumSamples, float *pfBuffer, int *pnError);

BOOL WINAPI ABF_SetChunkSize( int hFile, ABFFileHeader *pFH, UINT *puMaxSamples, DWORD *pdwMaxEpi, int *pnError );

BOOL WINAPI ABF_SetOverlap(int nFile, const ABFFileHeader *pFH, BOOL bAllowOverlap, int *pnError);

BOOL WINAPI ABF_SetEpisodeStart(int nFile, UINT uEpisode, UINT uEpiStart, int *pnError);

// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                                       
void *WINAPI ABF_GetSynchArray(int nFile, int *pnError);

BOOL WINAPI ABF_WriteAnnotation( int nFile, ABFFileHeader *pFH, LPCSTR pszText, int *pnError );
BOOL WINAPI ABF_ReadAnnotation( int nFile, const ABFFileHeader *pFH, DWORD dwIndex, 
                                LPSTR pszText, DWORD dwBufSize, int *pnError );
DWORD WINAPI ABF_GetMaxAnnotationSize( int nFile, const ABFFileHeader *pFH );

BOOL WINAPI ABF_WriteStringAnnotation( int nFile, ABFFileHeader *pFH, LPCSTR pszName, LPCSTR pszData, int *pnError );
BOOL WINAPI ABF_WriteIntegerAnnotation( int nFile, ABFFileHeader *pFH, LPCSTR pszName, int nData, int *pnError );

BOOL WINAPI ABF_ReadStringAnnotation( int nFile, const ABFFileHeader *pFH, DWORD dwIndex, 
                                     LPSTR pszName, UINT uSizeName, LPSTR pszValue, UINT uSizeValue, 
                                     int *pnError );
BOOL WINAPI ABF_ReadIntegerAnnotation( int nFile, const ABFFileHeader *pFH, DWORD dwIndex, 
                                       LPSTR pszName, UINT uSizeName, int *pnValue, int *pnError );

BOOL WINAPI ABF_ParseStringAnnotation( LPCSTR pszAnn, LPSTR pszName, UINT uSizeName, 
                                       LPSTR pszValue, UINT uSizeValue, int *pnError);

BOOL WINAPI ABF_CalculateCRC(int nFile, int *pnError);

UINT WINAPI ABF_GetActualEpisodes(int nFile);

UINT WINAPI ABF_GetActualSamples(int nFile);


#ifdef __cplusplus
}
#endif

#endif   // INC_ABFFILES2_H

