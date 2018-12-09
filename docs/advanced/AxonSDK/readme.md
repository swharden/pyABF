
# Axon SDK Notes

Axon pCLAMP ABF File Support Pack Download Page:
[Download the Support files for Axon pClamp](http://mdc.custhelp.com/app/answers/detail/a_id/18881/~/axon%E2%84%A2-pclamp%C2%AE-abf-file-support-pack-download-page).
_This link is now broken, and the SDK is distributed as a ZIP with pCLAMP 11_.

_This page was generated automatically by [convert.py](convert.py)_

## ABFFILES.H


 * BOOL **ABF_BuildErrorText**(int nErrorNum, const char *szFileName, char *sTxtBuf, UINT uMaxLen)
 * BOOL **ABF_CalculateCRC**(int nFile, int *pnError)
 * BOOL **ABF_Close**(int nFile, int *pnError)
 * BOOL **ABF_EpisodeFromSynchCount**(int nFile, const ABFFileHeader *pFH, DWORD *pdwSynchCount,                                        DWORD *pdwEpisode, int *pnError)
 * BOOL **ABF_FormatDelta**(const ABFFileHeader *pFH, const ABFDelta *pDelta,                              char *pszText, UINT uTextLen, int *pnError)
 * BOOL **ABF_FormatTag**(int nFile, const ABFFileHeader *pFH, long lTagNumber,                            char *pszBuffer, UINT uSize, int *pnError)
 * BOOL **ABF_GetEpisodeDuration**(int nFile, const ABFFileHeader *pFH, DWORD dwEpisode,                                     double *pdDuration, int *pnError)
 * BOOL **ABF_GetEpisodeFileOffset**(int nFile, const ABFFileHeader *pFH, DWORD dwEpisode,                                       DWORD *pdwFileOffset, int *pnError)
 * BOOL **ABF_GetFileHandle**(int nFile, HANDLE *phHandle, int *pnError)
 * BOOL **ABF_GetFileName**( int nFile, LPSTR pszFilename, UINT uTextLen, int *pnError )
 * BOOL **ABF_GetMissingSynchCount**(int nFile, const ABFFileHeader *pFH, DWORD dwEpisode,                                       DWORD *pdwMissingSynchCount, int *pnError)
 * BOOL **ABF_GetNumSamples**(int nFile, const ABFFileHeader *pFH, DWORD dwEpisode,                                UINT *puNumSamples, int *pnError)
 * BOOL **ABF_GetStartTime**(int nFile, const ABFFileHeader *pFH, int nChannel, DWORD dwEpisode,                               double *pdStartTime, int *pnError)
 * BOOL **ABF_GetTrialDuration**(int nFile, const ABFFileHeader *pFH,                                     double *pdDuration, int *pnError)
 * BOOL **ABF_GetVoiceTag**( int nFile, const ABFFileHeader *pFH, UINT uTag, LPCSTR pszFileName,                               long lDataOffset, ABFVoiceTagInfo *pVTI, int *pnError)
 * BOOL **ABF_GetWaveform**(int nFile, const ABFFileHeader *pFH, UINT uDACChannel, DWORD dwEpisode,                                float *pfBuffer, int *pnError)
 * BOOL **ABF_HasData**(int nFile, const ABFFileHeader *pFH)
 * BOOL **ABF_HasOverlappedData**(int nFile, BOOL *pbHasOverlapped, int *pnError)
 * BOOL **ABF_IsABFFile**(const char *szFileName, int *pnDataFormat, int *pnError)
 * BOOL **ABF_MultiplexRead**(int nFile, const ABFFileHeader *pFH, DWORD dwEpisode,                                void *pvBuffer, UINT *puSizeInSamples, int *pnError)
 * BOOL **ABF_MultiplexWrite**(int nFile, const ABFFileHeader *pFH, UINT uFlags, const void *pvBuffer,                                 DWORD dwEpiStart, UINT uSizeInSamples, int *pnError)
 * BOOL **ABF_ParamReader**( int nFile, ABFFileHeader *pFH, int *pnError)
 * BOOL **ABF_ParamWriter**(const char *pszFilename, ABFFileHeader *pFH, int *pnError)
 * BOOL **ABF_ParseStringAnnotation**( LPCSTR pszAnn, LPSTR pszName, UINT uSizeName,                                         LPSTR pszValue, UINT uSizeValue, int *pnError)
 * BOOL **ABF_PlayVoiceTag**( int nFile, const ABFFileHeader *pFH, UINT uTag, int *pnError)
 * BOOL **ABF_ReadAnnotation**( int nFile, const ABFFileHeader *pFH, DWORD dwIndex,                                  LPSTR pszText, DWORD dwBufSize, int *pnError )
 * BOOL **ABF_ReadChannel**(int nFile, const ABFFileHeader *pFH, int nChannel, DWORD dwEpisode,                              float *pfBuffer, UINT *puNumSamples, int *pnError)
 * BOOL **ABF_ReadDACFileEpi**(int nFile, const ABFFileHeader *pFH, short *pnDACArray,                                UINT nChannel, DWORD dwEpisode, int *pnError)
 * BOOL **ABF_ReadDeltas**(int nFile, const ABFFileHeader *pFH, DWORD dwFirstDelta,                             ABFDelta *pDeltaArray, UINT uNumDeltas, int *pnError)
 * BOOL **ABF_ReadIntegerAnnotation**( int nFile, const ABFFileHeader *pFH, DWORD dwIndex,                                         LPSTR pszName, UINT uSizeName, int *pnValue, int *pnError )
 * BOOL **ABF_ReadOpen**( LPCSTR szFileName, int *phFile, UINT fFlags, ABFFileHeader *pFH,                            UINT *puMaxSamples, DWORD *pdwMaxEpi, int *pnError )
 * BOOL **ABF_ReadRawChannel**(int nFile, const ABFFileHeader *pFH, int nChannel, DWORD dwEpisode,                                 void *pvBuffer, UINT *puNumSamples, int *pnError)
 * BOOL **ABF_ReadScopeConfig**( int nFile, ABFFileHeader *pFH, ABFScopeConfig *pCfg,                                   UINT uMaxScopes, int *pnError)
 * BOOL **ABF_ReadStatisticsConfig**( int nFile, const ABFFileHeader *pFH, ABFScopeConfig *pCfg, int *pnError)
 * BOOL **ABF_ReadStringAnnotation**( int nFile, const ABFFileHeader *pFH, DWORD dwIndex,                                       LPSTR pszName, UINT uSizeName, LPSTR pszValue, UINT uSizeValue,                                       int *pnError )
 * BOOL **ABF_ReadTags**(int nFile, const ABFFileHeader *pFH, DWORD dwFirstTag, ABFTag *pTagArray,                           UINT uNumTags, int *pnError)
 * BOOL **ABF_SaveVoiceTag**( int nFile, LPCSTR pszFileName, long lDataOffset,                               ABFVoiceTagInfo *pVTI, int *pnError)
 * BOOL **ABF_SetChunkSize**( int hFile, ABFFileHeader *pFH, UINT *puMaxSamples, DWORD *pdwMaxEpi, int *pnError )
 * BOOL **ABF_SetEpisodeStart**(int nFile, UINT uEpisode, UINT uEpiStart, int *pnError)
 * BOOL **ABF_SetErrorCallback**(int nFile, ABFCallback fnCallback, void *pvThisPointer, int *pnError)
 * BOOL **ABF_SetOverlap**(int nFile, const ABFFileHeader *pFH, BOOL bAllowOverlap, int *pnError)
 * BOOL **ABF_SynchCountFromEpisode**(int nFile, const ABFFileHeader *pFH, DWORD dwEpisode,                                        DWORD *pdwSynchCount, int *pnError)
 * BOOL **ABF_UpdateEpisodeSamples**(int nFile, const ABFFileHeader *pFH, int nChannel, UINT uEpisode,                                       UINT uStartSample, UINT uNumSamples, float *pfBuffer, int *pnError)
 * BOOL **ABF_UpdateHeader**(int nFile, ABFFileHeader *pFH, int *pnError)
 * BOOL **ABF_UpdateTag**(int nFile, UINT uTag, const ABFTag *pTag, int *pnError)
 * BOOL **ABF_WriteAnnotation**( int nFile, ABFFileHeader *pFH, LPCSTR pszText, int *pnError )
 * BOOL **ABF_WriteDACFileEpi**(int nFile, ABFFileHeader *pFH, UINT uDACChannel, const short *pnDACArray, int *pnError)
 * BOOL **ABF_WriteDelta**(int nFile, ABFFileHeader *pFH, const ABFDelta *pDelta, int *pnError)
 * BOOL **ABF_WriteIntegerAnnotation**( int nFile, ABFFileHeader *pFH, LPCSTR pszName, int nData, int *pnError )
 * BOOL **ABF_WriteOpen**( LPCSTR szFileName, int *phFile, UINT fFlags, ABFFileHeader *pFH, int *pnError )
 * BOOL **ABF_WriteRawData**(int nFile, const void *pvBuffer, DWORD dwSizeInBytes, int *pnError)
 * BOOL **ABF_WriteScopeConfig**( int nFile, ABFFileHeader *pFH, int nScopes,                                    /*const*/ ABFScopeConfig *pCfg, int *pnError)
 * BOOL **ABF_WriteStatisticsConfig**( int nFile, ABFFileHeader *pFH,                                         const ABFScopeConfig *pCfg, int *pnError)
 * BOOL **ABF_WriteStringAnnotation**( int nFile, ABFFileHeader *pFH, LPCSTR pszName, LPCSTR pszData, int *pnError )
 * BOOL **ABF_WriteTag**(int nFile, ABFFileHeader *pFH, const ABFTag *pTag, int *pnError)
 * DWORD **ABF_GetMaxAnnotationSize**( int nFile, const ABFFileHeader *pFH )
 * UINT **ABF_GetActualEpisodes**(int nFile)
 * UINT **ABF_GetActualSamples**(int nFile)
 * void **ABF_Cleanup**(void)
## ABFFIO.DLL

Function Name | Relative Address | Ordinal
--------------|------------------|--------
ABF_BuildErrorText|0x00008430|0x00008430
ABF_CalculateCRC|0x00009220|0x00009220
ABF_Close|0x00004300|0x00004300
ABF_EpisodeFromSynchCount|0x00007300|0x00007300
ABF_FormatDelta|0x00006ff0|0x00006ff0
ABF_FormatTag|0x00006bb0|0x00006bb0
ABF_GetActualEpisodes|0x00007860|0x00007860
ABF_GetActualSamples|0x000078a0|0x000078a0
ABF_GetEpisodeDuration|0x000078e0|0x000078e0
ABF_GetEpisodeFileOffset|0x00007530|0x00007530
ABF_GetFileHandle|0x00008570|0x00008570
ABF_GetFileName|0x000091d0|0x000091d0
ABF_GetMaxAnnotationSize|0x00009140|0x00009140
ABF_GetMissingSynchCount|0x00007600|0x00007600
ABF_GetNumSamples|0x00007750|0x00007750
ABF_GetStartTime|0x00007a10|0x00007a10
ABF_GetSynchArray|0x000085b0|0x000085b0
ABF_GetTrialDuration|0x00007970|0x00007970
ABF_GetVoiceTag|0x000083a0|0x000083a0
ABF_GetWaveform|0x000065e0|0x000065e0
ABF_HasData|0x00003c50|0x00003c50
ABF_HasOverlappedData|0x000076f0|0x000076f0
ABF_IsABFFile|0x000038b0|0x000038b0
ABF_MultiplexRead|0x00005440|0x00005440
ABF_MultiplexWrite|0x00005790|0x00005790
ABF_ParamReader|0x00003630|0x00003630
ABF_ParamWriter|0x00003760|0x00003760
ABF_ParseStringAnnotation|0x00008de0|0x00008de0
ABF_PlayVoiceTag|0x00017d60|0x00017d60
ABF_ReadAnnotation|0x00008d20|0x00008d20
ABF_ReadChannel|0x00005be0|0x00005be0
ABF_ReadDACFileEpi|0x00006410|0x00006410
ABF_ReadDeltas|0x00006eb0|0x00006eb0
ABF_ReadIntegerAnnotation|0x00008f80|0x00008f80
ABF_ReadOpen|0x00003090|0x00003090
ABF_ReadRawChannel|0x00006250|0x00006250
ABF_ReadScopeConfig|0x00007e80|0x00007e80
ABF_ReadStatisticsConfig|0x00008250|0x00008250
ABF_ReadStringAnnotation|0x00008ea0|0x00008ea0
ABF_ReadTags|0x000068f0|0x000068f0
ABF_SaveVoiceTag|0x00008330|0x00008330
ABF_SetChunkSize|0x000089c0|0x000089c0
ABF_SetEpisodeStart|0x00005af0|0x00005af0
ABF_SetErrorCallback|0x00008530|0x00008530
ABF_SetOverlap|0x00008a10|0x00008a10
ABF_SynchCountFromEpisode|0x00007440|0x00007440
ABF_UpdateEpisodeSamples|0x000085f0|0x000085f0
ABF_UpdateHeader|0x00003cf0|0x00003cf0
ABF_UpdateTag|0x00006870|0x00006870
ABF_WriteAnnotation|0x00008a60|0x00008a60
ABF_WriteDACFileEpi|0x00006520|0x00006520
ABF_WriteDelta|0x00006e20|0x00006e20
ABF_WriteIntegerAnnotation|0x00008c00|0x00008c00
ABF_WriteOpen|0x000039c0|0x000039c0
ABF_WriteRawData|0x00005b80|0x00005b80
ABF_WriteScopeConfig|0x00007af0|0x00007af0
ABF_WriteStatisticsConfig|0x000080c0|0x000080c0
ABF_WriteStringAnnotation|0x00008af0|0x00008af0
ABF_WriteTag|0x000067e0|0x000067e0
ABFH_CheckScopeConfig|0x0000a5a0|0x0000a5a0
ABFH_CheckUserList|0x0000f820|0x0000f820
ABFH_ClipADCUUValue|0x0000ad20|0x0000ad20
ABFH_ClipDACUUValue|0x0000ae50|0x0000ae50
ABFH_ConvertABF2ToABF1Header|0x0000b150|0x0000b150
ABFH_ConvertFromABF1|0x0000c570|0x0000c570
ABFH_DisplayRangeToGainOffset|0x0000acc0|0x0000acc0
ABFH_GainOffsetToDisplayRange|0x0000abb0|0x0000abb0
ABFH_GetAdaptDuration|0x0000d210|0x0000d210
ABFH_GetADCDisplayRange|0x0000ab70|0x0000ab70
ABFH_GetADCtoUUFactors|0x0000aa80|0x0000aa80
ABFH_GetChannelOffset|0x0000c960|0x0000c960
ABFH_GetCreatorInfo|0x0000c7e0|0x0000c7e0
ABFH_GetDACtoUUFactors|0x0000add0|0x0000add0
ABFH_GetDigitalWaveform|0x0000e230|0x0000e230
ABFH_GetEpisodeDuration|0x0000f000|0x0000f000
ABFH_GetEpisodeStartToStart|0x0000f330|0x0000f330
ABFH_GetEpochDuration|0x0000ca60|0x0000ca60
ABFH_GetEpochLevel|0x0000cc20|0x0000cc20
ABFH_GetEpochLevelRange|0x0000cd60|0x0000cd60
ABFH_GetEpochLimits|0x0000d6d0|0x0000d6d0
ABFH_GetErrorText|0x0000c670|0x0000c670
ABFH_GetHoldingDuration|0x0000d520|0x0000d520
ABFH_GetMathChannelName|0x0000b110|0x0000b110
ABFH_GetMathValue|0x0000af00|0x0000af00
ABFH_GetMaxPNSubsweeps|0x0000d050|0x0000d050
ABFH_GetMetaEpisodeDuration|0x0000f270|0x0000f270
ABFH_GetModifierInfo|0x0000c8e0|0x0000c8e0
ABFH_GetNumberOfChangingSweeps|0x0000ea70|0x0000ea70
ABFH_GetPNDuration|0x0000f120|0x0000f120
ABFH_GetPostTrainDuration|0x0000d2c0|0x0000d2c0
ABFH_GetPostTrainLevel|0x0000d1a0|0x0000d1a0
ABFH_GetTimebase|0x0000e9f0|0x0000e9f0
ABFH_GetTrainDuration|0x0000f1e0|0x0000f1e0
ABFH_GetWaveform|0x0000d930|0x0000d930
ABFH_Initialize|0x00009970|0x00009970
ABFH_InitializeScopeConfig|0x0000a140|0x0000a140
ABFH_IsADCLeakSubtracted|0x0000f0c0|0x0000f0c0
ABFH_IsConstantDigitalOutput|0x0000eee0|0x0000eee0
ABFH_IsConstantWaveform|0x0000ec00|0x0000ec00
ABFH_IsPNEnabled|0x0000f050|0x0000f050
ABFH_MSToSynchCount|0x0000c7b0|0x0000c7b0
ABFH_ParamReader|0x0000c560|0x0000c560
ABFH_ParamWriter|0x0000c590|0x0000c590
ABFH_SweepLenFromUserLen|0x0000d620|0x0000d620
ABFH_SynchCountToMS|0x0000c720|0x0000c720
ABFH_UserLenFromSweepLen|0x0000d660|0x0000d660
ABFU_FixSignalName|0x00017cc0|0x00017cc0
ABFU_FormatDouble|0x00017a10|0x00017a10
ABFU_FormatHMS|0x00017a40|0x00017a40
ABFU_GetABFString|0x00017b00|0x00017b00
ABFU_GetValidSignalNameChars|0x00017c30|0x00017c30
ABFU_IsValidSignalName|0x00017c40|0x00017c40
ABFU_SetABFString|0x00017ab0|0x00017ab0
INFO_FormatDate|0x00010300|0x00010300
INFO_FormatTime|0x00010240|0x00010240
INFO_GetBufferSize|0x000177d0|0x000177d0
INFO_GetInfo|0x00010550|0x00010550
