#include <avr/pgmspace.h>
#include <avr/interrupt.h>
#include "cli.h"
#include "softuart.h"

// Setup streams
static FILE uart_stream = FDEV_SETUP_STREAM(uart_put, uart_get, _FDEV_SETUP_RW);

// Wrappers around UART I/O
static int uart_put(char c, FILE *stream)
{
    softuart_putchar(c);
    return 0;
}
static int uart_get(FILE *stream)
{
    char c;
    c = softuart_getchar();
    return c;
}

void init_cli()
{
    softuart_init();
    stdout = stdin = &uart_stream;
    sei();
}


void command(char c)
{
    switch(c)
    {
      case 's':
        // 'set' command
      break;
      case 'v':
        // 'view' command
      break;
      case 'a':
        // 'auto' command
      break;
    }
}
