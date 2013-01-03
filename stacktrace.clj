(ns stacktrace)

(def format-single)
(def load-line)
(def read-file-or-nil)
(def read-file-from-classpath)

(def color-clojure "\033[1;32m")
(def color-header "\033[1;4m")
(def color-code "\033[0;33m")
(def color-code-java "\033[0;33m")
(def color-normal "\033[0m")

(defn format-trace [trace]
  (str
   (clojure.string/join "\n" (map format-single (reverse trace)))))

(defn format-single [element]
  (let [stru {:fn (.getFileName element),
              :lineno (.getLineNumber element),
              :class (.getClassName element),
              :method (.getMethodName element)}
        is-clojure (.endsWith (:fn stru) ".clj")]
    (str (if is-clojure color-clojure)
         (format "  File '%s', line %d, in %s.%s" (:fn stru) (:lineno stru) (:class stru) (:method stru))
         (let [line (load-line (:fn stru) (:lineno stru))]
           (when line
             (str (if is-clojure color-code color-code-java)
                  "\n     "
                  (.trim line)
                  color-normal)))
         color-normal)))

(defn load-line [fn lineno]
  (let [file (read-file-from-classpath fn)]
    (if (and file lineno (> (count file) lineno))
      (nth file (- lineno 1)))))

(defn read-file-from-classpath [fn]
  (loop [classpath (.getURLs (java.lang.ClassLoader/getSystemClassLoader))]
    (if (empty? classpath)
      nil
      (let [url (first classpath)
            dir (java.io.File. (.getFile url))
            filepath (java.io.File. dir fn)
            file (read-file-or-nil filepath)]
        (or file (recur (rest classpath)))))))

(defn read-file-or-nil [fn]
  (try
    (seq (.split (slurp fn) "\n"))
    (catch java.io.IOException err nil)))

(defn print-trace [trace]
  (println (format-trace trace)))

(defn print-throwable-trace-noheader [t]
  (print-trace (.getStackTrace t))
  (println (str color-header (.toString t) color-normal))
  (when (.getCause t)
    (println (str color-header "Caused by:" color-normal))
    (print-throwable-trace-noheader (.getCause t))))

(defn print-throwable-trace [t]
  (println (str color-header "Traceback (most recent call last):" color-normal))
  (print-throwable-trace-noheader t))

(defmacro with-stacktrace [& body]
  '(try
    ~@body
    (catch Throwable err (print-throwable-trace err))))
