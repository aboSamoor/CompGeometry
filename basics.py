#! /usr/bin/env python

import sys, os
import math


class Vertex(object):

    def __init__(self, x = 0, y = 0, z = 0):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return "Point: " + str(self.x) + " " + str(self.y)

    def coordinates(self):
        return [self.x, self.y]

    def __add__(self, v):
        if hasattr(v, 'x'):
            return Vertex(self.x + v.x, self.y + v.y)
        return Vertex(self.x + v, self.y + v)

    def __sub__(self, v):
        if hasattr(v, 'x'):
            return Vertex(self.x - v.x, self.y - v.y)
        return Vertex(self.x - v, self.y - v)

    def __mul__(self, v2):
        if hasattr(v2, 'x'):
            return self.x * v2.x + self.y * v2.y
        return Vertex(self.x * v2, self.y * v2)

    def __eq__(self, v2):
        return self.x == v2.x and self.y == v2.y

    def distance(self, v):
        return math.sqrt((self.x - v.x) ** 2 + (self.y - v.y) ** 2 + (self.z - v.z) ** 2)

    def cProduct2D(self, vector):
        return vector.cPPoint2D(self)

    def collinear(self, vector):
        return self.cProduct2D(vector) == 0

    def toVector(self, v2):
        return vector(self, v2)

    def leftOf(self, vector):
        return vector.cPPoint2D(self) > 0

    def leftOfOn(self, vector):
        return vector.cPPoint2D(self) >= 0


class Vector():
    def __init__(self, v1 = Vertex(), v2 = Vertex()):
        self.start = v1
        self.end = v2
        self.dx = v2.x - v1.x
        self.dy = v2.y - v1.y

    def __str__(self):
        return "Vector: " + self.start.__str__() + " -->  " + self.end.__str__()

    def coordinates(self):
        tmp = []
        tmp = self.start.coordinates()
        tmp.extend(self.end.coordinates())
        return tmp

    def cPVector2D(self, vector):
        return (self.dx * vector.dy) - (self.dy * vector.dx)

    def cPPoint2D(self, vertex):
        return self.cPVector2D(Vector(self.start, vertex))

    def length(self):
        return self.start.distance(self.end)

    def collinear(self, vertex):
        return vertex.collinear(self)

    def intersectP(self, vector):
        if self.collinear(vector.start) or self.collinear(vector.end) or vector.collinear(self.start) or vector.collinear(self.end):
            return False
        if (vector.start.leftOf(self) ^ vector.end.leftOf(self)) and (self.start.leftOf(vector) ^ self.end.leftOf(vector)):
            return True
        return False

    def intersect(self, vector):
        if (vector.start.leftOf(self) ^ vector.end.leftOf(self)) and (self.start.leftOf(vector) ^ self.end.leftOf(vector)):
            return True
        return False

    def xPoint(self, vector):
        if self.intersectP(vector):
            E = self.end - self.start
            F = vector.end - vector.start
            P = Vertex(-self.dy, self.dx)
            h = (((self.start - vector.start) * P) / (float(F * P)))
            return vector.start + (F * h)
        return None

class Polygon:
    def __init__(self, vertices = []):
        self.vertices = vertices
    def coordinates(self):
        res = []
        for v in self.vertices:
            res.extend(v.coordinates())
        return res

    def getVectors(self):
        vectors = []
        for i in range(0, len(self.vertices)):
            start = self.vertices[i]
            end = self.vertices[(i + 1) % len(self.vertices)]
            if start.x < end.x:
                vectors.append(Vector(start, end))
            else:
                vectors.append(Vector(end, start))
        return vectors


    def isSimple(self):
        pass
    def isConvex(self):
        pass
    def area(self):
        pass


v1 = Vertex(0, 1)
v2 = Vertex(1, 0)
v3 = Vertex(1, 1)
v4 = Vertex(2, 2)
v5 = Vertex(5, 5)

if __name__ == "__main__":
    print "testing the logic"

