#include <avr/io.h>
#include <avr/interrupt.h>
#include <avr/eeprom.h>
#include "pid.h"

uint8_t eeKp EEMEM = 0;
uint8_t eeKi EEMEM = 0;
uint8_t eeKd EEMEM = 0;
uint8_t eeAttn EEMEM = 1;
uint8_t eeInitValue EEMEM = 0;
uint8_t eeInitMode EEMEM = STOP;

uint8_t Kp, KpAttn, Ki, Kd;
uint8_t y;
uint8_t w, x;
uint8_t opmode;


ISR(WDT_vect)
{
	// keep WDT from resetting, interrupt instead
	WDTCR |= (1 << WDIE);
    if (opmode != STOP)
        contr();
}


void init_pid()
{
    uint8_t initv = eeprom_read_byte(&eeInitValue);

    Kp = eeprom_read_byte(&eeKp);
    Ki = eeprom_read_byte(&eeKi);
    Kd = eeprom_read_byte(&eeKd);
    KpAttn = eeprom_read_byte(&eeAttn);

    w = 0;
    x = 0;
    y = 0;
    
    cli();

    // I/O setup
    IO_PORT = 0xFF;
    IO_DDR |=_BV(IO_PWM);

    // PWM setup
    // Timer1, does FAST PWM, prescaler = 1
    TCCR1 =  _BV(CS10); //| _BV(CS11);
    GTCCR  = _BV(COM1B0) | _BV(PWM1B);
    OCR1C = 0xFF; // TOP
    PWM = 0;

    // WDT setup
    // enable watchdog timer, use interrupt instead of reset, every 0.016 seconds
    WDTCR = (1 << WDE) | (1 << WDIE);
    
    // ADC setup
    // enable ADC, VCC ref., set prescaler to 8
    ADCSRA = (1 << ADEN) | (1 << ADPS1) | (1 << ADPS0);
    // set ADC channel, left-justify result
    ADMUX = ADCHAN | (1 << ADLAR);

    // Operation mode setup and initial values
    opmode = eeprom_read_byte(&eeInitMode); 
    if (opmode == AUTO)
        w = initv;
    else if (opmode == MANUAL)
        PWM = initv;
    else { // if sth. went wrong with the mode
        opmode = STOP;
        PWM = 0;
    }

    // enable interrupts
    sei();
}

void contr()
{
    static int16_t e = 0;
    static int16_t e_sum = 0;
    static int16_t e_last = 0;
    float u = 0;

    x = read_pv();

    if (opmode == AUTO)
    {
        e_last = e;
        e = w - x;
        e_sum += e;
        if (e_sum >  3000) e_sum =  3000; // magic!
        if (e_sum < -3000) e_sum = -3000; // magic!

        u  = Kp * 1./KpAttn * e;
        u += Ki * Ts * e_sum;
        u += Kd * fs * (e - e_last);

        if (u > 255) y = 255;
        else if (u < 0) y = 0;
        else
            y = (uint8_t) u;
    }
    else 
    {
        e = e_last = e_sum = 0;
    }


    PWM = y;
}

uint8_t read_pv()
{
    uint8_t a = 0, i = 0;

    ADMUX = ADCHAN | (1 << ADLAR);
	
	// read ADC, take 4 samples
	for (i=0; i < 4; i++) {
		ADCSRA |= (1 << ADSC);         // start conversion
		while (ADCSRA & (1 << ADSC));  // wait till end of conversion

		a = ADCL;      // must be read first
        a = ADCH;      // overwrite with 8 MSB
	}

    return a/4;
}
