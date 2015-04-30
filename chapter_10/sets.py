#!/usr/bin/env python -u

mySets = []
for i in range(10):
    mySets.append(set(range(i, i+5)))

for i in mySets:
    print i

print reduce(set.union, mySets)
print reduce(lambda x,y: x+y, [n for n in xrange(101)])
print reduce(lambda x,y: x+y, xrange(101))
