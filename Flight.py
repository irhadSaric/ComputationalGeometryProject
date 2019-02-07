from Point import *
from copy import deepcopy

class Flight:
    def __init__(self, start: 'Point', end: 'Point', velocity: float):
        self.start = start
        self.end = end
        self.velocity = velocity
        self.currentPosition = deepcopy(start)
        self.closeRange = 50

    def __lt__(self, other: 'Flight'):
        return self.currentPosition.x < other.currentPosition.x or (self.currentPosition.x == other.currentPosition.x and self.currentPosition.y < other.currentPosition.y) or (self.currentPosition.x == other.currentPosition.x and
                                                                                self.currentPosition.y == other.currentPosition.y and
                                                                                self.currentPosition.z < other.currentPosition.z)

    def __gt__(self, other: 'Point'):
        return self.currentPosition.x > other.currentPosition.x or (self.currentPosition.x == other.currentPosition.x and self.currentPosition.y > other.currentPosition.y) or (self.currentPosition.x == other.currentPosition.x and
                                                                                self.currentPosition.y == other.currentPosition.y and
                                                                                self.currentPosition.z > other.currentPosition.z)


    def calculateCurrentPosition(self):
        distanceBetweenStartAndEnd = self.start.euclidean_distance_2D(self.end)
        timeToGoAtoB = distanceBetweenStartAndEnd / self.velocity
        distanceBetweenXCoordinates = self.end.x - self.start.x
        velocityForX = distanceBetweenXCoordinates / timeToGoAtoB

        if (abs(self.currentPosition.x - self.end.x) >= self.velocity or abs(self.currentPosition.y - self.end.y) >= self.velocity) and abs(self.currentPosition.x - self.end.x) != 0:
            m = (self.currentPosition.y - self.end.y) / (self.currentPosition.x - self.end.x)
            b = (self.currentPosition.x * self.end.y - self.end.x * self.currentPosition.y) / (self.currentPosition.x - self.end.x)

            self.currentPosition.x += velocityForX
            self.currentPosition.y = m * self.currentPosition.x + b
        else:
            return -1

    @staticmethod
    def intersects(f1: 'Flight', f2: 'Flight') -> bool:
        if f1.closeRange + f2.closeRange >= f1.currentPosition.euclidean_distance_2D(f2.currentPosition):
            if f1.currentPosition.euclidean_distance_3D(f2.currentPosition) < f1.closeRange:
                return True
        return False

