"""
This script increases the minor version of the current project.
"""

import os
PATH_HERE = os.path.abspath(os.path.dirname(__file__))


def increaseVersion(fname):
    assert os.path.exists(fname)
    with open(fname) as f:
        lines = f.read().split("\n")
    for i, line in enumerate(lines):
        if line.startswith("__version__"):
            oldVersionString = eval(line.split("=")[1])
            oldVersion = oldVersionString.split(".")
            oldVersion = [int(x) for x in oldVersion]
            newVersion = oldVersion
            newVersion[-1] = newVersion[-1]+1
            newVersion = [str(x) for x in newVersion]
            newVersionString = ".".join(newVersion)
        lines[i] = lines[i].replace(oldVersionString, newVersionString)
    newText = "\n".join(lines)
    with open(fname, 'w') as f:
        f.write(newText)
    bn = os.path.basename(fname)
    print(f"Upgraded {bn}: {oldVersionString} -> {newVersionString}")
    return


if __name__ == "__main__":
    versionFile = os.path.abspath(PATH_HERE+"/../../src/pyabf/__init__.py")
    increaseVersion(versionFile)
