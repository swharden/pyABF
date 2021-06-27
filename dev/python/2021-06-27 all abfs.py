import os
import sys
import matplotlib.pyplot as plt
import glob

try:
    PATH_HERE = os.path.abspath(os.path.dirname(__file__))
    PATH_DATA = os.path.abspath(PATH_HERE+"../../../data/abfs/")
    PATH_SRC = os.path.abspath(PATH_HERE+"../../../src/")
    DATA_FOLDER = os.path.join(PATH_SRC, "../data/abfs/")
    sys.path.insert(0, PATH_SRC)
    import pyabf
except:
    raise EnvironmentError()


if __name__ == "__main__":
    for abfPath in glob.glob(DATA_FOLDER + "/*.abf"):
        abf = pyabf.ABF(abfPath)
        print(abf)