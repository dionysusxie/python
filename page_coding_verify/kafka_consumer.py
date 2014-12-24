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

ACTION_ADD_FILTER = 'add_filter'
ACTION_QUERY = 'query'
g_supported_actions = (ACTION_ADD_FILTER, ACTION_QUERY)


#
# log system
#

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


def periodic_check():
    try:
        msg = read_queue.get_nowait()
    except Queue.Empty:
        return

    ret = {}

    action = msg[0]
    if action not in g_supported_actions:
        ret['succeed'] = False
        ret['error'] = 'Unsupported action: %s' % action
        write_queue.put(ret)
        return

    action_param = msg[1]
    if 'request_url' in action_param and 'advertiser_id' in action_param:
        pass
    else:
        ret['succeed'] = False
        ret['error'] = 'Missing some fileds!'
        write_queue.put(ret)
        return

    if action == ACTION_ADD_FILTER:
        ret['succeed'] = True
    elif action == ACTION_QUERY:
        time_now = int(time.time())
        ret['succeed'] = True
        ret['last_encountered'] = time_now
        ret['sitepage'] = time_now   # => '1'
        ret['skupage'] = time_now    # => '2'
        ret['cartpage'] = 0          # => '3'
        ret['conversionpage'] = 0    # => '4'
        ret['orderpage'] = 0         # => '5'
        ret['paidpage'] = time_now   # => '6'
        ret['conversionbutton'] = 0  # => '7'
        ret['eventpage'] = 0         # => '8'
        ret['eventbutton'] = 0       # => '9'
    else:
        assert False

    write_queue.put(ret)

log_info('Connecting to kafka cluster: ' + g_brokers_addr)
kafka = KafkaClient(g_brokers_addr)

try:
    log_info('Consumer topic: ' + g_topic)
    log_info('Consumer group: ' + g_consumer_group)
    log_info('Consumer init position: ' + str(g_consume_init_position))

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
    last_check_time = time.time()
    CHECK_INTERVAL_IN_SECONDS = 0.05
    while True:
        msg = consumer.get_message(block = True,
                                   timeout = CHECK_INTERVAL_IN_SECONDS,
                                   get_partition_info = False)
        if msg:
            log_info('Message received - ' + str(msg))

        TIME_NOW = time.time()
        if TIME_NOW < last_check_time: last_check_time = TIME_NOW
        if TIME_NOW - last_check_time >= CHECK_INTERVAL_IN_SECONDS:
            # log_info('Time now: ' + str(TIME_NOW))
            last_check_time = TIME_NOW
            periodic_check()

except KeyboardInterrupt:
    log_info('User interrupt this app.')

log_info('App close now.')
kafka.close()
