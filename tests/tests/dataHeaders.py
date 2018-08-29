"""
This script loads every ABF in the data folder and generates a summary of its 
header (in both HTML and markdown format).
"""

import os
import sys
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_PROJECT = os.path.abspath(PATH_HERE+"/../../")
PATH_DATA = os.path.abspath(PATH_PROJECT+"/data/abfs/")
sys.path.insert(0, PATH_PROJECT+"/src/")
import pyabf
import glob

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
#log.setLevel(logging.DEBUG)


def infoPage(abf, markdown=True, html=False):
    """Create the markdown summary of the ABF header."""
    page = abf.getInfoPage()
    if markdown:
        fname = f"{PATH_DATA}/../headers/{abf.abfID}.md"
        fname = os.path.abspath(fname)
        log.debug(f"Generating {fname}")
        with open(fname, 'w') as f:
            f.write(page.generateMarkdown())
    if html:
        fname = f"{PATH_DATA}/../headers/{abf.abfID}.html"
        fname = os.path.abspath(fname)
        log.debug(f"Generating {fname}")
        with open(fname, 'w') as f:
            f.write(page.generateHTML())

def deletePages():
    """Delete all markdown and HTML files from the data folder."""
    for fname in glob.glob(PATH_DATA.replace("abfs", "headers")+'/*.html'):
        log.debug(f"Deleting {fname}")
        os.remove(fname)
    for fname in glob.glob(PATH_DATA.replace("abfs", "headers")+'/*.md'):
        log.debug(f"Deleting {fname}")
        os.remove(fname)

def go():
    """Create markdown header summary for every ABF in the data folder"""
    print("Generating header info pages", end=" ")
    deletePages()
    for fname in sorted(glob.glob(PATH_DATA+"/*.abf")):
        abf = pyabf.ABF(fname)
        infoPage(abf)
        print(".", end="")
        sys.stdout.flush()
    print(" OK")


if __name__ == "__main__":
    go()
