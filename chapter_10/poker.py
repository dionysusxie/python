#!/usr/bin/env python -u

import random
import pprint


values = range(1, 11) + 'Jack Queen King'.split()
print 'values:', values

suits = 'diamonds clubs hearts spades'.split()
print 'suits:', suits

deck = ['%s of %s' % (v, s) for v in values for s in suits]
print 'all deck:'
for d in deck:
    print d


print '\n After shuffle:'
random.shuffle(deck)
pprint.pprint(deck)


MAX_COUNT = 5
count = 0
print 'Give me', MAX_COUNT, 'pokers please:'
print 'You get:'
while deck and count < MAX_COUNT:
    count += 1
    print '%5d -> %s' % (count, deck.pop())

print '\n*** GAME OVER ***'