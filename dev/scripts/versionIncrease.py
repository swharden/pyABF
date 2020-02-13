"""This script increases the minor version of the current project."""

import os

def increaseVersion(fname):
    assert os.path.exists(fname)
    with open(fname) as f:
        oldVersionString = f.read().strip()
    oldVersion = oldVersionString.split(".")
    oldVersion = [int(x) for x in oldVersion]
    newVersionString = "%d.%d.%d" % (oldVersion[0], oldVersion[1], oldVersion[2] + 1)	
    with open(fname, 'w') as f:
        f.write(newVersionString)
    print(f"Upgraded: {oldVersionString} -> {newVersionString}")
    return


if __name__ == "__main__":
    PATH_HERE = os.path.abspath(os.path.dirname(__file__))
    versionFile = os.path.abspath(PATH_HERE+"/../../src/pyabf/version.txt")
    increaseVersion(versionFile)
