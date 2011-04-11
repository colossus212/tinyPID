/*
 * PID.h
 * Definitions for PID controller algorithm of tinyPID and for running the controller.
 * PID.c/PID.h may be useful in other projects too. The hardware part must probably
 * be changed.
 * 
 * http://github.com/modul/tinyPID
 * 
 */

#include <avr/io.h>
#include <avr/interrupt.h>
#include <avr/eeprom.h>

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
	
	uint8_t  outmin;
	uint8_t  outmax;
	uint8_t  pvmin;
	uint8_t  pvmax;
	uint16_t pvscale;
	
	uint8_t last_pv;
	int16_t esum;
} piddata_t;

// Initialize and setup hardware
void init_periph();

// Initialize PID controller, load parameters
void init_pid();

// Run controller (to be called in a forever loop)
void pid_run();

// Calculate output according to controller equation
void pid_contr();

// Read process value (ADC)
uint8_t pid_read_pv();

// Scale PV according to settings (min, max)
uint8_t pid_scale_pv(uint8_t adc);

// Return current output value
uint8_t pid_get_output();

// Set output, limit if neccassary
void pid_set_output(int32_t y);

// Reset algorithm data
void pid_reset();

// Set manual mode (user sets output)
void pid_manual();

// Set automatic mode (controlling, output is calculated)
void pid_auto();

// Save PID parameters to EEPROM
void pid_save_parameters();

// Load PID parametesr to EEPROM
void pid_load_parameters();
