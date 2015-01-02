#!/usr/bin/env python -u

import multiprocessing
import os
import time
import Queue
import sys
import json
import base64
import page_coding_verifier
import carpenter_log_pb2
import idigger_util
from idigger_util import IdiggerUtil
from kafka import KafkaClient, SimpleConsumer


#
# configs
#

CONSUME_FROM_HEAD = 0
CONSUME_FROM_CURRENT = 1
CONSUME_FROM_TAIL = 2

# g_brokers_addr = 'localhost:9092'
# g_topic = 'test'
g_brokers_addr = ('kk001.karl.kafka.allyes.com:9092,'
                  'kk002.karl.kafka.allyes.com:9092,'
                  'kk003.karl.kafka.allyes.com:9092')
g_topic = 'idigger'

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

class PageCodingVerifier(object):

    TXT_DEATH_TIME = 'death_time'
    TXT_UPDATE_TIMESTAMPS = 'update_timestamps'
    TXT_LAST_ENCOUNTERED = 'last_encountered'

    def __init__(self, filter_life_time_in_minuter=5):
        self.filter_life_time_in_minuter = filter_life_time_in_minuter
        assert self.filter_life_time_in_minuter > 0

        self.filters = {}
        self.last_check_time = time.time()

    def add_filter(self, new_filter):
        """Add a new filter.

        Every filter will survive for 'self.filter_life_time_in_minuter'.
        If alreadly existed, it'll get another 'self.filter_life_time_in_minuter'
        of lifetime.

        Args:
            new_filter: A dict; E.g., {"request_url":"abc"}

        Returns:
            None

        Raises:
            ActionParamError will be raised if 'new_filter' contains wrong
                content.
        """

        try:
            new_filter["request_url"].lower()  # make sure it's a string
            key = new_filter["request_url"]
        except:
            raise ActionParamError

        if not self.filters.has_key(key):
            self.filters[key] = {}

        page_info = self.filters[key]

        # update lifetime
        page_info[self.TXT_DEATH_TIME] = (
            time.time() + self.filter_life_time_in_minuter * 60)

        # initialize updating-timestamps
        if self.TXT_UPDATE_TIMESTAMPS not in page_info:
            page_info[self.TXT_UPDATE_TIMESTAMPS] = {}
            page_update_timestamps = page_info[self.TXT_UPDATE_TIMESTAMPS]
            page_update_timestamps[self.TXT_LAST_ENCOUNTERED] = 0
            for page_type in IdiggerUtil.PAGE_TYPES:
                page_update_timestamps[page_type] = 0

    def query(self, query_obj):
        """Do a query with the specific condition.

        Args:
            query_obj: A dict; E.g., {"request_url":"abc"}

        Returns:
            A dict. E.g.,
            {
                'succeed': False,
                'error': 'some error',
            }
            or
            {
                'succeed': True,
                'last_encountered': 123,
                ...
            }
        """

        try:
            query_obj["request_url"].lower()  # make sure it's a string
            key = query_obj["request_url"]
        except:
            return {
                'succeed': False,
                'error': 'Invalid param: %s' % json.dumps(query_obj),
            }

        if key not in self.filters:
            return {
                'succeed': False,
                'error': 'Not registed: %s' % key,
            }

        r = {}
        r.update(self.filters[key][self.TXT_UPDATE_TIMESTAMPS])
        r['succeed'] = True
        return r

    def periodic_check(self, time_now):
        """ check every 1 minutes to delete dead filters """

        if time_now < self.last_check_time:
            self.last_check_time = time_now

        if time_now - self.last_check_time >= 60:
            keys_to_be_deleted = []
            for key in self.filters:
                if time_now >= self.filters[key][self.TXT_DEATH_TIME]:
                    keys_to_be_deleted.append(key)
            for key in keys_to_be_deleted:
                del self.filters[key]
            self.last_check_time = time_now

    def handle_message(self, msg):
        try:
            log_content = msg.message.value.strip()
            binary_stream = base64.standard_b64decode(log_content)
            rawlog = carpenter_log_pb2.RawLog()
            rawlog.ParseFromString(binary_stream)
            self._handle_rawlog(rawlog)
        except:
            return

    def _handle_rawlog(self, rawlog):
        page_url = IdiggerUtil.get_page_url(rawlog.request_url)
        if not page_url: return
        if page_url not in self.filters: return

        update_timestamps = self.filters[page_url][self.TXT_UPDATE_TIMESTAMPS]

        self._update_dict_if_greater(update_timestamps,
                                     self.TXT_LAST_ENCOUNTERED,
                                     rawlog.timestamp)

        page_kinds = IdiggerUtil.get_page_kinds(rawlog.request_url)
        for kind in page_kinds:
            self._update_dict_if_greater(update_timestamps, kind,
                                         rawlog.timestamp)

    @classmethod
    def _update_dict_if_greater(cls, the_dict, key, new_value):
        if (not the_dict.has_key(key)) or new_value > the_dict[key]:
            the_dict[key] = new_value

def handle_web_requests(time_now, read_queue, write_queue, page_verifier):
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
            page_verifier.add_filter(action_param)
            ret['succeed'] = True
        except ActionParamError:
            ret['succeed'] = False
            ret['error'] = "Invalid param: %s" % json.dumps(action_param)
    elif action == ACTION_QUERY:
        ret = page_verifier.query(action_param)
    else:
        assert False

    write_queue.put(ret)

def main():
    log_info('Connecting to kafka cluster: ' + g_brokers_addr)
    kafka = KafkaClient(g_brokers_addr)

    log_info('Consumer topic: ' + g_topic)
    log_info('Consumer group: ' + g_consumer_group)
    log_info('Consumer init position: ' + str(g_consume_init_position))

    consumer = SimpleConsumer(kafka, g_consumer_group, g_topic)

    # create a sub process to handle http requests
    read_queue  = multiprocessing.Queue()
    write_queue = multiprocessing.Queue()
    web_server_process = multiprocessing.Process(
        target = page_coding_verifier.run,
        args = (8000, write_queue, read_queue))
    web_server_process.start()

    # adjust offset
    consumer.seek(0, g_consume_init_position)

    try:
        # get messages from kafka to handle

        pg_verifier = PageCodingVerifier()

        last_check_time = time.time()
        CHECK_INTERVAL_IN_SECONDS = 0.05

        last_time_to_check_pending = 0
        PENDING_CHECK_INTERVAL_IN_SECONDS = 60

        while True:
            msg = consumer.get_message(block=True,
                                       timeout=CHECK_INTERVAL_IN_SECONDS,
                                       get_partition_info=False)
            if msg:
                pg_verifier.handle_message(msg)

            TIME_NOW = time.time()

            if TIME_NOW < last_check_time: last_check_time = TIME_NOW
            if TIME_NOW - last_check_time >= CHECK_INTERVAL_IN_SECONDS:
                pg_verifier.periodic_check(TIME_NOW)
                handle_web_requests(TIME_NOW, read_queue, write_queue, pg_verifier)
                last_check_time = TIME_NOW

            # pending check
            if TIME_NOW < last_time_to_check_pending:
                last_time_to_check_pending = TIME_NOW
            if TIME_NOW - last_time_to_check_pending >= PENDING_CHECK_INTERVAL_IN_SECONDS:
                log_info('PENDING: %d' % consumer.pending())
                last_time_to_check_pending = TIME_NOW

    except KeyboardInterrupt:
        log_info('User interrupt this app.')

    log_info('App close now.')
    kafka.close()


if __name__ == '__main__':
    main()
