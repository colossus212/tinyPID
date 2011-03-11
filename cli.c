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
#include <util/delay.h>
#include "cli.h"
#include "softuart.h"
#include "pid.h"

extern piddata_t piddata;
extern pidcalc_t pidcalc;

enum states {
	init, 
	g, gp, 
	s, sp, 
	sy, sv,  
	si, sim,
	spp, sppM, 
	spi, spiM, 
	spd, spdM,
};

#define state_reset() (state = init)

/* This is a very dirty workaround to a communication error with softuart.
 * Sometimes, bytes are received in a strange way, adding one most-significant
 * bit to the character. 
 * This function tries to restore the byte to an expected character.
 */
uint8_t testchar(char expected, char received)
{
	return (expected == received || expected == (received - 128));
}

void put_word(uint16_t word)
{
	softuart_putchar((uint8_t) (word >> 8));
	softuart_putchar((uint8_t) (word & 0xFF));
}

void init_cli()
{
    softuart_init();
    sei();
}

void command_loop(char c)
{
	static char msb = 0;
	static uint8_t state = init;
	
	switch (state) {
		case init:
			if (testchar('s', c))
				state = s;
			else if (testchar('g', c))
				state = g;
			else if (testchar('a', c))
				pid_auto();
			else if (testchar('m', c))
				pid_manual();
			else if (testchar('r', c))
				pid_reset();
			else if (testchar('e', c))
				pid_save_parameters();
		break;
		
		case s:
			if (testchar('v', c)) 
				state = sv;
			else if (testchar('y', c))
				state = sy;
			else if (testchar('p', c))
				state = sp;
			else if (testchar('i', c))
				state = si;
			else
				state_reset();
		break;
		
		case sp:
			if (testchar('p', c))
				state = spp;
			else if (testchar('i', c))
				state = spi;
			else if (testchar('d', c))
				state = spd;
			else
				state_reset();
		break;
		
		case spp:
			msb = c;
			state = sppM;
		break;
		
		case spi:
			msb = c;
			state = spiM;
		break;
		
		case spd:
			msb = c;
			state = spdM;
		break;
		
		case sppM:
			state_reset();
			piddata.P_factor = (msb << 8) + c;
		break;
		
		case spiM:
			state_reset();
			piddata.I_factor = (msb << 8) + c;
		break;
		
		case spdM:
			state_reset();
			piddata.D_factor = (msb << 8) + c;
		break;
		
		case sy:
			state_reset();
			pid_set_output(c);
			piddata.opmode = MANUAL;
		break;
		
		case sv:
			state_reset();
			piddata.setpoint = c;
		break;
		
		case si:
			if (testchar('a', c) || testchar('m', c) || testchar('o', c)) {
				state = sim;
				msb = c;
			}
			else 
				state_reset();
		break;
		
		case sim:
			state_reset();
		break;
		
		case g:
			if (testchar('p', c))
				state = gp;
			else {
				state_reset();

				if (testchar('v', c)) 
					softuart_putchar(piddata.setpoint);
				else if (testchar('x', c))
					softuart_putchar(piddata.processvalue);
				else if (testchar('y', c)) 
					softuart_putchar(pid_get_output());
				else if (testchar('m', c))
					softuart_putchar(piddata.opmode);
				
				// Debug information
				else if (testchar('d', c)) {
				
					if (pidcalc.esum < 0) {
						softuart_putchar(1);
						put_word(-pidcalc.esum);
					}
					else {
						softuart_putchar(0);
						put_word(pidcalc.esum);
					}
					
					if (pidcalc.pterm < 0) {
						softuart_putchar(1);
						put_word((uint16_t) (-pidcalc.pterm >> 16));
						put_word((uint16_t) (-pidcalc.pterm & 0xFFFF));
					}
					else {
						softuart_putchar(0);
						put_word((uint16_t) (pidcalc.pterm >> 16));
						put_word((uint16_t) (pidcalc.pterm & 0xFFFF));
					}
					if (pidcalc.iterm < 0) {
						softuart_putchar(1);
						put_word((uint16_t) (-pidcalc.iterm >> 16));
						put_word((uint16_t) (-pidcalc.iterm & 0xFFFF));
					}
					else {
						softuart_putchar(0);
						put_word((uint16_t) (pidcalc.iterm >> 16));
						put_word((uint16_t) (pidcalc.iterm & 0xFFFF));
					}
					if (pidcalc.dterm < 0) {
						softuart_putchar(1);
						put_word((uint16_t) (-pidcalc.dterm >> 16));
						put_word((uint16_t) (-pidcalc.dterm & 0xFFFF));
					}
					else {
						softuart_putchar(0);
						put_word((uint16_t) (pidcalc.dterm >> 16));
						put_word((uint16_t) (pidcalc.dterm & 0xFFFF));
					}
					
				}
			}
		break;
		
		case gp:
			state_reset();
			
			if (testchar('p', c)) 
				put_word(piddata.P_factor);
			else if (testchar('i', c))
				put_word(piddata.I_factor);
			else if (testchar('d', c))
				put_word(piddata.D_factor);
		break;
		
		default: 
			state = init;
    }    
}
