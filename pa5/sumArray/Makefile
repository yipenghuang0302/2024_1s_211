OUTPUT=sumArray
CFLAGS=-Og -Wall -Werror -std=c99
# -floop-interchange
# -floop-nest-optimize
LFLAGS=-lm

%: %.c %.h
	gcc $(CFLAGS) -o $@ $< $(LFLAGS)

%: %.c
	gcc $(CFLAGS) -o $@ $< $(LFLAGS)

all: $(OUTPUT)

clean:
	rm -f *.o $(OUTPUT)
