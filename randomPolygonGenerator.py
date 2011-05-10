#! /usr/bin/env python


import os, sys
import random

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "usage: $randomPolygonGenerator.py size"
    size  = int (sys.argv[1])
    points = []
    text = []
    for i in range(size):
        points.append((random.randint(0,500),random.randint(0,500)))
    for i in range(size):
        x,y = points[i]
        text.append(str(x)+","+str(y))
    open("polygon-"+str(size)+".p",'w').write('\n'.join(text))
