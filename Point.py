from math import sqrt
from sys import maxsize
from Flight import *

class Point:
    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0):

        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return '({}, {}, {})'.format(self.x, self.y, self.z)

    def __eq__(self, other: 'Point'):
        return (self.x == other.x) and (self.y == other.y) and (self.z == other.z)

    def __ne__(self, other: 'Point'):
        return not self.__eq__(other)

    def __lt__(self, other: 'Point'):
        return self.x < other.x or (self.x == other.x and self.y < other.y) or (self.x == other.x and
                                                                                self.y == other.y and
                                                                                self.z < other.z)

    def __gt__(self, other: 'Point'):
        return self.x > other.x or (self.x == other.x and self.y > other.y) or (self.x == other.x and
                                                                                self.y == other.y and
                                                                                self.z > other.z)

    def __sub__(self, other: 'Point'):
        return Point(self.x - other.x, self.y - other.y, self.z - other.z)

    def euclidean_distance(self, b: 'Point') -> float:
        return sqrt((b.x - self.x)**2 + (b.y - self.y)**2 + (b.z - self.z)**2)

    def euclidean_distance_2D(self, b: 'Point') -> float:
        return sqrt((b.x - self.x)**2 + (b.y - self.y)**2)

    def euclidean_distance_3D(self, b: 'Point') -> float:
        return sqrt((b.x - self.x)**2 + (b.y - self.y)**2 + (b.z - self.z)**2)

    def between2D(self, p1: 'Point', p2: 'Point'):
        return min(p1.x, p2.x) <= self.x <= max(p1.x, p2.x) and min(p1.y, p2.y) <= self.y <= max(p1.y, p2.y)

    @staticmethod
    def orientation2D(a: 'Point', b: 'Point', c: 'Point'):
        p1: Point = b - a
        p2: Point = c - a

        crossProduct = p1.x * p2.y - p1.y * p2.x

        if crossProduct > 0:
            return 1 # Left orientation, counter clockwise direction
        elif crossProduct < 0:
            return 0 # Right orientation, clockwise direction
        else:
            return -1 # Colinear points

    def calculateCoordinates(self, endingPoint, velocity: float):
        if self.x - endingPoint.x != 0:
            m = (self.y - endingPoint.y) / (self.x - endingPoint.x)
            b = (self.x * self.y - endingPoint.x * self.y) / (self.x - endingPoint.x)
            self.x += velocity
            self.y = m * self.x + b
        else:
            print("Izasao")


class EventPoint(Point):
    def __init__(self, eventType: str, point: Point, flight):
        super().__init__(point.x, point.y, point.z)
        self.eventType = eventType
        self.flightIdentifier = flight