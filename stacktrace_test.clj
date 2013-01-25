(ns stacktrace-test
  [:use stacktrace])

;(println (read-file-or-nil "/home/generic/clojure-pool/stub.clj"))

(defn cause-exception []
  (/ 1 0))

(defn cause-exception2 []
  (try
    (cause-exception)
    (catch Throwable err
      (let [err (java.lang.Exception. "foobar" err)]
        (throw err)))))

(try
  (cause-exception2)
  (catch Throwable err (print-throwable-trace err)))
