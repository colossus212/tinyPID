// PWM output
#define IO_PWM PB4
#define IO_PIN PINB
#define IO_PORT PORTB
#define IO_DDR DDRB
#define PWM OCR1B

// PID Things
#define Ts 0.016
#define fs 1/Ts
#define ADCHAN ADC1

void init_wdt();
void init_pwm();
void init_adc();
void init();

uint8_t read_pv();

void contr();

void save_parameters();
