"""Minimal-case demonstration how to read an ABF2 header and data. https://github.com/swharden/pyABF/"""

import struct
import varfmt

class ABFheader:
    def __init__(self,abfFileName):
        """Given an ABF2 file, parse its header and provide simple access to its settings and data."""
        self.abfFileName=abfFileName
        self.header={}
        self._fb = open(abfFileName,'rb')
        self._fileReadStructMap(varfmt.HEADER)
        self._fileReadStructMap(varfmt.SECTIONS,76,16)
        self._fileReadSection('ProtocolSection',varfmt.PROTO)
        self._fileReadSection('ADCSection',varfmt.ADC)
        self._fileReadSection('DACSection',varfmt.DAC)
        self._fileReadSection('EpochPerDACSection',varfmt.EPPERDAC)
        self._fileReadSection('EpochSection',varfmt.EPSEC)      
        self._fileReadSection('TagSection',varfmt.TAGS)        
        self._fb.close()
        for key in [key for key in self.header.keys() if len(self.header[key])==1]:
            self.header[key]=self.header[key][0]
        
    def _fileReadStructMap(self,structMap,startByte=0,fixedOffset=None):
        """Given a string of varName_varFormat structs, read the ABF file and return the objects."""
        self._fb.seek(startByte)
        for structCode in structMap.replace("\n","").split(","):
            varName,varFormat=structCode.strip().split("_")
            varVal=struct.unpack(varFormat,self._fb.read(struct.calcsize(varFormat)))
            varVal=varVal if len(varVal)>1 else varVal[0]
            if not varName in self.header: self.header[varName]=[]
            self.header[varName]=self.header[varName]+[varVal]
            if fixedOffset: self._fb.read(fixedOffset-struct.calcsize(varFormat))

    def _fileReadSection(self,sectionName,structMap):
        """Given a section in the map, read its structure repeatedly and return the result."""
        entryStartBlock,entryBytes,entryCount=self.header[sectionName][0]
        for entryNumber in range(entryCount):
            self._fileReadStructMap(structMap,entryStartBlock*512+entryNumber*entryBytes)
                
    def showHeader(self):
        for key in sorted(self.header.keys()):
            print("%s = %s"%(key,self.header[key]))

if __name__=="__main__":
    abf=ABFheader(R"../../../../data/17o05028_ic_steps.abf")
    abf.showHeader()