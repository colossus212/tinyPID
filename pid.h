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

enum modes {AUTO, MANUAL, STOP};

void init_pid();

uint8_t read_pv();

void contr();

void save_parameters();
