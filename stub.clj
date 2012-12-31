(ns stub
  [:require stacktrace])
(println "classpath:" (seq (.getURLs (java.lang.ClassLoader/getSystemClassLoader))))
(import DupHelper)

(def input (java.io.BufferedReader. (java.io.InputStreamReader. System/in)))

(defn -main []
;  (println 'starting)
  (def stdin (.readLine input))
  (def stdout (.readLine input))
  (def stderr (.readLine input))

  (DupHelper/reopen stdin 0 false)
  (DupHelper/reopen stdout 1 true)
  (DupHelper/reopen stderr 2 true)

  (def arg-count (Integer/parseInt (.readLine input)))
  (def args (map (fn [n] (.readLine input)) (range arg-count)))
  (binding [*command-line-args* (vec (rest args))]
    (try
      (load-file (first args))
      (catch Throwable err (stacktrace/print-throwable-trace err)))))

(-main)
