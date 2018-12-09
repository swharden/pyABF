"""
DLL Export Viewer (http://www.nirsoft.net/utils/dll_export_viewer.html) can save
all functions in a DLL as a text file. This script converts that text file to
a markdown-formatted file.
"""

import os
PATH_HERE = os.path.dirname(__file__)
dllTextFile = PATH_HERE+"/ABFFIO.dll.txt"
mdOutputFile = PATH_HERE+"/readme.md"
abfHfile = PATH_HERE+"/ABF_FileSupportPack/AxonDev/Comp/ABFFIO/ABFFILES.H"

# read the content of the file
with open(dllTextFile) as f:
    lines = f.readlines()

# strip-out the values we want
values = []
titles = []
for line in lines:
    line = line.strip()
    if not ":" in line:
        continue
    title, value = line.split(":", 1)
    titles.append(title.strip())
    values.append(value.strip())

md = """
# Axon SDK Notes

Axon pCLAMP ABF File Support Pack Download Page:
[Download the Support files for Axon pClamp](http://mdc.custhelp.com/app/answers/detail/a_id/18881/~/axon%E2%84%A2-pclamp%C2%AE-abf-file-support-pack-download-page).
_This link is now broken, and the SDK is distributed as a ZIP with pCLAMP 11_.

_This page was generated automatically by [convert.py](convert.py)_

"""

# create markdown with lines from the H file
md += "## ABFFILES.H\n\n"
with open(abfHfile) as f:
    raw = f.read()
raw = raw.replace("\n", " ")
lines = raw.split(";")
lines = lines[2:]
lines = [x.strip() for x in lines]
lines = sorted(lines)
for line in lines:
    line=line.strip()
    if line.startswith("#") \
    or line.startswith("//") \
    or line.startswith("typedef"):
        continue
    line = line.replace(" WINAPI", "")
    line = line.replace("(", " (")
    line = line.split(" ")
    line[1] = "**"+line[1]+"**"
    line = " ".join(line)
    line = line.replace(" (", "(")
    md += "\n * %s"%line

# create markdown with only the values we care about from the DLL

md += """
## ABFFIO.DLL

Function Name | Relative Address | Ordinal
--------------|------------------|--------
"""
for i in range(0, len(values), 7):
    name = values[i+0]
    address = values[i+1]
    addressRel = values[i+2]
    ordinal = values[i+3]
    md += "%s|%s|%s\n" % (name, addressRel, ordinal)

# write the markdown to disk
with open(mdOutputFile, 'w') as f:
    f.write(md)

print("DONE")
