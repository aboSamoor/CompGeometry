#! /usr/bin/env python
import pyglet
import itertools
import graph 

win = pyglet.window.Window()
label = pyglet.text.Label('Rami Eid')

vertices = []
lines = []
polygons = [[]]

fps_display = pyglet.clock.ClockDisplay()
run = False
mode = "vertex"

EQ = ""

def updatePts(points, opX, opY):
    for i in range(0,2*(len(points)/2),2):
        points[i] = opX(points[i])
        points[i+1] = opY(points[i+1])

@win.event
def on_mouse_press(x, y, button, modifiers):
    global vertices, polygons, lines, EQ
    if button == pyglet.window.mouse.LEFT:
        if mode == "polygon":
            polygons[-1].append(x)
            polygons[-1].append(y)
        elif mode == "vertex":
            vertices.append(x)
            vertices.append(y)
            node = graph.Node(x , children= [None, None], data = (x,y))
            if len(vertices) == 2:
                EQ = graph.BST(node) 
            else:
                EQ.insert(node)
            print "\n\ninorder sorted points"
            print EQ.toString(graph.Tree.INORDER) 
            print "\npreorder sorted points"
            print EQ.toString(graph.Tree.PREORDER) 
            print "\nThe actual points"
            for i in xrange(0,len(vertices), 2):
                print vertices[i],
        elif mode == "line":
            lines.append(x)
            lines.append(y)

@win.event
def on_key_press(symbol, modifiers):
    global run
    global mode, polygons, vertices
    if symbol == pyglet.window.key.S:
        run = not run
    if symbol == pyglet.window.key.L:
        mode = "line"
    if symbol == pyglet.window.key.P:
        mode = "polygon"
    if symbol == pyglet.window.key.V:
        mode = "vertex"
    if symbol == pyglet.window.key.N:
        if mode == "polygon":
            polygons.append([])


def validVertex(vertex):
    x,y = vertex
    X,Y = win.get_size()
    if x > 0 and x < X and y > 0 and y < Y:
        return True

def boundary(vertex):
    x,y = vertex
    result = []
    shift = 1
    x_range = range(x-shift, x+shift+1)
    y_range = range(y-shift, y+shift+1)
    result = [v for v in itertools.product(x_range,y_range)] 
    return result
       
def validBoundary(vertex):
    return filter(validVertex, boundary(vertex)) 

def magnify(vertices):
    result = []
    if len(vertices)%2 > 0:
        print "error in vertices"
    for i in range(0, len(vertices), 2):
        result.extend(validBoundary((vertices[i],vertices[i+1])))
    return result

def drawVertices(points):
    toBeDrawn = []
    for v in magnify(points):
        x,y = v
        toBeDrawn.append(x)
        toBeDrawn.append(y)
    pyglet.graphics.draw(len(toBeDrawn)/2, pyglet.gl.GL_POINTS,('v2i', toBeDrawn))
    

def drawPolygons(polygons):
    for poly in polygons:
        if len(poly) > 2:
            pyglet.graphics.draw(len(poly)/2, pyglet.gl.GL_LINE_LOOP,('v2i', poly))
        else:
            drawVertices(poly)

def drawLines(lines):
    size = len(lines)
    if size%4 in [1,3]:
        print "error in lines"
        return -1
    if size%4 == 2:
        if size>3:
            pyglet.graphics.draw(size/2-1, pyglet.gl.GL_LINES,('v2i', lines[:-2]))
        drawVertices(lines[-2:])
    else:
        pyglet.graphics.draw(size/2, pyglet.gl.GL_LINES,('v2i', lines))

@win.event
def on_draw():
    global polygons, lines, vertices
    win.clear()
    drawVertices(vertices)
    drawPolygons(polygons)
    drawLines(lines)
#    pyglet.graphics.draw_indexed(4, pyglet.gl.GL_TRIANGLES, [0, 1, 2, 0, 2], ('v2i', (100, 100, 150, 100, 150, 150, 100, 150)))
    fps_display.draw()

def update(dt):
    if run:
        global vertices
        X,Y = win.get_size()
        updatePts(vertices, lambda x: (x+1)%X, lambda x: (x+1)%Y)

pyglet.clock.schedule(update)
pyglet.app.run()
