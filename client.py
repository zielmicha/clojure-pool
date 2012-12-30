#!/usr/bin/python
import os
import socket
import sys
import signal

if len(sys.argv) == 1:
    sys.exit('usage: %s [--server directory] args...' % sys.argv[0])

if sys.argv[1] == '--server':
    dir = sys.argv[2]
    del sys.argv[1:3]
else:
    dir = '.'

stdin_path = os.readlink('/proc/self/fd/0')
stdout_path = os.readlink('/proc/self/fd/1')
stderr_path = os.readlink('/proc/self/fd/2')

def connect():
    sock = socket.socket(socket.AF_UNIX)
    sock.connect('%s/.pool/serv' % dir)
    return sock

try:
    sock = connect()
except socket.error, err:
    import errno
    import subprocess
    import time
    if err.errno == errno.ECONNREFUSED:
        server_path = os.path.join(os.path.dirname(__file__), 'server.py')
        os.environ['CLASSPATH'] = '.'
        if sys.stderr.isatty():
            print >>sys.stderr, 'starting Clojure Pool server on `screen` with CLASSPATH=.'
        subprocess.check_call(['screen', '-d', '-m', '-S', 'clojurepool', server_path])
        for i in xrange(5):
            try:
                sock = connect()
            except socket.error:
                time.sleep(0.2)
            else:
                break
        sock = connect()
    else:
        raise

data = '%s\n%s\n%s\n%d\n%s\n' % (stdin_path, stdout_path, stderr_path, len(sys.argv[1:]), '\n'.join(sys.argv[1:]))
sock.sendall('%d\n%s' % (len(data), data))

pid = int(sock.makefile('r').readline())
try:
    status = int(sock.makefile('r').readline())
except KeyboardInterrupt:
    os.kill(pid, signal.SIGINT)
    print
else:
    sys.exit(status)
