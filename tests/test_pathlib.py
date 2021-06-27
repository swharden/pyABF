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
    assert abf1.sweepCount == abf2.sweepCount


@pytest.mark.parametrize("atfPath", glob.glob("data/abfs/*.atf"))
def test_pathlib_ATFs(atfPath):
    atf1 = pyabf.ATF(atfPath, loadData=False)
    atf2 = pyabf.ATF(pathlib.Path(atfPath), loadData=False)
    assert atf1.sweepCount == atf2.sweepCount

def test_pathThrowsIfFolder_ABFs():
    with pytest.raises(Exception) as excinfo:
        abf = pyabf.ABF("data/abfs", loadData=False)
    assert "FILE not a FOLDER" in str(excinfo.value)


def test_pathMustBeFile_ATFs():
    with pytest.raises(Exception) as excinfo:
        atf = pyabf.ATF("data/abfs", loadData=False)
    assert "FILE not a FOLDER" in str(excinfo.value)
