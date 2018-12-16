R"""
Code here ensures that core API changes don't modify any header values.
"""

import os
import sys
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_PROJECT = os.path.abspath(PATH_HERE+"/../../")
PATH_DATA = os.path.abspath(PATH_PROJECT+"/data/abfs/")
PATH_HEADERS = os.path.dirname(PATH_DATA)+"/headers/"
sys.path.insert(0, PATH_PROJECT+"/src/")
import pyabf
import glob
import numpy as np
import inspect
import datetime

import logging
logging.basicConfig(level=logging.WARNING)
log = logging.getLogger(__name__)

def go():
    print("Ensuring headers are stable", end=" ")
    print(" OK")


def dot():
    """print a dot to the screen indicating a test completed okay."""
    print(".", end="")
    sys.stdout.flush()

def ensureAbfHeaderDidNotChange(abfFilePath):
    """throw an exception if the abf header markdown file changed"""
    abf = pyabf.ABF(abfFilePath)
    mdHeaderPath = f"{PATH_HEADERS}/{abf.abfID}.md"
    newMarkdown = abf.headerMarkdown.split("\n")
    with open(mdHeaderPath) as f:
        previousMarkdown = f.read().split("\n")
    for i in range(len(newMarkdown)):
        if "abfFilePath = " in newMarkdown[i]:
            continue
        if "strings =" in newMarkdown[i]:
            continue
        if newMarkdown[i]!=previousMarkdown[i]:
            if "abfDateTime" in newMarkdown[i]:
                continue
            log.critical(f"MARKDOWN FILE CHANGED: {mdHeaderPath}")
            log.critical(f"OLD FILE LINE {i}:")
            log.critical(previousMarkdown[i])
            log.critical(f"NEW FILE LINE {i}:")
            log.critical(newMarkdown[i])
            raise NotImplementedError("HEADER CHANGED (save new headers?)")
    return

def go():
    """ensure all no existing ABF header changed."""
    print("Ensuring ABF headers are unchanged", end=" ")
    for abfFileName in glob.glob(PATH_DATA+"/*.abf"):
        ensureAbfHeaderDidNotChange(abfFileName)
        dot()
    print(" OK")

if __name__ == "__main__":
    go()
