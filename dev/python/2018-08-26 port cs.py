"""
code here helps port this code to csharp
"""

import os
import sys
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_SRC = os.path.abspath(PATH_HERE+"../../../src/")

types = {
    "s":"string",
    "c":"char",
    "b":"char",
    "B":"uchar",
    "h":"short",
    "H":"ushort",
    "i":"int",
    "I":"uint",
    "l":"long",
    "L":"ulong",
    "f":"float",
    "d":"double"
    }

funcs = {
    "s":"String",
    "c":"Char",
    "b":"SignedChar",
    "B":"UnsignedChar",
    "h":"Short",
    "H":"UnsignedShort",
    "i":"Int",
    "I":"UnsignedInt",
    "l":"Long",
    "L":"UnsignedLong",
    "f":"Float",
    "d":"Double"
    }

def lineParts(line):
    line=line.replace("'",'"').strip()
    if not '"' in line:
        return
    if line.count("=")!=1:
        return
    cTypeCode = line.split('"')[1]
    if cTypeCode == "IIl":
        # skip the second two
        cTypeCode = "I"
        line=line.replace("Section","Section_byteStart")
    varCount=1
    if len(cTypeCode)>1:
        cTypeCode=list(cTypeCode)
        varCount=int("".join(cTypeCode[:-1]))
        cTypeCode=cTypeCode[-1]
    cInit = types[cTypeCode]
    varName = line.split("=")[0].strip().split(" ")[-1].replace("self.",'')
    plural = ""
    if not cTypeCode=="s" and varCount>1:
        plural="s"
    newline=f'{varName} = FileRead{funcs[cTypeCode]}{plural}("{varName}", bytePos, {varCount});'
    if not "[" in varName:
        newline=f"{cInit} {newline}"
    origVars = line.split("(")[1].split(")")[0].split(",")
    if len(origVars)==3:
        newline = newline.replace("bytePos", origVars[-1].strip())
    else:
        newline = newline.replace("bytePos", "-1")
    newline = newline + " //" + line.split('"')[1]
    #print(newline)
    return newline

if __name__=="__main__":
    out=""
    with open(PATH_SRC+"/pyabf/abfHeader.py") as f:
        raw=f.read().split("\n")
    for line in raw:
        line=line.strip()
        if line.startswith("class"):
            line=line.replace("class ","").replace(":","").strip()
            out+="\n//"+line+"\n"
        if not line.startswith("self."):
            continue
        if not "readStruct(" in line:
            continue
        if "#" in line:
            line=line.split("#")[0]
        line = lineParts(line)
        if line:
            out+=line.strip()+";\n"
    with open(PATH_HERE+"/2018-08-26 port cs.cs",'w') as f:
        f.write(out)
    print("DONE")