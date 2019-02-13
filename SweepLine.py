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

            tree.insert(currentFlight)
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

            tree.insert(currentFlight)
        else:
            currentFlight = eventPoint.flightIdentifier
            tree.remove(currentFlight)
    return listOfIntersections

def getIntersectionsn2(flightsList: list) -> list:
    lista = set()
    for i in range(0, len(flightsList)):
        for j in range(i+1, len(flightsList)):
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
for j in range(0, 200):
    flightList = []
    sumBolji, sumGori = 0.0, 0.0
    for i in range(0, 5000):
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
    getIntersectionsImprovedv3(flightList)
    zavrsno1 = time.process_time() - startTime
    print(zavrsno1, end=", ")
    startTime = time.process_time()
    getIntersectionsImprovedv2(flightList)
    zavrsno1 = time.process_time() - startTime
    print(zavrsno1)
"""
