"""this script creates a HTML header for every ABF file in the parent folder."""

import sys
sys.path.append("../../src/")
sys.path.insert(0,sys.path.pop())
import pyabf
import glob
import os

if __name__=="__main__":
    out="# Sample ABF Header Data\n"
    out+="This folder contains automatically-generated header summaries of all ABFs in the data folder.\n\n"
    for fname in sorted(glob.glob("../*.abf")):
        print(fname)
        abf=pyabf.ABF(fname)
        abf._abfHeader.saveHTML(abf.ID+".html")
        abf._abfHeader.saveMarkdown(abf.ID+".md")
        out+="* [%s](%s)\n"%(os.path.basename(abf.filename),abf.ID+".md")
    with open('readme.md','w') as f:
        f.write(out)
    print("updated readme.md")