"""
WARNING: this code is HIGHLY destructive to ABF files!
When run on a folder, this makes ABF files empty.
This is useful for rapidly emptying folders of ABF files
to practice writing directory browsing functions.
"""

import os
import glob

def makeFileEmpty(fname):
    """Delete the contents of a file."""
    assert os.path.exists(fname)
    print(fname)
    with open(fname,'w') as f:
        f.write("EMPTY")
    f.close()

if __name__=="__main__":
    for fname in glob.glob(R"C:\Users\swharden\Documents\temp\demoFolder\*.abf"):
        makeFileEmpty(fname)
    print("DONE")