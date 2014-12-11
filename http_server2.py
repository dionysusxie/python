#!/usr/bin/env python

import sys
from SimpleHTTPServer import SimpleHTTPRequestHandler
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler


class MyHTTPRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        print '===== self.path: ' + str(self.path)
        print '===== translate path: ' + str(self.translate_path(self.path))

        f = "[1, 2, 3]"

        self.send_response(200)
        encoding = sys.getfilesystemencoding()
        self.send_header("Content-type", "text/html; charset=%s" % encoding)
        self.send_header("Content-Length", str(len(f)))
        self.end_headers()
        self.wfile.write(f)


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
