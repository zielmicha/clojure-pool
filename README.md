clojure-pool
============

Clojure startup accelerator

Usage
----------------

Build:

    make

Start server:

    $ CLASSPATH=... python server.py
    ----------------------------------------------------
    Use the following command to connect to clojure:
    /home/michal/myclojureapp/.pool/clojure
    ----------------------------------------------------

Run clojure:

    $ /home/michal/myclojureapp/.pool/clojure

Profit!
----------------

    $ time clojure ~/null.clj

    real    0m0.900s
    user    0m1.244s
    sys     0m0.036s

    $ time .pool/clojure ~/null.clj

    real    0m0.089s
    user    0m0.020s
    sys     0m0.000s
