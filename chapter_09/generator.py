#!/usr/bin/env python -u

def flatten(nested):
    for sublist in nested:
        for element in sublist:
            yield element

nested = [[1,2], [3,4], [5]]
for num in flatten(nested):
    print num
print
for num in flatten(nested):
    print num


####################
def repeater(value):
    while True:
        new = (yield value)
        if new is not None: value = new

print
r = repeater(42)
print r.next()
print r.next()
print r.next()

r.send('Hello, world!')
print r.next()
print r.next()

r.close()
print r.next()
