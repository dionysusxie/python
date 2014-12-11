#!/usr/bin/env python
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

from SimpleHTTPServer import SimpleHTTPRequestHandler
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

def normalize_path(path):
    # abandon query parameters
    path = path.split('?', 1)[0]
    path = path.split('#', 1)[0]
    path = posixpath.normpath(urllib.unquote(path))
    return path.strip()

def get_path_sec(path, index):
    """
    Paras:
        path  The path seperated with /
        index The section index, starting from 1.

    Note: The first char of 'path' will set to be / forcedly!
        And if 'index' is out of range, return None.

    E.g.,
        get_path_sec('/abc/def', 0) ==> ''
        get_path_sec('/abc/def', 1) ==> 'abc'
        get_path_sec('/abc/def', 2) ==> 'def'
        get_path_sec('/abc/def', 3) ==> None

    """

    if len(path) == 0:
        return None

    # make sure begin with /
    if path[0] != '/':
        path = '/' + path

    sec_list = path.split('/')
    if 0 <= index < len(sec_list):
        return sec_list[index]
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
            'error': 'Bad json format',
        }
        return (False, json.dumps(err))

class MyHTTPRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        try:
            normalized_path = normalize_path(self.path)
            action = get_path_sec(normalized_path, 1)
            action_json = get_path_sec(normalized_path, 2)

            print ''
            print '=== self.path          : ' + str(self.path)
            print '=== Normalized path    : ' + normalized_path
            print '=== Action : ' + str(action)
            print '=== Action Json: ' + str(action_json)

            res = self.handle_action(action, action_json)
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
            ret['succeed'] = True
            ret['last_encountered'] = 0
            ret['sitepage'] = 0          # => '1'
            ret['skupage'] = 0           # => '2'
            ret['cartpage'] = 0          # => '3'
            ret['conversionpage'] = 0    # => '4'
            ret['orderpage'] = 0         # => '5'
            ret['paidpage'] = 0          # => '6'
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

def run(HandlerClass = MyHTTPRequestHandler,
        ServerClass = HTTPServer,
        protocol = "HTTP/1.0"):
    """Test the HTTP request handler class.

    This runs an HTTP server on port 8000 (or the first command line argument).

    """

    if sys.argv[1:]:
        port = int(sys.argv[1])
    else:
        port = 8000

    server_address = ('', port)
    HandlerClass.protocol_version = protocol
    httpd = ServerClass(server_address, HandlerClass)

    sa = httpd.socket.getsockname()
    print "Serving HTTP on", sa[0], "port", sa[1], "..."
    httpd.serve_forever()

if __name__ == '__main__':
    run()
