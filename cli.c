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
 * slXX   set limits (OUTmin, OUTmax)
 * ssXXML set scale (PVmin, PVmax, PVscale = SCALING_FACTOR * 255/(pvmax-pvmin))
 * 
 * gp     get parameter P_factor, returns MSB, LSB
 * gi     get parameter I_factor, returns MSB, LSB
 * gd     get parameter D_factor, returns MSB, LSB
 * gm     get operation mode, returns 'a' or 'm'
 * gv     get setpoint
 * gx     get process value
 * gy     get output value
 * gc     get calculation constants SAMPLING_TIME (in ms) and SCALING_FACTOR
 * gl     get limits (output min/max)
 * gs     get scale (pv min/max,scale)
 * 
 */


#include <avr/pgmspace.h>
#include <avr/interrupt.h>
#include "cli.h"
#include "softuart.h"
#include "pid.h"

extern piddata_t piddata;

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

uint16_t get_word()
{
	char lsb, msb;
	
	msb = softuart_getchar();
	lsb = softuart_getchar();
	
	return (uint16_t) ((msb<<8) + lsb);
}

void init_cli()
{
    softuart_init();
    sei();
}

void command_loop()
{
	char c;
	
	if (softuart_kbhit())
		c = softuart_getchar();
	else
		return;
	
	if (testchar('a', c))
		pid_auto();
	
	else if (testchar('m', c))
		pid_manual();
	
	else if (testchar('e', c))
		pid_save_parameters();
	
	else if (testchar('s', c)) {
		c = softuart_getchar();
		
		if (testchar('v', c))
			piddata.setpoint = softuart_getchar();
		
		else if (testchar('y', c)) {
			pid_manual();
			pid_set_output(softuart_getchar());
		}
		
		else if (testchar('p', c)) 
			piddata.P_factor = get_word();
		
		else if (testchar('i', c)) 
			piddata.I_factor = get_word();
		
		else if (testchar('d', c))
			piddata.D_factor = get_word();
		
		else if (testchar('l', c)) {
			piddata.outmin = softuart_getchar();
			piddata.outmax = softuart_getchar();
		}
		
		else if (testchar('s', c)) {
			piddata.pvmin   = softuart_getchar();
			piddata.pvmax   = softuart_getchar();
			piddata.pvscale = get_word();
		}
		
	}
	
	else if (testchar('g', c)) {
		c = softuart_getchar();
		
		if (testchar('v', c))
			softuart_putchar(piddata.setpoint);
		
		else if (testchar('y', c))
			softuart_putchar(pid_get_output());
		
		else if (testchar('x', c))
			softuart_putchar(piddata.processvalue);
		
		else if (testchar('m', c))
			softuart_putchar(piddata.opmode);
		
		else if (testchar('s', c)) {
			softuart_putchar(piddata.pvmin);
			softuart_putchar(piddata.pvmax);
			put_word(piddata.pvscale);
		}
		
		else if (testchar('l', c)) {
			softuart_putchar(piddata.outmin);
			softuart_putchar(piddata.outmax);
		}
		
		else if (testchar('p', c))
			put_word(piddata.P_factor);
		
		else if (testchar('i', c))
			put_word(piddata.I_factor);
		
		else if (testchar('d', c))
			put_word(piddata.D_factor);
		
		else if (testchar('c', c)) {
			softuart_putchar(SAMPLING_TIME);
			softuart_putchar(SCALING_FACTOR);
		}
	}
}
