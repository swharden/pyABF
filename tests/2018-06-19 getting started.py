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

# now you are free to import additional modules
import glob

if __name__=="__main__":
    for fname in sorted(glob.glob(PATH_DATA+"/*.abf")):
        abf = pyabf.ABF(fname)
        print(abf.abfID, abf.dataChannelCount)
    print("DONE")