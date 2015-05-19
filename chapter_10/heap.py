#!/usr/bin/env python -u

import heapq
import random

print '--- heap ---'

data = range(10)
print data

random.shuffle(data)
print data

heap = []
for n in data:
    heapq.heappush(heap, n)
print heap

heapq.heappush(heap, 0.5)
print heap

print 'the smallest item:', heapq.heappop(heap)
print heap

heap = [5, 8, 0, 3, 6, 7, 9, 1, 4, 2]
heapq.heapify(heap)
print heap

print heapq.heapreplace(heap, 10)
print heap

heap = [0, 5, 4, 3, 1, 2]

for n in range(len(heap)):
    print heapq.nlargest(n+1, heap)

for n in range(len(heap)):
    print heapq.nsmallest(n+1, heap)
