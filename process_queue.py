import multiprocessing
import time
from multiprocessing import Queue, Process


PARALLEL_NUM = 2
TXT_EXIT = 'exit'

def f(rq, wq):
    while True:
        msg = rq.get()
        if msg == TXT_EXIT:
            return
        wq.put('received')

def main():
    rq = Queue(1)
    wq = Queue(1)

    p = Process(target=f, args=(wq,rq))
    p.start()

    MSG_ONE_KB = 'a' * 1024
    assert len(MSG_ONE_KB) == 1024

    NUM_MSGS = 100 * 1024
    time_begin = time.time()

    for i in xrange(NUM_MSGS):
        wq.put(MSG_ONE_KB)
        rq.get()

    wq.put(TXT_EXIT)
    p.join()

    time_used = int(time.time() - time_begin)
    print 'msg count: %d' % NUM_MSGS
    print 'time used: %d seconds' % time_used
    print 'speed: %.2f MB/s' % (NUM_MSGS / 1024.0 / time_used)

if __name__ == '__main__':
    main()
