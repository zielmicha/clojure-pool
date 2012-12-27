#!/usr/bin/python
import os
import socket
import sys

stdin_path = os.readlink('/proc/self/fd/0')
stdout_path = os.readlink('/proc/self/fd/1')
stderr_path = os.readlink('/proc/self/fd/2')

sock = socket.socket(socket.AF_UNIX)
sock.connect('.pool/serv')
data = '%s\n%s\n%s\n%d\n%s\n' % (stdin_path, stdout_path, stderr_path, len(sys.argv[1:]), '\n'.join(sys.argv[1:]))
sock.sendall('%d\n%s' % (len(data), data))

status = int(sock.makefile('r').readline())
sys.exit(status)
