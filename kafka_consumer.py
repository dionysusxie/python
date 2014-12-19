#!/usr/bin/env python -u

import time
from kafka import KafkaClient, SimpleConsumer
from syslog import LOG_INFO

#
# configs
#

g_brokers_addr = 'localhost:9092'
g_consumer_group = 'page_code_verify'
g_topic = 'test'


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

    for message in consumer:
        # message is raw byte string -- decode if necessary!
        # e.g., for unicode: `message.decode('utf-8')`
        # print 'message.__dict__:', message.__dict__
        log_info('Message received - ' + repr(message.message.value))

except KeyboardInterrupt:
    log_info('User interrupt this app.')
except:
    log_error('Unknow exception!')

log_info('App close now.')
kafka.close()
