#include <avr/io.h>

// Peripherals
#define IO_PWM PB4
#define IO_PIN PINB
#define IO_PORT PORTB
#define IO_DDR DDRB
#define PWM OCR1B
#define ADCHAN 1

// Controller Constants
#define SAMPLING_TIME  16
#define SCALING_FACTOR 128 
#define MAX_ERROR_SUM  500
#define MAX_ERROR      255 
#define MAX_OUTPUT     255
#define MIN_OUTPUT     0

enum modes {AUTO='a', MANUAL='m', STOP='o'};

struct PID_DATA {
    uint16_t P_factor;
    uint16_t I_factor;
    uint16_t D_factor;
    uint8_t InitMode;
    uint8_t InitValue;

    uint8_t manual_output;
    uint8_t setpoint;
    uint8_t opmode;
    uint8_t processvalue;
    uint8_t last_pv;
    int16_t esum;
};

struct PID_FLAGS {
    uint8_t timer :1;
    uint8_t dummy :7;
};

void init_periph();
struct PID_DATA* init_pid();

void pid_reset(struct PID_DATA *piddata);
void pid_run(struct PID_DATA *piddata);
int32_t pid_contr(struct PID_DATA *piddata);

uint8_t pid_read_pv();
void pid_set_output(int32_t y);
uint8_t pid_get_output();

void pid_save_parameters(struct PID_DATA *piddata);
void pid_load_parameters(struct PID_DATA *piddata);
