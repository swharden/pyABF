import os
import struct
import glob

STRUCTS_HEADER="""fFileSignature_4s,fFileVersionNumber_4b,uFileInfoSize_I,lActualEpisodes_I,
    uFileStartDate_I,uFileStartTimeMS_I,uStopwatchTime_I,nFileType_H,nDataFormat_H,nSimultaneousScan_H,
    nCRCEnable_H,uFileCRC_I,FileGUID_I,unknown1_I,unknown2_I,unknown3_I,uCreatorVersion_I,uCreatorNameIndex_I,
    uModifierVersion_I,uModifierNameIndex_I,uProtocolPathIndex_I"""
STRUCTS_SECTIONS="""ProtocolSection_IIl,ADCSection_IIl,DACSection_IIl,EpochSection_IIl,ADCPerDACSection_IIl,
    EpochPerDACSection_IIl,UserListSection_IIl,StatsRegionSection_IIl,MathSection_IIl,StringsSection_IIl,
    DataSection_IIl,TagSection_IIl,ScopeSection_IIl,DeltaSection_IIl,VoiceTagSection_IIl,
    SynchArraySection_IIl,AnnotationSection_IIl,StatsSection_IIl"""

class ABFheader:
    def __init__(self,abfFileName):
        self.abfFileName=abfFileName
        self.header={}
        self.fb = open(abfFileName,'rb')
        self.header['header']=self.fileReadStructMap(STRUCTS_HEADER) # always byte 0
        self.header['map']=self.fileReadStructMap(STRUCTS_SECTIONS,76,16) # always byte 0
        self.fb.close()
        
    def fileReadStructMap(self,structMap,bytePosition=0,fixedOffset=None):
        values={}
        self.fb.seek(bytePosition)
        for structCode in structMap.replace("\n","").split(","):
            varName,varFormat=structCode.strip().split("_")
            varVal=struct.unpack(varFormat,self.fb.read(struct.calcsize(varFormat)))
            values[varName]=varVal if len(varVal)>1 else varVal[0]
            if fixedOffset:
                self.fb.read(fixedOffset-struct.calcsize(varFormat))
        return values

    def showHeader(self):
        for headerGroup in self.header:
            print("\n### %s ###"%headerGroup.upper())
            for item in self.header[headerGroup]:
                print(item,self.header[headerGroup][item])

if __name__=="__main__":
    for fname in glob.glob('../../../../data/*.abf'):
        print("\n"*5+"#"*80)
        print("loading",fname,"...")
        abf=ABFheader(fname)
        abf.showHeader()

    print("DONE")