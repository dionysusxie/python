#!/usr/bin/env python -u
# /usr/local/bin/python -u

# E.g.,
# localhost:8000/add_filter/{"request_url":"abc","advertiser_id":"123"}

import os
import posixpath
import BaseHTTPServer
import urllib
import cgi
import shutil
import mimetypes
import sys
import json
import time

from SimpleHTTPServer import SimpleHTTPRequestHandler
from BaseHTTPServer import HTTPServer


def normalize_path(path):
    # abandon query parameters
    #path = path.split('?', 1)[0]
    #path = path.split('#', 1)[0]
    #path = posixpath.normpath(urllib.unquote(path))
    path = urllib.unquote(path)
    return path.strip()

def get_action_from_path(path):
    if len(path) == 0:
        return None

    # make sure begin with /
    if path[0] != '/':
        path = '/' + path

    sec_list = path.split('/', 2)
    return sec_list[1]

def get_action_json_from_path(path):
    if len(path) == 0:
        return None

    # make sure begin with /
    if path[0] != '/':
        path = '/' + path

    sec_list = path.split('/', 2)
    if len(sec_list) >= 3:
        return sec_list[2]
    else:
        return None

def parseJsonStr(s):
    """
    Paras:
        s  A json string.

    Return
        A tuple: (True, JsonObj) or (False, ErrorStr)

    """

    try:
        js_obj = json.loads(s)
        return (True, js_obj)
    except:
        err = {
            'succeed': False,
            'error': 'Bad json format: %s' % s
        }
        return (False, json.dumps(err))

class MyHTTPRequestHandler(SimpleHTTPRequestHandler):
    process_queue_in = None
    process_queue_out = None

    def do_GET(self):
        try:
            normalized_path = normalize_path(self.path)
            action = get_action_from_path(normalized_path)
            action_json = get_action_json_from_path(normalized_path)

            print ''
            print '=== self.path      : ' + str(self.path)
            print '=== Normalized path: ' + normalized_path
            print '=== Action         : ' + str(action)
            print '=== Action Json    : ' + str(action_json)

            res = self.handle_action(action, action_json)
            print '=== Return         : ' + res

        except Exception, e:
            err = {
                'succeed': False,
                'error': 'Exception: %s' % str(e),
            }
            res = json.dumps(err)
            print '=== Exception: ' + res

        self.send_response(200)
        encoding = sys.getfilesystemencoding()
        self.send_header("Content-type", "text/html; charset=%s" % encoding)
        self.send_header("Content-Length", str(len(res)))
        self.end_headers()
        self.wfile.write(res)

    def handle_action(self, action, action_json):
        if action == 'add_filter':
            return self.handle_add_filter(action_json)
        elif action == 'query':
            return self.handle_query(action_json)
        else:
            err = {
                'succeed': False,
                'error': 'unsupported action: %s' % str(action),
            }
            return json.dumps(err)

    def handle_add_filter(self, action_json):
        res = parseJsonStr(action_json)
        if not res[0]:
            return res[1]

        new_filter = res[1]
        ret = {}
        if 'request_url' in new_filter and 'advertiser_id' in new_filter:
            ret['succeed'] = True
            MyHTTPRequestHandler.process_queue_out.put(['add_filter'])
        else:
            ret['succeed'] = False
            ret['error'] = 'Missing some fileds'
        return json.dumps(ret)

    def handle_query(self, action_json):
        res = parseJsonStr(action_json)
        if not res[0]:
            return res[1]

        new_query = res[1]
        ret = {}

        if 'request_url' in new_query and 'advertiser_id' in new_query:
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
            ret['succeed'] = False
            ret['error'] = 'Missing some fileds'

        return json.dumps(ret)

#
# run
#

def run(port,
        process_queue_in,
        process_queue_out):

    MyHTTPRequestHandler.process_queue_in = process_queue_in
    MyHTTPRequestHandler.process_queue_out = process_queue_out
    MyHTTPRequestHandler.protocol_version = "HTTP/1.0"

    server_address = ('', port)
    httpd = HTTPServer(server_address, MyHTTPRequestHandler)

    sa = httpd.socket.getsockname()
    print "Serving HTTP on", sa[0], "port", sa[1], "..."

    httpd.serve_forever()