"""
Code here relates to displaying and string-manipulating header dictionaries created by the ABFheader class.
"""

import os

def show(header):
    """Display the contents of the header in an easy to read format."""
    for key in header.keys():
        if key.startswith("###"):
            print("\n%s"%key)
        else:
            print("%s = %s"%(key,header[key]))

def html(header,fname):
    """Generate a HTML-formatted document with all header information."""
    html="<html><body><code>"
    for key in header.keys():
        if key.startswith("###"):
            key=key.replace("#","").strip()
            html+="<br><b style='font-size: 200%%;'>%s</b><br>"%key
        else:
            html+="%s = %s<br>"%(key,header[key])
    html+="</code></html></body>"
    with open(fname,'w') as f:
        f.write(html)
    print("wrote",os.path.abspath(fname))
    
def markdown(header,fname):
    """Generate a markdown-formatted document with all header information."""
    out="# ABF Header Contents\n"
    for key in header.keys():
        if key.startswith("###"):
            key=key.replace("#","").strip()
            out+="\n## %s\n"%key
        else:
            out+="* %s = `%s`\n"%(key,header[key])
    with open(fname,'w') as f:
        f.write(out)
    print("wrote",os.path.abspath(fname))   