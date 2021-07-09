import pytest
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
    import pyabf.tools.memtest
except:
    raise ImportError("couldn't import local pyABF")


def test_values_matchExpected():
    abfPath = pathlib.Path(PATH_DATA).joinpath("vc_drug_memtest.abf")
    abf = pyabf.ABF(abfPath)
    memtest = pyabf.tools.memtest.Memtest(abf)

    assert -6.9107 == pytest.approx(memtest.Ih.values[0], 5)
    assert -25.4053 == pytest.approx(memtest.Ih.values[-1], 5)

    assert 177.8927 == pytest.approx(memtest.Rm.values[0], 5)
    assert 184.7151 == pytest.approx(memtest.Rm.values[-1], 5)

    assert 27.9074 == pytest.approx(memtest.Ra.values[0], 5)
    assert 38.4206 == pytest.approx(memtest.Ra.values[-1], 5)

    assert 43.613 == pytest.approx(memtest.CmStep.values[0], 5)
    assert 42.3425 == pytest.approx(memtest.CmStep.values[-1], 5)
