import pytest
import glob
import os
import sys
import pathlib
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_PROJECT = os.path.abspath(PATH_HERE+"/../")
PATH_DATA = os.path.abspath(PATH_PROJECT+"/data/abfs/")
PATH_HEADERS = os.path.abspath(PATH_PROJECT+"/data/headers/")

try:
    # this ensures pyABF is imported from this specific path
    sys.path.insert(0, "src")
    import pyabf
except:
    raise ImportError("couldn't import local pyABF")


@pytest.mark.parametrize("abfPath", glob.glob("data/abfs/*.abf"))
def test_pathlib_ABFs(abfPath):
    abf1 = pyabf.ABF(abfPath, loadData=False)
    abf2 = pyabf.ABF(pathlib.Path(abfPath), loadData=False)


@pytest.mark.parametrize("atfPath", glob.glob("data/abfs/*.atf"))
def test_pathlib_ATFs(atfPath):
    abf1 = pyabf.ATF(atfPath, loadData=False)
    abf2 = pyabf.ATF(pathlib.Path(atfPath), loadData=False)
