"""
Code here relates to text parsing and other ninjary
"""

import tempfile
import webbrowser
import time
import glob
import os


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

    def addDocs(self, docs):
        self.things.append([docs, "~DOCS~"])

    def showText(self):
        for item in self.things:
            name, value = item
            if value == "~SECTION~":
                print("\n### %s ###" % name)
            elif value == "~DOCS~":
                print("\n~~~ %s ~~~" % name)
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
                html += "<div class='section'>%s</div>" % name
            elif str(value) == "~DOCS~":
                html += "<div class='docs'>%s</div>" % name.strip().replace("\n", "<br>")
            else:
                if value is None:
                    html += "<div class='item'>%s</div>" % (name)
                else:
                    html += "<div class='item'>%s = <code>%s</code></div>" % (
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


if __name__ == "__main__":

    indexFolder(R"C:\Users\scott\Documents\temp")

    print("DONE")
