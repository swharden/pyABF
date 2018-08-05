
"""
Code here makes it easy to glance at a header item from every demo ABF file.
"""
from imports import *

if __name__=="__main__":
    for fname in sorted(glob.glob(PATH_DATA+"/*.abf")):
        abf = pyabf.ABF(fname)
        print(abf.abfDateTime)
    plt.show()