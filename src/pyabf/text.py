"""
Code here relates to text parsing and other ninjary
"""

import tempfile
import webbrowser
import time

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
            if value=="~SECTION~":
                print("\n### %s ###"%name)
            elif value=="~DOCS~":
                print("\n~~~ %s ~~~"%name)
            else:
                if value is None:
                    print("%s"%(name))
                else:
                    print("%s = %s"%(name, value))
        return

    def getMarkdown(self):
        out="# %s\n"%(self.title)
        for item in self.things:
            name, value = item
            if str(value)=="~SECTION~":
                out+="\n## %s\n\n"%(name)
            elif str(value)=="~DOCS~":                    
                out+="> %s \n\n"%(name.strip().replace("\n"," "))
            else:
                if value is None:
                    out+="* %s\n"%(name)
                else:
                    out+="* %s = `%s`\n"%(name, str(value).replace("\n"," "))
        return out
        


    def getHTML(self):
        html="<html>"
        html+="<head>"
        html+="<style>"
        html+="body {font-family: sans-serif;}"
        html+="code {background-color: #F2F2F2; padding: 2px;}"
        html+=".item {margin-left: 2em; margin-top: .5em;}"
        html+=".section {font-size: 150%; font-weight: bold; margin-top: 2em; }"
        html+=".docs {font-style: italic; font-family: serif;}"
        html+="</style>"
        html+="<title>%s</title>"%(self.title)
        html+="</head>"
        html+="<body>"
        html+="<h1>%s</h1>"%self.title
        for item in self.things:
            name, value = item
            if str(value)=="~SECTION~":
                html+="<div class='section'>%s</div>"%name
            elif str(value)=="~DOCS~":
                html+="<div class='docs'>%s</div>"%name.strip().replace("\n","<br>")
            else:
                if value is None:
                    html+="<div class='item'>%s</div>"%(name)
                else:
                    html+="<div class='item'>%s = <code>%s</code></div>"%(name, value)
        html+="</body></html>"
        return html

    def launchTempWebpage(self):
        html = self.getHTML()
        with tempfile.TemporaryDirectory() as tempDir:
            fname = tempDir+"/header.html"
            print(fname)
            f = open(fname,'w')
            f.write(html)
            f.flush()
            webbrowser.open(fname)
            time.sleep(1)
            f.close()


if __name__ == "__main__":

    page = InfoPage()

    page.addSection("Methods")
    page.addDocs("Some cool description of some interesting thing")
    page.addThing("abf.infoBrowser()")
    page.addThing("abf.infoDisplay()")
    page.addThing("abf.setSweep()")

    page.addSection("Variables")
    page.addThing("abfID", "16d22006_kim_gapfree")
    page.addThing("abfVersion", 2.123)
    page.addThing("adcNames", ['IN 2', 'IN 3'])

    #page.launchTempWebpage("tester")

    print(page.getMarkdown())

    print("DONE")
