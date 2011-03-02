#include <avr/io.h>
#include <avr/interrupt.h>
#include <avr/eeprom.h>

float eeKp EEMEM = 0;
float eeKi EEMEM = 0;
float eeKd EEMEM = 0;
uint8_t eeInitValue EEMEM = 0;
uint8_t eeInitMode EEMEM = MANUAL;

float Kp, Ki, Kd, y;
uint8_t w, x;
int16_t e, e_sum;
uint8_t opmode;


ISR(WDT_vect)
{
	// keep WDT from resetting, interrupt instead
	WDTCR |= (1 << WDIE);
    if (opmode == AUTO)
        contr();
}


void init()
{
    uint8_t initv = eeprom_read_byte(&eeInitValue);

    Kp = eeprom_read_float(&eeKp);
    Ki = eeprom_read_float(&eeKi);
    Kd = eeprom_read_float(&eeKd);

    w = 0;
    x = 0;
    y = 0;
    e = 0;
    e_sum = 0;
    
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
        opmode = MANUAL;
        PWM = initv;
    }

    // enable interrupts
    sei();
}

void contr()
{
    int16_t e_last = e;

    x = read_pv();
    e = w - x;

    e_sum += e;
    if (e_sum >  3000) e_sum =  3000; // magic!
    if (e_sum < -3000) e_sum = -3000; // magic!

    y  = Kp * e;
    y += Ki * Ts * e_sum;
    y += Kd * fs * (e - e_last);

    if (y > 255) y = 255;
    if (y < 0) y = 0;

    PWM = (uint8_t) y;
}

uint8_t read_pv()
{
    uint8_t a = 0;
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
