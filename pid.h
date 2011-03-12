#ifndef __PID_H__
#define __PID_H__

#include <avr/io.h>

#define PID_DEBUG

// Peripherals
#define IO_PWM PB4
#define IO_PIN PINB
#define IO_PORT PORTB
#define IO_DDR DDRB
#define PWM OCR1B
#define ADCHAN 1

// Controller constants
#define SAMPLING_TIME  16
#define SCALING_FACTOR 128 
#define MAX_ERROR_SUM  1000
#define MAX_OUTPUT     255
#define MIN_OUTPUT     0

// Operation modes 
#define AUTO   'a'
#define MANUAL 'm'

typedef struct {
    uint16_t P_factor;
    uint16_t I_factor;
    uint16_t D_factor;

    uint8_t setpoint;
    uint8_t opmode;
    uint8_t processvalue;
	
	uint8_t pvmin;
	uint8_t pvmax;
	uint8_t outmin;
	uint8_t outmax;
	
	uint8_t last_pv;
	int16_t esum;
} piddata_t;

#ifdef PID_DEBUG
typedef struct {
	int32_t pterm;
	int32_t iterm;
	int32_t dterm;
	int16_t e;
} piddebug_t;
#endif

void init_periph();
void init_pid();

void pid_run();
void pid_contr();

uint8_t pid_read_pv();
void pid_set_output(int32_t y);
uint8_t pid_get_output();

void pid_reset();
void pid_manual();
void pid_auto();

void pid_save_parameters();
void pid_load_parameters();

#endif