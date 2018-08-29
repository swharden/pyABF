"""
Code here helps lock-in certain API functions.

Once functionality is added here, extreme efforts are taken never to remove
support for these functions.
"""

import os
import sys
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_PROJECT = os.path.abspath(PATH_HERE+"/../../")
PATH_DATA = os.path.abspath(PATH_PROJECT+"/data/abfs/")
sys.path.insert(0, PATH_PROJECT+"/src/")
import pyabf
import glob
import numpy as np

import logging
logging.basicConfig(level=logging.WARNING)
log = logging.getLogger(__name__)

if __name__=="__main__":
    print("DONE")