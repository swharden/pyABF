import glob
import sys
import os
sys.path.insert(0,os.path.abspath("../../../src/"))
import pyabf

if __name__=="__main__":
    PATH=R"X:\Data\projects\2017-01-09 AT1-Cre mice\2017-01-09 global expression NTS\data"
    for fname in sorted(glob.glob(PATH+"/*.abf")):
        abf=pyabf.ABF(fname)
        if not abf.commentsExist:
            continue
        print(abf.ID,abf.commentTags)
    print("DONE")