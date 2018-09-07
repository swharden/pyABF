R"""
Code here helps lock-in certain API functions.

Once functionality is added here, extreme efforts are taken never to remove
support for these functions.
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


if __name__ == "__main__":
    # log.setLevel(logging.DEBUG)
    #go()
    abf = pyabf.ABF(PATH_DATA+"/16d05007_vc_tags.abf")
    txt = abf.getInfoPage().generateMarkdown(f"{PATH_HEADERS}/{abf.abfID}.md")
    print(txt)
    print("DONE")
