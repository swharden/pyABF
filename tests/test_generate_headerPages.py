"""
This script loads every ABF in the data folder and generates a summary of its 
header (in both HTML and markdown format).
"""

import pytest
import glob
import os
import sys
import warnings
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_PROJECT = os.path.abspath(PATH_HERE+"/../")
PATH_DATA = os.path.abspath(PATH_PROJECT+"/data/abfs/")
PATH_HEADERS = os.path.abspath(PATH_PROJECT+"/data/headers/")

try:
    # this ensures pyABF is imported from this specific path
    sys.path.insert(0, "src")
    import pyabf
    from pyabf.abfHeaderDisplay import abfInfoPage
except:
    raise ImportError("couldn't import local pyABF")


@pytest.mark.parametrize("abfPath", glob.glob("data/abfs/*.abf"))
def test_cookbook_createHeaderPages(abfPath):
    warnings.simplefilter("ignore")
    abf = pyabf.ABF(abfPath)
    assert isinstance(abf, pyabf.ABF)
    page = abfInfoPage(abf)

    # modify a few infos to make things cleaner for source control
    abfFilePath = f"C:/some/path/to/{abf.abfID}.abf"
    abfFolderPath = f"C:/some/path"
    page.replaceThing("abfFilePath", abfFilePath)
    page.replaceThing("stimulusFileFolder", abfFilePath)
    page.replaceThing("abfFolderPath", abfFolderPath)
    page.replaceThing("strings", "not shown due to non-ASCII characters")

    with open(f"{PATH_HEADERS}/{abf.abfID}.md", 'w') as f:
        f.write(page.generateMarkdown())

    # with open(f"{PATH_HEADERS}/{abf.abfID}.html", 'w') as f:
        # f.write(page.generateHTML())
