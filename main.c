/*
   tinyPID

   Implementing a discrete PID Controller on an ATtiny AVR.

   author: Remo Giermann (mo@liberejo.de)
   created: 2010/03/01


   The microcontroller uses the equation

   y = Kp * e + Ki * Ts * e_sum + Kd/Ts * (e - e_last)

   with y being the output value
   the actual output is done via PWM and ranges from 0 to 255

   Kp, Ki and Kd being the control parameters set by the user
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
#include <math.h>
#include "softuart.h"

#define Ts 0.016
#define fs 1/Ts
#define PWM OCR1B
#define ADCHAN ADC1

float Kp = 0;
float Ki = 0;
float Kd = 0;
uint8_t w = 0;

float y = 0;
uint8_t x = 0;
float e = 0;
float e_sum = 0;

void init_wdt();
void init_adc();
void init_pwm();

void output();
uint8_t read_pv();

void contr()
{
    float e_last = e;

    x = read_pv();
    e = w - x;
    e_sum += e;

    y  = Kp * e;
    y += Ki * Ts * e_sum;
    y += Kd * fs * (e - e_last);
}
