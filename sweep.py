#! /usr/bin/env python

import graph
import basics


class Event(graph.Node):
    def __init__(self, vectors):
        #the node should have exactly 2 children
        self.point = self.__getPoint()
        super(Event, self).__init__(self.point.x, [None, None])
        self.vectors = vectors
        self.type = "Event"

    def __getPoint(self):
        return self.point

    def __str__(self):
        return ''.join([self.type, self.point.__str__()])

    def process(self):
        pass

    @staticmethod
    def lineEvents(vector):
        s = startEvent(vector)
        e = endEvent(vector)
        s.endEvent = e
        e.startEvent = s
        return [s, e]

class startEvent(Event):
    def __init__(self, line):
        self.point = line.start
        super(startEvent, self).__init__([line])
        self.endEvent = None
        self.slEvents = []
        self.type = "Start"


    def process(self, EQ, SL):
        lineEvent = slEvent(self)
        SL.insert(lineEvent)
        pre = SL.predecessor(lineEvent)
        succ = SL.successor(lineEvent)
        if pre and pre.eqEvent.vectors[0].intersectP(self.vectors[0]):
            x1 = crossEvent([pre, lineEvent])
            EQ.insert(x1)
        if succ and succ.eqEvent.vectors[0].intersectP(self.vectors[0]):
            x2 = crossEvent([lineEvent, succ])
            EQ.insert(x2)

class endEvent(Event):
    def __init__(self, line):
        self.point = line.end
        super(endEvent, self).__init__([line])
        self.startEvent = None
        self.type = "End"

    def process(self, EQ, SL):
        line = self.startEvent.slEvents[0]
        pre = SL.predecessor(line)
        succ = SL.successor(line)
        SL.delete(line)
        if pre and succ:
            if pre.eqEvent.vectors[0].intersect(succ.eqEvent.vectors[0]):
                if event.eqEvent.vectors[0].start.x < pre.eqEvent.vectors[0].start.x:
                    EQ.insert(crossEvent([succ, pre]))

class crossEvent(Event):
    def __init__(self, slEvents):
        if len(slEvents) != 2:
            print "Error: can not calculate intersection for less than 2 lines"
            return None
        self.point = slEvents[0].vectors[0].xPoint(slEvents[1].vectors[0])
        super(crossEvent, self).__init__([lambda e: e.vectors[0], slEvents])
        self.slEvents = slEvents
        self.startEvent = None
        self.endEvent = None
        self.type = "Cross"

    def process(self, EQ, SL):
        keys = [(e.key, e) for e in self.slEvents]
        keys.sort()
        lines = [pair[1] for pair in keys]
        lines.reverse()
        for i in range(len(lines)):
            SL.delete(lines[i])
            lines[i].key = keys[i][0]
            SL.insert(lines[i])



class slEvent(startEvent):
    def __init__(self, event):
        super(slEvent, self).__init__(event.vectors[0])
        self.eqEvent = event
        self.key = event.point.y
        self.type = "slEvent"
        event.slEvents.append(self)

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

class sweepCrossingLines(Sweep):
    def __init__(self, points = []):
        super(sweepCrossingLines, self).__init__(points)

    def process(self):
        if not self.EQ.empty():
            e = self.next()
            e.process(self.EQ, self.SL)
            self.extract_next()
            yield e.point

    def addEvent(self, event):
        self.EQ.insert(event)

if __name__ == "__main__":
        print "hi"


#TODO:
# 1- remove redundant crossing points !
