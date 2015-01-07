#!/usr/bin/env python -u

import multiprocessing
import time

def f():
    print 'f() begin'
    while True:
        pass


print 'Begin'

p = multiprocessing.Process(target=f, args=())
p.start()

time.sleep(3)
p.terminate()

print 'End'