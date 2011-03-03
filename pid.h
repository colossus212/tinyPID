#include <avr/io.h>

// PWM output
#define IO_PWM PB4
#define IO_PIN PINB
#define IO_PORT PORTB
#define IO_DDR DDRB
#define PWM OCR1B

// PID Things
#define Ts 0.016
#define fs 1/Ts
#define ADCHAN 1

#define KpAttn 0.1

enum modes {AUTO='a', MANUAL='m', STOP='o'};

void init_pid();

uint8_t read_pv();
void contr();

void pid_save_parameters();
