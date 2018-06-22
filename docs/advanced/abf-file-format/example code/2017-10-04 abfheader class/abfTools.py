"""
A few functions which act as tools to help with development and debugging.
Mostly does some python ninja magic to turn headers into text documents, markdown, or HTML
"""

import os

def headerToHTML(h,htmlFileName=None):
    """given an ABFheader class object, create a HTML report."""
    html="<html><head><style>"
    html+="body{font-family: sans-serif;}"
    html+=".title{font-size: 150%; font-weight: bold;}"
    html+=".title2{font-size: 250%; font-weight: bold;}"
    html+=".subtitle{font-style: italic; font-size: 80%;}"
    html+=".block{font-family: monospace; border-left: 10px solid rgba(0,0,0,0.1); padding-left: 10px;}"
    html+="</style></head><body>"
    html+="<div class='title'>ABF File Information</div>"
    html+="<code>%s</code><br><br><br>"%h.abfFileName    
    
    
    ### FIELDS WE INTEND TO TAKE OUTSIDE THIS CLASS
    html+="<div style='background-color: #EEEEFF; padding: 10px; margin: 10px;'>"
    html+="<div class='title2'>Simplified ABF Data Access</div>"
    msg="These python objects are intended to provide intuitive access to all useful ABF information."
    html+="<div class='subtitle'>%s</div><br>"%msg
    
    html+="<div class='title'>ABFheader.info (dictionary of objects)</div>"
    html+="<div class='block'>"
    for key in sorted(h.info.keys()):
        html+="%s = %s<br>"%(key,str(h.info[key]))
    html+="</div><br><br>"
    
    html+="<div class='title'>ABFheader.epochs (dictionary of lists)</div>"
    html+="<div class='block'>"
    for key in sorted(h.epochs.keys()):
        print(str(h.epochs[key]))
        html+="%s = %s<br>"%(key,str(h.epochs[key]))
    html+="</div>"
    
    html+="</div><br>"
    
    
    
    ### INTERNAL FIELDS
    html+="<div style='background-color: #FFEEEE; padding: 10px; margin: 10px;'>"    
    html+="<div class='title2'>Full ABF Header</div>"
    msg="All python objects here available as part of the via the ABFheader class. "
    msg+="However, these items can be a bit overwhelming. "
    msg+="Rather than access these features directly, expose them via ABFheader.info"
    html+="<div class='subtitle'>%s</div><br>"%msg
    
    html+="<div class='title'>Header</div>"
    html+="<div class='block'>"
    for key in sorted(h.header.keys()):
        html+="%s = %s<br>"%(key,str(h.header[key]))
    html+="</div><br><br>"    
    
    html+="<div class='title'>Section Map (byte order)</div>"
    html+="<div class='block'>"
    d=h.sectionMap
    sectionStartAndName=sorted([[d[x]['byteStart'],x] for x in d.keys()])
    for sectionName in [x[1] for x in sectionStartAndName]:
        d=h.sectionMap[sectionName]        
        sectionName=sectionName.rjust(20).replace(" ","&nbsp;")
        if d['entryCount']==0:
            html+="<span style='color: #CCC;'>%s</span>"%(sectionName)
        else:
            html+="%s"%(sectionName)
            html+=" %d x %d bytes "%(d['entryCount'],d['entrySize'])
            html+="(%.02f kb)"%(d['entryCount']*d['entrySize']/1024)
            html+=" [bytes %d-%d]"%(d['byteStart'],d['byteLast'])
            html+=" [blocks %d-%.02f]"%(d['byteStart']/512,d['byteLast']/512)
        html+="<br>"
    html+="</div><br><br>"
    
    html+="<div class='title'>Strings</div>"
    html+="<div class='block'>"
    for stringNumber,stringText in enumerate(h.strings):
        html+="%04d: %s<br>"%(stringNumber,stringText)
    html+="</div><br><br>"    
    
    html+="<div class='title'>All Strings</div>"
    html+="<div class='block'>"
    for stringNumber,stringText in enumerate(h.stringsAll):
        stringText=stringText.replace("<",'&lt;').replace(">",'&gt;')
        html+="%04d: %s<br>"%(stringNumber,stringText)
    html+="</div><br><br>"   
    
    html+="<div class='title'>Protocol</div>"
    html+="<div class='block'>"
    d=h.protocol[0]
    for key in sorted(d.keys()):
        html+="%s = %s<br>"%(key,str(d[key]))
    html+="</div><br><br>"   

    html+="<div class='title'>Tags</div>"
    html+="<div class='block'>"
    if len(h.tags)==0:
        html+="<br>(none)<br>&nbsp;"
    for tagNum,tag in enumerate(h.tags):
        html+="<br><b><u>TAG %d</b></u><br>"%tagNum
        for key in sorted(tag.keys()):
            html+="%s = %s<br>"%(key,str(tag[key]))
    html+="</div><br><br>"  
        
    html+="<div class='title'>Epochs</div>"
    html+="<div class='block'>"
    for i,d in enumerate(h.epochPerDac):
        html+="<br><b><u>EPOCH %d</b></u><br>"%i
        for key in sorted(d.keys()):
            html+="%s = %s<br>"%(key,str(d[key]))
    html+="</div><br><br>" 
    
    html+="<div class='title'>DAC Information (ABFheader.dac[0])</div>"
    html+="<div class='block'>"
    d=h.dac[0]
    for key in sorted(d.keys()):
        html+="%s = %s<br>"%(key,str(d[key]))
    html+="</div><br><br>" 
    
    html+="<div class='title'>ADC Information (ABFheader.adc[0])</div>"
    html+="<div class='block'>"
    d=h.adc[0]
    for key in sorted(d.keys()):
        html+="%s = %s<br>"%(key,str(d[key]))
    html+="</div><br><br>" 
    
    html+="</div>"
    html+="</code></body></html>"
    if htmlFileName is None:
        #htmlFileName=h.abfFileName+".html"
        htmlFileName=os.path.abspath(os.path.dirname(__file__)+"/temp/"+h.info["abfID"]+".html")
        if not os.path.exists(os.path.dirname(htmlFileName)):
            os.mkdir(os.path.dirname(htmlFileName))
    with open(htmlFileName,'w') as f:
        f.write(html)
    print('wrote',htmlFileName)
    return