#include <avr/io.h>
#include <math.h>

float Kp, Ki, Kd, y;
uint8_t w, x;
int16_t e, e_sum;
bit pid_manual;

void init()
{
    // read parameters etc. from eeprom here
    pid_manual = 1;

    init_wdt();
    init_pwm();
    init_adc();

    Kp = 0;
    Ki = 0;
    Kd = 0;

    w = 0;
    x = 0;
    y = 0;
    e = 0;
    e_sum = 0;

    PWM = 0;
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


void init_pwm()
{
	/* I/O initialization */
	IO_PORT = 0xFF;
	IO_DDR |=_BV(IO_PWM);

	// PWM for Timer 1, does FAST PWM, prescaler = 1
	TCCR1 =  _BV(CS10); //| _BV(CS11);
	GTCCR  = _BV(COM1B0) | _BV(PWM1B);
	OCR1C = 0xFF; // TOP

    PWM = 0;
}
