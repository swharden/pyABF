"""
Refactor the membrane test module to provide a clean interface.
You can always refactor the core later.
"""

import os
import sys
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_DATA = os.path.abspath(PATH_HERE+"../../../data/abfs/")
PATH_SRC = os.path.abspath(PATH_HERE+"../../../src/")
sys.path.insert(0, PATH_SRC)

import pyabf
import pyabf.tools

abf = pyabf.ABF(PATH_DATA+"/2018_08_23_0009.abf")
mt = pyabf.tools.Memtest(abf)
print(mt)
print(mt.summary)
print(mt.CmStep.values)