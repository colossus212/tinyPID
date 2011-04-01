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

void init_periph();
void init_pid();

void pid_run();
void pid_contr();

uint8_t pid_read_pv();
uint8_t pid_get_output();
uint8_t scale_pv(uint8_t adc);
void pid_set_output(int32_t y);

void pid_reset();
void pid_manual();
void pid_auto();

void pid_save_parameters();
void pid_load_parameters();
