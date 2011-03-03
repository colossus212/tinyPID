/*
 * CLI.c
 *
 * Command-line interface (sort of) for tinyPID.
 *
 * The format is kind of raw, each incoming byte is interpreted and should
 * should have a meaning.
 * Arguments to commands have a range of 0…255 and are sent as raw bytes too.
 * The commands itself can be intrepreted as ASCII characters. No line-ending 
 * is needed. A command is terminated when all of its arguments have been read.
 *
 * In the following table, X is any byte
 *
 * ASCII         HEX          DESCRIPTION
 * a             61           set mode to automatic
 * m             6D           set mode to manual
 * o             6F           set mode to off, no output
 *
 * svX           73 76  X     set the set-value to X
 * syX           73 79  X     set output value to X, 
 *                             this toggles manual mode
 * spXXX         73 70  X X X set the parameters 10Kp, Ki, Kd to the X's (in that order)
 * siaX          73 69 61 X   set initial mode (after power-up) to automatic, 
 *                             initial set-value to X
 * simX          73 69 6D X   set initial mode to manual,
 *                             initial output to X
 * gp            67 70        get parameters, returns 10Kp, Ki, Kd, in that order
 * gm            67 6D        get operation mode, returns 'a', 'm' or 'o'
 * gi            67 69        get initial mode and value, in that order
 * gv            67 76        get set-value, returns that byte
 * gx            67 76        get process value, returns that byte
 * gy            67 76        get output value, returns that byte
 *
 */


#include <avr/pgmspace.h>
#include <avr/interrupt.h>
#include <stdio.h>
#include "cli.h"
#include "softuart.h"
#include "pid.h"

extern uint8_t opmode, y, x, w, Kp, Kd, Ki, InitMode, InitValue;


void init_cli()
{
    softuart_init();
    sei();
}


void command_loop()
{
    char c;

    if (softuart_kbhit()) {
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
                        InitMode  = softuart_getchar();
                        InitValue = softuart_getchar();
                        pid_save_parameters();
                    break;

                    case 'y':
                        y = softuart_getchar();
                        opmode = MANUAL;
                    break;
                }
            break;

            case 'g':
                c = softuart_getchar();
                switch (c) {
                    case 'v':
                        softuart_putchar(w);
                    break;

                    case 'x':
                        softuart_putchar(x);
                    break;

                    case 'y':
                        softuart_putchar(y);
                    break;

                    case 'p':
                        softuart_putchar(Kp);
                        softuart_putchar(Ki);
                        softuart_putchar(Kd);
                    break;

                    case 'm':
                        softuart_putchar(opmode);
                    break;

                    case 'i':
                        softuart_putchar(InitMode);
                        softuart_putchar(InitValue);
                    break;
                }
            break;

            default:
                softuart_putchar('?');
            break;
        }
    }
}
