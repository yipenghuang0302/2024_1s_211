OUTPUT=rootFinder
CFLAGS=-g -Wall -Werror -fsanitize=address -std=c99
LFLAGS=

%: %.c %.h
	gcc $(CFLAGS) -o $@ $< $(LFLAGS)

%: %.c
	gcc $(CFLAGS) -o $@ $< $(LFLAGS)

all: $(OUTPUT)

clean:
	rm -f *.o $(OUTPUT)
