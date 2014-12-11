#!/usr/bin/env python

import sys
import shutil
from SimpleHTTPServer import SimpleHTTPRequestHandler
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


class MyHTTPRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        """Serve a GET request."""

        print '===== self.path: ' + str(self.path)
        print '===== translate path: ' + str(self.translate_path(self.path))

        f = self.send_head()
        if f:
            self.copyfile(f, self.wfile)
            f.close()

    def nothing(self):
        return


#
# run
#

def run(HandlerClass = MyHTTPRequestHandler,
        ServerClass = HTTPServer,
        protocol = "HTTP/1.0"):
    """Test the HTTP request handler class.

      This runs an HTTP server on port 8000 (or the first command line
      argument).

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
