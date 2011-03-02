/*
   tinyPID

   Implementing a discrete PID Controller on an ATtiny AVR.

   author: Remo Giermann (mo@liberejo.de)
   created: 2010/03/01


   The microcontroller uses the equation

   y = Kp * 1/KpAttn e + Ki * Ts * e_sum + Kd/Ts * (e - e_last)

   with y being the output value
   the actual output is done via PWM and ranges from 0 to 255

   Kp, Ki and Kd being the control parameters set by the user
   KpAttn is an attenuation factor to allow overall amplification
   lower than 1
   
   Ts being the sampling time, hardcoded in the program, 16ms

   e being the error, e = w - x
   e_sum - accumulated error
   e_last - error of last sample

   w being the set value, given by the user
   x being the process value, read via built-in ADC in 8bit mode
   ranging from 0 to 255.


   User interaction is done via software UART.


   Short info on parameters:
   
   Kp is the proportional factor
   Ki is the integrating factor
   Kd is the differential factor
   
   Ki = Kp/Tn
   Kd = Kp/Td

*/

#include <avr/io.h>
#include "pid.h"
#include "cli.h"

void main()
{
    init_cli();
    init_pid();
}
