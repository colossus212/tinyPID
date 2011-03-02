#include <avr/io.h>
#include <avr/interrupt.h>
#include <avr/eeprom.h>

float eeKp EEMEM = 0;
float eeKi EEMEM = 0;
float eeKd EEMEM = 0;
uint8_t eeInitial EEMEM = 0;
uint8_t eeOpMode EEMEM = 0;

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
    Kp = eeprom_read_float(&eeKp);
    Ki = eeprom_read_float(&eeKi);
    Kd = eeprom_read_float(&eeKd);
    w  = eeprom_read_byte(&eeInitial);

    opmode = eeprom_read_byte(&eeOpMode); 

    x = 0;
    y = 0;
    e = 0;
    e_sum = 0;

    cli();

	// I/O initialization
	IO_PORT = 0xFF;
	IO_DDR |=_BV(IO_PWM);

	// PWM for Timer 1, does FAST PWM, prescaler = 1
	TCCR1 =  _BV(CS10); //| _BV(CS11);
	GTCCR  = _BV(COM1B0) | _BV(PWM1B);
	OCR1C = 0xFF; // TOP

    PWM = 0;

    // enable watchdog timer, use interrupt instead of reset, every 0.016 seconds
	WDTCR = (1 << WDE) | (1 << WDIE);
    
    // enable ADC, VCC ref., set prescaler to 8
    ADCSRA = (1 << ADEN) | (1 << ADPS1) | (1 << ADPS0);
    // set ADC channel, left-justify result
    ADMUX = ADCHAN | (1 << ADLAR);

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
