#!/usr/bin/env python -u
# /usr/local/bin/python -u

# E.g.,
# localhost:8000/add_filter/{"request_url":"abc"}

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
        A tuple: (True, JsonObj) or (False, )

    """

    try:
        js_obj = json.loads(s)
        return (True, js_obj)
    except:
        return (False,)

class MyHTTPRequestHandler(SimpleHTTPRequestHandler):
    process_read_queue = None
    process_write_queue = None

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
        res = parseJsonStr(action_json)
        if not res[0]:
            err = {
                'succeed': False,
                'error': 'Bad json format: %s' % action_json
            }
            return json.dumps(err)

        action_param = res[1]
        MyHTTPRequestHandler.process_write_queue.put((action, action_param))
        ret = MyHTTPRequestHandler.process_read_queue.get()
        return json.dumps(ret)


#
# run
#

def run(port,
        process_read_queue,
        process_write_queue):

    MyHTTPRequestHandler.process_read_queue = process_read_queue
    MyHTTPRequestHandler.process_write_queue = process_write_queue
    MyHTTPRequestHandler.protocol_version = "HTTP/1.0"

    server_address = ('', port)
    httpd = HTTPServer(server_address, MyHTTPRequestHandler)

    sa = httpd.socket.getsockname()
    print "Serving HTTP on", sa[0], "port", sa[1], "..."

    httpd.serve_forever()