#include <stdio.h>
#include <avr/pgmspace.h>
#include "softuart.h"

static FILE mystdout = FDEV_SETUP_STREAM(softuart_putchar, NULL, _FDEV_SETUP_WRITE);
static FILE mystdin  = FDEV_SETUP_STREAM(NULL, softuart_getchar, _FDEV_SETUP_READ);

stdout = &mystdout;
stdin  = &mystdin;

void command(char c)
{
    switch(c)
    {
      case 's':
        // 'set' command
      break;
      case 'v':
        // 'view' command
      break;
      case 'a':
        // 'auto' command
      break;
    }
}

