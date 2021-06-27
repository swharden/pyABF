"""
Code here relates to text parsing and creation of HTML and markdown files
to display the ABF header in a neat and organized way.
"""

import tempfile
import webbrowser
import time
import glob
import os
import datetime
import numpy as np
np.set_printoptions(precision=4, suppress=True, threshold=5)

import pyabf.waveform


def standardNumpyText(data):
    """return a numpy array as a standard string regardless of numpy version"""
    if isinstance(data, np.ndarray):
        if len(data.shape) == 0:
            return str(data)
        out = "array (%dd) with values like: " % (len(data.shape))
        data = data.flatten()
        if len(data) < 10:
            data = ["%.05f" % x for x in data]
            data = ", ".join(data)
            out += data
        else:
            dataFirst = ["%.05f" % x for x in data[:3]]
            dataFirst = ", ".join(dataFirst)
            dataLast = ["%.05f" % x for x in data[-3:]]
            dataLast = ", ".join(dataLast)
            out += "%s, ..., %s" % (dataFirst, dataLast)
    elif isinstance(data, list):
        if len(data) < 20:
            return str(data)
        else:
            dataFirst = [str(x) for x in data[:3]]
            dataFirst = ", ".join(dataFirst)
            dataLast = [str(x) for x in data[-3:]]
            dataLast = ", ".join(dataLast)
            out = "[%s, ..., %s]" % (dataFirst, dataLast)
    else:
        out = str(data)
    return out


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
        for i, line in enumerate(self.things):
            if line[0] == name:
                self.things[i] = [name, newValue]

    def addDocs(self, docs):
        self.things.append([docs, "~DOCS~"])

    def showText(self):
        print(self.getText())

    def getText(self):
        """Return information about all objects as markdown-formatted text."""
        text = ""
        for item in self.things:
            name, value = item
            if value == "~SECTION~":
                text += "\n### %s ###\n" % name
            elif value == "~DOCS~":
                text += "\n~~~ %s ~~~\n" % name
            elif str(name) == "~CODE~":
                text += value+"\n"
            else:
                if value is None:
                    text += "%s" % (name)+"\n"
                else:
                    text += "%s = %s\n" % (name, value)
        lines = text.split("\n")
        lines = [x.strip() for x in lines]
        text = "\n".join(lines)
        return text

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
                    value = ""
                out += "\n```\n"+value.strip("\n")+"\n```\n"
            else:
                if value is None:
                    if "()" in name:
                        out += "* %s\n" % (name)
                    else:
                        out += "* %s = `None`\n" % (name)
                else:
                    if type(value) in [list, np.ndarray]:
                        val = standardNumpyText(value)
                    else:
                        val = str(value)
                    val = val.replace("\n", " ")
                    out += "* %s = `%s`\n" % (name, val)

        if saveAs:
            with open(saveAs, 'w') as f:
                f.write(out)

        return out

    def generateHTML(self, saveAs=False):
        html = "<html>"
        html += "<head>"
        html += "<style>"
        html += "body {font-family: sans-serif;}"
        html += "code {background-color: #F2F2F2; padding: 2px;}"
        html += ".item {margin-left: 2em; margin-top: .5em;}"
        html += ".section {font-size: 150%;font-weight:bold;margin-top:2em;}"
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
                part = "\n<div class='docs'>%s</div>" % name.strip()
                html += part.replace("\n", "<br>")
            elif str(name) == "~CODE~":
                if value is None:
                    value = ""
                html += "\n<pre>\n"+value.strip("\n")+"\n</pre>\n"
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

    # create a list of all methods in this object
    thingNames = sorted(dir(abf))

    # remove methods that call this function (causing infinite loops)
    thingNames.remove("headerText")
    thingNames.remove("headerHTML")
    thingNames.remove("headerMarkdown")
    thingNames.remove("headerLaunch")

    for thingName in thingNames:
        if thingName.startswith("_"):
            continue
        thing = getattr(abf, thingName)
        if "method" in str(type(thing)):
            page.addThing("abf.%s()" % (thingName))

    page.addSection("ABF Class Variables")
    for thingName in thingNames:
        if thingName.startswith("_"):
            continue
        thing = getattr(abf, thingName)
        if "method" in str(type(thing)):
            continue
        if isinstance(thing, (int, list, dict, float, datetime.datetime, str,
                              np.ndarray, pyabf.waveform.EpochSweepWaveform)):
            page.addThing(thingName, thing)
        elif thing is None or thing is False or thing is True:
            page.addThing(thingName, thing)
        else:
            print("Unsure how to generate info for:", thingName, type(thing))

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
        headerParts.append(["ProtocolSection", abf._protocolSection])
        headerParts.append(["ADCSection", abf._adcSection])
        headerParts.append(["DACSection", abf._dacSection])
        headerParts.append(
            ["EpochPerDACSection", abf._epochPerDacSection])
        headerParts.append(["EpochSection", abf._epochSection])
        headerParts.append(["TagSection", abf._tagSection])
        headerParts.append(["SynchArraySection", abf._synchArraySection])
        headerParts.append(["StringsSection", abf._stringsSection])
        #headerParts.append(["StringsIndexed", abf._stringsIndexed])
    for headerItem in headerParts:
        thingTitle, thingItself = headerItem
        page.addSection(thingTitle)
        page.addDocs(thingItself.__doc__)
        for subItemName in sorted(dir(thingItself)):
            if subItemName.startswith("_"):
                continue
            thing = getattr(thingItself, subItemName)
            if callable(thing):
                continue
            if hasattr(thing, "seek"):
                continue
            page.addThing(subItemName, thing)

    return page


if __name__ == "__main__":
    print("DO NOT RUN THIS MODULE DIRECTLY")
