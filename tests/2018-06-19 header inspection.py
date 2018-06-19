"""
Example code demonstrating how to interact with pyabf
"""

# import the pyabf module from this development folder
import os
import sys
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_SRC = os.path.abspath(PATH_HERE+"/../src/")
PATH_DATA = os.path.abspath(PATH_HERE+"/../data/")
sys.path.insert(0,PATH_SRC) # for importing
sys.path.append("../src/") # for your IDE
import pyabf
pyabf.info()
import datetime
import numpy as np

# now you are free to import additional modules
import glob

if __name__=="__main__":
    md="# Sample ABFs\n\n"
    md+="This is a small collection of various ABFs I practice developing with. "
    md+="Many of them were emailed to me by contributors. If you have a unique type "
    md+="of ABF file, email it to me and I will include it here. Note that this page "
    md+="is generated automatically.\n\n"

    md+="ABF | channels | sweeps | protocol\n"
    md+="---|---|---|---\n"

    for fname in sorted(glob.glob(PATH_DATA+"/*.abf")):
        abf = pyabf.ABF(fname)
        print(abf.abfID)
        page = abf.getInfoPage()
        headerPath=os.path.abspath(PATH_HERE+"/../data/headers/")
        with open(headerPath+"/%s.md"%(abf.abfID),'w') as f:
            f.write(page.getMarkdown())
        with open(headerPath+"/%s.html"%(abf.abfID),'w') as f:
            f.write(page.getHTML())

        md+="[%s.abf](headers/%s.md)|"%(abf.abfID,abf.abfID)
        md+="%s (%s)|"%(abf.dataChannelCount, ", ".join(abf.adcUnits))
        md+="%s|"%(abf.sweepCount)
        md+="%s\n"%(abf.protocol)

    with open(PATH_HERE+"/../data/readme.md",'w') as f:
        f.write(md)
    print("DONE")