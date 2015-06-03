#!/usr/bin/env python -u

import random

print 'random module:'

print 'a random real number:', random.random()

print 'getrandbits(4):', random.getrandbits(4)

print 'random.uniform(0, 10):', random.uniform(0, 10)

print 'random.randrange(10):', random.randrange(10)

print random.choice((1, 2, 3, 4))


# shuffle
a = [0, 1, 2, 3, 4, 5]
print a
random.shuffle(a)
print a

# sample
a = range(10)
print a
print random.sample(a, 3)
