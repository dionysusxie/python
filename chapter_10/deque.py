#!/usr/bin/env python -u

print '--- double-ended queue ---'

from collections import deque

q = deque(xrange(5))
print q

q.append(5)
q.appendleft(6)
print q

print q.pop()
print q

print q.popleft()
print q

print
for n in range(len(q)):
    q.rotate()
    print q

print
q.extend([7, 8, 9])
print q

q.extendleft([10, 11, 12])
print q

