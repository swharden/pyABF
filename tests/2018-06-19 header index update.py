"""
This code reads every ABF in the data folder and updates its header information.
This script outputs HTML files, markdown files, and generates the readme.md in
the root folder of the data directory. It also generates thumbnails for each ABF.
"""

# import the pyabf module from this development folder
import os
import sys
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_SRC = os.path.abspath(PATH_HERE+"/../src/")
PATH_DATA = os.path.abspath(PATH_HERE+"/../data/")
sys.path.insert(0, PATH_SRC)  # for importing
sys.path.append("../src/")  # for your IDE
import pyabf
pyabf.info()
import datetime
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('bmh') # alternative color scheme

# now you are free to import additional modules
import glob

if __name__ == "__main__":
    md = "# Sample ABFs\n\n"
    md += "This is a small collection of various ABFs I practice developing with. "
    md += "Many of them were emailed to me by contributors. If you have a unique type "
    md += "of ABF file, email it to me and I will include it here. Note that this page "
    md += "is generated automatically.\n\n"

    md += "ABF (version) | channels | sweeps | protocol | thumbnail\n"
    md += "---|---|---|---|---\n"

    for fname in sorted(glob.glob(PATH_DATA+"/*.abf")):
        abf = pyabf.ABF(fname)
        print(abf.abfID)

        # create info pages
        page = abf.getInfoPage()
        headerPath = os.path.abspath(PATH_HERE+"/../data/headers/")
        with open(headerPath+"/%s.md" % (abf.abfID), 'w') as f:
            f.write(page.getMarkdown())
        with open(headerPath+"/%s.html" % (abf.abfID), 'w') as f:
            f.write(page.getHTML())

        # create thumbnail
        abf.setSweep(-1) # go to the last sweep
        plt.figure(figsize=(6, 4))
        plt.title("{} channel {} sweep {}".format(
            abf.abfID, abf.sweep.channel, abf.sweep.number))
        plt.plot(abf.sweep.x, abf.sweep.y)
        plt.ylabel(abf.sweep.units)
        plt.xlabel(abf.sweep.unitsX)
        plt.tight_layout()
        plt.savefig(headerPath+"/%s.jpg" % (abf.abfID))
        plt.close()

        # update main readme
        md += "[%s.abf](headers/%s.md) (%s)|" % (abf.abfID, abf.abfID, abf.abfVersion)
        md += "%s (%s)|" % (abf.dataChannelCount, ", ".join(abf.adcUnits))
        md += "%s|" % (abf.sweepCount)
        md += "%s|" % (abf.protocol)
        md += "![headers/%s.jpg](headers/%s.jpg)\n" % (abf.abfID, abf.abfID)

    # write main readme
    with open(PATH_HERE+"/../data/readme.md", 'w') as f:
        f.write(md)
    print("DONE")
