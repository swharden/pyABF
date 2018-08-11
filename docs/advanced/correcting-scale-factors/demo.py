"""
Code here identifies ABFs with mismatched ADC/DAC settings.
"""

import os
import sys
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_SRC = os.path.abspath(PATH_HERE+"../../../../src/")
sys.path.insert(0, PATH_SRC)  # useful for imports
import pyabf
import glob
import shutil

class ABFmodify:
    def __init__(self, abfFilePath, backup=True):
        """
        The ABFmodify class is intended to simplify the act of modifyinig
        the contents of ABF files. Typically this means modifying header values.

        If backup is enabled, ABFs will be backed-up before modifying them.
        The backup is the original filename with a .abf.backup extension.
        """
        assert isinstance(abfFilePath,str)
        self.abfFilePath = os.path.abspath(abfFilePath)
        assert os.path.exists(abfFilePath)
        self.backup = backup

    def ensureBackupExists(self):
        return

    def setScaleFactor(self, fInstrumentScaleFactor):
        return

if __name__ == "__main__":
    #abf_file_folder = R"X:\Data\C57\BLA injection microspheres\technique development\abfs"
    abf_file_folder = PATH_HERE+"/demoABFs/"
    abfFiles = glob.glob(abf_file_folder+"/*.abf")

    for abfNumber,fname in enumerate(sorted(abfFiles)):
        print(f"Analyzing ({abfNumber}/{len(abfFiles)}) {os.path.basename(fname)}", end=" ... ")
        abf = pyabf.ABF(fname, preLoadData=False)

        # ensure units arent the same
        if abf.adcUnits[0] == abf.dacUnits[0]:
            print("ERROR!!!",abf.adcUnits[0],abf.dacUnits[0])
            abfMod = ABFmodify(abf.abfFilePath)
        else:
            print("OK")