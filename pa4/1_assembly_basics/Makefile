OUTPUT=1_swap
CC=gcc
CFLAGS= -Og -Wall -Werror -std=c99
ASM = 1_swap.s

%.s: %.c
	$(CC) $(CFLAGS) -S -fno-inline -fno-if-conversion $^ -o $@

$(OUTPUT): $(OUTPUT).s
	$(CC) $(CFLAGS) $^ -o $@

all: $(OUTPUT)

clean:
	rm -f *.s *.o $(OUTPUT)
