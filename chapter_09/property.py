#!/usr/bin/env python -u

class Rectangle(object):

    def __init__(self):
        self.width = 0
        self.height = 0

    def getSize(self):
        return self.width, self.height

    def setSize(self, size):
        self.width, self.height = size

    size = property(getSize, setSize)

r = Rectangle()
print r.size

r.size = 19, 11
print r.size
