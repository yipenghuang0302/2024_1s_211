OUTPUT=2_multstore
CC=gcc
CFLAGS=-Og -Wall -Werror -std=c99
ASM = swap.s

%.s: %.c
	$(CC) $(CFLAGS) -g -S -fno-inline -fno-if-conversion $^ -o $@

$(OUTPUT): $(OUTPUT).s
	$(CC) $(CFLAGS) $^ -o $@

all: $(OUTPUT)

clean:
	rm -f *.s *.o $(OUTPUT)
