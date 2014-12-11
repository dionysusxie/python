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

class MyHTTPRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        normalized_path = normalize_path(self.path)
        action = get_path_sec(normalized_path, 1)
        action_json = get_path_sec(normalized_path, 2)

        print ''
        print '=== self.path          : ' + str(self.path)
        print '=== Normalized path    : ' + normalized_path
        print '=== Action : ' + str(action)
        print '=== Action Json: ' + str(action_json)

        f = self.handle_action(action, action_json)

        self.send_response(200)
        encoding = sys.getfilesystemencoding()
        self.send_header("Content-type", "text/html; charset=%s" % encoding)
        self.send_header("Content-Length", str(len(f)))
        self.end_headers()
        self.wfile.write(f)

    def handle_action(self, action, action_json):
        return '[2, 3, 4]'

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
