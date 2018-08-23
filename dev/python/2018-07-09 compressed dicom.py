
"""
This script converts compressed DICOM files to images.
Lots of code came from here:
https://groups.google.com/forum/#!topic/pydicom/PJ9K37dsmBk
I used this to convert images from my CT to somthing ImageJ can easily open.
https://github.com/pydicom/pydicom/blob/master/examples/input_output/plot_read_dicom.py

pip install https://github.com/pydicom/pydicom/archive/master.zip

run("Bio-Formats Importer", "open=C:/Users/swharden/Documents/important/CTs/DICOM/00006.dcm color_mode=Default rois_import=[ROI manager] view=Hyperstack stack_order=XYCZT");

conda install -c clinicalgraphics gdcm 

"""

LINE = """run("Bio-Formats Importer", "open=FNAME color_mode=Default rois_import=[ROI manager] view=Hyperstack stack_order=XYCZT"); saveAs("Tiff", "FNAME.tif"); close();"""
import pydicom
import glob
import os
import matplotlib.pyplot as plt

def renameToDCM():
    for fname in glob.glob(R"C:\Users\swharden\Documents\important\CTs\DICOM\*"):
        i += 1
        if os.path.isfile(fname) and not "." in fname:
            bd = os.path.dirname(fname)
            fname2 = bd+"/%05d.dcm" % (i)
            fname2 = os.path.abspath(fname2)

            os.rename(fname, fname2)
            print(fname2)

import gdcm
import sys

def method2(file1, file2):

  reader = gdcm.ImageReader()
  reader.SetFileName( file1 )

  if not reader.Read():
    sys.exit(1)

  change = gdcm.ImageChangeTransferSyntax()
  change.SetTransferSyntax( gdcm.TransferSyntax(gdcm.TransferSyntax.ImplicitVRLittleEndian) )
  change.SetInput( reader.GetImage() )
  if not change.Change():
    sys.exit(1)

  writer = gdcm.ImageWriter()
  writer.SetFileName( file2 )
  writer.SetFile( reader.GetFile() )
  writer.SetImage( change.GetOutput() )

  if not writer.Write():
    raise ValueError

from PIL import Image
from PIL.TiffTags import TAGS

if __name__ == "__main__":
  
    # filenames come out right if you use the imaging software to export an image sequence.
    fldr = R"C:\Users\swharden\Documents\important\CTs\2018-08-16 pet CT\1.3.12.2.1107.5.1.4.60012.30000018081613365058600005183"
    fnames = sorted(glob.glob(fldr+R"/*.dcm"))
    fnames = [x for x in fnames if not ".raw." in x]
    for i,fname in enumerate(fnames):
        print(fname)
        method2(fname, fname+".raw.dcm")

    # fldr = R"C:\Users\swharden\Documents\important\CTs\2018-08-16 pet CT\1.3.12.2.1107.5.1.4.60012.30000018081613365058600005183"
    # fnames = sorted(glob.glob(fldr+R"/*.dcm"))
    # for i,fname in enumerate(fnames):
    #   dataset = pydicom.dcmread(fname)
    #   s = str(dataset).split("\n")
    #   s = [x.strip() for x in s]
    #   s = [x for x in s if "Instance Number" in x][0]
    #   s = int(s.split('"')[1])
    #   s = "%05d.dcm"%(s)
    #   fname2 = os.path.join(fldr,s)
    #   print(fname, fname2)
    #   if True:
    #     os.rename(fname,fname2)
        