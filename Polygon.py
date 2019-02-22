from Point import Point
from Segment import *
from Point import *
import random

class Polygon:
    def __init__(self, listOfEdges: list, lowerLimit: int, upperLimit: int):
        self.listOfEdges = listOfEdges
        self.lowerLimit = lowerLimit
        self.upperLimit = upperLimit

    def isInPoly(self, point:'Point') -> bool:
        mostLeftPoint = self.listOfEdges[0].start
        for edge in self.listOfEdges:
            if mostLeftPoint > edge.start:
                mostLeftPoint = edge.start
            if mostLeftPoint > edge.end:
                mostLeftPoint = edge.end

        mostUpPoint = self.listOfEdges[0].start
        for edge in self.listOfEdges:
            if mostUpPoint.y > edge.start.y:
                mostUpPoint = edge.start
            if mostUpPoint.y > edge.end.y:
                mostUpPoint = edge.end

        segment = Segment(Point(mostLeftPoint.x - 1, mostUpPoint.y), point)

        counter = 0
        for edge in self.listOfEdges:
            if Segment.doIntersect(segment, edge):
                counter += 1

        return counter % 2

    @staticmethod
    def getRandomPoint(poly: 'Polygon', lower: int) -> 'Point':
        mostLeftPoint = poly.listOfEdges[0].start
        for edge in poly.listOfEdges:
            if mostLeftPoint > edge.start:
                mostLeftPoint = edge.start
            if mostLeftPoint > edge.end:
                mostLeftPoint = edge.end
        mostRightPoint = poly.listOfEdges[0].start
        for edge in poly.listOfEdges:
            if mostRightPoint < edge.start:
                mostRightPoint = edge.start
            if mostRightPoint < edge.end:
                mostRightPoint = edge.end

        mostUpPoint = poly.listOfEdges[0].start
        for edge in poly.listOfEdges:
            if mostUpPoint.y > edge.start.y:
                mostUpPoint = edge.start
            if mostUpPoint.y > edge.end.y:
                mostUpPoint = edge.end

        mostDownPoint = poly.listOfEdges[0].start
        for edge in poly.listOfEdges:
            if mostDownPoint.y < edge.start.y:
                mostDownPoint = edge.start
            if mostDownPoint.y < edge.end.y:
                mostDownPoint = edge.end

        randomx = random.uniform(mostLeftPoint.x, mostRightPoint.x)
        randomy = random.uniform(mostDownPoint.y, mostUpPoint.y)
        randomPoint = Point(randomx, randomy, lower)
        segment = Segment(Point(mostLeftPoint.x - 1, mostUpPoint.y), randomPoint)

        counter = 0
        for edge in poly.listOfEdges:
            if Segment.doIntersect(segment, edge):
                counter += 1

        while not counter % 2:
            randomx = random.uniform(mostLeftPoint.x, mostRightPoint.x)
            randomy = random.uniform(mostDownPoint.y, mostUpPoint.y)
            randomPoint = Point(randomx, randomy, lower)
            segment = Segment(Point(mostLeftPoint.x - 1, mostUpPoint.y), randomPoint)
            counter = 0
            for edge in poly.listOfEdges:
                if Segment.doIntersect(segment, edge):
                    counter += 1
        return randomPoint

    @staticmethod
    def getRandomPointHigher(poly: 'Polygon', lower: int, upper: int) -> 'Point':
        randomPoint = Polygon.getRandomPoint(poly, lower)
        randomPoint.z = random.randint(lower, upper)
        return randomPoint

    @staticmethod
    def getRandomPointSameHeight(poly: 'Polygon', point: 'Point') -> 'Point':
        return Polygon.getRandomPoint(poly, point.z)

    def draw(self, screen):
        import pygame
        green = (0, 255, 0)
        for edge in self.listOfEdges:
            pygame.draw.line(screen, green, (edge.start.x, edge.start.y), (edge.end.x, edge.end.y))
