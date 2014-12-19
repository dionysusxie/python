#!/usr/bin/env python -u

import multiprocessing # Process, Queue
import os
import time
import Queue


def pid_info(title):
    print
    print title
    print 'module name:', __name__
    if hasattr(os, 'getppid'):
        print 'parent process id:', os.getppid()
    print 'process id:', os.getpid()


def f(q):
    pid_info('function f()')

    for i in xrange(10):
        q.put([i])
        time.sleep(1)

    q.put([])

if __name__ == '__main__':
    pid_info('main line')

    q = multiprocessing.Queue()
    p = multiprocessing.Process(target=f, args=(q,))
    p.start()

    while True:
        try:
            item = q.get_nowait()
        except Queue.Empty:
            pass
        else:
            if len(item) == 0: break
            print item

    p.join()

