#!/usr/bin/env python -u


class ArithmeticSequence(object):

    def __init__(self, start=0, step=1):
        self.start = start
        self.step = step
        self.changed = {}

    @classmethod
    def checkIndex(cls, key):
        if not isinstance(key, (int, long)):
            raise TypeError

        if key < 0:
            raise IndexError

    def __getitem__(self, key):
        self.checkIndex(key)

        try:
            return self.changed[key]
        except KeyError:
            return self.start + key * self.step

    def __setitem__(self, key, value):
        self.checkIndex(key)
        self.changed[key] = value

#     def __len__(self):
#         return 0
#
#     def __delitem__(self, key):
#         pass


def printArithmeticSequence(s, key):
    print 's[%s] = %s' % (i, s[key])


s = ArithmeticSequence(start=0, step=1)
for i in range(10):
    printArithmeticSequence(s, i)

print
s[1] = 1.1
for i in range(10):
    printArithmeticSequence(s, i)

print
s = ArithmeticSequence(start=1, step=1)
for i in range(10):
    printArithmeticSequence(s, i)

print
s = ArithmeticSequence(start=1, step=2)
for i in range(10):
    printArithmeticSequence(s, i)

# print len(s)
# del s[4]
