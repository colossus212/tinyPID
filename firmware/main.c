/*
 * tinyPID
 *
 * Implementing a discrete PID Controller on an ATtiny AVR.
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

#include <avr/io.h>
#include "pid.h"
#include "cli.h"

int main()
{
    init_periph();
	init_cli();
	init_pid();
	
    while (1) {
		command_loop();
		pid_run();        
    }
    
    return 0;
}
