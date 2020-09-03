"""This script increases the minor version of the current project."""

import os


def nextVersionString(oldVersionString):
    oldVersion = oldVersionString.split(".")
    assert len(oldVersion) == 3
    oldVersion = [int(x) for x in oldVersion]
    return "%d.%d.%d" % (oldVersion[0], oldVersion[1], oldVersion[2] + 1)


def increaseVersion(fname):
    assert os.path.exists(fname)

    with open(fname) as f:
        lines = f.read().split("\n")

    for i, line in enumerate(lines):
        strippedLine = line.replace(" ", "")
        if strippedLine.startswith("version=") or strippedLine.startswith("__version__="):
            oldVersion = line.split("'")[1]
            newVersion = nextVersionString(oldVersion)
            print(f"{os.path.basename(fname)}\t{oldVersion} -> {newVersion}")
            lines[i] = line.replace(oldVersion, newVersion)

    with open(fname, 'w') as f:
        f.write("\n".join(lines))

    return newVersion


if __name__ == "__main__":
    PATH_HERE = os.path.abspath(os.path.dirname(__file__))
    setupVersion = increaseVersion(PATH_HERE+"/../../src/setup.py")
    pyAbfVersion = increaseVersion(PATH_HERE+"/../../src/pyabf/__init__.py")
    assert setupVersion == pyAbfVersion
