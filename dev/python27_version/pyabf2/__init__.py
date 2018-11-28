"""This is a stripped-down version of pyABF designed to run on python 2.x"""
import sys
if sys.version_info >= (3,0):
    print("ERROR: this pyABF module is intended just for python 2.x")
from pyabf2.abf import ABF