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
plt.style.use('bmh')  # alternative color scheme

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

    # clear everything that used to be in the headers folder
    for fname in glob.glob(PATH_DATA+"/headers/*.*"):
        print("deleting", fname, "...")
        os.remove(fname)

    for fname in sorted(glob.glob(PATH_DATA+"/abfs/*.abf")):
        abf = pyabf.ABF(fname)
        print("processing", abf.abfID, "...")

        # create info pages
        page = abf.getInfoPage()
        headerPath = os.path.abspath(PATH_HERE+"/../data/headers/")
        with open(headerPath+"/%s.md" % (abf.abfID), 'w') as f:
            f.write(page.generateMarkdown())
        with open(headerPath+"/%s.html" % (abf.abfID), 'w') as f:
            f.write(page.generateHTML())

        # create figure and subplots
        fig = plt.figure(figsize=(8, 6))
        fig.patch.set_alpha(0)  # transparent background
        ax1 = plt.subplot(211)
        ax2 = plt.subplot(212)
        ax1.patch.set_facecolor('w')
        ax2.patch.set_facecolor('w')
        ax1.set_xmargin(0)
        ax2.set_xmargin(0)

        # overlap or continuous view depends on protocol
        absoluteTime = False
        if "0111" in abf.protocol:
            absoluteTime = True
        if "loose" in abf.protocol:
            absoluteTime = True

        # plot the data sweep by sweep
        for sweep in abf.sweepList:
            abf.setSweep(sweep, absoluteTime=absoluteTime)
            ax1.plot(abf.sweepX, abf.sweepY, alpha=.5, color='b', lw=.5)
            ax2.plot(abf.sweepX, abf.sweepC, color='r')

        # decorate plot and save it
        ax1.set_title("{}.abf [channel: {}/{}] [sweeps: {}]".format(
            abf.abfID, abf.sweepChannel+1, abf.channelCount, abf.sweepNumber+1))
        ax1.set_ylabel(abf.sweepLabelY)
        ax1.set_xlabel(abf.sweepLabelX)
        ax2.set_ylabel(abf.sweepLabelC)
        ax2.set_xlabel(abf.sweepLabelX)
        fig.tight_layout()
        fig.savefig(PATH_HERE+"/../data/headers/%s.png" % abf.abfID)
        plt.close()

        # update main readme
        md += "[%s.abf](headers/%s.md) (%s)|" % (abf.abfID,
                                                 abf.abfID, abf.abfVersion)
        md += "%s (%s)|" % (abf.channelCount, ", ".join(abf.adcUnits))
        md += "%s|" % (abf.sweepCount)
        md += "%s|" % (abf.protocol)
        md += "![headers/%s.jpg](headers/%s.png)\n" % (abf.abfID, abf.abfID)

    # write main readme
    with open(PATH_HERE+"/../data/readme.md", 'w') as f:
        f.write(md)

    # update the file index
    pyabf.text.indexFolder(PATH_HERE+"/../data/headers/")
    print("DONE")
