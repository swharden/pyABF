import os
import glob
import logging

log = logging.getLogger(__name__)
log.debug(f"autoabf imported")
log.setLevel(level=logging.INFO)
# log.setLevel(level=logging.INFO)

import pyabf
pyabf.abf.log.setLevel(level=logging.WARN)
pyabf.abfHeader.log.setLevel(level=logging.WARN)
pyabf.sweep.log.setLevel(level=logging.WARN)


import analysisByProtocol
analysisByProtocol.log.setLevel(level=logging.DEBUG)



def guessProtocol(abf):
    # TODO: guess best analysis to run
    return "unknown"


def autoAnalyzeABF(abf):
    log.info(f"Auto-analyzing {abf.abfID}.abf")
    log.debug(f"protocol: {abf.protocol}")
    functionName = None
    if " " in abf.protocol and len(abf.protocol.split(" ")[0]) == 4:
        functionName = "protocol_"+abf.protocol.split(" ")[0]
        if functionName in dir(analysisByProtocol):
            log.debug(f"ANALYZING VIA: {functionName}()")
        else:
            log.warn(f"NOT FOUND: {functionName}() {abf.protocol}")
            functionName = None
    else:
        log.debug(f"UNKNOWN PROTOCOL: {abf.protocol}.pro")
    if not functionName:
        functionName = guessProtocol(abf)
    log.debug(f"analyzing via: {functionName}()")

    # for testing
    #if not "0501" in abf.protocol:
        #return

    if hasattr(analysisByProtocol, functionName):
        log.debug(f"calling analysisByProtocol.{functionName}()")
        getattr(analysisByProtocol, functionName)(abf)
    else:
        log.warn(f"analysis function not found: {functionName}")
    return


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
                autoAnalyzeABF(abf)
