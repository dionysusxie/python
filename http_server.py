#!/usr/bin/env python

import sys
import shutil
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


class MyHTTPRequestHandler(BaseHTTPRequestHandler):
  def do_GET(self):
    f = StringIO()
    f.write('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">')
    f.write("<html><body>abc</body></html>")

    self.send_response(200)
    encoding = sys.getfilesystemencoding()
    self.send_header("Content-type", "text/html; charset=%s" % encoding)
    self.send_header("Content-Length", str(f.tell()))
    self.end_headers()
    self.copyfile(f, self.wfile)
    print f.getvalue()
    f.close()

  def copyfile(self, source, outputfile):
    """Copy all data between two file objects.
  
    The SOURCE argument is a file object open for reading
    (or anything with a read() method) and the DESTINATION
    argument is a file object open for writing (or
    anything with a write() method).
  
    The only reason for overriding this would be to change
    the block size or perhaps to replace newlines by CRLF
    -- note however that this the default server uses this
    to copy binary data as well.
  
    """
    shutil.copyfileobj(source, outputfile)


#
# run
#
def test(HandlerClass = MyHTTPRequestHandler,
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
  test()
