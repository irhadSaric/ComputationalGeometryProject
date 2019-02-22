import pygame
import time

from SweepLine import *
from Polygon import *

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

lowerVelocity = int(input("Enter lower speed limit"))
upperVelocity = int(input("Enter upper speed limit"))

closeRange = int(input("Enter close range"))

poly = Polygon(inputListPoly, lowerLimit, upperLimit)
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
100
1
5
25
"""
startTime = time.time()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(white)

    intersections = []
    currentTime = time.time()
    if currentTime - startTime >= 0.25:
        flightType = random.randint(1, 3)
        if flightType == 3:
            newFlight = Flight.generateFlight(poly, lowerVelocity, upperVelocity, "external", closeRange)
        elif flightType == 2:
            newFlight = Flight.generateFlight(poly, lowerVelocity, upperVelocity, "internal", closeRange)
        else:
            newFlight = Flight.generateFlight(poly, lowerVelocity, upperVelocity, "half-internal", closeRange)
        flightList.append(newFlight)
        startTime = currentTime

    for flight in flightList:
        if poly.isInPoly(flight.currentPosition):
            flight.outsidePoly = False
        else:
            flight.outsidePoly = True

    intersections = getIntersectionsTry(flightList)

    poly.draw(screen)
    Flight.draw(flightList, pygame, screen, intersections, myfont)

    clock.tick(10)
    pygame.display.update()
pygame.quit()
