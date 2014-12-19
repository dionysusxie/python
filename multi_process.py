#!/usr/bin/env python -u

import multiprocessing # Process, Queue
import os
import time
import Queue
import sys

TXT_EXIT = 'EXIT'

def pid_info(title):
    print
    print title
    print 'module name:', __name__
    if hasattr(os, 'getppid'):
        print 'parent process id:', os.getppid()
    print 'process id:', os.getpid()


def f(in_queue, out_queue):
    pid_info('function f()')

    try:
        i = 0
        while True:
            out_queue.put([i])
            i += 1

            # Check the input queue
            to_exit = False
            while True:
                try:
                    in_msg = in_queue.get_nowait()
                except Queue.Empty:
                    break
                else:
                    sys.stderr.write('[' + str(os.getpid()) + '] RECEIVED ' + str(in_msg) + '\n')
                    if TXT_EXIT == in_msg:
                        to_exit = True
                        break

            if to_exit: break

            # sleep
            time.sleep(1)
    except KeyboardInterrupt:
        print 'user interupt the app in sub process'
    except:
        pass

    out_queue.put(TXT_EXIT)

if __name__ == '__main__':
    pid_info('main line')

    queue_out = multiprocessing.Queue()
    queue_in  = multiprocessing.Queue()

    p = multiprocessing.Process(target=f, args=(queue_out, queue_in))
    p.start()

    try:
        while True:
            try:
                item = queue_in.get_nowait()
            except Queue.Empty:
                pass
            else:
                print '[' + str(os.getpid()) + '] RECEIVED', item
                if TXT_EXIT == item: break
                queue_out.put('OK')
    except KeyboardInterrupt:
        print 'user interupt the app in main process'
    except:
        pass

    queue_out.put(TXT_EXIT)
    p.join()

