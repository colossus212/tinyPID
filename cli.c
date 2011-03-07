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
 * In the following table, X is any byte, M is most-significant, L - least significant byte
 *
 * ASCII         HEX          DESCRIPTION
 * a             61           set mode to automatic
 * m             6D           set mode to manual
 * o             6F           set mode to off, no output
 *
 * svX           73 76  X     set the setpoint to X
 * syX           73 79  X     set output value to X, this toggles manual mode
 * sppML         73 70 70 M L set the parameter P_factor
 * spiML         73 70 69 M L set I_factor
 * spdML         73 70 64 M L set D_factor
 * siaX          73 69 61 X   set initial mode (after power-up) to automatic, 
 *                             initial setpoint to X
 * simX          73 69 6D X   set initial mode to manual,
 *                             initial output to X
 *
 * gpp           67 70 70     get parameter P_factor, returns MSB, LSB
 * gpi           67 70 69     get parameter I_factor, returns MSB, LSB
 * gpd           67 70 64     get parameter D_factor, returns MSB, LSB
 * gm            67 6D        get operation mode, returns 'a', 'm' or 'o'
 * gi            67 69        get initial mode and value, in that order
 * gv            67 76        get setpoint
 * gx            67 76        get process value
 * gy            67 76        get output value
 *
 */


#include <avr/pgmspace.h>
#include <avr/interrupt.h>
#include "cli.h"
#include "softuart.h"

void init_cli()
{
    softuart_init();
    sei();
}

uint16_t get_word()
{
    char a, b;
    a = softuart_getchar();
    b = softuart_getchar();
#ifdef MSB_FIRST
    return (a << 8) & b;
#else
    return (b << 8) & a;
#endif
}

void put_word(uint16_t word)
{
    uint8_t msb = word >> 8;
    uint8_t lsb = word & 0x00FF;
#ifdef MSB_FIRST
    softuart_putchar(msb);
    softuart_putchar(lsb);
#else
    softuart_putchar(lsb);
    softuart_putchar(msb);
#endif
}

void command_loop(struct PID_DATA *piddata)
{
    char c, msb, lsb;

    if (softuart_kbhit()) {
        c = softuart_getchar();
        switch (c) {
            case 'a':
                piddata->opmode = AUTO;
            break;

            case 'm':
                piddata->opmode = MANUAL;
            break;

            case 'o':
                piddata->opmode = STOP;
            break;

            case 's':
                c = softuart_getchar();
                switch (c) {
                    case 'v':
                        piddata->setpoint = softuart_getchar();
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
