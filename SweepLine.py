import random
import time
from queue import PriorityQueue
from collections import deque
from Flight import *
from Point import *


def getIntersections(flightsList: list) -> set:
    priorityQueue = PriorityQueue()
    Deque = deque()
    listOfIntersections = set()

    for flight in flightsList:
        priorityQueue.put(EventPoint("s", Point(flight.currentPosition.x - flight.closeRange, flight.currentPosition.y, flight.currentPosition.z), flight))
        priorityQueue.put(EventPoint("e", Point(flight.currentPosition.x + flight.closeRange, flight.currentPosition.y, flight.currentPosition.z), flight))

    while not priorityQueue.empty():
        eventPoint = priorityQueue.get()
        if eventPoint.eventType == "s":
            currentFlight = eventPoint.flightIdentifier
            for flight in Deque:
                if Flight.intersects(currentFlight, flight) and not currentFlight.outsidePoly and not flight.outsidePoly:
                    listOfIntersections.add(flight)
                    listOfIntersections.add(currentFlight)
            Deque.appendleft(currentFlight)
        else:
            if Deque.__len__() != 0:
                Deque.pop()

    return listOfIntersections

def getIntersectionsTry(flightsList: list) -> set:
    from AVLTree import AVLTree
    priorityQueue = PriorityQueue()
    tree = AVLTree()
    listOfIntersections = set()

    for flight in flightsList:
        priorityQueue.put(
            EventPoint("s", Point(flight.currentPosition.x - flight.closeRange, flight.currentPosition.y, flight.currentPosition.z),
                       flight))
        priorityQueue.put(
            EventPoint("e", Point(flight.currentPosition.x + flight.closeRange, flight.currentPosition.y, flight.currentPosition.z),
                       flight))

    while not priorityQueue.empty() != 0:
        eventPoint = priorityQueue.get()
        if eventPoint.eventType == "s":
            currentFlight = eventPoint.flightIdentifier
            tree.insert(currentFlight)
            prevFlight = tree.get_prev(currentFlight)
            while prevFlight != None and Flight.intersects(currentFlight, prevFlight) and not currentFlight.outsidePoly and not prevFlight.outsidePoly:
                listOfIntersections.add(prevFlight)
                listOfIntersections.add(currentFlight)
                prevFlight = tree.get_prev(prevFlight)

            succFlight = tree.get_succ(currentFlight)
            while succFlight != None and Flight.intersects(currentFlight, succFlight) and not currentFlight.outsidePoly and not succFlight.outsidePoly:
                listOfIntersections.add(succFlight)
                listOfIntersections.add(currentFlight)
                succFlight = tree.get_succ(succFlight)
        else:
            currentFlight = eventPoint.flightIdentifier
            tree.remove(currentFlight)
    return listOfIntersections

def getIntersectionsn2(flightsList: list) -> list:
    lista = set()
    for i in range(0, len(flightsList)):
        for j in range(0, len(flightsList)):
            if i != j:
                if Flight.intersects(flightsList[i], flightsList[j]):
                    lista.add(flightsList[i])
                    lista.add(flightsList[j])
    return lista

"""
width = 800
height = 600
from Segment import *
for j in range(0, 200):
    flightList = []
    sumBolji, sumGori = 0.0, 0.0
    for i in range(0, 5000):
        randx = random.randint(50, 1750)
        randy = random.randint(50, 1000)
        randx2 = random.randint(0, 1750)
        randy2 = random.randint(0, 1000)
        randz = random.randint(0, 50)
        randz2 = random.randint(0, 100)
        v1 = random.randint(1, 5)
        newFlight = Flight(Point(randx, randy, randz), Point(randx2, randy2, randz2), v1, "external", [Segment(Point(randx, randy, randz), Point(randx2, randy2, randz2))], 50)
        flightList.append(newFlight)
    startTime = time.process_time()
    getIntersectionsImprovedv2(flightList)
    zavrsno1 = time.process_time() - startTime
    print(zavrsno1, end=", ")
    startTime = time.process_time()
    getIntersections(flightList)
    zavrsno1 = time.process_time() - startTime
    print(zavrsno1)
"""