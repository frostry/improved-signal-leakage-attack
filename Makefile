CC      := gcc
TARGETS:= c_poly.so
ARGS   := reduce.c

.PHONY: all clean

all: c_poly.so

c_poly.so: $(ARGS) poly.c
	$(CC) -std=c99 -shared $^ -o $@ -fPIC $(CFLAGS)

clean:
	rm -f $(TARGETS) *.o 
