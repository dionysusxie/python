#!/usr/bin/env python -u

import multiprocessing
import os
import time
import Queue
import sys
import json
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


#
# class PageCodingVerifier
#

class ActionParamError(Exception): pass

class PageCodingVerifier:
    def __init__(self, filter_life_time_in_minuter = 5):
        self.filter_life_time_in_minuter = filter_life_time_in_minuter
        assert self.filter_life_time_in_minuter > 0

        self.filters = {}
        self.last_check_time = time.time()

    def add_filter(self, new_filter):
        """
        Add a new filter. Every filter will survive for
        'self.filter_life_time_in_minuter'. If existed, it'll get another
        'self.filter_life_time_in_minuter' of lifetime.

        new_filter: A dict; e.g., {"request_url":"abc", "advertiser_id":"123"}
        @return: None
        @except: A ActionParamError will be raised if 'new_filter' contains
                 wrong content.
        """

        try:
            new_filter["request_url"].lower()   # make sure it's a string
            new_filter["advertiser_id"].lower() # make sure it's a string
            key = (new_filter["request_url"], new_filter["advertiser_id"])
        except:
            raise ActionParamError

        if not self.filters.has_key(key):
            self.filters[key] = {}
        self.filters[key]['death_time'] = time.time() + self.filter_life_time_in_minuter * 60

    def query(self, query_obj):
        pass

    def periodic_check(self, time_now):
        if time_now < self.last_check_time:
            self.last_check_time = time_now

        # check every 1 minutes to delete dead filters
        if time_now - self.last_check_time >= 60:
            keys_to_be_deleted = []
            for key in self.filters:
                if time_now >= self.filters[key]['death_time']:
                    keys_to_be_deleted.append(key)
            for key in keys_to_be_deleted:
                del self.filters[key]
            self.last_check_time = time_now


g_pg_verifier = PageCodingVerifier()


def periodic_check(time_now):
    g_pg_verifier.periodic_check(time_now)

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

    if action == ACTION_ADD_FILTER:
        try:
            g_pg_verifier.add_filter(action_param)
            ret['succeed'] = True
        except ActionParamError:
            ret['succeed'] = False
            ret['error'] = "Invalid param: %s" % json.dumps(action_param)
    elif action == ACTION_QUERY:
        time_now_int = int(time_now)
        ret['succeed'] = True
        ret['last_encountered'] = time_now_int
        ret['sitepage'] = time_now_int  # => '1'
        ret['skupage'] = time_now_int   # => '2'
        ret['cartpage'] = 0             # => '3'
        ret['conversionpage'] = 0       # => '4'
        ret['orderpage'] = 0            # => '5'
        ret['paidpage'] = time_now_int  # => '6'
        ret['conversionbutton'] = 0     # => '7'
        ret['eventpage'] = 0            # => '8'
        ret['eventbutton'] = 0          # => '9'
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
            last_check_time = TIME_NOW
            periodic_check(TIME_NOW)

except KeyboardInterrupt:
    log_info('User interrupt this app.')

log_info('App close now.')
kafka.close()
