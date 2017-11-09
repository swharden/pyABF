"""
Code related to interacting with ABF files. The ABFHeader class in ABFHeaderReader to pulls header info out
of an ABF, but code here uses that information to do things like get data from individual sweeps.
"""

import abfHeaderReader
import abfHeaderTools

class ABF:
    def __init__(self,abf):
        print("ABF CLASS: you gave me a",type(abf))
        self.header=abfHeaderReader.ABFheader(abf).header
            
    def headerShow(self):
        """Display the header to the console window."""
        abfHeaderTools.show(self.header)
        
    def headerSaveHTML(self,fname="./demo.html"):
        """Save header information as an HTML-formatted file."""
        abfHeaderTools.html(self.header,fname)
        
    def headerSaveMarkdown(self,fname="./demo.md"):
        """Save header information as a markdown-formatted file."""
        abfHeaderTools.markdown(self.header,fname)

                
if __name__=="__main__":   
    abf=ABF(R"../../../../data/17o05028_ic_steps.abf")
    abf.headerShow()