.PHONY: all clean install
export PREFIX ?= /usr

CFLAGS ?= -Wall -g
textlabel: CFLAGS += $(shell pkg-config --cflags freetype2)
textlabel: LDLIBS += $(shell pkg-config --libs freetype2) -lfontconfig

all: pt1230 textlabel line2bitmap

install:
	mkdir -p "$(PREFIX)/sbin"
	mkdir -p "$(PREFIX)/bin"
	install -m 0755 pt1230 "$(PREFIX)/sbin"
	install -m 0755 textlabel "$(PREFIX)/bin"
	install -m 0755 line2bitmap "$(PREFIX)/bin"

clean:
	-rm interactive
	-rm pt1230
	-rm textlabel
	-rm line2bitmap
