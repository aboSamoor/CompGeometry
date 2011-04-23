#! /usr/bin/env python

import graph
import basics


class Event(graph.Node):
    Lstart, Lend, xPoint = 0, 1, 2
    def __init__(self, key, eventType, vertex, lines):
        super(Event, self).__init(key, [], None, None, None)
        self.eventType = eventType
        self.point = vertex
        self.lines = lines

    def convertLine(vector):
        startE = Event(vector.start.x, Event.Lstart, vector.start, [vector])
        endE = Event(vector.end.x, Event.Lend, vector.end, [vector])

class Sweep(object):
    def __init__(self, events):
        self.EQ = graph.Heap()
        for e in events:
            self.EQ.insert(e)
        self.SL = graph.BSTree()
    def extract_next(self):
        return self.EQ.extract_next()
    def next(self):
        return self.EQ.next()
    def process(self):
        pass

class sweepCrossingLines(sweep):
    def __init__(self, points):
        super(sweepCrossingLines, self).__init__(events)
    def __newLineEvent(self, event):
        event.key = event.coordinates[1]
        self.SL.insert(event)
        pre = self.SL.predecessor(event)
        succ = self.SL.successor(event)
        if pre:
            if pre.lines[0].intersect(event.lines[0]):
                pass
#                self.EQ.insert()
        if succ:
            if succ.lines[0].intersect(event.lines[0]):
                pass
#                self.EQ.insert()
    def __endLineEvent(self, event):
        event.key = event.point.y
        pre = self.SL.predecessor(event)
        succ = self.SL.successor(event)
        self.SL.delete(event)
        if pre and succ:
            if pre.lines[0].intersect(succ.lines[0]):
                pass
#                self.EQ.insert()
    def __crossingPointEvent(self, event):
        keys = [(line.key, line) for line in event.lines]
        keys.sort()
        lines = [pair[1] for pair in keys]
        lines.reverse()
        for i in range(len(lines)):
            self.SL.delete(lines[i].start)
            Lines[i].start.key = keys[i][0]
            self.SL.insert(lines[i].start)
        pass
    def process(self):
        if not self.EQ.empty():
            e = self.next()
            if e.eventType == Event.Lstart:
                self.__newLineEvent(e)
            elif e.eventType == Event.Lend:
                self.__endLineEvent(e)
            elif e.eventType == Event.xPoint:
                self.__crossingPointEvent(e)

if __name__ == "__main__":
        print "hi"
