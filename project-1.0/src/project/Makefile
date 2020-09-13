#!/usr/bin/make -f

.PHONY: build install uninstall

build: project
	g++ project.cc -o project
	# prepare stuff - probably don't need unless i compile py to bin 
	
	
install: build
	cp project /usr/local/bin

uninstall: /usr/local/bin/project
	rm /usr/local/bin/project