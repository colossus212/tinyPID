#include <stdio.h>

// Wrappers around UART I/O
static int uart_put(char c, FILE *stream);
static int uart_get(FILE *stream);

void init_cli();
void command(char c);
