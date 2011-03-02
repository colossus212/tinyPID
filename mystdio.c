#include "mystdio.h"
#include "softuart.h"


// Setup streams
static FILE mystdout = FDEV_SETUP_STREAM(uart_put, NULL, _FDEV_SETUP_WRITE);
static FILE mystdin  = FDEV_SETUP_STREAM(NULL, uart_get, _FDEV_SETUP_READ);

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


void mystdio_init()
{
    softuart_init();
    stdout = &mystdout;
    stdin  = &mystdin;
}
