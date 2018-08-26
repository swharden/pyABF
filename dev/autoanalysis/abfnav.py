"""
Code here relates to directory navigation, abf parent/child grouping, and
abf/data file grouping.

ABF PARENT/CHILD RULES:
    * A parent ABF is the first ABF recorded for a cell
    * Each parent ABF parent has children (all subsequent ABFs for that cell)
    * The first child of every ABF parent is itself.
    * ABF parents are ABFs which exist in the same folder as another file with
      the same filename but a different extension.
      * Usually the matching file is a TIF (dic image of the patched cell)
      * Basenames can be exact: 17713014.abf and d17713014.tif
      * but they don't have to: 17713014.abf and d17713014_cell6.tif
    * Once a parent is defined, all subsequent files (alphabetical) are children
      until a new parent is defined or the end of the file list is reached.
    * ABFs listed before a parent is defined are assigned the parent "orphan".
"""

import os
import glob
import logging
log = logging.getLogger(__name__)
log.setLevel(level=logging.INFO)

DATAFOLDER = "swhlab"

def dataFolderCreate(abfFolder):
    """Given an ABF folder (or abf file), make the data folder if needed."""
    if abfFolder.endswith(".abf"):
        abfFolder = os.path.dirname(abfFolder)
    dirData = os.path.join(abfFolder, DATAFOLDER)
    if not os.path.exists(dirData):
        log.info(f"Creating {dirData}")
        os.mkdir(dirData)
    return

def dataFilesForAbf(abfFileName):
    """Given an ABF file, return the list of data file paths."""
    dirABF = os.path.dirname(abfFileName)
    abfID = os.path.basename(abfFileName).replace(".abf","")
    dirData = os.path.join(dirABF, DATAFOLDER)
    files = glob.glob(f"{dirABF}/{DATAFOLDER}/{abfID}*.*")
    return sorted(files)

if __name__=="__main__":
    demoAbfFilePath=R"C:\Users\scott\Documents\important\abfs\17713014.abf"
    dataFolderCreate(demoAbfFilePath)
    print(dataFilesForAbf(demoAbfFilePath))
