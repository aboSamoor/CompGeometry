#! /usr/bin/env python

from window import *
import sweep
import pyglet
import sys
import basics
import os
from optparse import OptionParser

def getVertex(line):
    x, y = line.split(',')
    return basics.Vertex(float(x), float(y))

def parse_lines_file(fName):
    absName = os.path.abspath(fName)
    lines = open(absName, 'r').read().splitlines()
    if len(lines) % 2 != 0:
        print "File format error"
        sys.exit()
    vectors = []
    for i in range(0, len(lines), 2):
        start = getVertex(lines[i])
        end = getVertex(lines[i + 1])
        if start.x < end.x:
            vectors.append(basics.Vector(start, end))
        else:
            vectors.append(basics.Vector(end, start))
    return vectors


def parse_polygons_file(fName):
    absName = os.path.abspath(fName)
    lines = open(absName, 'r').read().splitlines()
    vertices = []
    for i in range(0, len(lines)):
        vertices.append(getVertex(lines[i]))
    poly = basics.Polygon(vertices)
    return poly.getVectors()

def parse_file(fName):
    base, ext = os.path.splitext(fName)
    if ext == ".p":
        return parse_polygons_file(fName)
    return parse_lines_file(fName)

if __name__ == "__main__":
#    pyglet.clock.schedule(update)
    parser = OptionParser()
    parser.add_option("-f", "--file", dest = "filename", help = "File contains points, *.p files contain polygons, *.l contain lines", metavar = "FILE")
    parser.add_option("-x", "--novisual", action = "store_false", dest = "visual", default = True, help = "run visualization of the algorithm")
    (options, args) = parser.parse_args()
    if options.filename:
         user.lines = parse_file(options.filename)
    for line in user.lines:
        for e in sweep.Event.lineEvents(line):
            ottman.addEvent(e)
    if options.visual:
        pyglet.app.run()
