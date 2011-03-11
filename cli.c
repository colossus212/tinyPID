/*
 * CLI.c
 *
 * Command-line interface (sort of) for tinyPID.
 *
 * The format is kind of raw, numbers don't get converted to ASCII.
 * Arguments to commands have a range of 0…255 and are sent as raw bytes.
 * The commands itself can be intrepreted as ASCII characters. No line-ending 
 * is needed. A command is executed when all of its arguments have been read.
 *
 * In the following table, X is any byte, M is most-significant, L - least significant byte
 *
 * ASCII  DESCRIPTION
 * a      set mode to automatic
 * m      set mode to manual
 * 
 * e      save configuration to EEPROM
 * 
 * 
 * svX    set the setpoint to X
 * syX    set output value to X, this toggles manual mode
 * spML   set the parameter P_factor
 * siML   set I_factor
 * sdML   set D_factor
 * srXXXX set ranges (PVmin, PVmax, OUTmin, OUTmax)
 * 
 * gp     get parameter P_factor, returns MSB, LSB
 * gi     get parameter I_factor, returns MSB, LSB
 * gd     get parameter D_factor, returns MSB, LSB
 * gm     get operation mode, returns 'a', 'm' or 'o'
 * gv     get setpoint
 * gx     get process value
 * gy     get output value
 * gc     get calculation constants SAMPLING_TIME (in ms) and SCALING_FACTOR
 * gr     get ranges (process value min/max, output min/max)
 * 
 */


#include <avr/pgmspace.h>
#include <avr/interrupt.h>
#include "cli.h"
#include "softuart.h"
#include "pid.h"

extern piddata_t piddata;
#ifdef PID_DEBUG
extern piddebug_t piddebug;
#endif

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
					
#ifndef PID_DEBUG
					softuart_puts_P("No debug.");
#else
				
					if (piddata.esum < 0) {
						softuart_putchar(1);
						put_word(-piddata.esum);
					}
					else {
						softuart_putchar(0);
						put_word(piddata.esum);
					}
					
					if (piddebug.pterm < 0) {
						softuart_putchar(1);
						put_word((uint16_t) (-piddebug.pterm >> 16));
						put_word((uint16_t) (-piddebug.pterm & 0xFFFF));
					}
					else {
						softuart_putchar(0);
						put_word((uint16_t) (piddebug.pterm >> 16));
						put_word((uint16_t) (piddebug.pterm & 0xFFFF));
					}
					if (piddebug.iterm < 0) {
						softuart_putchar(1);
						put_word((uint16_t) (-piddebug.iterm >> 16));
						put_word((uint16_t) (-piddebug.iterm & 0xFFFF));
					}
					else {
						softuart_putchar(0);
						put_word((uint16_t) (piddebug.iterm >> 16));
						put_word((uint16_t) (piddebug.iterm & 0xFFFF));
					}
					if (piddebug.dterm < 0) {
						softuart_putchar(1);
						put_word((uint16_t) (-piddebug.dterm >> 16));
						put_word((uint16_t) (-piddebug.dterm & 0xFFFF));
					}
					else {
						softuart_putchar(0);
						put_word((uint16_t) (piddebug.dterm >> 16));
						put_word((uint16_t) (piddebug.dterm & 0xFFFF));
					}
#endif
					
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
