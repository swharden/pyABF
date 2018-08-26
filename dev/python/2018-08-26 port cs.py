"""
code here helps port this code to csharp
"""

import os
import sys
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_SRC = os.path.abspath(PATH_HERE+"../../../src/")

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
        line=line.replace("'",'"')
        if '"f"' in line:
            line=line.replace("self.","float ")
        if 'f"' in line:
            line=line.replace("self.","float[] ")
        elif '"h"' in line:
            line=line.replace("self.","short ")
        elif 'h"' in line:
            line=line.replace("self.","short[] ")
        elif '"H"' in line:
            line=line.replace("self.","unsigned short ")
        elif '"i"' in line:
            line=line.replace("self.","int ")
        elif 'i"' in line:
            line=line.replace("self.","int[] ")
        elif '"I"' in line:
            line=line.replace("self.","unsigned int ")
        elif '"b"' in line:
            line=line.replace("self.","signed char ")
        elif 'b"' in line:
            line=line.replace("self.","signed char[] ")
        elif '"c"' in line:
            line=line.replace("self.","char ")
        elif 'c"' in line:
            line=line.replace("self.","char[] ")
        elif 's"' in line:
            line=line.replace("self.","string[] ")
        elif '"IIl"' in line:
            line=line.replace("self.","Object[] ")
        elif 'B"' in line:
            line=line.replace("self.","unsigned char[] ")
        else:
            line=line.replace("self.","var ")
        out+=line.strip()+";\n"
    with open(PATH_HERE+"/2018-08-26 port cs.cs",'w') as f:
        f.write(out)
    print("DONE")