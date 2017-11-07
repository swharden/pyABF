"""
This script demonstrates how to use the ABFclass in abfHeader.py
"""
import os
import glob
import abfTools
import abfHeader

if __name__=="__main__":
    abfFileFolder=os.path.abspath(os.path.dirname(__file__)+"/../../data/")
    for abfFileName in sorted(glob.glob(abfFileFolder+"/*.abf")):
        header=abfHeader.ABFheader(abfFileName)
        abfTools.headerToHTML(header)