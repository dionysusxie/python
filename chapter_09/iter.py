#!/usr/bin/env python -u

class Fibs(object):

    def __init__(self, max=None):
        self.a = 0
        self.b = 1
        self.max = max

    def next(self):
        self.a, self.b = self.b, self.a + self.b

        if self.max and self.a > self.max:
            raise StopIteration

        return self.a

    def __iter__(self):
        return self


fibs = Fibs(1000)
for f in fibs:
    print f


print
fibs2 = Fibs()
for f in fibs2:
    if f > 1000: break
    print f


print
l = list(Fibs(1000))
print l
