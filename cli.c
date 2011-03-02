#include <avr/pgmspace.h>
#include <avr/interrupt.h>
#include <stdio.h>
#include "cli.h"
#include "softuart.h"
#include "pid.h"

extern uint8_t opmode, y, x, w, Kp, KpAttn, Kd, Ki;

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


void command_loop()
{
    char cmd[5];
    int argv, a, b, c;

    if (softuart_kbhit())
    {
        argv = scanf("%s %i %i %i", cmd, &a, &b, &c);

        if (strcmp_P(cmd, PSTR("man") ) == 0)
            opmode = MANUAL;
        else if (strcmp_P(cmd, PSTR("auto")) == 0)
            opmode = AUTO;
        else if (strcmp_P(cmd, PSTR("stop")) == 0)
            opmode = STOP;
        else if (strcmp_P(cmd, PSTR("sv")) == 0)
        {
        }
        else if (strcmp_P(cmd, PSTR("sp")) == 0)
        {
        }
        else if (strcmp_P(cmd, PSTR("sa")) == 0)
        {
        }
        else if (strcmp_P(cmd, PSTR("si")) == 0)
        {
        }
        else if (strcmp_P(cmd, PSTR("sy")) == 0)
        {
        }
        else if (strcmp_P(cmd, PSTR("vc")) == 0)
        {
        }
        else if (strcmp_P(cmd, PSTR("vx")) == 0)
        {
        }
        else if (strcmp_P(cmd, PSTR("vy")) == 0)
        {
        }
        else if (strcmp_P(cmd, PSTR("vw")) == 0)
        {
        }
        else
            puts_P(PSTR("?"));

    }
}
