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
 * r             72           reset algorithm
 * 
 * e             65           save configuration to EEPROM
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
    return (a << 8) + b;
}

void put_word(uint16_t word)
{
    uint8_t msb = word >> 8;
    uint8_t lsb = word & 0x00FF;
	
    softuart_putchar(msb);
    softuart_putchar(lsb);
}

void command_loop(struct PID_DATA *piddata)
{
    char c;

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
			
			case 'r':
				pid_reset(piddata);
			break;
			
			case 'e':
				pid_save_parameters(piddata);
			break;

            case 's':
                c = softuart_getchar();
                switch (c) {
                    case 'v':
                        piddata->setpoint = softuart_getchar();
                    break;

                    case 'p':
						c = softuart_getchar();
						switch (c) {
							case 'p':
								piddata->P_factor = get_word();
							break;
							
							case 'i':
								piddata->I_factor = get_word();
							break;
							
							case 'd':
								piddata->D_factor = get_word();
							break;
						}
                    break;

                    case 'i':
						piddata->InitMode  = softuart_getchar();
						piddata->InitValue = softuart_getchar();
                    break;

                    case 'y':
						piddata->manual_output = softuart_getchar();
                        piddata->opmode = MANUAL;
                    break;
                }
            break;

            case 'g':
                c = softuart_getchar();
                switch (c) {
                    case 'v':
                        softuart_putchar(piddata->setpoint);
                    break;

                    case 'x':
                        softuart_putchar(piddata->processvalue);
                    break;

                    case 'y':
                        softuart_putchar(pid_get_output());
                    break;

                    case 'p':
                        c = softuart_getchar();
						switch (c) {
							case 'p':
								put_word(piddata->P_factor);
							break;
							
							case 'i':
								put_word(piddata->I_factor);
							break;
							
							case 'd':
								put_word(piddata->D_factor);
							break;
							
						}
                    break;

                    case 'm':
                        softuart_putchar(piddata->opmode);
                    break;

                    case 'i':
                        softuart_putchar(piddata->InitMode);
                        softuart_putchar(piddata->InitValue);
                    break;
                }
            break;
        }
    }
}
