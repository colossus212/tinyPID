/*
 
   tinyPID

   Implementing a discrete PID Controller on an ATtiny AVR.

   author: Remo Giermann (mo@liberejo.de)
   created: 2010/03/01


   The microcontroller uses the equation

   y = Kp * e + Ki * Ts * e_sum + Kd/Ts * (e - e_last)
   
   (y - output value,
    Kp - proportional factor
    Ki - integral factor
	Kd - derivative factor
	e  - error = setpoint - process value
	e_sum - sum of all last errors
	e_last - last error
	Ts - sampling time)
   
   to make things more robust, simpler and to avoid floating point arithmetic,
   the actual algorithm uses:
   
   u = P_factor * e + I_factor * e_sum + D_factor * (x - x_last)
   y = u / SCALING_FACTOR
   
   (P_factor - Kp*SCALING_FACTOR
    I_factor - Ki*Ts*SCALING_FACTOR
    D_factor - Kd/Ts * SCALING_FACTOR
    x - process value)
    
    It's possible to limit the input (process value) and output value.
   

*/

#include <avr/io.h>
#include "pid.h"
#include "cli.h"

int main()
{
	char c;
    init_periph();
	init_cli();
	init_pid();
	
    while (1) {
		command_loop();
		pid_run();        
    }
    
    return 0;
}
