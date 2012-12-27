all: duphelper.so DupHelper.class

duphelper.so: DupHelper.c DupHelper.h
	gcc DupHelper.c -shared -fPIE -I/usr/lib/jvm/java-7-openjdk-amd64/include/ -Wall -o duphelper.so

DupHelper.class: DupHelper.java
	javac DupHelper.java
