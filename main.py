import pygame
import time
from SweepLine import *
from math import sqrt
from math import acos
from Segment import *


def getRandomPoint(poly: list, lower: int) -> 'Point':
    mostLeftPoint = poly[0].start
    for edge in poly:
        if mostLeftPoint > edge.start:
            mostLeftPoint = edge.start
        if mostLeftPoint > edge.end:
            mostLeftPoint = edge.end
    mostRightPoint = poly[0].start
    for edge in poly:
        if mostRightPoint < edge.start:
            mostRightPoint = edge.start
        if mostRightPoint < edge.end:
            mostRightPoint = edge.end

    mostUpPoint = poly[0].start
    for edge in poly:
        if mostUpPoint.y > edge.start.y:
            mostUpPoint = edge.start
        if mostUpPoint.y > edge.end.y:
            mostUpPoint = edge.end

    mostDownPoint = poly[0].start
    for edge in poly:
        if mostDownPoint.y < edge.start.y:
            mostDownPoint = edge.start
        if mostDownPoint.y < edge.end.y:
            mostDownPoint = edge.end

    randomx = random.uniform(mostLeftPoint.x, mostRightPoint.x)
    randomy = random.uniform(mostDownPoint.y, mostUpPoint.y)
    randomPoint = Point(randomx, randomy, lower)
    segment = Segment(Point(mostLeftPoint.x-1, mostUpPoint.y), randomPoint)

    counter = 0
    for edge in poly:
        if Segment.doIntersect(segment, edge):
            counter += 1

    while not counter % 2:
        randomx = random.uniform(mostLeftPoint.x, mostRightPoint.x)
        randomy = random.uniform(mostDownPoint.y, mostUpPoint.y)
        randomPoint = Point(randomx, randomy, lower)
        segment = Segment(Point(mostLeftPoint.x - 1, mostUpPoint.y), randomPoint)
        counter = 0
        for edge in poly:
            if Segment.doIntersect(segment, edge):
                counter += 1
    return randomPoint

def getRandomPointHigher(poly, randomEnterPoint, lower, upper):
    randomPoint = getRandomPoint(poly, lower)
    randomPoint.z = random.randint(lower, upper)
    return randomPoint

def getRandomPointSameHeight(poly, point):
    return getRandomPoint(poly, point.z)

def generateFlight(poly: list, lower: int, upper: int, flightType: str) -> 'Flight':
    if flightType == "external":
        randomEdgeEnter = random.randint(0, len(poly) - 1)
        randomEdgeExit = random.randint(0, len(poly) - 1)

        enterPoint = poly[randomEdgeEnter].getRandomPoint(lower, upper, flightType)
        exitPoint = poly[randomEdgeExit].getRandomPoint(lower, upper, flightType)

        v = random.randint(1, 5)
        return Flight(enterPoint, exitPoint, v, flightType, [Segment(enterPoint, exitPoint)])
    elif flightType == "internal":
        randomEnterPoint = getRandomPoint(poly, lower)
        randomExitPoint = getRandomPoint(poly, lower)
        randomPoint1 = getRandomPointHigher(poly, randomEnterPoint, lower, upper)
        randomPoint2 = getRandomPointSameHeight(poly, randomPoint1)
        segment1 = Segment(randomEnterPoint, randomPoint1)
        segment2 = Segment(randomPoint1, randomPoint2)
        segment3 = Segment(randomPoint2, randomExitPoint)

        v = random.randint(1, 5)
        return Flight(randomEnterPoint, randomPoint1, v, "internal", [segment1, segment2, segment3])
    elif flightType == "half-internal":
        randNum = random.randint(1, 2)
        if randNum == 1:
            #ulazi i silazi
            randomEdgeEnter = random.randint(0, len(poly) - 1)
            enterPoint = poly[randomEdgeEnter].getRandomPoint(lower, upper, flightType)
            randomHeight = random.uniform(lower, upper)
            randomPoint = getRandomPoint(poly, randomHeight)
            exitPoint = getRandomPoint(poly, lower)
            segment1 = Segment(enterPoint, randomPoint)
            segment2 = Segment(randomPoint, exitPoint)
            v = random.randint(1, 5)
            return Flight(enterPoint, randomPoint, v, "half-internal", [segment1, segment2])
        else:
            #penje se i izlazi
            enterPoint = getRandomPoint(poly, lower)
            randomHeight = random.uniform(lower, upper)
            randomPoint = getRandomPoint(poly, randomHeight)
            exitPoint = getRandomPoint(poly, lower)
            segment1 = Segment(enterPoint, randomPoint)
            segment2 = Segment(randomPoint, exitPoint)
            v = random.randint(1, 5)
            return Flight(enterPoint, randomPoint, v, "half-internal", [segment1, segment2])

pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 10)
width = 800
height = 600

screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
clock = pygame.time.Clock()

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)
brown = (160, 58, 0)
purple = (80, 0, 160)

xPositionRect = 20
yPositionRect = 20
running = True
flightList = []

inputListPoly = []
xCoordinate = input("Enter starting point of segment: x")
yCoordinate = input("Enter starting point of segment: y")
xCoordinateEnd = input("Enter ending point of segment: x")
yCoordinateEnd = input("Enter ending point of segment: y")
while xCoordinate.isnumeric() and yCoordinate.isnumeric() and xCoordinateEnd.isnumeric() and yCoordinateEnd.isnumeric():
    try:
        x1 = float(xCoordinate)
        y1 = float(yCoordinate)
        x2 = float(xCoordinateEnd)
        y2 = float(yCoordinateEnd)
        inputListPoly.append(Segment(Point(x1, y1), Point(x2, y2)))
        xCoordinate = input("Enter starting point of segment: x")
        yCoordinate = input("Enter starting point of segment: y")
        xCoordinateEnd = input("Enter ending point of segment: x")
        yCoordinateEnd = input("Enter ending point of segment: y")
    except ValueError:
        print("Input error")

lowerLimit = int(input("Enter lower limit of airspace"))
upperLimit = int(input("Enter upper limit of airspace"))
"""
50
50
500
50
500
50
300
200
300
200
300
400
300
400
600
550
600
550
150
550
150
550
50
50




100
500
"""
startTime = time.time()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(white)

    for edge in inputListPoly:
        pygame.draw.line(screen, green, (edge.start.x, edge.start.y), (edge.end.x, edge.end.y))

    intersections = []
    currentTime = time.time()
    if currentTime - startTime >= 1:
        flightType = random.randint(1, 3)
        if flightType == 3:
            newFlight = generateFlight(inputListPoly, lowerLimit, upperLimit, "external")
        elif flightType == 2:
            newFlight = generateFlight(inputListPoly, lowerLimit, upperLimit, "internal")
        else:
            newFlight = generateFlight(inputListPoly, lowerLimit, upperLimit, "half-internal")
        flightList.append(newFlight)
        startTime = currentTime
    intersections = getIntersections(flightList)

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
        #print(flight.start.x, flight.start.y, flight.end.x, flight.end.y, len(flightList))
        if abs(flight.currentPosition.x - flight.path[-1].end.x) <= flight.velocity and abs(flight.currentPosition.y - flight.path[-1].end.y) <= flight.velocity:
            if flight.flightType == "external":
                pygame.draw.rect(screen, blue, (flight.currentPosition.x, flight.currentPosition.y, 5, 5))
                pygame.draw.circle(screen, blue, (int(flight.currentPosition.x), int(flight.currentPosition.y)), 50, 1)
                pygame.draw.line(screen, green, (flight.start.x, flight.start.y), (flight.end.x, flight.end.y))
                flightList.remove(flight)
            else:
                if abs(flight.currentPosition.x - flight.path[-1].end.x) <= flight.velocity and abs(flight.currentPosition.y - flight.path[-1].end.y) <= flight.velocity:
                    pygame.draw.rect(screen, blue, (flight.currentPosition.x, flight.currentPosition.y, 5, 5))
                    pygame.draw.circle(screen, blue, (int(flight.currentPosition.x), int(flight.currentPosition.y)), 50,
                                       1)
                    pygame.draw.line(screen, green, (flight.start.x, flight.start.y), (flight.end.x, flight.end.y))
                    flightList.remove(flight)
                else:
                    if flight.flightType == "internal":
                        if abs(flight.currentPosition.x - flight.path[1].start.x) <= flight.velocity and abs(flight.currentPosition.y - flight.path[1].start.y) <= flight.velocity:
                            #print("Uso")
                            flight.start = flight.path[1].start
                            flight.end = flight.path[1].end
                        if abs(flight.currentPosition.x - flight.path[2].start.x) <= flight.velocity and abs(flight.currentPosition.y - flight.path[2].start.y) <= flight.velocity:
                            flight.start = flight.path[2].start
                            flight.end = flight.path[2].end
                    if flight.flightType == "half-internal":
                        if abs(flight.currentPosition.x - flight.path[1].start.x) < flight.velocity and abs(flight.currentPosition.y - flight.path[1].start.y) < flight.velocity:
                            flight.start = flight.path[1].start
                            flight.end = flight.path[1].end
        else:
            #pygame.draw.line(screen, green, (flight.start.x, flight.start.y), (flight.end.x, flight.end.y))
            textsurface = myfont.render("("+str(round(flight.currentPosition.x))+","+str(round(flight.currentPosition.y))+","+str(round(flight.currentPosition.z))+")", False, (0, 0, 0))
            screen.blit(textsurface, (flight.currentPosition.x-25, flight.currentPosition.y))
            #pygame.draw.rect(screen, color, (flight.currentPosition.x, flight.currentPosition.y - 2.5, 5, 5))
            pygame.draw.circle(screen, color, (int(flight.currentPosition.x), int(flight.currentPosition.y)), 50, 1)

        """--------------------------------------------------------------------------------------------------------"""
        flight.calculateCurrentPosition()
        """--------------------------------------------------------------------------------------------------------"""

        if flight.calculateCurrentPosition() == -1:
            if flight.flightType == "external":
                pygame.draw.rect(screen, blue, (flight.currentPosition.x, flight.currentPosition.y, 5, 5))
                pygame.draw.circle(screen, blue, (int(flight.currentPosition.x), int(flight.currentPosition.y)), 50, 1)
                pygame.draw.line(screen, green, (flight.start.x, flight.start.y), (flight.end.x, flight.end.y))
                if flight in flightList:
                    flightList.remove(flight)
            else:
                if abs(flight.currentPosition.x - flight.path[-1].end.x) <= flight.velocity and abs(flight.currentPosition.y - flight.path[-1].end.y) <= flight.velocity:
                    pygame.draw.rect(screen, blue, (flight.currentPosition.x, flight.currentPosition.y, 5, 5))
                    pygame.draw.circle(screen, blue, (int(flight.currentPosition.x), int(flight.currentPosition.y)), 50,
                                       1)
                    pygame.draw.line(screen, green, (flight.start.x, flight.start.y), (flight.end.x, flight.end.y))
                    if flight in flightList:
                        flightList.remove(flight)
                else:
                    if flight.flightType == "internal":
                        if abs(flight.currentPosition.x - flight.path[1].start.x) <= flight.velocity and abs(flight.currentPosition.y - flight.path[1].start.y) <= flight.velocity:
                            print("Uso")
                            flight.start = flight.path[1].start
                            flight.end = flight.path[1].end
                        if abs(flight.currentPosition.x - flight.path[2].start.x) <= flight.velocity and abs(flight.currentPosition.y - flight.path[2].start.y) <= flight.velocity:
                            flight.start = flight.path[2].start
                            flight.end = flight.path[2].end
                    if flight.flightType == "half-internal":
                        if abs(flight.currentPosition.x - flight.path[1].start.x) <= flight.velocity and abs(flight.currentPosition.y - flight.path[1].start.y) <= flight.velocity:
                            flight.start = flight.path[1].start
                            flight.end = flight.path[1].end
    clock.tick(10)
    pygame.display.update()
pygame.quit()
