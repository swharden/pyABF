"""
This file lists the size of every structure in the structures file.

sectionSizes = {'HeaderV1': 1678, 'HeaderV2': 76, 'SectionMap': 216, 
                'ProtocolSection': 208, 'ADCSection': 82, 'DACSection': 132, 
                'EpochPerDACSection': 30, 'EpochSection': 4, 'TagSection': 64, 
                'StringsSection': 0, 'StringsIndexed': 0}

"""
import struct
import os
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_SRC = os.path.abspath(PATH_HERE+"/../../src/")

with open(PATH_SRC+"/pyabf/structures.py") as f:
    lines = f.readlines()

bytePositions = []
className = None
for line in lines:
    line = line.strip()
    if line.startswith("class") and line.endswith(":"):
        className = line.replace("class ", "").replace(":", "").strip()
        continue
    if not className:
        continue
    if className == "StringsSection":
        continue
    if "readStruct(fb" in line:
        if line.count(",")==2:
            bytePos = int(line.split(",")[-1][:-1])
        else:
            bytePos = None
        varName = line.split("=")[0].strip().replace("[i]","").replace("self.","")
        structFormat = line.split(",")[1].strip().replace(")", "")
        structFormat = eval(structFormat)
        byteSize = struct.calcsize(structFormat)
        print(className, varName, byteSize, line.count(","))