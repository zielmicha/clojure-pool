#!/usr/bin/python
import socket
import os
import sys
import subprocess
import Queue
import threading

children = Queue.Queue(7)
child_args = ['clojure', os.path.join(os.path.dirname(__file__), 'stub.clj')]

if os.environ.get('CLASSPATH'):
    os.environ['CLASSPATH'] += ':'
else:
    os.environ['CLASSPATH'] = ''

os.environ['POOL_BASEDIR'] = os.path.abspath(os.path.dirname(__file__))
os.environ['CLASSPATH'] += os.path.abspath(os.path.dirname(__file__))

def main():
    if not os.path.exists('.pool'):
        os.mkdir('.pool')

    threading.Thread(target=child_spawner).start()

    sock = socket.socket(socket.AF_UNIX)
    sock.bind('.pool/serv')
    sock.listen(1)
    while True:
        client, addr = sock.accept()
        threading.Thread(target=handle, args=[client]).start()
        del client

def handle(sock):
    print 'connection'
    pipe_w, pid = children.get()
    f = sock.makefile('r+', 1)
    pipe_w.write(f.read(int(f.readline())))
    pipe_w.flush()
    _pid, status = os.waitpid(pid, 0)
    f.write('%s\n' % status)

def spawn_child():
    print 'spawning child'
    pipe_r, pipe_w = os.pipe()
    pipe_w = os.fdopen(pipe_w, 'w')
    proc = subprocess.Popen(child_args, stdin=pipe_r)
    return [pipe_w, proc.pid]

def child_spawner():
    # rate is limited by queue size
    while True:
        children.put(spawn_child())

if __name__ == '__main__':
    main()
