OUTPUT=anyToAny
CFLAGS=-g -Wall -Werror -fsanitize=address -std=c99 -lm
LFLAGS=

%: %.c %.h
	gcc $(CFLAGS) -o $@ $< $(LFLAGS)

%: %.c
	gcc $(CFLAGS) -o $@ $< $(LFLAGS)

all: $(OUTPUT)

clean:
	rm -f *.o $(OUTPUT)
