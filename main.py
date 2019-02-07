import pygame
import time
from SweepLine import *

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

startTime = time.time()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(white)
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

    intersections = getIntersections(flightList)

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
