/*
 * CLI.h
 * Definitions for commandline interface of tinyPID.
 * 
 * http://github.com/modul/tinyPID
 * 
 * Command description:
 * The format is kind of raw, numbers don't get converted to ASCII. Arguments
 * are either 8 bit or 16 bit unsigned integers.
 * The commands itself can be intrepreted as ASCII characters. No line-ending 
 * is needed. A command is executed when all of its arguments have been read.
 *
 * (X is a byte, H is higher byte, L - lower byte)
 * ASCII  DESCRIPTION
 * a      set mode to automatic
 * m      set mode to manual
 * e      save configuration to EEPROM
 * 
 * svX    set the setpoint to X
 * syX    set output value to X, this toggles manual mode
 * spHL   set the parameter P_factor
 * siHL   set I_factor
 * sdHL   set D_factor
 * slXX   set limits (OUTmin, OUTmax)
 * ssXXHL set scale (PVmin, PVmax, PVscale = SCALING_FACTOR * 255/(pvmax-pvmin))
 * 
 * gp     get parameter P_factor, returns MSB, LSB
 * gi     get parameter I_factor, returns MSB, LSB
 * gd     get parameter D_factor, returns MSB, LSB
 * gm     get operation mode, returns 'a' or 'm'
 * gv     get setpoint
 * gx     get process value
 * gy     get output value
 * gc     get calculation constants SAMPLING_TIME (in ms) and SCALING_FACTOR
 * gl     get limits (output min/max)
 * gs     get scale (pv min/max,scale)
 * 
 */

#include <avr/pgmspace.h>
#include <avr/interrupt.h>
#include "softuart.h"
#include "pid.h"

void init_cli();

void command_loop();
