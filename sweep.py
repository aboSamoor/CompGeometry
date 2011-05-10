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
        tmp = vector
        if vector.start.x > vector.end.x:
            tmp = basics.Vector(vector.end, vector.start)
        if vector.start.x == vector.end.x:
            if vector.end.y < vector.start.y:
                tmp = basics.Vector(vector.end, vector.start)
        s = startEvent(tmp)
        e = endEvent(tmp)
        if s.point.x == e.point.x:
            delta = 0.0001
            s.key -= delta
            e.key += delta
        s.endEvent = e
        e.startEvent = s
        return [s, e]

class startEvent(Event):
    def __init__(self, vector):
        self.point = vector.start
        super(startEvent, self).__init__([vector])
        self.endEvent = None
        self.slEvents = []
        self.type = "Start"

    def process(self, sweep):
        lineEvent = slEvent(self)
        sweep.SL.insert(lineEvent)
        pre = sweep.SL.predecessor(lineEvent)
        succ = sweep.SL.successor(lineEvent)
        sweep.checkCrossing(pre, lineEvent)
        sweep.checkCrossing(lineEvent, succ)

class endEvent(Event):
    def __init__(self, line):
        self.point = line.end
        super(endEvent, self).__init__([line])
        self.startEvent = None
        self.type = "End"

    def process(self, sweep):
        line = self.startEvent.slEvents[0]
        pre = sweep.SL.predecessor(line)
        succ = sweep.SL.successor(line)
        try:
            sweep.SL.delete(line)
        except:
            print line, 333
        sweep.checkCrossing(pre, succ)

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

    def process(self, sweep):
        #swap the order of the lines, by taking reversing order of their keys
        self.slEvents = list(set(self.slEvents))
        keys = [(e.key, e) for e in self.slEvents]
        keys.sort()
        lines = [pair[1] for pair in keys]
        lines.reverse()

        #update the lines with the new keys
        for i in range(len(lines)):
            try:
                sweep.SL.delete(lines[i])
            except:
                print lines[i], 333
        for i in range(len(lines)):
            lines[i].key = keys[i][0]
            sweep.SL.insert(lines[i])
        highestLine = lines[-1]
        succ = sweep.SL.successor(highestLine)
        lowestLine = lines[0]
        pre = sweep.SL.predecessor(lowestLine)
        sweep.checkCrossing(highestLine, succ)
        sweep.checkCrossing(lowestLine, pre)


class slEvent(startEvent):
    #it should be a start event
    def __init__(self, event):
        super(slEvent, self).__init__(event.vectors[0])
        self.eqEvent = event
        self.key = event.point.y
        delta = 0.000001
        dy = (event.endEvent.point.y - event.point.y)
        tmp = dy
        if event.endEvent.point.x != event.point.x:
            tmp = dy / event.endEvent.point.x - event.point.x
        self.key += tmp * delta
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
        self.linesHistory = {}
        self.xPointsHistory = {}

    def process(self):
        if not self.EQ.empty():
            e = self.next()
            print e
            e.process(self)
            self.extract_next()
            yield e

    def checkCrossing(self, line1, line2):
        if line1 and line2 and (line1, line2) not in self.linesHistory:
            if line1.eqEvent.vectors[0].intersectP(line2.vectors[0]):
                x1 = crossEvent([line1, line2])
                if x1.point not in self.xPointsHistory:
                    self.EQ.insert(x1)
                    self.xPointsHistory[x1.point] = x1
                else:
                    self.xPointsHistory[x1.point].slEvents.extend([line1, line2])
                    self.xPointsHistory[x1.point].slEvents = list(set(self.xPointsHistory[x1.point].slEvents))
            self.linesHistory[(line1, line2)] = True
            self.linesHistory[(line2, line1)] = True

    def addEvent(self, event):
        self.EQ.insert(event)

if __name__ == "__main__":
        print "hi"
