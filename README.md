clojure-pool
============

Clojure startup accelerator

Usage
----------------

Build:
    
    make

Start server:

    mkdir .pool
    CLASSPATH=... python server.py

Run clojure:
    
    python client.py args...

Profit!
----------------

    $ time clojure ~/null.clj

    real    0m0.900s
    user    0m1.244s
    sys     0m0.036s

    $ time python client.py ~/null.clj 

    real    0m0.089s
    user    0m0.020s
    sys     0m0.000s
