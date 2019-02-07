#!/usr/bin/env python3

"""
Usage:
ttaf2srt subtitlefilettafinput.xml > output.srt

From https://github.com/haraldF/ttaf2srt
edited for 'SWR - Pälzisch im Abgang' subtitles
www.swr.de/paelzisch-im-abgang/
and 'Tatort' subtitles.
"""
"""
From https://github.com/haraldF/ttaf2srt

ttaf2srt

Simple python script to convert ttaf subtitles to srt subtitles.
Note - only tested on German 'Tatort' subtitles.
Note2 - if using vlc or mplayer, make sure to specify 'utf8' as encoding, otherwise, special characters will not render correctly.
"""
import sys
from xml.dom import minidom

def dumpText(item):
    for child in item.childNodes:
        if child.nodeType == child.TEXT_NODE:
            print(child.nodeValue, end="")
        elif child.nodeType == child.ELEMENT_NODE:
            if child.nodeName == "tt:br":
                print()
            elif child.nodeName == "tt:span":
                print("<font color=\"" + styles[child.getAttribute("style")] + "\">", end="")
                dumpText(child)
                print("</font>", end="")
            else:
                print("Unknown Node: " + child.nodeName, file=sys.stderr)

def dumpHeader(item, subCount):
    print(subCount)
    begin = item.getAttribute("begin")
    end = item.getAttribute("end")
    # ### this is a silly hack - for some reason, my ttaf files all start at hour 10? Resetting
    # the hour makes it work again
    begin = '0' + begin[1:]
    end = '0' + end[1:]
    print(begin + " --> " + end)

def parseStyles(styles):
    result = {}
    for style in styles:
        result[style.getAttribute('xml:id')] = style.getAttribute('tts:color')
    return result

with open(sys.argv[1]) as f:
    xmldoc = f.read().replace('\n', ' ').replace('\r', '')
xmldoc = minidom.parseString(xmldoc)

header = xmldoc.getElementsByTagName('tt:head')
if len(header):
    styling = header[0].getElementsByTagName('tt:styling')
    if len(styling):
        styles = parseStyles(styling[0].getElementsByTagName('tt:style'))

body = xmldoc.getElementsByTagName('tt:body')

itemlist = body[0].getElementsByTagName('tt:p') 

subCount = 0

for item in itemlist:
    if item.hasAttribute('xml:id'):
        dumpHeader(item, subCount)
        subCount += 1
        if item.hasAttribute('style'):
            color = styles[item.getAttribute("style")]
        if color:
            print("<font color=\"" + color + "\">", end="")
        dumpText(item)
        if color:
            print("</font>", end="")
        print("\n")
