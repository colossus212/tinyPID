/*
 * CLI.c
 *
 * Command-line interface (sort of) for tinyPID.
 * 
 * ----------------------------------------------------------------------------
 * "THE BEER-WARE LICENSE" (Revision 42):
 * <mo@liberejo.de> wrote this file. As long as you retain this notice you
 * can do whatever you want with this stuff. If we meet some day, and you think
 * this stuff is worth it, you can buy me a beer in return - Remo Giermann.
 * ----------------------------------------------------------------------------
 * 
 * author:   Remo Giermann (mo@liberejo.de)
 * created:  2010/03/01
 * homepage: http://github.com/modul/tinyPID
 *
 */

#include "cli.h"

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

/* Send an unsigned 16bit int as two bytes. */
void put_word(uint16_t word)
{
	softuart_putchar((uint8_t) (word >> 8));
	softuart_putchar((uint8_t) (word & 0xFF));
}

/* Receive two bytes and put them together to a 16bit value. */
uint16_t get_word()
{
	char lsb, msb;
	
	msb = softuart_getchar();
	lsb = softuart_getchar();
	
	return (uint16_t) ((msb<<8) + lsb);
}

/* Initialize command-line interface. */
void init_cli()
{
    softuart_init();
    sei();
}

/* Receive commands and perform corresponding actions. */
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
