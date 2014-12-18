#!/usr/bin/env python -u

import time
from kafka import KafkaClient, SimpleConsumer
from syslog import LOG_INFO

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


brokers_addr = 'localhost:9092'
log_info('Connecting to kafka cluster: ' + brokers_addr)
kafka = KafkaClient(brokers_addr)

try:
    consumer = SimpleConsumer(kafka, "my-group", "test")

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
