tinyPID
=======

*tinyPID* is an implementation of a discrete PID controller on AVR ATtiny45
microcontrollers. It can be used for most closed loop controlling applications.
For real life applications the only additional thing probably needed is a 
circuit to adapt tinyPID’s electrical input and output to the process.

It is fully functional and configurable, comes with some nice features, a Python
frontend module and a Qt GUI. With each of the frontends you can configure the 
controller’s parameters, view process variables such as output, process value, 
setpoint and error, configure a scale conversion, set the setpoint or limit the 
output, set the output manually etc.

![tinyPID scheme][1]

At minimum the hardware consists of one ATtiny45, a power supply, a pull-down resistor
for the ADC input and some wires to connect it to the process. 
Communication can be done with an external UART to USB/Serial adapter.

The source and description of tinyPID lives at http://github.com/modul/tinyPID.

License
----------------------------------------------------------------------------
"THE BEER-WARE LICENSE" (Revision 42):

<mo@liberejo.de> wrote this file. As long as you retain this notice you
can do whatever you want with this stuff. If we meet some day, and you think
this stuff is worth it, you can buy me a beer in return - Remo Giermann.


[1]: https://github.com/modul/tinyPID/raw/master/doc/schema.png

