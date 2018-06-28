# import the pyabf module from this development folder
import os
import sys
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_SRC = os.path.abspath(PATH_HERE+"/../src/")
PATH_DATA = os.path.abspath(PATH_HERE+"/../data/abfs/")
sys.path.insert(0, PATH_SRC)  # for importing
sys.path.append("../src/")  # for your IDE
import pyabf
import glob

BLOCKSIZE=512

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import matplotlib.pyplot as plt

sectionSizes = {'HeaderV1': 1678, 'HeaderV2': 76, 'SectionMap': 216,
                'ProtocolSection': 208, 'ADCSection': 82, 'DACSection': 132,
                'EpochPerDACSection': 30, 'EpochSection': 4, 'TagSection': 64,
                'StringsSection': 0, 'StringsIndexed': 0}

def sectionBytes(section):
    """return [firstByte, byteCount]"""
    assert len(section)==3
    firstByte = section[0]*BLOCKSIZE
    byteCount = section[1]*section[2]
    return [firstByte, byteCount]

if __name__ == "__main__":
    for fname in glob.glob(PATH_DATA+"/*.abf")[4:5]:
        fileParts = {}
        fileParts["file"] = [0, os.path.getsize(fname)-1]
        abf = pyabf.ABF(fname)
        if abf.abfFileFormat == 1:
            fileParts["ABFheaderV1"] = [0, 4898+684]  # start byte and size
            fileParts["DataSection"] = [abf._headerV1.lDataSectionPtr*BLOCKSIZE]
        else:
            fileParts["ABFheaderV2"] = [0, 75]
            fileParts["SectionMap"] = [76, 348+16]
            fileParts["ProtocolSection"] = sectionBytes(abf._sectionMap.ProtocolSection)
            fileParts["ADCSection"] = sectionBytes(abf._sectionMap.ADCSection)
            fileParts["DACSection"] = sectionBytes(abf._sectionMap.DACSection)
            fileParts["EpochPerDACSection"] = sectionBytes(abf._sectionMap.EpochPerDACSection)
            fileParts["EpochSection"] = sectionBytes(abf._sectionMap.EpochSection)
            fileParts["TagSection"] = sectionBytes(abf._sectionMap.TagSection)
            fileParts["StringsSection"] = sectionBytes(abf._sectionMap.StringsSection)
            fileParts["DataSection"] = sectionBytes(abf._sectionMap.DataSection)
        
        plt.figure(figsize=(12,6))
        for i,part in enumerate(fileParts.keys()):
            firstByte, byteCount = fileParts[part]
            lastByte = firstByte + byteCount
            print(part, firstByte,lastByte)
            if part=="file":
                plt.plot([firstByte,lastByte],[1,1],'k-',label=part, lw=3)
            else:
                ls = "-"
                color = plt.get_cmap("jet")(i/len(fileParts))
                plt.axvspan(firstByte, lastByte, alpha=.2, label=part, color=color, lw=0)
            
        
        print()
        plt.legend(loc='upper right', fontsize=8)
        plt.show()
        plt.close()
            
    print("DONE")
