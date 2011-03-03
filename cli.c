#include <avr/pgmspace.h>
#include <avr/interrupt.h>
#include <stdio.h>
#include "cli.h"
#include "softuart.h"
#include "pid.h"

extern uint8_t opmode, y, x, w, Kp, KpAttn, Kd, Ki;

void init_cli()
{
    softuart_init();
    sei();
}


void command_loop()
{
    char c, d;

    if (softuart_kbhit())
    {
        c = softuart_getchar();
        switch (c) {
            case 'a':
                opmode = AUTO;
            break;

            case 'm':
                opmode = MANUAL;
            break;

            case 'o':
                opmode = STOP;
            break;

            case 's':
                c = softuart_getchar();
                switch (c) {
                    case 'v':
                        w = softuart_getchar();
                    break;

                    case 'p':
                        Kp = softuart_getchar();
                        Ki = softuart_getchar();
                        Kd = softuart_getchar();
                        pid_save_parameters();
                    break;

                    case 'i':
                        pid_set_initial(
                           softuart_getchar(),
                           softuart_getchar());
                    break;

                    case 'y':
                        y = softuart_getchar();
                        opmode = MANUAL;
                    break;
                }
            break;

            case 'v':
            break;
        }
    }
}
