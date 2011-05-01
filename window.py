#! /usr/bin/env python
import pyglet
import itertools
import graph
import sweep
import basics

win = pyglet.window.Window()
label = pyglet.text.Label('Rami Eid')

fps_display = pyglet.clock.ClockDisplay()
run = False
mode = "line"

ottman = sweep.sweepCrossingLines()

class Environment():
    def __init__(self, color = (1.0, 1.0, 1.0, 1.0)):
        self.points = []
        self.lines = []
        self.polygons = []
        self.lineStart = []
        self.color = color

    def getCoords(self, items):
        coords = []
        for item in items:
            coords.extend([int(v) for v in item.coordinates()])
        return coords

    def drawVertices(self, pts = []):
        toBeDrawn = self.getCoords(pts) if pts != [] else self.getCoords(self.points)
        pyglet.graphics.draw(len(toBeDrawn) / 2, pyglet.gl.GL_POINTS, ('v2i', toBeDrawn))

    def drawPolygons(self):
        for poly in self.polygons:
            if len(poly) > 2:
                pyglet.graphics.draw(len(poly), pyglet.gl.GL_LINE_LOOP, ('v2i', poly))
            else:
                self.drawVertices(poly)

    def drawLines(self, segments = []):
        lines = self.getCoords(segments) if segments != [] else self.getCoords(self.lines)
        size = len(lines)
        if size % 4 in [1, 3]:
            print "error in lines"
            return - 1
        if size % 4 == 2:
            if size > 3:
                pyglet.graphics.draw(size / 2 - 1, pyglet.gl.GL_LINES, ('v2i', lines[:-2]))
            self.drawVertices(lines[-2:])
        else:
            pyglet.graphics.draw(size / 2, pyglet.gl.GL_LINES, ('v2i', lines))

    def draw(self):
        pyglet.gl.glColor4f(*self.color)
        self.drawVertices(self.points)
        self.drawPolygons()
        self.drawLines(self.lines)
        self.drawVertices(self.lineStart)

user = Environment()
demonstration = Environment((1.0, 0, 0, 1.0))

def updatePts(points, opX, opY):
    for i in range(0, 2 * (len(points) / 2), 2):
        points[i] = opX(points[i])
        points[i + 1] = opY(points[i + 1])

@win.event
def on_mouse_press(x, y, button, modifiers):
    if button == pyglet.window.mouse.LEFT:
        if mode == "polygon":
            v = basics.Vertex(x, y)
            polygons[-1].points.append(v)
        elif mode == "vertex":
            v = basics.Vertex(x, y)
            user.points.append(v)
        elif mode == "line":
            v = basics.Vertex(x, y)
            user.lineStart.append(v)
            if len(user.lineStart) == 2:
                v1 = basics.Vertex(user.lineStart[0].x, user.lineStart[0].y)
                v2 = basics.Vertex(user.lineStart[1].x, user.lineStart[1].y)
                if user.lineStart[0].x < user.lineStart[1].x:
                    vector = basics.Vector(v1, v2)
                else:
                    vector = basics.Vector(v2, v1)
                user.lines.append(vector)
                for e in sweep.Event.lineEvents(user.lines[-1]):
                    ottman.addEvent(e)
                user.lineStart = []
@win.event
def on_key_press(symbol, modifiers):
    global run
    global mode, polygons, vertices, vectors
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
            polygons.append(basics.Polygon())
    if symbol == pyglet.window.key.X:
        for vertex in ottman.process():
            print vertex
            print ottman.EQ
            X, Y = win.get_size()
            v1 = basics.Vertex(vertex.x, 0)
            v2 = basics.Vertex(vertex.x, Y)
            demonstration.lines.append(basics.Vector(v1, v2))


def validVertex(vertex):
    x, y = vertex
    X, Y = win.get_size()
    if x > 0 and x < X and y > 0 and y < Y:
        return True

def boundary(vertex):
    x, y = vertex
    result = []
    shift = 1
    x_range = range(x - shift, x + shift + 1)
    y_range = range(y - shift, y + shift + 1)
    result = [v for v in itertools.product(x_range, y_range)]
    return result

def validBoundary(vertex):
    return filter(validVertex, boundary(vertex))

def magnify(vertices):
    result = []
    if len(vertices) % 2 > 0:
        print "error in vertices"
    for i in range(0, len(vertices), 2):
        result.extend(validBoundary((vertices[i], vertices[i + 1])))
    return result

@win.event
def on_draw():
    global polygons, lines, vertices
    win.clear()
    user.draw()
    demonstration.draw()
#    drawVertices(vertices)
#    drawPolygons(polygons)
#    drawLines(user.getLinesCoords())
#    drawLines(demonstration.getLinesCoords())
#    drawVertices(user.lineStart)
#    pyglet.graphics.draw_indexed(4, pyglet.gl.GL_TRIANGLES, [0, 1, 2, 0, 2], ('v2i', (100, 100, 150, 100, 150, 150, 100, 150)))
#    fps_display.draw()

def update(dt):
    if run:
        global vertices
        X, Y = win.get_size()
        updatePts(vertices, lambda x: (x + 1) % X, lambda x: (x + 1) % Y)

pyglet.clock.schedule(update)
pyglet.app.run()
