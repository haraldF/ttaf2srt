#!/usr/bin/env python3

import sys
from xml.dom import minidom

def dumpText(item):
    for child in item.childNodes:
        if child.nodeType == child.TEXT_NODE:
            print(child.nodeValue, end="")
        elif child.nodeType == child.ELEMENT_NODE:
            if child.nodeName == "br":
                print()
            elif child.nodeName == "span":
                print("<font color=\"" + child.getAttribute("tts:color") + "\">", end="")
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
        result[style.getAttribute('id')] = style.getAttribute('tts:color')
    return result

xmldoc = minidom.parse(sys.argv[1])

header = xmldoc.getElementsByTagName('head')
if len(header):
    styling = header[0].getElementsByTagName('styling')
    if len(styling):
        styles = parseStyles(styling[0].getElementsByTagName('style'))

body = xmldoc.getElementsByTagName('body')

itemlist = body[0].getElementsByTagName('p') 

subCount = 0

for item in itemlist:
    if item.hasAttribute('id'):
        dumpHeader(item, subCount)
        subCount += 1
        color = styles[item.getAttribute("style")]
        if color:
            print("<font color=\"" + color + "\">", end="")
        dumpText(item)
        if color:
            print("</font>", end="")
        print("\n")
