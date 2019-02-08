import random
import time
from queue import PriorityQueue
from collections import deque
from Point import *


def getIntersections(flightsList: list) -> list:
    priorityQueue = PriorityQueue()
    Deque = deque()
    listOfIntersections = set()

    for flight in flightsList:
        priorityQueue.put(EventPoint("s", Point(flight.currentPosition.x - 500, flight.currentPosition.y, flight.currentPosition.z), flight))
        priorityQueue.put(EventPoint("e", Point(flight.currentPosition.x + 500, flight.currentPosition.y, flight.currentPosition.z), flight))

    while not priorityQueue.empty():
        eventPoint = priorityQueue.get()
        if eventPoint.eventType == "s":
            currentFlight = eventPoint.flightIdentifier
            for flight in Deque:
                if Flight.intersects(currentFlight, flight):
                    listOfIntersections.add(flight)
                    listOfIntersections.add(currentFlight)
            Deque.appendleft(currentFlight)
        else:
            if Deque.__len__() != 0:
                Deque.popleft()

    return listOfIntersections

def getIntersectionsn2(flightsList: list) -> list:
    lista = set()
    for i in range(0, len(flightsList)):
        for j in range(i+1, len(flightsList)):
            if Flight.intersects(flightsList[i], flightsList[j]):
                lista.add(flightsList[i])
                lista.add(flightsList[j])
    return lista

def sortiraj(flightList: list) -> list:
    return sorted(flightList)


flightList = []
for i in range (0, 1000):
    randx = random.randint(0, 500)
    randy = random.randint(0, 500)
    randx2 = random.randint(0, 500)
    randy2 = random.randint(0, 500)
    randz = random.randint(100, 400)
    randz2 = random.randint(100, 400)
    v1 = random.randint(1, 5)
    newFlight = Flight(Point(randx, randy, randz), Point(randx2, randy2, randz2), v1)
    flightList.append(newFlight)



startTime = time.time()
print("Pocetno za kvadratno", startTime)
print(getIntersectionsn2(flightList))
print("Krajnje za kvadratno", time.time() - startTime)
print("---------")

startTime = time.time()
print("Pocetno za mozda nlogn", startTime)
print(getIntersections(flightList))
print("Krajnje za mozda nlogn", time.time() - startTime)
print("---------")

