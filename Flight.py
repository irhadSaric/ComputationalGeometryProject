from Point import *
from copy import deepcopy
import random
from Polygon import *
from Segment import *
import pygame

class Flight:
    def __init__(self, start: 'Point', end: 'Point', velocity: int, flightType: str, path: list, closeRange: int, outsidePoly = False):
        self.start = start
        self.end = end
        self.velocity = velocity
        self.currentPosition = deepcopy(start)
        self.closeRange = closeRange
        self.flightType = flightType
        self.path = path
        self.outsidePoly = outsidePoly

    def __repr__(self):
        return "({},{},{})".format(self.currentPosition.x, self.currentPosition.y, self.currentPosition.z)

    def __lt__(self, other: 'Flight'):
        return self.currentPosition.y > other.currentPosition.y or (self.currentPosition.y == other.currentPosition.y and self.currentPosition.x < other.currentPosition.x) or (self.currentPosition.x == other.currentPosition.x and
                                                                                self.currentPosition.y == other.currentPosition.y and
                                                                                self.currentPosition.z < other.currentPosition.z)

    def __gt__(self, other: 'Point'):
        return self.currentPosition.y < other.currentPosition.y or (self.currentPosition.y == other.currentPosition.y and self.currentPosition.x < other.currentPosition.x) or (self.currentPosition.x == other.currentPosition.x and
                                                                                self.currentPosition.y == other.currentPosition.y and
                                                                                self.currentPosition.z > other.currentPosition.z)

    def calculateCurrentPosition(self):
        distanceBetweenStartAndEnd = self.start.euclidean_distance_3D(self.end)
        timeToGoAtoB = distanceBetweenStartAndEnd / self.velocity
        distanceBetweenXCoordinates = self.end.x - self.start.x
        distanceBetweenZCoordinates = self.end.z - self.start.z
        changeForX = distanceBetweenXCoordinates / timeToGoAtoB
        changeForZ = distanceBetweenZCoordinates / timeToGoAtoB
        if (abs(self.currentPosition.x - self.end.x) >= self.velocity or abs(self.currentPosition.y - self.end.y) >= self.velocity) and abs(self.currentPosition.x - self.end.x) != 0:
            m = (self.currentPosition.y - self.end.y) / (self.currentPosition.x - self.end.x)
            b = (self.currentPosition.x * self.end.y - self.end.x * self.currentPosition.y) / (self.currentPosition.x - self.end.x)

            self.currentPosition.x += changeForX
            self.currentPosition.y = m * self.currentPosition.x + b
            self.currentPosition.z += changeForZ
        else:
            return -1

    @staticmethod
    def intersects(f1: 'Flight', f2: 'Flight') -> bool:
        if f1.closeRange + f2.closeRange >= f1.currentPosition.euclidean_distance_2D(f2.currentPosition):
            if f1.currentPosition.euclidean_distance_3D(f2.currentPosition) < f1.closeRange + f2.closeRange:
                return True
        return False

    @staticmethod
    def generateFlight(poly: 'Polygon', lower: int, upper: int, flightType: str, closeRange: int) -> 'Flight':
        if flightType == "external":
            randomEdgeEnter = random.randint(0, len(poly.listOfEdges) - 1)
            randomEdgeExit = random.randint(0, len(poly.listOfEdges) - 1)

            enterPoint = poly.listOfEdges[randomEdgeEnter].getRandomPoint(poly.lowerLimit, poly.upperLimit, flightType)
            exitPoint = poly.listOfEdges[randomEdgeExit].getRandomPoint(poly.lowerLimit, poly.upperLimit, flightType)

            v = random.randint(lower, upper)
            return Flight(enterPoint, exitPoint, v, flightType, [Segment(enterPoint, exitPoint)], closeRange)
        elif flightType == "internal":
            randomEnterPoint = Polygon.getRandomPoint(poly, poly.lowerLimit)
            randomExitPoint = Polygon.getRandomPoint(poly, poly.lowerLimit)
            randomPoint1 = Polygon.getRandomPointHigher(poly, poly.lowerLimit, poly.upperLimit)
            randomPoint2 = Polygon.getRandomPointSameHeight(poly, randomPoint1)
            segment1 = Segment(randomEnterPoint, randomPoint1)
            segment2 = Segment(randomPoint1, randomPoint2)
            segment3 = Segment(randomPoint2, randomExitPoint)

            v = random.randint(lower, upper)
            return Flight(randomEnterPoint, randomPoint1, v, "internal", [segment1, segment2, segment3], closeRange)
        elif flightType == "half-internal":
            randNum = random.randint(1, 2)
            if randNum == 1:
                # ulazi i silazi
                randomEdgeEnter = random.randint(0, len(poly.listOfEdges) - 1)
                enterPoint = poly.listOfEdges[randomEdgeEnter].getRandomPoint(poly.lowerLimit, poly.upperLimit, flightType)
                randomHeight = random.uniform(poly.lowerLimit, poly.upperLimit)
                randomPoint = Polygon.getRandomPoint(poly, randomHeight)
                exitPoint = Polygon.getRandomPoint(poly, poly.lowerLimit)
                segment1 = Segment(enterPoint, randomPoint)
                segment2 = Segment(randomPoint, exitPoint)
                v = random.randint(lower, upper)
                return Flight(enterPoint, randomPoint, v, "half-internal", [segment1, segment2], closeRange)
            else:
                # penje se i izlazi
                enterPoint = Polygon.getRandomPoint(poly, poly.lowerLimit)
                randomHeight = random.uniform(poly.lowerLimit, poly.upperLimit)
                randomPoint = Polygon.getRandomPoint(poly, randomHeight)
                exitPoint = Polygon.getRandomPoint(poly, poly.lowerLimit)
                segment1 = Segment(enterPoint, randomPoint)
                segment2 = Segment(randomPoint, exitPoint)
                v = random.randint(lower, upper)
                return Flight(enterPoint, randomPoint, v, "half-internal", [segment1, segment2], closeRange)

    @staticmethod
    def draw(flightList, pygame, screen, intersections, myfont):
        red = (255, 0, 0)
        green = (0, 255, 0)
        blue = (0, 0, 255)
        white = (255, 255, 255)
        black = (0, 0, 0)
        brown = (160, 58, 0)
        purple = (80, 0, 160)

        for flight in flightList:
            if flight in intersections:
                color = red
            else:
                if flight.flightType == "external":
                    color = black
                if flight.flightType == "internal":
                    color = purple
                if flight.flightType == "half-internal":
                    color = brown
            # print(flight.start.x, flight.start.y, flight.end.x, flight.end.y, len(flightList))
            if abs(flight.currentPosition.x - flight.path[-1].end.x) <= flight.velocity and abs(
                    flight.currentPosition.y - flight.path[-1].end.y) <= flight.velocity:
                if flight.flightType == "external":
                    pygame.draw.rect(screen, blue, (flight.currentPosition.x, flight.currentPosition.y, 5, 5))
                    pygame.draw.circle(screen, blue, (int(flight.currentPosition.x), int(flight.currentPosition.y)), flight.closeRange,
                                       1)
                    pygame.draw.line(screen, green, (flight.start.x, flight.start.y), (flight.end.x, flight.end.y))
                    flightList.remove(flight)
                else:
                    if abs(flight.currentPosition.x - flight.path[-1].end.x) <= flight.velocity and abs(
                            flight.currentPosition.y - flight.path[-1].end.y) <= flight.velocity:
                        pygame.draw.rect(screen, blue, (flight.currentPosition.x, flight.currentPosition.y, 5, 5))
                        pygame.draw.circle(screen, blue, (int(flight.currentPosition.x), int(flight.currentPosition.y)),
                                           flight.closeRange,
                                           1)
                        pygame.draw.line(screen, green, (flight.start.x, flight.start.y), (flight.end.x, flight.end.y))
                        flightList.remove(flight)
                    else:
                        if flight.flightType == "internal":
                            if abs(flight.currentPosition.x - flight.path[1].start.x) <= flight.velocity and abs(
                                    flight.currentPosition.y - flight.path[1].start.y) <= flight.velocity:
                                # print("Uso")
                                flight.start = flight.path[1].start
                                flight.end = flight.path[1].end
                            if abs(flight.currentPosition.x - flight.path[2].start.x) <= flight.velocity and abs(
                                    flight.currentPosition.y - flight.path[2].start.y) <= flight.velocity:
                                flight.start = flight.path[2].start
                                flight.end = flight.path[2].end
                        if flight.flightType == "half-internal":
                            if abs(flight.currentPosition.x - flight.path[1].start.x) < flight.velocity and abs(
                                    flight.currentPosition.y - flight.path[1].start.y) < flight.velocity:
                                flight.start = flight.path[1].start
                                flight.end = flight.path[1].end
            else:
                if not flight.outsidePoly:
                    # pygame.draw.line(screen, green, (flight.start.x, flight.start.y), (flight.end.x, flight.end.y))
                    textsurface = myfont.render(
                        "(" + str(round(flight.currentPosition.x)) + "," + str(round(flight.currentPosition.y)) + "," + str(
                            round(flight.currentPosition.z)) + ")", False, (0, 0, 0))
                    screen.blit(textsurface, (flight.currentPosition.x - 25, flight.currentPosition.y))
                    # pygame.draw.rect(screen, color, (flight.currentPosition.x, flight.currentPosition.y - 2.5, 5, 5))
                    pygame.draw.circle(screen, color, (int(flight.currentPosition.x), int(flight.currentPosition.y)), flight.closeRange, 1)

            """--------------------------------------------------------------------------------------------------------"""
            flight.calculateCurrentPosition()
            """--------------------------------------------------------------------------------------------------------"""

            if flight.calculateCurrentPosition() == -1:
                if flight.flightType == "external":
                    pygame.draw.rect(screen, blue, (flight.currentPosition.x, flight.currentPosition.y, 5, 5))
                    pygame.draw.circle(screen, blue, (int(flight.currentPosition.x), int(flight.currentPosition.y)), flight.closeRange,
                                       1)
                    pygame.draw.line(screen, green, (flight.start.x, flight.start.y), (flight.end.x, flight.end.y))
                    if flight in flightList:
                        flightList.remove(flight)
                else:
                    if abs(flight.currentPosition.x - flight.path[-1].end.x) <= flight.velocity and abs(
                            flight.currentPosition.y - flight.path[-1].end.y) <= flight.velocity:
                        pygame.draw.rect(screen, blue, (flight.currentPosition.x, flight.currentPosition.y, 5, 5))
                        pygame.draw.circle(screen, blue, (int(flight.currentPosition.x), int(flight.currentPosition.y)),
                                           flight.closeRange,
                                           1)
                        pygame.draw.line(screen, green, (flight.start.x, flight.start.y), (flight.end.x, flight.end.y))
                        if flight in flightList:
                            flightList.remove(flight)
                    else:
                        if flight.flightType == "internal":
                            if abs(flight.currentPosition.x - flight.path[1].start.x) <= flight.velocity and abs(
                                    flight.currentPosition.y - flight.path[1].start.y) <= flight.velocity:
                                flight.start = flight.path[1].start
                                flight.end = flight.path[1].end
                            if abs(flight.currentPosition.x - flight.path[2].start.x) <= flight.velocity and abs(
                                    flight.currentPosition.y - flight.path[2].start.y) <= flight.velocity:
                                flight.start = flight.path[2].start
                                flight.end = flight.path[2].end
                        if flight.flightType == "half-internal":
                            if abs(flight.currentPosition.x - flight.path[1].start.x) <= flight.velocity and abs(
                                    flight.currentPosition.y - flight.path[1].start.y) <= flight.velocity:
                                flight.start = flight.path[1].start
                                flight.end = flight.path[1].end