"""
Boilerplate dev test
"""

from imports import *

if __name__ == "__main__":
    abf = pyabf.ABF(PATH_DATA+"/180415_aaron_temp.abf")
    print(abf.sweepY)
    print(abf.sweepC)