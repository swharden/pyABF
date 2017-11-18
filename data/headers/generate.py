"""this script creates a HTML header for every ABF file in the parent folder."""

import sys
sys.path.append("../../src/")
sys.path.insert(0,sys.path.pop())
import pyabf
import glob

if __name__=="__main__":
    for fname in glob.glob("../*.abf"):
        print(fname)
        abf=pyabf.ABF(fname)
        abf._abfHeader.saveHTML(abf.ID+".html")
        abf._abfHeader.saveMarkdown(abf.ID+".md")