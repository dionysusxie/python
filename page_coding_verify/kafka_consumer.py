#!/usr/bin/env python -u

import multiprocessing
import os
import time
import Queue
import sys
import page_coding_verifier

from kafka import KafkaClient, SimpleConsumer


#
# configs
#

CONSUME_FROM_HEAD = 0
CONSUME_FROM_CURRENT = 1
CONSUME_FROM_TAIL = 2

g_brokers_addr = 'localhost:9092'
g_topic = 'test'
g_consumer_group = 'page_code_verify_001'
g_consume_init_position = CONSUME_FROM_TAIL



LOG_INFO = 0
LOG_WARNING = 1
LOG_ERROR = 2

def mlog(level, log):
    if level == LOG_INFO:
        print '[' + time.asctime() + '] INFO ' + log
    elif level == LOG_WARNING:
        print '[' + time.asctime() + '] WARNING ' + log
    elif level == LOG_ERROR:
        print '[' + time.asctime() + '] ERROR ' + log
    else:
        assert False, 'Invalid log level'

def log_info(log):
    return mlog(LOG_INFO, log)

def log_warning(log):
    return mlog(LOG_WARNING, log)

def log_error(log):
    return mlog(LOG_ERROR, log)


log_info('Connecting to kafka cluster: ' + g_brokers_addr)
kafka = KafkaClient(g_brokers_addr)

try:
    log_info('Consumer group: ' + g_consumer_group)
    log_info('Consumer topic: ' + g_topic)
    consumer = SimpleConsumer(kafka, g_consumer_group, g_topic)

    # create a sub process to handle http requests
    write_queue = multiprocessing.Queue()
    read_queue  = multiprocessing.Queue()
    web_server_process = multiprocessing.Process(
        target = page_coding_verifier.run,
        args = (8000, write_queue, read_queue))
    web_server_process.start()

    # adjust offset
    consumer.seek(0, g_consume_init_position)

    # get messages from kafka
    while True:
        msg = consumer.get_message(block = True, timeout = 0.1,
                                   get_partition_info = False)
        if msg:
            log_info('Message received - ' + str(msg))

except KeyboardInterrupt:
    log_info('User interrupt this app.')

log_info('App close now.')
kafka.close()