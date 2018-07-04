# import the pyabf module from this development folder
import os
import sys
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_SRC = os.path.abspath(PATH_HERE+"/../../src/")
PATH_DATA = os.path.abspath(PATH_HERE+"/../../data/abfs/")
sys.path.insert(0, PATH_SRC)  # for importing
sys.path.append("../../src/")  # for your IDE
import pyabf
import glob

import matplotlib.pyplot as plt
import numpy as np
import warnings