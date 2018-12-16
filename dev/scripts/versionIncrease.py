"""This script increases the minor version of the current project."""

import os

def increaseVersion(fname):
    assert os.path.exists(fname)
    with open(fname) as f:
        lines = f.read().split("\n")
    for i, line in enumerate(lines):
        if line.startswith("__version__"):
            oldVersionString = line.split("'")[1]
            newVersion = [int(x) for x in oldVersionString.split(".")]
            newVersion[-1] += 1
            newVersionString = ".".join([str(x) for x in newVersion])
            lines[i] = lines[i].replace(oldVersionString, newVersionString)
    with open(fname, 'w') as f:
        f.write("\n".join(lines))
    print(f"Upgraded: {oldVersionString} -> {newVersionString}")
    return


if __name__ == "__main__":
    PATH_HERE = os.path.abspath(os.path.dirname(__file__))
    versionFile = os.path.abspath(PATH_HERE+"/../../src/pyabf/__init__.py")
    increaseVersion(versionFile)
