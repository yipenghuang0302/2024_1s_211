OUTPUT=3_branch
CC=gcc
CFLAGS=-Og -Wall -Werror -std=c99
ASM = 3_branch.s

%.s: %.c
	$(CC) $(CFLAGS) -S -fno-inline -fno-if-conversion $^ -o $@

$(OUTPUT): $(OUTPUT).s
	$(CC) $(CFLAGS) $^ -o $@

all: $(OUTPUT)

clean:
	rm -f *.s *.o $(OUTPUT)
