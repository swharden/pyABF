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

if __name__=="__main__":
    aq = autoabf.ABFwatcher()
    #aq.addWatchedFolder(R"X:/some/crazy/path/")
    aq.addWatchedFolder(R"C:\Users\scott\Documents\important\abfs")
    #aq.addWatchedFolder(R"Y:/some/crazy/path/")
    aq.rescan()
    print("DONE")