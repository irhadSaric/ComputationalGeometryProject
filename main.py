import pygame
import time
from SweepLine import *
from math import sqrt
from math import acos

pygame.init()
width = 800
height = 600

screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
clock = pygame.time.Clock()

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)


def find_most_left(vertices):
    return min(vertices)

def dot(vector1, vector2):
    return vector1.x*vector2.x + vector1.y*vector2.y

def magnitude(vector):
    return sqrt(dot(vector, vector))

def euclidean_distance(vector):
    return sqrt(vector.x**2 + vector.y**2)

def angle(imaginaryPoint, mostLeft, v):
    mostLeftVector = (imaginaryPoint[0]-mostLeft[0], imaginaryPoint[1]-mostLeft[1])
    currentVector = (v[0]-mostLeft[0], v[1]-mostLeft[1])
    angle = acos((dot(mostLeftVector, currentVector))/magnitude(mostLeftVector)/magnitude(currentVector))
    return (angle, euclidean_distance(currentVector))

def simplePoly(vertices):
    mostLeft = find_most_left(vertices)
    imaginaryPoint = (mostLeft.x-1, mostLeft.y)
    mostLeftIndex = vertices.index(mostLeft)
    vertices[0], vertices[mostLeftIndex] = vertices[mostLeftIndex], vertices[0]

    return vertices[0] + sorted(vertices[1:], key = lambda v : angle(imaginaryPoint, mostLeft, v))


def makePointsForPolygon(pointsList: list) -> list:
    polygonPoints = []
    for point in pointsList:
        polygonPoints.append(point)

    polygonPoints.sort()

    resultPoly = []
    for point in polygonPoints:
        tempTuple = (point.x, point.y)
        resultPoly.append(tempTuple)

    print(resultPoly)
    return resultPoly

xPositionRect = 20
yPositionRect = 20
running = True

x1 = 10
y1 = 50
z1 = 100
startingPoint = Point(x1, y1, z1)
x2 = 110
y2 = 150
z2 = 150
endingPoint = Point(x2, y2, z2)
f1 = Flight(startingPoint, endingPoint, 1.0)
flightList = [f1]

inputListPoly = []
xCoordinate = input("Enter x coordinate")
yCoordinate = input("Enter y coordinate")
zCoordinate = input("Enter z coordinate")
while xCoordinate.isnumeric() and yCoordinate.isnumeric() and zCoordinate.isnumeric():
    try:
        x = float(xCoordinate)
        y = float(yCoordinate)
        z = float(zCoordinate)
        inputListPoly.append(Point(x, y, z))
        xCoordinate = input("Enter x coordinate")
        yCoordinate = input("Enter y coordinate")
        zCoordinate = input("Enter z coordinate")
    except ValueError:
        print("Input error")
"""
10
10
10
500
10
10
250
250
10
450
250
10



"""
poly = makePointsForPolygon(inputListPoly)
print(poly)
startTime = time.time()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(white)

    pygame.draw.polygon(screen, blue, poly, 1)

    intersections = []
    currentTime = time.time()
    if currentTime - startTime >= 1:
        randx = random.randint(0, width)
        randy = random.randint(0, height)
        randx2 = random.randint(0, width)
        randy2 = random.randint(0, height)
        randz = random.randint(100, 150)
        randz2 = random.randint(100, 150)
        v1 = random.randint(1, 5)
        newFlight = Flight(Point(randx, randy, randz), Point(randx2, randy2, randz2), v1)
        flightList.append(newFlight)
        startTime = currentTime

    intersections = getIntersectionsImprovedv3(flightList)

    color = black
    for flight in flightList:
        if flight in intersections:
            color = red
        else:
            color = black
        #print(flight.start.x, flight.start.y, flight.end.x, flight.end.y, len(flightList))
        if flight.currentPosition.x == flight.end.x and flight.currentPosition.y == flight.end.y:
            pygame.draw.rect(screen, blue, (flight.currentPosition.x, flight.currentPosition.y, 5, 5))
            pygame.draw.circle(screen, blue, (int(flight.currentPosition.x), int(flight.currentPosition.y)), 50, 1)
            pygame.draw.line(screen, green, (flight.start.x, flight.start.y), (flight.end.x, flight.end.y))
            flightList.remove(flight)
        else:
            #pygame.draw.line(screen, green, (flight.start.x, flight.start.y), (flight.end.x, flight.end.y))
            pygame.draw.rect(screen, color, (flight.currentPosition.x, flight.currentPosition.y - 2.5, 5, 5))
            pygame.draw.circle(screen, color, (int(flight.currentPosition.x), int(flight.currentPosition.y)), 50, 1)
        flight.calculateCurrentPosition()
        if flight.calculateCurrentPosition() == -1:
            pygame.draw.rect(screen, blue, (flight.currentPosition.x, flight.currentPosition.y, 5, 5))
            pygame.draw.circle(screen, blue, (int(flight.currentPosition.x), int(flight.currentPosition.y)), 50, 1)
            pygame.draw.line(screen, green, (flight.start.x, flight.start.y), (flight.end.x, flight.end.y))
            if flight in flightList:
                flightList.remove(flight)
    clock.tick(10)
    pygame.display.update()
pygame.quit()
