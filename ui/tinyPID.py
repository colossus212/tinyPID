#!/usr/bin/env python
# -*- coding: utf8 -*-
#
# Frontend to tinyPID.
#
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <mo@liberejo.de> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return - Remo Giermann.
# ----------------------------------------------------------------------------
# 
# author:   Remo Giermann (mo@liberejo.de)
# created:  2011/03/03
# homepage: http://github.com/modul/tinyPID
#

import serial
from time import sleep
from struct import pack, unpack


FULLSCALE = 255
SAMPLING_TIME  = 16e-3 # both can be updated
SCALING_FACTOR = 128   # by calling tinyPID.get_constants()


# Utilities

uint16_t = '!H' # format strings understood by struct.pack/struct.unpack
uint8_t  = '!B'

def format(s, fmt):
	"""
	If 's' is a string, it’s assumed to be in 'fmt' 
	and converted to an integer.
	If 's' is an integer, it’s converted to a string
	representing 'fmt'.

	fmt may be uint8_t, uint16_t (see above definitions)
	or any string understood by struct.pack/struct.unpack.
	"""

	if type(s) is str:
		return unpack(fmt, s)[0]
	elif type(s) is int:
		return pack(fmt, s)
	else:
		return None

uint8  = lambda s: format(s, uint8_t)
uint16 = lambda s: format(s, uint16_t)


# PID parameter conversions

def Ki_to_Tn(kp, ki):
    if ki > 0:
        return float(kp)/ki
    else:
        return 0

def Kd_to_Tv(kp, kd):
    if kp > 0:
        return float(kd)/kp
    else:
        return 0

def Tn_to_Ki(kp, tn):
    if tn > 0:
        return kp/tn
    else:
        raise ValueError

def Tv_to_Kd(kp, tv):
    return kp * tv


# Controller factor scaling

def pfactor_scale(kp):
	f = SCALING_FACTOR * kp 
	return int(round(f))

def pfactor_unscale(f):
	return f/float(SCALING_FACTOR)

def ifactor_scale(ki):
	f = ki * SCALING_FACTOR * SAMPLING_TIME 
	return int(round(f))

def ifactor_unscale(f):
	return f/(SCALING_FACTOR * SAMPLING_TIME)

def dfactor_scale(kd):
	f = kd * SCALING_FACTOR/SAMPLING_TIME 
	return int(round(f))

def dfactor_unscale(f):
	return f * SAMPLING_TIME/SCALING_FACTOR


# Frontend class

class tinyPID (object):
	"""
	Frontend to tinyPID.
	
	Methods:
	--------
	auto():          set controller to automatic mode
	manual():        set controller to manual mode
	save():          save parameters to device's EEPROM
	
	get_mode():      return the operation mode of the controller
	get_constants(): get calculation constants scaling factor and sampling time
	                  used on the controller
	get_scale():     return the process value scaling limits pvmin, pvmax
	get_limits():    return the output limits
	
	get_Kd():        return the differential factor of the PID controller
	get_Ki():        return the integral factor 
	get_Kp():        return the proportional factor
	
	get_output():    return the current output reading
	get_pv():        return the current process value reading
	get_setpoint():  return the setpoint
	
	set_Kp(k):       set PID proportional factor 
	set_Ki(k):       set PID integral factor 
	set_Kd(k):       set PID differential factor 
	
	set_limits(min, max):
	                 set output limits to 'min' and 'max'
	set_scale(min, max):
	                 set process value scale limits to 'min', 'max'.
					  The controller rescales the PV to fullscale 0…255.
						  
	set_output(y):   set output value to 'y' (this toggles manual mode internally)
	set_setpoint(w): set the setpoint to 'w'
	
	info():          print out most of the PID data
	log(interval):   continuously get and print setpoint, 
					  process value, output and error
	flush():         flush the serial input buffer
	
	display_configuration(vmin, vmax, vunit, omin, omax, ounit):
				     Convert all values to a different scale and optionally append a string (vunit, ounit)
	reset_display(): Reset display scale to 0…255
	
	percentage():    Display all values in percent, or reset to 0…255
	
	
	Attributes:
	-----------
	Kp, Ki, Kd: get/set PID factors
	Tv, Tn:     get/set PID time constants (same effect as Kd, Ki)
	
	w, x, y, e: get/set setpoint, process value, output, error
	SP, PV:     get/set setpoint, process value
	opmode:     get/set operation mode ('a', or 'm')
	
	xmin, xmax, pvmin, pvmax:
	            get/set process value scale limits
	ymin, ymax, outmin, outmax:
	            get/set output limits

	"""


	def __init__(self, *args, **kwargs):
		"""
		Arguments are directly passed to serial.Serial(). Should need at least 'port' and 'baudrate'.
		"""
		self.com = serial.Serial(*args, **kwargs)
		if not self.com.getTimeout():
			self.com.setTimeout(2)
			
		self.__valmin = 0
		self.__valmax = FULLSCALE
		self.__valunit = ''
		
		self.__outmin = 0
		self.__outmax = FULLSCALE
		self.__outunit = ''
	
	def __del__(self):
		del self.com

	def __readc(self, count=1):
		""" Read and return character(s). """
		s = self.com.read(count)
		if len(s) < count:
			return None
		else:
			return s	
	
	def __readb(self, count=1):
		""" Read byte(s) and return integer(s). """
		s = self.__readc(count)
		if s is not None:
			b = map(uint8, s)
			if len(b) == 1:
				return b[0]
			else:
				return b
		else:
			return None

	def __readw(self, count=1):
		""" Read byte pair(s) MSB, LSB and return integer(s). """
		r = []
		for i in range(0, count):
			b = self.__readc(2)
			if b is not None and len(b) == 2:
				r.append(uint16(b))
		
		if len(r) == 1:
			return r[0]
		elif len(r) == 0:
			return None
		else:
			return r

	def __write(self, *args):
		""" Write characters/bytes. """
		for s in args:
			if not type(s) in (str, int):
				raise TypeError			
			if type(s) is int:
				s = chr(s)
			self.com.write(s)
	
	def __display_value(self, *args):
		""" 
		Convert each arg to the configured display scale. 
		See display_configuration() for more.
		"""
		r = []
		factor = float(self.__valmax-self.__valmin)/FULLSCALE
				
		for a in args:
			if a == FULLSCALE:
				r.append(self.__valmax)
			elif a == 0:
				r.append(self.__valmin)
			else:
				r.append(a * factor + self.__valmin)
		
		if len(r) == 1:
			return r[0]
		else:
			return r
	
	def __display_output(self, *args):
		""" 
		Convert each arg to the configured output scale. 
		See display_configuration() for more.
		"""
		r = []
		factor = float(self.__outmax-self.__outmin)/FULLSCALE
				
		for a in args:
			if a == FULLSCALE:
				r.append(self.__outmax)
			elif a == 0:
				r.append(self.__outmin)
			else:
				r.append(a * factor + self.__outmin)
		
		if len(r) == 1:
			return r[0]
		else:
			return r
	
	def __device_value(self, *args):
		"""
		Convert each arg back to the fullscale used on the device.
		See display_configuration() for more.
		"""
		r = []
		factor = FULLSCALE/float(self.__valmax-self.__valmin)
				
		for a in args:
			if a >= self.__valmax:
				r.append(FULLSCALE)
			elif a <= self.__valmin:
				r.append(0)
			else:
				a = round((a - self.__valmin) * factor)
				r.append(int(a))
		
		if len(r) == 1:
			return r[0]
		else:
			return r
		
	def __device_output(self, *args):
		"""
		Convert each arg back to the fullscale used on the device.
		See display_configuration() for more.
		"""
		r = []
		factor = FULLSCALE/float(self.__outmax-self.__outmin)
				
		for a in args:
			if a >= self.__outmax:
				r.append(FULLSCALE)
			elif a <= self.__outmin:
				r.append(0)
			else:
				a = round((a - self.__outmin) * factor)
				r.append(int(a))
		
		if len(r) == 1:
			return r[0]
		else:
			return r
		
	def get_mode(self):
		""" Get operation mode. """
		self.__write("gm")
		return self.__readc()

	def get_Kp(self):
		""" Get proportional factor. """
		self.__write("gp")
		return pfactor_unscale(self.__readw())

	def get_Ki(self):
		""" Get integral factor. """
		self.__write("gi")
		return ifactor_unscale(self.__readw())

	def get_Kd(self):
		""" Get derivative factor. """
		self.__write("gd")
		return dfactor_unscale(self.__readw())

	def get_pv(self):
		""" Get process value 'x'. """
		self.__write("gx")
		x = self.__readb()
		return self.__display_value(x)

	def get_setpoint(self):
		""" Get setpoint 'w'. """
		self.__write("gv")
		w = self.__readb()
		return self.__display_value(w)

	def get_output(self):
		""" Get output value 'y'. """
		self.__write("gy")
		y = self.__readb()
		return self.__display_output(y)

	def get_limits(self):
		""" Get output limits. """
		self.__write("gl")
		limits = self.__readb(2)
		return self.__display_output(*limits)

	def get_scale(self):
		""" Get PV scale. """
		self.__write("gs")
		xmin, xmax = self.__readb(2)
		xscale = self.__readw()
		return self.__display_value(xmin, xmax)

	def get_constants(self):
		""" Get calculation constants sampling time and scaling factor. """
		self.__write("gc")
		return self.__readb(2)

	def set_Kp(self, Kp):
		""" Set proportional factor 'Kp'. """
		self.__write("sp", uint16(pfactor_scale(Kp)))

	def set_Ki(self, Ki):
		""" Set integral factor 'Ki'. """
		self.__write("si", uint16(ifactor_scale(Ki)))

	def set_Kd(self, Kd):
		""" Set derivative factor 'Kd'. """
		self.__write("sd", uint16(dfactor_scale(Kd)))

	def set_setpoint(self, w):
		""" Set setpoint 'w'. """
		w = self.__device_value(w)
		self.__write("sv", w)

	def set_output(self, y):
		""" Set output value 'y' manually. """
		self.__write("sy", self.__device_output(y))

	def set_limits(self, ymin, ymax):
		""" Set output limits. """
		ymin, ymax = self.__device_output(ymin, ymax)
		self.__write("sl", ymin, ymax)

	def set_scale(self, xmin, xmax):
		""" Set PV scale. """
		xmin, xmax = self.__device_value(xmin, xmax)
		xscale = SCALING_FACTOR * FULLSCALE/(xmax-xmin)
		self.__write("ss", xmin, xmax, uint16(xscale))

	def auto(self):
		""" Set to automatic mode. """
		self.__write("a")

	def manual(self):
		""" Set to manual mode. """
		self.__write("m")

	def save(self):
		""" Save device configuration to EEPROM. """
		self.__write("e")

	def info(self):
		""" Print PID data. """
		p, i, d = self.Kp, self.Ki, self.Kd
		v, n = Kd_to_Tv(p, d), Ki_to_Tn(p, i)
		w, x, y = self.w, self.x, self.y
		ymin, ymax = self.get_limits();
		xmin, xmax = self.get_scale();
		e = w - x
		m = self.opmode
		
		datafmt = {'w': w, 'x': x, 'e': e, 'unit': self.__valunit, 'min': xmin, 'max': xmax}
		parafmt = {'p': p, 'i': i, 'd': d, 'v': v, 'n': n}
		outfmt  = {'y': y, 'unit': self.__outunit, 'min': ymin, 'max': ymax}
		
		datastr = "w: {w}{unit} \nx: {x}{unit} ({min}..{max}{unit}) \ne: {e}{unit}"
		outstr = "y: {y}{unit} ({min}..{max}{unit})"
		parastr = "Kp: {p:.2f} \nKi: {i:.2f} (Tn: {n:.2f}) \nKd: {d:.2f} (Tv: {v:.2f})"
		
		print parastr.format(**parafmt)
		print datastr.format(**datafmt)
		print outstr.format(**outfmt)
		
		print m == 'a' and "automatic" or "manual"

	def log(self, interval=1):
		""" Print out w, x, y, e continuously in an interval of 'interval'. """
		try:
			while True:
				w, x, y = self.w, self.x, self.y
				e = w - x
				
				string = "w: {w}{unit} x: {x}{unit} e: {e}{unit} y: {y}{outunit}"
				print string.format(w=w, x=x, e=e, y=y, unit=self.__valunit, outunit=self.__outunit)
				
				sleep(interval)
		except KeyboardInterrupt:
			return
	
	def flush(self):
		""" Flush the serial input buffer. """
		self.com.readlines()
	
	def display_configuration(self, vmin, vmax, vunit='', omin=0, omax=100, ounit='%'):
		"""
		Convert and scale process value and setpoint to the interval [vmin, vmax],
		output value to [omin, omax] and optionally append a unit (vunit, ounit).
		
		Example: display_configuration(0, 100, '%') will convert all values to a
		percentage and append a percent sign.
		
		The unit can also be changed by setting the class attribute 'displayunit'.
		
		Parameters:
		-----------
		vmin:    minimum of scale
		vmax:    maximum of scale
		unit:    a unit string to append
		outperc: convert output to percentage (True, default) or fullscale (False)
		"""
		
		self.__valmin = vmin
		self.__valmax = vmax
		self.__valunit = vunit
		
		self.__outmin = omin
		self.__outmax = omax
		self.__outunit = ounit
		
	def reset_display(self):
		"""
		Reset display configuration to display fullscale values (0…255).
		"""
		self.__valmin = 0
		self.__valmax = FULLSCALE
		self.__valunit = ''
		
		self.__outmin = 0
		self.__outmax = FULLSCALE
		self.__outunit = ''
	
	def percentage(self, enable=True):
		"""
		Display all values in percent or reset to 0…255.
		"""
		if enable is True:
			self.display_configuration(0, 100, '%', 0, 100, '%')
		else:
			self.reset_display()
			
	def __getattr__(self, name):
		if name == "Kp":
			return self.get_Kp()
		elif name == "Ki":
			return self.get_Ki()
		elif name == "Kd":
			return self.get_Kd()
		elif name == "Tn":
			p, i = self.get_Kp(), self.get_Ki()
			return Ki_to_Tn(p, i)
		elif name == "Tv":
			p, d = self.get_Kp(), self.get_Kd()
			return Kd_to_Tv(p, d)

		elif name == "opmode":
			return self.get_mode()

		elif name == "w" or name == "SP":
			return self.get_setpoint()
		elif name == "x" or name == "PV":
			return self.get_pv()
		elif name == "y":
			return self.get_output()
		elif name == "e":
			return self.w-self.x
		
		elif name in ("ymax, ymin, outmax, outmin"):
			ymin, ymax = self.get_limits()
			if name in ("ymin", "outmin"):
				return ymin
			elif name in ("ymax", "outmax"):
				return ymax
				
		elif name in ("xmax, xmin, pvmax, pvmin"):
			xmin, xmax = self.get_scale()
			if name in ("xmin", "pvmin"):
				return xmin
			elif name in ("pvmin", "pvmax"):
				return xmax
		
		else:
			object.__getattr__(self, name)

	def __setattr__(self, name, value):
		if name == "Kp":
			self.set_Kp(value)
		elif name == "Ki":
			self.set_Ki(value)
		elif name == "Kd":
			self.set_Kd(value)
		elif name == "Tn":
			Ki = Tn_to_Ki(self.get_Kp(), value)
			self.set_Ki(Ki)
		elif name == "Tv":
			Kd = Tv_to_Kd(self.get_Kp(), value)
			self.set_Kd(Kd)
			
		elif name == "w" or name == "SP":
			self.set_setpoint(value)

		elif name == "y":
			self.set_output(value)

		elif name == "opmode":
			if value == 'a':
				self.auto()
			elif value == 'm':
				self.manual()
			else:
				raise AttributeError("opmode must be 'a' or 'm'")
			
		elif name in ("ymax, ymin, outmax, outmin"):
			ymin, ymax = self.get_limits()
			if name in ("ymin", "outmin"):
				ymin = value
			elif name in ("ymax", "outmax"):
				ymax = value
			
			self.set_limits(ymin, ymax)
		
		elif name in ("xmax, xmin, pvmax, pvmin"):
			xmin, xmax = self.get_scale()
			if name in ("xmin", "pvmin"):
				xmin = value
			elif name in ("pvmin", "pvmax"):
				xmax = value
			
			self.set_scale(xmin, xmax)
		
		
		else:
			object.__setattr__(self, name, value)
