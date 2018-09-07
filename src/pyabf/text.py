"""
Code here relates to text parsing and other ninjary
"""

import tempfile
import webbrowser
import time
import glob
import os
import datetime
import numpy as np
np.set_printoptions(precision=4, suppress=True, threshold=5)

def indexFolder(folder, launch=True):
    html = "<html><head><style>"
    html+="body {background-color: #ddd;}"
    html+="img {border: 1px solid black; margin: 20px;}"
    html+="img {box-shadow: 5px 5px 15px rgba(0, 0, 0, .3);}"
    html+="img {height: 300px; background-color: white;}"
    html+="</style></head><body>"

    html+="<h1>Images</h1>"
    pics = []
    pics += glob.glob(folder+"/*.png")
    pics += glob.glob(folder+"/*.jpg")
    for pic in sorted(pics):
        url = os.path.basename(pic)
        html += f"<a href='{url}'><img src='{url}'></a> "

    html+="<h1>HTML Files</h1>"
    for pic in sorted(glob.glob(folder+"/*.html")):
        url = os.path.basename(pic)
        html += f"<li><a href='{url}'>{url}</a> "

    html += "</body></html>"
    fname = folder+"/index-pics.html"
    with open(fname, 'w') as f:
        f.write(html)
    if launch:
        webbrowser.open(fname)


class InfoPage:
    """
    The InfoPage class is designed to hold information about
    python objects in such a way that it can be easily viewed.
    Build the page with sections, docs, and things, then
    get it as HTML, markdown, or text.
    """

    def __init__(self, title="PageTitle"):
        self.things = []
        self.title = title

    def addSection(self, name):
        self.things.append([name, "~SECTION~"])

    def addThing(self, name, value=None):
        self.things.append([name, value])

    def replaceThing(self, name, newValue):
        for i,line in enumerate(self.things):
            if line[0]==name:
                self.things[i] = [name, newValue]

    def addDocs(self, docs):
        self.things.append([docs, "~DOCS~"])

    def showText(self):
        for item in self.things:
            name, value = item
            if value == "~SECTION~":
                print("\n### %s ###" % name)
            elif value == "~DOCS~":
                print("\n~~~ %s ~~~" % name)
            elif str(name) == "~CODE~":
                print(value)
            else:
                if value is None:
                    print("%s" % (name))
                else:
                    print("%s = %s" % (name, value))
        return

    def generateMarkdown(self, saveAs=False):
        out = "# %s\n" % (self.title)
        for item in self.things:
            name, value = item
            if str(value) == "~SECTION~":
                out += "\n## %s\n\n" % (name)
            elif str(value) == "~DOCS~":
                out += "> %s \n\n" % (name.strip().replace("\n", " "))
            elif str(name) == "~CODE~":
                if value is None:
                    value=""
                out+="\n```\n"+value.strip("\n")+"\n```\n"
            else:
                if value is None:
                    out += "* %s\n" % (name)
                else:
                    out += "* %s = `%s`\n" % (name,
                                              str(value).replace("\n", " "))

        if saveAs:
            with open(saveAs, 'w') as f:
                f.write(html)

        return out

    def generateHTML(self, saveAs=False):
        html = "<html>"
        html += "<head>"
        html += "<style>"
        html += "body {font-family: sans-serif;}"
        html += "code {background-color: #F2F2F2; padding: 2px;}"
        html += ".item {margin-left: 2em; margin-top: .5em;}"
        html += ".section {font-size: 150%; font-weight: bold; margin-top: 2em; }"
        html += ".docs {font-style: italic; font-family: serif;}"
        html += "</style>"
        html += "<title>%s</title>" % (self.title)
        html += "</head>"
        html += "<body>"
        html += "<h1>%s</h1>" % self.title
        for item in self.things:
            name, value = item
            if str(value) == "~SECTION~":
                html += "\n<div class='section'>%s</div>" % name
            elif str(value) == "~DOCS~":
                html += "\n<div class='docs'>%s</div>" % name.strip().replace("\n", "<br>")
            elif str(name) == "~CODE~":
                if value is None:
                    value=""
                html+="\n<pre>\n"+value.strip("\n")+"\n</pre>\n"
            else:
                if value is None:
                    html += "\n<div class='item'>%s</div>" % (name)
                else:
                    html += "\n<div class='item'>%s = <code>%s</code></div>" % (
                        name, value)
        html += "</body></html>"

        if saveAs:
            with open(saveAs, 'w') as f:
                f.write(html)

        return html

    def launchTempWebpage(self):
        html = self.generateHTML()
        with tempfile.TemporaryDirectory() as tempDir:
            fname = tempDir+"/header.html"
            print(fname)
            f = open(fname, 'w')
            f.write(html)
            f.flush()
            webbrowser.open(fname)
            time.sleep(1)
            f.close()


def abfInfoPage(abf):
    """
    Return an object to let the user inspect methods and variables
    of this ABF class as well as the full contents of the ABF header
    """
    page = InfoPage(abf.abfID+".abf")

    # add info about this ABF instance

    page.addSection("ABF Class Methods")
    for thingName in sorted(dir(abf)):
        if thingName.startswith("_"):
            continue
        thing = getattr(abf, thingName)
        if "method" in str(type(thing)):
            page.addThing("abf.%s()" % (thingName))

    page.addSection("ABF Class Variables")
    for thingName in sorted(dir(abf)):
        if thingName.startswith("_"):
            continue
        thing = getattr(abf, thingName)
        if "method" in str(type(thing)):
            continue
        if isinstance(thing, (int, list, dict, float, datetime.datetime, str, np.ndarray, range)):
            page.addThing(thingName, thing)
        elif thing is None or thing is False or thing is True:
            page.addThing(thingName, thing)
        else:
            print("Unsure how to generate info for:",
                    thingName, type(thing))

    for channel in abf.channelList:
        page.addSection("Epochs for Channel %d" % channel)
        text = abf.stimulusByChannel[channel].text
        page.addThing("~CODE~", text)

    # add all ABF header information (different in ABF1 vs ABF2)

    headerParts = []
    if abf.abfVersion["major"] == 1:
        headerParts.append(["ABF1 Header", abf._headerV1])
    elif abf.abfVersion["major"] == 2:
        headerParts.append(["ABF2 Header", abf._headerV2])
        headerParts.append(["SectionMap", abf._sectionMap])
        headerParts.append(["ProtocolSection", abf._protocolSection])
        headerParts.append(["ADCSection", abf._adcSection])
        headerParts.append(["DACSection", abf._dacSection])
        headerParts.append(
            ["EpochPerDACSection", abf._epochPerDacSection])
        headerParts.append(["EpochSection", abf._epochSection])
        headerParts.append(["TagSection", abf._tagSection])
        headerParts.append(["StringsSection", abf._stringsSection])
        headerParts.append(["StringsIndexed", abf._stringsIndexed])
    for headerItem in headerParts:
        thingTitle, thingItself = headerItem
        page.addSection(thingTitle)
        page.addDocs(thingItself.__doc__)
        for subItemName in sorted(dir(thingItself)):
            if subItemName.startswith("_"):
                continue
            page.addThing(subItemName, getattr(thingItself, subItemName))

    return page

if __name__ == "__main__":

    indexFolder(R"C:\Users\scott\Documents\temp")

    print("DONE")
