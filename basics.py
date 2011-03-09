#! /usr/bin/env python

import sys, os
import math


class Vertex:

    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def distance(self, v):
        return math.sqrt((self.x-v.x)**2  + (self.y-v.y)**2 + (self.z -v.z)**2)

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
    def __init__(self, v1 = Vertex(), v2= Vertex()):
        self.start = v1
        self.end = v2
        self.dx = v2.x - v1.x
        self.dy = v2.y - v1.y

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
    
class Polygon:
    def __init__(self, vertices=[Vertex()]):
        self.vertices = vertices

    def isSimple(self):
        pass
    def isConvex(self):
        pass
    def area(self):
        pass
    

v1 = Vertex(0,1)
v2 = Vertex(1,0)
v3 = Vertex(1,1)
v4 = Vertex(2,2)
v5 = Vertex(5,5)

if __name__ == "__main__":
    print "testing the logic"
    
