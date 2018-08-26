import os
PATH_HERE = os.path.dirname(__file__)
PATH_DATA = os.path.abspath(os.path.dirname(__file__)+"/../../data/abfs/")
import sys
sys.path.insert(0, PATH_HERE+"/../../src/")

import glob
import logging

log = logging.getLogger(__name__)
log.debug(f"autoabf imported")
log.setLevel(level=logging.DEBUG)
# log.setLevel(level=logging.INFO)

import pyabf
pyabf.abf.log.setLevel(level=logging.WARN)
pyabf.abfHeader.log.setLevel(level=logging.WARN)
pyabf.sweep.log.setLevel(level=logging.WARN)

import analysisByProtocol
analysisByProtocol.log.setLevel(level=logging.DEBUG)

import abfnav

def autoAnalyzeFolder(abfFolder):
    assert os.path.isdir(abfFolder)
    log.info(f"auto-analyzing folder: {abfFolder}")
    for abfFile in glob.glob(abfFolder+"/*.abf"):
        autoAnalyzeAbf(abfFile)

def autoAnalyzeAbf(abf, reanalyze=True):
    """
    Given an abf filename (or ABF object), produce an analysis graph of its
    data. If the protocol has a known analysis routine, run it. If not, run
    the unknown() analysis routine. In all cases, an input ABF should produce
    at least some type of output graph.
    """

    # error checking
    if isinstance(abf, str):
        abf = pyabf.ABF(abf)
    assert isinstance(abf, pyabf.ABF)
    log.info(f"Auto-analyzing {abf.abfID}.abf")

    # determine if old files exist
    matchingFiles = abfnav.dataFilesForAbf(abf.abfFilePath)
    if reanalyze is False:
        if len(matchingFiles):
            log.debug(f"skipping {abf.abfID} (data files exist)")
            return
    else:
        for fname in matchingFiles:
            log.debug(f"deleting {fname}")
            os.remove(fname)
        
    # if the protocol is in the autoanalysis format determine its function
    functionName = None
    if " " in abf.protocol and len(abf.protocol.split(" ")[0]) == 4:
        functionName = "protocol_"+abf.protocol.split(" ")[0]
        if not functionName in dir(analysisByProtocol):
            functionName = None
        if functionName and not hasattr(analysisByProtocol, functionName):
            functionName = None

    # if a properly formatted protoocl was found, run its analysis
    if functionName:
        log.debug(f"analyzing known protocol via: {functionName}()")
        getattr(analysisByProtocol, functionName)(abf)
    else:
        log.warn(f"{abf.abfID} uses an unknown protocol: {abf.protocol}")
        log.debug("analyzing with unknown()")
        analysisByProtocol.unknown(abf)
    return


if __name__ == "__main__":
    demoAbfFilePath = R"C:\Users\scott\Documents\important\abfs\17713014.abf"
    demoAbfFolder = os.path.dirname(demoAbfFilePath)
    #autoAnalyzeAbf(demoAbfFilePath)
    autoAnalyzeFolder(R"C:\abfs")
    print("DONE")
