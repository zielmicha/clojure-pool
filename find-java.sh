#!/bin/bash
base=$(dirname $(readlink -f $(which java)))
if [ -e $base/../../include ]; then
    echo $base/../../include
elif [ -e $base/../include ]; then
    echo $base/../include
else
    echo 'Java include not found.' >&2
    echo 'Use "make JAVA_INC=<folder with jni.h>"' >&2
    exit 1
fi
