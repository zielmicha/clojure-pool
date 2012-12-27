JAVA_INC=$(shell ./find-java.sh)

all: duphelper.so DupHelper.class

duphelper.so: DupHelper.c DupHelper.h
	gcc DupHelper.c -shared -fPIE -I$(JAVA_INC) -Wall -o duphelper.so

DupHelper.class: DupHelper.java
	javac DupHelper.java
