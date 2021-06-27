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


@pytest.mark.skip(reason="this is slow, hard to run in cloud, and does not need to be run frequently")
@pytest.mark.parametrize("abfPath", glob.glob("data/abfs/*.abf"))
def test_saveABF1_forEveryFile(abfPath):
    testOutput = pathlib.Path("testOutput")
    if not testOutput.exists():
        testOutput.mkdir()
    abf = pyabf.ABF(abfPath)

    # don't attempt to save ABFs with variable-length sweeps
    if (abf.nOperationMode == 1):
        return

    abf.saveABF1(f"testOutput/{abf.abfID}.abf")
