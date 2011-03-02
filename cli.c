#include <avr/pgmspace.h>
#include <avr/interrupt.h>
#include <stdio.h>
#include "cli.h"
#include "softuart.h"
#include "pid.h"

extern uint8_t opmode;

// Wrappers around UART I/O
static int uart_put(char c, FILE *stream);
static int uart_get(FILE *stream);

// Setup streams
static FILE uart_stream = FDEV_SETUP_STREAM(uart_put, uart_get, _FDEV_SETUP_RW);


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
    char *buf[10];

    switch (c)
    {
      case 's':
        // 'set' command or 'stop'
        c = getchar();
        switch (c)
        {
            case 't':
                // 'stop' command
                if (scanf("op\n"))
                    opmode = STOP;
            break;

            case 'v':
            break;

            case 'p':
            break;

            case 'a':
            break;

            case 'i':
            break;

            case 'y':
            break;

            default:
              puts("?");
        }
      break;

      case 'v':
        // 'view' command
        c = getchar();
        switch (c)
        {
            case 'c':
            break;

            case 'x':
            break;

            case 'y':
            break;

            default:
              puts("?");
        }
      break;

      case 'a':
        // 'auto' command
        if (scanf("uto\n"))
            opmode = AUTO;
      break;

      case 'm':
        // 'man' command
        if (scanf("an\n"))
            opmode = MANUAL;
      break;

      default:
        puts("?");
    }
}

void command_loop()
{
    char c;
    if(softuart_kbhit())
    {
        c = getchar();
        command(c);
    }
}
