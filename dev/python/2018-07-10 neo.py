"""
Crash course on using NeoIO to display info about ABF files
"""
from imports import *
from neo.io import AxonIO
import pprint
pp = pprint.PrettyPrinter(indent=4)

if __name__=="__main__":
    fname = PATH_DATA+"/18702001-biphasicTrain.abf"
    reader = AxonIO(fname)  
    headerText = pprint.pformat(reader._axon_info)

    out = "# AxonIO()._axon_info\n"
    out += f"\n```\n{headerText}\n```\n"
    with open(__file__+".md",'w') as f:
        f.write(out)
    print("DONE")