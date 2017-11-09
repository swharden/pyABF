"""Code to interact with the ABF2 header. https://github.com/swharden/pyABF/"""

import os
import datetime
import struct
import collections

import abfHeaderVars
import abfHeaderTools

class ABFheader:
    def __init__(self,abfFile):
        """
        Given an ABF (ABF2) file, return its header contents in a simple flat dictionary.
        abfFile could be a path (string) or an already-open file buffer (opened in rb mode)
        """
        
        # do what it takes to ensure our abf file is opened as a file buffer
        if type(abfFile) is str:
            self._fb = open(abfFile,'rb')
        elif abfFile.__class__.__name__ == 'BufferedReader':
            self._fb = abfFile
        else:
            raise ValueError('abfFile must be a path (string) or file buffer (opened in rb mode)')
        
        # the header will be a dictionary maintained in order so section groups are easy to determine later
        self.header=collections.OrderedDict()
        
        # read the primary sections directly from the ABF file buffer
        self._fileReadStructMap(abfHeaderVars.HEADER,sectionName="Header")
        self._fileReadStructMap(abfHeaderVars.SECTIONS,76,16,sectionName="Section Map")
        self._fileReadSection('ProtocolSection',abfHeaderVars.PROTO)
        self._fileReadSection('ADCSection',abfHeaderVars.ADC)
        self._fileReadSection('DACSection',abfHeaderVars.DAC)
        self._fileReadSection('EpochPerDACSection',abfHeaderVars.EPPERDAC)
        self._fileReadSection('EpochSection',abfHeaderVars.EPSEC)      
        self._fileReadSection('TagSection',abfHeaderVars.TAGS)      
        
        # for lists with one element, simplify varName=[val] to varName=val
        for key in [key for key in self.header.keys() if len(self.header[key])==1]:
            self.header[key]=self.header[key][0]
        
        # add a few extra things I think are useful    
        self.header["### Extras ###"]=None
        self.header['abfFilePath']=os.path.abspath(self._fb.name)
        self.header['abfFileName']=os.path.basename(self._fb.name)
        self.header['abfID']=os.path.basename(self._fb.name)[:-4]
        dt=datetime.datetime.strptime(str(self.header['uFileStartDate']), "%Y%M%d")
        self.header['abfDatetime']=dt+datetime.timedelta(seconds=self.header['uFileStartTimeMS']/1000)
        self.header['sweepFirstByte']=self.header['DataSection'][0]*512
        self.header['sweepPointCount']=self.header['lNumSamplesPerEpisode']
        self.header['sweepCount']=self.header['lActualEpisodes']
        self.header['signalScale']=self.header['lADCResolution']/1e6
        
        # if we opened the file earlier, be polite and close it as soon as possible
        if type(abfFile) is str:
            self._fb.close()
        
    def _fileReadStructMap(self,structMap,startByte=0,fixedOffset=None,sectionName=None):
        """Given a string of varName_varFormat structs, get the objects from the file."""
        if sectionName:
            self.header["### %s ###"%sectionName]=[None]
        self._fb.seek(startByte)
        for structCode in structMap.replace("\n","").split(","):
            varName,varFormat=structCode.strip().split("_")
            varVal=struct.unpack(varFormat,self._fb.read(struct.calcsize(varFormat)))
            varVal=varVal if len(varVal)>1 else varVal[0]
            self.header.setdefault(varName,[]).append(varVal) # pythonista
            if fixedOffset: 
                self._fb.read(fixedOffset-struct.calcsize(varFormat))

    def _fileReadSection(self,sectionName,structMap):
        """Read a structure map repeatedly according to its name in the section map."""
        self.header["### %s ###"%sectionName]=[None]
        entryStartBlock,entryBytes,entryCount=self.header[sectionName][0]
        for entryNumber in range(entryCount):
            self._fileReadStructMap(structMap,entryStartBlock*512+entryNumber*entryBytes)


if __name__=="__main__":   
    print("DO NOT RUN THIS PROGRAM DIRECTLY!")
    
    # stuff here is for the developer to practice with
    demoHeader=ABFheader(R"../../../../data/17o05028_ic_steps.abf")
    abfHeaderTools.show(demoHeader.header)