from Point import *


class Segment:
    def __init__(self, start: 'Point', end: 'Point'):
        self.start = start
        self.end = end

    def __repr__(self):
        return '({}, {})'.format(self.start, self.end)