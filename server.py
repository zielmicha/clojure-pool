#!/usr/bin/python
import socket
import os
import sys
import subprocess
import Queue
import threading
import signal

children = Queue.Queue(7)
child_args = ['clojure', os.path.abspath(os.path.join(os.path.dirname(__file__), 'stub.clj'))]

if os.environ.get('CLASSPATH'):
    os.environ['CLASSPATH'] += ':'
else:
    os.environ['CLASSPATH'] = ''

basedir = os.environ['POOL_BASEDIR'] = os.path.abspath(os.path.dirname(__file__))
org_classpath = os.environ['CLASSPATH']
os.environ['CLASSPATH'] += basedir
pids = []

def exit():
    for pid in pids:
        try:
            os.kill(pid, 15)
        except OSError:
            pass
    print
    os._exit(0)

signal.signal(signal.SIGINT, lambda *_: exit())

def main():
    if not os.path.exists('.pool'):
        os.mkdir('.pool')
    if os.path.exists('.pool/serv'):
        os.remove('.pool/serv')

    with open('.pool/clojure', 'w') as f:
        f.write('#!/bin/bash\nif [ $# = 0 ]; then exec $0 %s/repl.clj; exit 1; fi\n'
                'exec %s/client.py --server %s $*\n' % (basedir, basedir, os.getcwd()))

    os.chmod('.pool/clojure', 0o755)
    with open('.pool/cp', 'w') as f:
        f.write(org_classpath)

    print '----------------------------------------------------'
    print 'Use the following command to connect to clojure:'
    print os.path.abspath('.pool/clojure')
    print '----------------------------------------------------'

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
    f.write('%d\n' % pid)
    _pid, status = os.waitpid(pid, 0)
    f.write('%s\n' % status)

def spawn_child():
    pipe_r, pipe_w = os.pipe()
    pipe_w = os.fdopen(pipe_w, 'w')
    proc = subprocess.Popen(child_args, stdin=pipe_r)
    pids.append(proc.pid)
    return [pipe_w, proc.pid]

def child_spawner():
    # rate is limited by queue size
    while True:
        children.put(spawn_child())

if __name__ == '__main__':
    if any( arg.startswith('-') for arg in sys.argv ) or len(sys.argv) > 2:
        sys.exit('usage: %s [listen-directory]' % sys.argv[0])
    if sys.argv[1:]:
        os.chdir(sys.argv[1])
    try:
        try:
            main()
        except:
            import traceback
            traceback.print_exc()
    finally:
        exit()
