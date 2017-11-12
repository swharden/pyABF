"""
Colormap collection - the purpose of this script is to create demo graphs of common ABF plots using all
available colormaps. Colormaps with extremely light traces are skipped. Graphics are saved and an HTML
page is made to view them, which can be easily converted to PDF.
"""

import os
import sys
sys.path.append("../../src/")
sys.path.insert(0,sys.path.pop())
import numpy as np

import pyabf
import matplotlib.pyplot as plt
import webbrowser

def makeFigure1(colormap):
    abf=pyabf.ABF("../../data/17o05028_ic_steps.abf")
    plt.figure(figsize=(6,3))
    for sweep in abf.sweepList[::3]:
        color = plt.cm.get_cmap(colormap)(sweep/abf.sweepCount)
        abf.setSweep(sweep)
        plt.plot(abf.dataX,abf.dataY,color=color)
    plt.margins(0,.1)
    plt.axis([0,1,None,None])
    plt.gca().axis('off') # remove square around edges
    plt.xticks([]) # remove x labels
    plt.yticks([]) # remove y labels
    plt.tight_layout()
    plt.savefig("_output/1_%s.png"%colormap,dpi=150)
    plt.show()
    plt.close()
    return

def makeFigure2(colormap):
    abf=pyabf.ABF("../../data/17o05026_vc_stim.abf")
    plt.figure(figsize=(6,3))
    for sweep in abf.sweepList[::-1]:
        color = plt.cm.get_cmap(colormap)(sweep/abf.sweepCount)
        abf.setSweep(sweep)
        abf.dataY[:-int(abf.pointsPerSec*1)]=np.nan
        abf.dataY+=4*sweep
        plt.plot(abf.dataX+.05*sweep,abf.dataY,color=color,alpha=.7)
    plt.margins(0,0)
    plt.gca().axis('off') # remove square around edges
    plt.xticks([]) # remove x labels
    plt.yticks([]) # remove y labels
    plt.tight_layout()
    plt.savefig("_output/2_%s.png"%colormap,dpi=150)
    plt.show()
    plt.close()
    return

if __name__=="__main__":
    
    if not os.path.exists("_output"):
        os.mkdir("_output")
    
    validColors=[]
    cutoff=.3 # try to only plot colors which don't have really light traces
    for colormap in sorted(plt.cm.datad):
        if np.mean(plt.cm.get_cmap(colormap)(.01)[:3])<cutoff:
            print(colormap,"is too light at the end")
        elif np.mean(plt.cm.get_cmap(colormap)(.99)[:3])<cutoff:
            print(colormap,"is too light at the start")
        elif np.mean(plt.cm.get_cmap(colormap)(.5)[:3])<cutoff:
            print(colormap,"is too light in the middle")
        elif "Pastel" in colormap:
            print(colormap,"is too pastel")
        else:
            print(colormap,"is plotting...")
            makeFigure1(colormap)
            makeFigure2(colormap)
            validColors.append(colormap)
    
    with open("_output/index.html",'w') as f:
        html="<html><body>"
        for colormap in sorted(validColors):
            html+="<h1>%s</h1>"%colormap
            html+="<img src='1_%s.png'> <br><br>"%colormap
            html+="<img src='2_%s.png'> "%colormap
            html+="<div style='page-break-after: always;'></div>"
        html+="</body></html>"
        f.write(html)
        webbrowser.open(os.path.abspath("_output/index.html"))
    
    print("DONE")