import random
import time
from queue import PriorityQueue
from collections import deque

from Flight import *
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


def getIntersectionsTry(flightsList: list) -> list:
    priorityQueue = PriorityQueue()
    Deque = deque()
    listOfIntersections = set()

    for flight in flightsList:
        priorityQueue.put(
            EventPoint("s", Point(flight.currentPosition.x - 500, flight.currentPosition.y, flight.currentPosition.z),
                       flight))
        priorityQueue.put(
            EventPoint("e", Point(flight.currentPosition.x + 500, flight.currentPosition.y, flight.currentPosition.z),
                       flight))

    while not priorityQueue.empty():
        eventPoint = priorityQueue.get()
        if eventPoint.eventType == "s":
            currentFlight = eventPoint.flightIdentifier
            i = 0
            j = -1
            if Deque.__len__() >= 1:
                while i != Deque.__len__() and currentFlight.currentPosition.y + 50 > Deque[i].currentPosition.y - 50:
                    if Flight.intersects(currentFlight, Deque[i]):
                        listOfIntersections.add(Deque[i])
                        listOfIntersections.add(currentFlight)
                    i += 1

                while -j - 1 != Deque.__len__() and currentFlight.currentPosition.x - 50 < Deque[j].currentPosition.x + 50:
                    if Flight.intersects(currentFlight, Deque[j]):
                        listOfIntersections.add(Deque[j])
                        listOfIntersections.add(currentFlight)
                    j -= 1
            Deque.appendleft(currentFlight)
        else:
            if Deque.__len__() != 0:
                Deque.pop()

    return listOfIntersections

def getIntersectionsTryOptimised(flightsList: list) -> list:
    priorityQueue = []
    Deque = deque()
    listOfIntersections = set()

    for flight in flightsList:
        priorityQueue.append(
            EventPoint("s", Point(flight.currentPosition.x - 500, flight.currentPosition.y, flight.currentPosition.z),
                       flight))
        priorityQueue.append(
            EventPoint("e", Point(flight.currentPosition.x + 500, flight.currentPosition.y, flight.currentPosition.z),
                       flight))

    priorityQueue.sort()
    print(priorityQueue)
    #priorityQueue = priorityQueue[::-1]

    while len(priorityQueue) != 0:
        eventPoint = priorityQueue[-1]
        if eventPoint.eventType == "s":
            currentFlight = eventPoint.flightIdentifier
            Deque.appendleft(currentFlight)
            i = -1
            while Deque[i].currentPosition.y - 50 < currentFlight.currentPosition.y + 50 and -i != Deque.__len__()\
                    and Deque[i] != currentFlight:
                if Flight.intersects(currentFlight, Deque[i]):
                    listOfIntersections.add(Deque[i])
                    listOfIntersections.add(currentFlight)
                i -= 1
            """for flight in Deque:
                if Flight.intersects(currentFlight, flight):
                    listOfIntersections.add(flight)
                    listOfIntersections.add(currentFlight)"""
        else:
            if Deque.__len__() != 0:
                Deque.popleft()
        del priorityQueue[-1]

    return listOfIntersections

def getIntersectionsImproved(flightsList: list) -> list:
    priorityQueue = []
    Deque = deque()
    listOfIntersections = set()

    for flight in flightsList:
        priorityQueue.append(EventPoint("s", Point(flight.currentPosition.x - 500, flight.currentPosition.y, flight.currentPosition.z), flight))
        priorityQueue.append(EventPoint("e", Point(flight.currentPosition.x + 500, flight.currentPosition.y, flight.currentPosition.z), flight))

    priorityQueue.sort()
    priorityQueue = priorityQueue[::-1]
    while len(priorityQueue) != 0:
        eventPoint = priorityQueue[-1]
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
        del priorityQueue[-1]
    return listOfIntersections

def getIntersectionsImprovedv2(flightsList: list) -> list:
    from AVLTree import AVLTree
    priorityQueue = []
    tree = AVLTree()
    listOfIntersections = set()

    for flight in flightsList:
        priorityQueue.append(EventPoint("s", Point(flight.currentPosition.x - 500, flight.currentPosition.y, flight.currentPosition.z), flight))
        priorityQueue.append(EventPoint("e", Point(flight.currentPosition.x + 500, flight.currentPosition.y, flight.currentPosition.z), flight))

    priorityQueue.sort()
    priorityQueue = priorityQueue[::-1]
    while len(priorityQueue) != 0:
        eventPoint = priorityQueue[-1]
        if eventPoint.eventType == "s":
            currentFlight = eventPoint.flightIdentifier
            tree.insert(currentFlight)
            prevFlight = tree.get_prev(currentFlight)
            while prevFlight != None:
                if Flight.intersects(currentFlight, prevFlight):
                    listOfIntersections.add(prevFlight)
                    listOfIntersections.add(currentFlight)
                prevFlight = tree.get_prev(prevFlight)

            succFlight = tree.get_succ(currentFlight)
            while succFlight != None:
                if Flight.intersects(currentFlight, succFlight):
                    listOfIntersections.add(succFlight)
                    listOfIntersections.add(currentFlight)
                succFlight = tree.get_succ(succFlight)
        else:
            currentFlight = eventPoint.flightIdentifier
            tree.remove(currentFlight)
        del priorityQueue[-1]
    return listOfIntersections

def getIntersectionsImprovedv3(flightsList: list) -> list:
    from AVLTree import AVLTree
    priorityQueue = PriorityQueue()
    tree = AVLTree()
    listOfIntersections = set()

    for flight in flightsList:
        priorityQueue.put(EventPoint("s", Point(flight.currentPosition.x - 500, flight.currentPosition.y, flight.currentPosition.z), flight))
        priorityQueue.put(EventPoint("e", Point(flight.currentPosition.x + 500, flight.currentPosition.y, flight.currentPosition.z), flight))

    while not priorityQueue.empty():
        eventPoint = priorityQueue.get()
        if eventPoint.eventType == "s":
            currentFlight = eventPoint.flightIdentifier
            tree.insert(currentFlight)

            prevFlight = tree.get_prev(currentFlight)
            while prevFlight != None:
                if Flight.intersects(currentFlight, prevFlight):
                    listOfIntersections.add(prevFlight)
                    listOfIntersections.add(currentFlight)
                prevFlight = tree.get_prev(prevFlight)

            succFlight = tree.get_succ(currentFlight)
            while succFlight != None:
                if Flight.intersects(currentFlight, succFlight):
                    listOfIntersections.add(succFlight)
                    listOfIntersections.add(currentFlight)
                succFlight = tree.get_succ(succFlight)
        else:
            currentFlight = eventPoint.flightIdentifier
            tree.remove(currentFlight)
    return listOfIntersections

def getIntersectionsImprovedv4(flightsList: list) -> list:
    from AVLTree import AVLTree
    priorityQueue = PriorityQueue()
    tree = AVLTree()
    listOfIntersections = set()

    for flight in flightsList:
        priorityQueue.put(EventPoint("s", Point(flight.currentPosition.x - 500, flight.currentPosition.y, flight.currentPosition.z), flight))
        priorityQueue.put(EventPoint("e", Point(flight.currentPosition.x + 500, flight.currentPosition.y, flight.currentPosition.z), flight))

    while not priorityQueue.empty():
        eventPoint = priorityQueue.get()
        if eventPoint.eventType == "s":
            currentFlight = eventPoint.flightIdentifier
            tree.insert(currentFlight)
            tree.inorder_check(currentFlight, listOfIntersections)
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

def testWhichOneIsBetter(numberOfRandomCombinations, numberOfFlights):
    flightList = []
    boljiMoj, boljiKvadratni = 0, 0
    sumBolji, sumGori = 0.0, 0.0
    sumKadJeBolji, sumKadJeGori = 0.0, 0.0
    width = 800
    height = 600
    for j in range(0, numberOfRandomCombinations):
        flightList = []
        sumBolji, sumGori = 0.0, 0.0
        for i in range(0, numberOfFlights):
            randx = random.randint(0, width)
            randy = random.randint(0, height)
            randx2 = random.randint(0, width)
            randy2 = random.randint(0, height)
            randz = random.randint(0, 100)
            randz2 = random.randint(0, 100)
            v1 = random.randint(1, 5)
            newFlight = Flight(Point(randx, randy, randz), Point(randx2, randy2, randz2), v1)
            flightList.append(newFlight)

        startTime = time.process_time()
        getIntersections(flightList)
        zavrsno1 = time.process_time() - startTime
        # print(zavrsno1, end=", ")

        startTime = time.process_time()
        getIntersectionsn2(flightList)
        zavrsno2 = time.process_time() - startTime
        # print(zavrsno2)

        if zavrsno1 <= zavrsno2:
            boljiMoj += 1
            sumBolji += abs(zavrsno1-zavrsno2)
            sumKadJeBolji += sumBolji
        else:
            boljiKvadratni += 1
            sumGori += abs(zavrsno1 - zavrsno2)
            sumKadJeGori += sumGori

    print("Za ", numberOfFlights, " aviona i ", numberOfRandomCombinations, " random kombinacija \nmoj:", boljiMoj, ", n2:",
          boljiKvadratni, "usteda: ", sumKadJeBolji-sumKadJeGori, ", bolji u prosjeku za: ", sumKadJeBolji/boljiMoj,
          ", gori u prosjeku: ", sumKadJeGori/boljiKvadratni)

#testWhichOneIsBetter(5000, 20)
#testWhichOneIsBetter(500, 200)
#testWhichOneIsBetter(20, 5000)

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
        newFlight = Flight(Point(randx, randy, randz), Point(randx2, randy2, randz2), v1, "external", [Segment(Point(randx, randy, randz), Point(randx2, randy2, randz2))])
        flightList.append(newFlight)
    startTime = time.process_time()
    getIntersections(flightList)
    zavrsno1 = time.process_time() - startTime
    print(zavrsno1, end=", ")
    startTime = time.process_time()
    getIntersectionsTry(flightList)
    zavrsno1 = time.process_time() - startTime
    print(zavrsno1)
"""
"""
    startTime = time.process_time()
    getIntersectionsImprovedv4(flightList)
    zavrsno1 = time.process_time() - startTime
    print(zavrsno1)"""
"""
flightList = []
for i in range(0, 5000):
    randx = random.randint(50, 1750)
    randy = random.randint(50, 1000)
    randx2 = random.randint(0, 1750)
    randy2 = random.randint(0, 1000)
    randz = random.randint(0, 50)
    randz2 = random.randint(0, 100)
    v1 = random.randint(1, 5)
    newFlight = Flight(Point(randx, randy, randz), Point(randx2, randy2, randz2), v1)
    flightList.append(newFlight)

startTime = time.process_time()
getIntersectionsn2(flightList)
zavrsno1 = time.process_time() - startTime
print(zavrsno1, end=", ")
startTime = time.process_time()
getIntersections(flightList)
zavrsno1 = time.process_time() - startTime
print(zavrsno1)"""