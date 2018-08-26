import os
PATH_HERE = os.path.dirname(__file__)
PATH_DATA = os.path.abspath(os.path.dirname(__file__)+"/../../data/abfs/")
import sys
sys.path.insert(0, PATH_HERE+"/../../src/")

import logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

import pyabf
import glob
import autoabf

#pyabf.abf.log.setLevel(logging.DEBUG)


class ABFwatcher:
    def __init__(self, abfFolder=None):
        self._folders = []
        self.addWatchedFolder(abfFolder)

    def addWatchedFolder(self, abfFolder=None):
        if not abfFolder:
            return
        if not os.path.exists(abfFolder):
            log.warn("PATH DOES NOT EXIST: %s" % abfFolder)
            return
        abfFolder = os.path.abspath(abfFolder)
        self._folders.append(abfFolder)
        self._folders = [os.path.abspath(x) for x in self._folders]
        self._folders = sorted(list(set(self._folders)))
        log.info("Added folder to watch list: %s" % abfFolder)

    def rescan(self):
        # clean up known folders
        log.debug(f"Scanning for ABFs in {len(self._folders)} folders")
        for folder in self._folders:
            log.debug("scanning %s" % folder)
            abfFiles = glob.glob(folder+"/*.abf")
            log.debug("found %d abf Files" % len(abfFiles))
            for abfFile in sorted(abfFiles):
                abf = pyabf.ABF(abfFile)
                autoabf.autoAnalyzeAbf(abf)


if __name__=="__main__":
    aq = ABFwatcher()
    #aq.addWatchedFolder(R"X:/some/crazy/path/")
    aq.addWatchedFolder(R"C:\Users\scott\Documents\important\abfs")
    #aq.addWatchedFolder(R"Y:/some/crazy/path/")
    aq.rescan()
    print("DONE")