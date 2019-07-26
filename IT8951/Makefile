SRCS=IT8951.c
CC=gcc
TARGETS=IT8951.so IT8951.o
LDFLAGS=-lbcm2835

default: IT8951.so

IT8951.o:IT8951.c
	$(CC) -c $^

IT8951.so:IT8951.o
	$(CC) -shared -Wl,-soname,IT8951 -o $@ $^ $(LDFLAGS)

clean:
	rm -f $(TARGETS)
