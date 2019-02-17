from Point import *
import random


class Segment:
    def __init__(self, start: 'Point', end: 'Point'):
        self.start = start
        self.end = end

    def __repr__(self):
        return '({}, {})'.format(self.start, self.end)

    def getRandomPoint(self, lower: int, upper: int, flightType: str) -> 'Point':
        a = self.end.y - self.start.y
        b = self.start.x - self.end.x
        c = a * self.start.x + b * self.start.y

        x = random.uniform(self.start.x, self.end.x)
        if b == 0:
            y = random.uniform(self.start.y, self.end.y)
        else:
            y = c / b - a / b * x
        z = random.randint(upper, upper + 100)

        return Point(x, y, z)

    @staticmethod
    def doIntersect(s_1: 'Segment', s_2: 'Segment') -> bool:

        # orientation of the (self.tail, self.head, s_2.tail) triangle
        s_1_orientation_tail = Point.orientation2D(s_1.end, s_1.start, s_2.end)

        # orientation of the (self.tail, self.head, s_2.head) triangle
        s_1_orientation_head = Point.orientation2D(s_1.end, s_1.start, s_2.start)

        # orientation of the (s_2.tail, s_2.head, self.tail) triangle
        s_2_orientation_tail = Point.orientation2D(s_2.end, s_2.start, s_1.end)

        # orientation of the (s_2.tail, s_2.head, self.head) triangle
        s_2_orientation_head = Point.orientation2D(s_2.end, s_2.start, s_1.start)

        # general case
        if s_1_orientation_tail != s_1_orientation_head and s_2_orientation_tail != s_2_orientation_head:
            return True

        # collinear case
        if s_1_orientation_tail == 0 and s_1_orientation_head == 0 and s_2_orientation_tail == 0 and s_2_orientation_head == 0:

            if s_1.end.between2D(s_2.start, s_2.end) or s_1.start.between2D(s_2.start, s_2.end) \
                    or s_2.end.between2D(s_1.start, s_1.end) or s_2.start.between2D(s_1.start, s_1.end):
                return True
        return False