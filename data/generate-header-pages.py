"""
This script loads every ABF in the data folder and generates a summary of its 
header (in both HTML and markdown format).
"""

import os
import sys
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_SRC = os.path.abspath(PATH_HERE+"/../src/")
PATH_DATA = os.path.abspath(PATH_HERE+"/../data/abfs/")
sys.path.insert(0, PATH_SRC)  # for importing
sys.path.append("../src/")  # for your IDE
import pyabf
import glob

def infoPage(abf):
    """
    Create markdown and HTML file containing header details.
    """
    page = abf.getInfoPage()
    headerPath = os.path.abspath(PATH_HERE+"/../data/headers/")
    with open(headerPath+"/%s.md" % (abf.abfID), 'w') as f:
        f.write(page.generateMarkdown())
    with open(headerPath+"/%s.html" % (abf.abfID), 'w') as f:
        f.write(page.generateHTML())

def go():

    print("Generating header info pages",end=" ")

    for fname in sorted(glob.glob(PATH_DATA+"/*.abf")):
        abf = pyabf.ABF(fname)
        infoPage(abf)
        print(".", end="")
        sys.stdout.flush()
    print(" OK")

if __name__ == "__main__":
    go()