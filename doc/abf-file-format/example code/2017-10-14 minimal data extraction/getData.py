
import struct
import numpy as np

def getSectionValue(fb,byteOfSectionBlock,sectionOffset=0,fmt="h"):
    """Return an arbitrary value from an arbitrary section in an ABF2 header."""
    fb.seek(byteOfSectionBlock)
    sectionBlock,entryByteSize,entryCount=struct.unpack("IIl",fb.read(struct.calcsize("IIl")))
    fmt=str(entryCount)+fmt
    fb.seek(sectionBlock*512+sectionOffset)
    val=struct.unpack(fmt,fb.read(struct.calcsize(fmt)))
    val=val[0] if len(val)==1 else val
    return val

def getScaledSignalData(abfFileName):
    """Return a numpy array of the scaled signal data for a recording."""
    fb=open(abfFileName,'rb')
    if not fb.read(4)==b'ABF2':
        raise ValueError("only ABF2 files are supported by this example")
    scalingFactor = getSectionValue(fb,76,118,"i") # ProtocolSection [76] (just want lADCResolution [118])
    data = getSectionValue(fb,236) # DataSection [236] (we want all of it)
    fb.close()    
    return np.array(data)*scalingFactor/1e6

dataY = getScaledSignalData("../../../../data/17o05027_ic_ramp.abf")
print(dataY)
    